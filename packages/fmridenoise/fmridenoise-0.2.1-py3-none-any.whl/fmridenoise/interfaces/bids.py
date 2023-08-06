# Interface for loading preprocessed fMRI data and confounds table
from os.path import exists

from bids import BIDSLayout
from nipype.interfaces.io import IOBase
from nipype.utils.filemanip import copyfile
from nipype.interfaces.base import (BaseInterfaceInputSpec, SimpleInterface,
    traits, TraitedSpec,
    Directory, Str, ImageFile,
    OutputMultiPath)
from traits.trait_base import Undefined
from traits.trait_types import Dict, List, Either, File, Int
from fmridenoise.pipelines import load_pipeline_from_json, is_IcaAROMA
import json
import os
from itertools import product
import typing as t
from fmridenoise.utils.entities import build_path, parse_file_entities_with_pipelines
import logging
logger = logging.getLogger(__name__)


def _lists_to_entities(subjects: list, tasks: list, sessions: t.List[str], runs: t.List[str]):
    """
    Convert lists of subjects, tasks and sessions into list of dictionaries
    (entities). It handles empty session list.
    """

    keys = ['subject', 'task']
    prod_elements = [subjects, tasks]
    if sessions:
        keys.append('session')
        prod_elements.append(sessions)
    if runs:
        keys.append('run')
        prod_elements.append(runs)

    return [{key: value for key, value in zip(keys, entity)} for entity in product(*prod_elements)]


def _fill_empty_lists(layout: BIDSLayout, subjects: list, tasks: list, sessions: list, runs: t.List[str]):
    """
    If filters are not provided by the user, load them from layout.
    """

    subjects = subjects if subjects else layout.get_subjects()
    tasks = tasks if tasks else layout.get_tasks()
    sessions = sessions if sessions else layout.get_sessions()
    runs = runs if runs else layout.get_runs()
    return subjects, tasks, sessions, runs


class MissingFile(IOError):
    pass


class BIDSGrabInputSpec(BaseInterfaceInputSpec):
    # TODO: Check this inteface, why are there 'either file or list'? ~Mateusz
    fmri_prep_files = List()
    fmri_prep_aroma_files = Either(List(ImageFile()), File())
    conf_raw_files = Either(List(File(exists=True)), File(exists=True))
    conf_json_files = Either(List(File(exists=True)), File(exists=True))
    subject = Str()
    task = Str()
    session = Str()
    run = Int()


class BIDSGrabOutputSpec(TraitedSpec):
    fmri_prep = ImageFile()
    fmri_prep_aroma = ImageFile()
    conf_raw = File(exists=True)
    conf_json = File(exists=True)


class BIDSGrab(SimpleInterface):
    """
    For each list of paths selects one file for given set of parameters - subject, session, task.
    """
    input_spec = BIDSGrabInputSpec
    output_spec = BIDSGrabOutputSpec

    def _run_interface(self, runtime):
        if self.inputs.fmri_prep_files != Undefined:
            self._results['fmri_prep'] = self._select_one(self.inputs.fmri_prep_files)
        if self.inputs.fmri_prep_aroma_files != Undefined:
            self._results['fmri_prep_aroma'] = self._select_one(self.inputs.fmri_prep_aroma_files)
        self._results['conf_raw'] = self._select_one(self.inputs.conf_raw_files)
        self._results['conf_json'] = self._select_one(self.inputs.conf_json_files)
        return runtime

    def _select_one(self, _list: t.List[str]) -> str:
        """
        Wrapper for select_one that uses class instance variable.
        Args:
            _list (List[str]): list of file paths
        Returns:
           str: resulting file path meeting criteria
        """
        return self.select_one(_list,
                               subject=self.inputs.subject,
                               session=self.inputs.session,
                               task=self.inputs.task,
                               run=self.inputs.run)

    @staticmethod
    def select_one(_list: t.List[str], subject: str, task: str, session: str, run: str) -> str:
        """
        For given list of file paths returns one path for given subject, session and task.
        If no paths meet criteria empty string is returned instead.
        If more than one path is found ValueError is raised.
        Args:
            _list (List[str]): list of file paths
            subject (str): subject identifier without 'sub-'
            session (str): session identifier without 'ses-'
            task (str): task identifier without 'task-'
            run (str): run identifier without 'run-'

        Returns:
           str: resulting file path meeting criteria
        """
        filters = [lambda x: f"sub-{subject}" in x, lambda x: f"task-{task}" in x]
        if session:
            filters.append(lambda x: f"ses-{session}" in x)
        if run:
            filters.append(lambda x: f"run-{run}" in x)
        result = _list
        for fil in filters:
            result = filter(fil, result)
        result = list(result)
        if not len(result) <= 1:
            raise ValueError(f"Unambiguous number of querried files, expected 1 or 0 but got {len(result)}")
        return result[0] if len(result) == 1 else ''


