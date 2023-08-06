import json
import os
from os.path import join
import pandas as pd
import numpy as np
from bids.layout.writing import build_path
from traits.trait_types import Dict, Str, List, Directory
from nipype.interfaces.base import (BaseInterfaceInputSpec, File, TraitedSpec, 
    SimpleInterface)
import typing as t
from fmridenoise.utils.entities import parse_file_entities_with_pipelines, build_path, \
    assert_all_entities_equal


class ConfoundsInputSpec(BaseInterfaceInputSpec):
    pipeline = Dict(
        mandatory=True,
        desc="Denoising pipeline")
    conf_raw = File(
        exist=True,
        mandatory=True,
        desc="Confounds table")
    conf_json = File(
        exist=True,
        mandatory=True,
        desc="Confounds description (aCompCor)")
    output_dir = Directory(
        exists=True,
        mandatory=True,
        desc="Output path")


class ConfoundsOutputSpec(TraitedSpec):
    conf_prep = File(
        exists=True,
        desc="Preprocessed confounds table")
    conf_summary = File(
        exists=True,
        desc="Confounds summary JSON")


class Confounds(SimpleInterface):
    """Preprocess and filter confounds table according to denoising pipeline.

    This interface reads raw confounds table (fmriprep output) and process it 
    retaining regressors of interest and creating additional regressors if 
    needed. Additionally, it creates summary file containing all relevant 
    information about confounds. This interface operates on single BIDS entity
    i.e. single subject, task and (optionally) session. 

    Output filenames for both processed confounds and summary JSON have 
    identical base but different extensions, since they are describing the same 
    piece of data. They are created by replacing regressors suffix from original
    filenames with expression pipeline-<pipeline_name>.
    
    Summary contains fields:
        'mean_fd': 
            Mean framewise displacement.
        'max_fd': 
            Highest recorded framewise displacement.
        'n_conf': 
            Total number of confounds included.
        'include':
            Decision about subject inclusion in connectivity analysis based on
            three criteria: (1) mean framewise displacement is lower than 
            specified by the pipeline, (2) max framewise displacement did not 
            exceed 5mm and (3) percentage of outlier scans did not exceed 20%. 
            Note that if spikes strategy is not specified, include flag defaults
            to True.
        'n_spikes':
            Number of outlier scans (only if spikes strategy is specified).
        'perc_spikes':
            Percentage of outlier scans (only if spikes strategy is specified).
    """
    input_spec = ConfoundsInputSpec
    output_spec = ConfoundsOutputSpec
    conf_prep_pattern = "sub-{subject}[_ses-{session}]_task-{task}[_run-{run}]_pipeline-{pipeline}_desc-{desc}.tsv"
    conf_summary_pattern = "sub-{subject}[_ses-{session}]_task-{task}[_run-{run}]_pipeline-{pipeline}" \
                           "_desc-{desc}_summary.json"

    def _retain(self, regressor_names: t.List[str]):
        """
        Copies selected regressors from conf_raw to conf_prep.
        """
        if regressor_names:
            self.conf_prep = pd.concat((
                self.conf_prep,
                self.conf_raw[regressor_names]
            ), axis=1)

    def _filter_tissue_signals(self):
        tissue_regressors = []
        for confound, setting in self.inputs.pipeline['confounds'].items():
            
            if confound in ('white_matter', 'csf', 'global_signal'):
                for transform, include in setting.items():
                    if transform == 'raw' and include:
                        tissue_regressors.append(confound)
                    elif include:
                        tissue_regressors.append(f'{confound}_{transform}')
        
        self._retain(tissue_regressors)

    def _filter_motion_parameters(self):
        hmp_regressors = []
        hmp_names = [f'{type_}_{axis}' 
                     for type_ in ('trans', 'rot') 
                     for axis in ('x', 'y', 'z')]

        setting = self.inputs.pipeline['confounds']['motion']

        for transform, include in setting.items():
            if transform == 'raw' and include:
                hmp_regressors.extend(hmp_names)
            elif include:
                hmp_regressors.extend(f'{hmp}_{transform}' for hmp in hmp_names)
        
        self._retain(hmp_regressors)

    def _filter_acompcors(self):
        if not self.inputs.pipeline['confounds']['acompcor']:
            return

        acompcor_regressors = []
        for mask in ('CSF', 'WM'):
            acompcors = {
                (name, dict_['VarianceExplained']) 
                for name, dict_ in self.conf_json.items()
                if dict_.get('Retained') and dict_.get('Mask') == mask 
                }
            acompcors = sorted(acompcors, key=lambda tpl: tpl[1], reverse=True)
            acompcor_regressors.extend(acompcor[0] for acompcor in acompcors[:5])

        self._retain(acompcor_regressors)

    def _create_spike_regressors(self):
        if not self.inputs.pipeline['spikes']:
            return

        fd_th = self.inputs.pipeline['spikes']['fd_th']
        dvars_th = self.inputs.pipeline['spikes']['dvars_th']

        outliers = (self.conf_raw['framewise_displacement'] > fd_th) \
                 | (self.conf_raw['std_dvars'] > dvars_th) 
        outliers = list(outliers[outliers].index)

        if outliers:
            spikes = np.zeros((self.n_volumes, len(outliers)))
            for i, outlier in enumerate(outliers):
                spikes[outlier, i] = 1.
                
            conf_spikes = pd.DataFrame(
                data=spikes, 
                columns=[f'motion_outlier_{i:02}' for i in range(len(outliers))]
                )

            self.conf_prep = pd.concat((
                self.conf_prep,
                conf_spikes,
            ),
            axis=1)
        
        self.n_spikes = len(outliers)

    def _create_summary_dict(self, subject: str, session: str, task: str, run: str):
        self.conf_summary = {
            'subject': subject,
            'task': task,
            'mean_fd': self.conf_raw["framewise_displacement"].mean(),
            'max_fd': self.conf_raw["framewise_displacement"].max(),
            'n_conf': len(self.conf_prep.columns),
            'include': self._inclusion_check()
        }

        if self.inputs.pipeline['spikes']:
            self.conf_summary['n_spikes'] = self.n_spikes 
            self.conf_summary['perc_spikes'] = self.n_spikes / self.n_volumes * 100

        if session:
            self.conf_summary['session'] = session
        if run:
            self.conf_summary['run'] = run

    def _inclusion_check(self):
        '''Decide if subject should be included in connectivity analysis'''
        if not self.inputs.pipeline['spikes']:
            return True

        mean_fd = self.conf_raw['framewise_displacement'].mean()
        max_fd = self.conf_raw['framewise_displacement'].max()
        fd_th = self.inputs.pipeline['spikes']['fd_th']

        if mean_fd > fd_th or max_fd > 5 or self.n_spikes / self.n_volumes > 0.2:
            return False
        return True

    def _run_interface(self, runtime):

        # Setup useful properties
        self.conf_raw = pd.read_csv(self.inputs.conf_raw, sep='\t')
        with open(self.inputs.conf_json, 'r') as json_file:
            self.conf_json = json.load(json_file)
        self.n_volumes = len(self.conf_raw)
        self.conf_prep = pd.DataFrame()

        # entities
        entities = parse_file_entities_with_pipelines(self.inputs.conf_raw)

        # Create preprocessed confounds step-by-step
        self._filter_motion_parameters()
        self._filter_tissue_signals()
        self._filter_acompcors()
        self._create_spike_regressors()
        self._create_summary_dict(
            subject=entities.get('subject'), task=entities.get('task'),
            session=entities.get('session'), run=entities.get('run'))

        # Store output
        entities['pipeline'] = self.inputs.pipeline['name']
        conf_prep = join(self.inputs.output_dir, build_path(entities, self.conf_prep_pattern, False))
        conf_summary = join(self.inputs.output_dir, build_path(entities, self.conf_summary_pattern, False))
        self.conf_prep.to_csv(conf_prep, sep='\t', index=False, na_rep=0)
        with open(conf_summary, 'w') as f:
            json.dump(self.conf_summary, f)
        self._results['conf_prep'] = conf_prep
        self._results['conf_summary'] = conf_summary
        return runtime