class BIDSValidateInputSpec(BaseInterfaceInputSpec):

    # Root directory only required argument
    bids_dir = Directory(
        exists=True,
        required=True,
        desc='BIDS dataset root directory'
    )

    # Default: 'fmriprep'
    derivatives = traits.List(desc='Specifies name of derivatives directory')

    # Separate queries from user
    tasks = traits.List(Str(), desc='Names of tasks to denoise')
    sessions = traits.List(Str(), desc='Labels of sessions to denoise')
    subjects = traits.List(Str(), desc='Labels of subjects to denoise')
    runs = traits.List(Int(), desc='Labels of runs to denoise')

    # Pipelines from user or default
    pipelines = traits.List(
        File(),
        desc='List of paths to selected pipelines'
    )


class BIDSValidateOutputSpec(TraitedSpec):

    # Goes to BIDSGrab (whole lists)
    fmri_prep = traits.List(File)
    fmri_prep_aroma = traits.List(File)
    conf_raw = traits.List(File)
    conf_json = traits.List(File)
    tasks = traits.List(Str)
    sessions = traits.List(Str)
    subjects = traits.List(Str)
    runs = traits.List(trait=Int())

    # Outputs pipelines loaded as dicts
    pipelines = traits.List(Dict)

    # Goes to Denoiser
    tr_dict = traits.Dict()


class BIDSValidate(SimpleInterface):
    """
     Interface responsible for calling BIDSLayout and validating file structure.

    It should output to:

    - layout (-> BIDSGrab)
    - task, session, subject  (-> iterNodes)
    - pipeline (-> ?)
    - tr_dict (-> Denoiser)

    It should raise exception when:

    - user specified incorrect flags (there are no matching files)
    - some files are missing e.g. these for AROMA pipeline, when it is required
    """

    input_spec = BIDSValidateInputSpec
    output_spec = BIDSValidateOutputSpec

    @staticmethod
    def validate_derivatives(bids_dir: str,
                             derivatives: t.Union[str, t.List[str]]) -> t.Tuple[t.List[str], t.List[str]]:
        """
        Validate derivatives argument provided by the user before calling
        layout. It creates required full path for derivatives directory. Also
        returns scope required for queries.

        Args:
            bids_dir (str):
                Path to bids root directory.
            derivatives (Union[str, List[str]]): str or list(str)
                Derivatives to use for denoising.

        Returns:
            derivatives_valid (list):
                Validated derivatives list.
            scope (list):
                Right scope keyword used in pybids query.
        """

        if isinstance(derivatives, str):
            derivatives_valid = [derivatives]
        else:
            derivatives_valid = derivatives

        # Create full paths to derivatives folders
        derivatives_valid = [os.path.join(bids_dir, 'derivatives', d)
                             for d in derivatives_valid]

        # Establish right scope keyword for arbitrary packages
        scope = []
        for derivative_path in derivatives_valid:
            dataset_desc_path = os.path.join(derivative_path,
                                             'dataset_description.json')
            if exists(dataset_desc_path):
                with open(dataset_desc_path, 'r') as f:
                    dataset_desc = json.load(f)
            else:
                raise MissingFile(f"{derivative_path} should contain" +
                                  " dataset_description.json file")
            try:
                major, minor, patch = (int(element) for element in str(dataset_desc['BIDSVersion']).split('.'))
            except Exception:
                raise Exception(f"Unable to parse bids version ({dataset_desc['BIDSVersion']}) into 3 parts")
            if major == 1 and minor <= 3:
                try:
                    scope.append(dataset_desc['PipelineDescription']['Name'])
                except KeyError as e:
                    raise KeyError("Key 'PipelineDescription.Name' is "
                                      f"required in {dataset_desc_path} file") from e
            else:
                pipeline = None
                try:
                    for pipeline in dataset_desc['GeneratedBy']:
                        scope.append(pipeline['Name'])
                except KeyError as e:
                    raise KeyError(f"Unable to extract Name from GeneratedBy: {pipeline} in file {dataset_desc_path}")

        return derivatives_valid, scope

    @staticmethod
    def get_entity_files(layout: BIDSLayout, include_no_aroma: bool, include_aroma: bool, entity: dict) -> tuple:
        """
        Checks if all required files are present for single entity defined by
        subject, session and task labels. If include_aroma is True also checks for
        AROMA file. Note that session argument can be undefined.

        Args:

        Returns:
            (missing: Union[bool, dict], dict)

        """
        filter_fmri = {
            'extension': ['nii', 'nii.gz'],
            'suffix': 'bold',
            'desc': 'preproc',
            'space': 'MNI152NLin2009cAsym'
        }
        filter_fmri_aroma = {
            'extension': ['nii', 'nii.gz'],
            'suffix': 'bold',
            'desc': 'smoothAROMAnonaggr',
            # 'space': 'MNI152NLin2009cAsym'
        }
        filter_conf = {
            'extension': 'tsv',
            'suffix': ['regressors', 'timeseries'],
            'desc': 'confounds',
        }
        filter_conf_json = {
            'extension': 'json',
            'suffix': ['regressors', 'timeseries'],
            'desc': 'confounds',
        }

        filters_names = ['conf_raw', 'conf_json']
        filters = [filter_conf, filter_conf_json]
        if include_no_aroma:
            filters.append(filter_fmri)
            filters_names.append('fmri_prep')
        if include_aroma:
            filters.append(filter_fmri_aroma)
            filters_names.append('fmri_prep_aroma')

        entity_files = {}
        for filter, filter_name in zip(filters, filters_names):
            files = layout.get(**entity, **filter)
            if len(files) != 1:
                return filter, entity_files
            entity_files[filter_name] = files[0]

        return False, entity_files

    @staticmethod
    def validate_files(
            layout: BIDSLayout,
            tasks: t.List[str],
            sessions: t.List[str],
            subjects: t.List[str],
            runs: t.List[str],
            include_aroma: bool,
            include_no_aroma: bool):
        """
        Checks if for all parameters permutations every file (confounds.tsv, confounds.json, img,
        img with aroma) exists. Aroma and no aroma files are checked if proper flag is set to true.

        Args:
            layout (BIDSLayout): BIDSLayout
            tasks (List[str]): tasks that are expected to exist
            sessions (List[str]): tasks that are expected to exist
            subjects (List[str]): subjects that are expected to exist
            runs (List[str]): runs that are expected to exists
            include_aroma (bool): check for aroma files for every task/session/subject configuration
            include_no_aroma (bool): check for no aroma files for every task/session/subject configuration

        Returns:
            entity files and tuple with all tasks, subjects, sessions
        """

        subjects_to_exclude = []
        # Select interface behavior depending on user behavior
        if not tasks and not sessions and not subjects:
            raise_missing = False
        else:
            raise_missing = True

        subjects, tasks, sessions, runs = _fill_empty_lists(layout, subjects, tasks, sessions, runs)
        entities = _lists_to_entities(subjects, tasks, sessions, runs)
        entities_files = []

        if raise_missing:
            # Raise error if there are missing files
            for entity in entities:

                missing, entity_files = BIDSValidate.get_entity_files(layout, include_no_aroma, include_aroma, entity)
                entities_files.append(entity_files)

                if missing:
                    miss = {**entity, **missing}
                    raise MissingFile(
                        f'missing file(s) for {miss} (check if you are using AROMA pipelines)')
        else:
            # Log missing files and exclude subjects for missing files
            for entity in entities:

                missing, entity_files = BIDSValidate.get_entity_files(layout, include_no_aroma, include_aroma, entity)
                entities_files.append(entity_files)

                if missing:
                    subjects_to_exclude.append(entity['subject'])
                    miss = {**entity, **missing}
                    import logging
                    logger.warning(f'missing file(s) for {miss}')

            subjects = [subject for subject in subjects if
                        subject not in subjects_to_exclude]

        return entities_files, (tasks, sessions, subjects, runs)

    def _run_interface(self, runtime):

        # Validate derivatives argument
        derivatives, _ = BIDSValidate.validate_derivatives(
            bids_dir=self.inputs.bids_dir,
            derivatives=self.inputs.derivatives
        )

        # Load layout
        layout = BIDSLayout(
            root=self.inputs.bids_dir,
            derivatives=derivatives,
            validate=False
        )

        # Load pipelines
        pipelines_dicts = []
        for pipeline in self.inputs.pipelines:
            pipelines_dicts.append(load_pipeline_from_json(pipeline))

        # Check if there is at least one pipeline requiring aroma
        include_aroma = any(map(is_IcaAROMA, pipelines_dicts))

        # Check if there is at least one pipeline requiring no armoa files
        include_no_aroma = not all(map(is_IcaAROMA, pipelines_dicts))

        # Check missing files and act accordingly
        entities_files, (tasks, sessions, subjects, runs) = BIDSValidate.validate_files(
            layout=layout,
            tasks=self.inputs.tasks,
            sessions=self.inputs.sessions,
            subjects=self.inputs.subjects,
            runs=self.inputs.runs,
            include_aroma=include_aroma,
            include_no_aroma=include_no_aroma
        )

        # Convert entities_files into separate lists of BIDSImageFile Objects
        def filter_entity(entity_files: t.List[t.Dict[str, t.Any]], key: str) -> t.List[str]:
            return list(entity[key].path for entity in entity_files if entity.get(key) is not None)
        
        conf_raw = filter_entity(entities_files, 'conf_raw')
        conf_json = filter_entity(entities_files, 'conf_json')

        if include_no_aroma:
            fmri_prep = filter_entity(entities_files, 'fmri_prep')
        else:
            fmri_prep = []

        if include_aroma:
            fmri_prep_aroma = filter_entity(entities_files, 'fmri_prep_aroma')
        else:
            fmri_prep_aroma = []

        # Extract TR for specific tasks
        tr_dict = {}

        # TODO: this is just a funny workaround, look for better solution later
        layout_for_tr = BIDSLayout(
            root=self.inputs.bids_dir,
            derivatives=derivatives,
            validate=True,
            index_metadata=True
        )

        for task in tasks:
            filter_fmri_tr = {
                'extension': ['nii', 'nii.gz'],
                'suffix': 'bold',
                'desc': 'preproc',
                'space': 'MNI152NLin2009cAsym',
                'task': task
            }

            try:
                example_file = layout_for_tr.get(**filter_fmri_tr)[0]
            except IndexError:
                raise MissingFile(f'no imaging file found for task {task}')
            tr_dict[task] = layout_for_tr.get_metadata(example_file.path)[
                'RepetitionTime']

        # check space
        # TODO:
        # spaces = layout.get_entities()['space'].unique()
        # for space in spaces:
        #     get_parcellation_file_path(space)

        # Prepare outputs
        self._results['fmri_prep'] = fmri_prep
        self._results['fmri_prep_aroma'] = fmri_prep_aroma
        self._results['conf_raw'] = conf_raw
        self._results['conf_json'] = conf_json
        self._results['tasks'] = tasks
        self._results['sessions'] = sessions
        self._results['subjects'] = subjects
        self._results['runs'] = runs
        self._results['pipelines'] = pipelines_dicts
        self._results['tr_dict'] = tr_dict

        return runtime