class GroupConfoundsInputSpec(BaseInterfaceInputSpec):
    conf_summary_json_files = List(
        File(exists=True),
        mandatory=True,
        desc="Confounds summary")
    output_dir = Directory(          # needed to save data in other directory
        mandatory=True,
        desc="Output path")


class GroupConfoundsOutputSpec(TraitedSpec):
    group_conf_summary = File(
        exists=True,
        desc="Confounds summary")


class GroupConfounds(SimpleInterface):
    input_spec = GroupConfoundsInputSpec
    output_spec = GroupConfoundsOutputSpec
    file_pattern = "[ses-{session}_]task-{task}_[run-{run}]_pipeline-{pipeline}_groupConfSummary.tsv"

    def _run_interface(self, runtime):
        group_conf_summary = pd.DataFrame()
        # noinspection PyUnreachableCode
        if __debug__:  # sanity check
            entities = [parse_file_entities_with_pipelines(path) for path in self.inputs.conf_summary_json_files]
            assert_all_entities_equal(entities, "session", "task", "run", "pipeline")
        for summary_json_file in self.inputs.conf_summary_json_files:
            with open(summary_json_file, 'r') as f:
                group_conf_summary = group_conf_summary.append(pd.DataFrame(json.load(f), index=[0]))
        entities = parse_file_entities_with_pipelines(self.inputs.conf_summary_json_files[0])
        file_path = build_path(entities, self.file_pattern)
        fname = os.path.join(self.inputs.output_dir, file_path)
        assert not os.path.exists(fname), f"Group confounds file already exists at {fname}"
        group_conf_summary.to_csv(fname, sep='\t', index=False)
        assert os.path.exists(fname), "File not created"
        self._results['group_conf_summary'] = fname
        return runtime