class BIDSDataSinkInputSpec(BaseInterfaceInputSpec):
    base_entities = Dict(
        key_trait=Str,
        value_trait=Str,
        value=dict(),  # default value
        mandatory=False,
        desc="Optional base entities that will overwrite values from incoming file"
    )
    in_file = File(
        desc="File from tmp to save in BIDS directory")


class BIDSDataSinkOutputSpec(TraitedSpec):
    out_file = OutputMultiPath(File, desc='output file')


class BIDSDataSink(IOBase):
    """
    Copies files created by workflow to bids-like folder.
    """
    input_spec = BIDSDataSinkInputSpec
    output_spec = BIDSDataSinkOutputSpec
    output_dir_pattern = "{bids_dir}/derivatives/{derivative}/[ses-{session}/][sub-{subject}/]"
    output_path_pattern = output_dir_pattern + "[sub-{subject}_][ses-{session}_][task-{task}_][run-{run}_]" \
                          "[pipeline-{pipeline}_][desc-{desc}_]{suffix}.{extension}"

    _always_run = True

    def _list_outputs(self):
        if self.inputs.in_file == Undefined:
            return {'out_file': Undefined}
        entities = parse_file_entities_with_pipelines(self.inputs.in_file)
        entities.update(self.inputs.base_entities)
        os.makedirs(build_path(entities, self.output_dir_pattern), exist_ok=True)
        path = build_path(entities, self.output_path_pattern)
        assert not os.path.exists(path), f"File already exists, overwriting protection: {path}"
        copyfile(self.inputs.in_file, path, copy=True)
        return {'out_file': path}
