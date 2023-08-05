#  Copyright (c) maiot GmbH 2020. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""Base High-level ZenML Pipeline definition"""

from abc import abstractmethod
from typing import Dict, Text, Any, Optional, List
from uuid import uuid4

from zenml.core.backends.base_backend import BaseBackend
from zenml.core.backends.orchestrator.local.orchestrator_local_backend import \
    OrchestratorLocalBackend
from zenml.core.datasources.base_datasource import BaseDatasource
from zenml.core.metadata.metadata_wrapper import ZenMLMetadataStore
from zenml.core.repo.artifact_store import ArtifactStore
from zenml.core.repo.repo import Repository
from zenml.core.repo.zenml_config import METADATA_KEY
from zenml.core.standards import standard_keys as keys
from zenml.core.steps.base_step import BaseStep
from zenml.utils.constants import CONFIG_VERSION
from zenml.utils.enums import PipelineStatusTypes
from zenml.utils.logger import get_logger
from zenml.utils.print_utils import to_pretty_string
from zenml.utils.zenml_analytics import track, CREATE_PIPELINE, RUN_PIPELINE, \
    GET_PIPELINE_ARTIFACTS

logger = get_logger(__name__)


class BasePipeline:
    """Base class for all ZenML pipelines.

    Every ZenML pipeline should override this class.
    """
    PIPELINE_TYPE = 'base'

    def __init__(self,
                 name: Text,
                 enable_cache: Optional[bool] = True,
                 steps_dict: Dict[Text, BaseStep] = None,
                 backends_dict: Dict[Text, BaseBackend] = None,
                 metadata_store: Optional[ZenMLMetadataStore] = None,
                 artifact_store: Optional[ArtifactStore] = None,
                 datasource: Optional[BaseDatasource] = None,
                 pipeline_name: Optional[Text] = None,
                 *args, **kwargs):
        """
        Construct a base pipeline. This is a base interface that is meant
        to be overridden in multiple other pipeline use cases.

        Args:
            name: Outward-facing name of the pipeline.
            pipeline_name: A unique name that identifies the pipeline after
             it is run.
            enable_cache: Boolean, indicates whether or not caching
             should be used.
            steps_dict: Optional dict of steps.
            backends_dict: Optional dict of backends
            metadata_store: Configured metadata store. If None,
             the default metadata store is used.
            artifact_store: Configured artifact store. If None,
             the default artifact store is used.
        """
        self.name = name

        # Metadata store
        if metadata_store:
            self.metadata_store: ZenMLMetadataStore = metadata_store
        else:
            # use default
            self.metadata_store: ZenMLMetadataStore = \
                Repository.get_instance().get_default_metadata_store()

        if pipeline_name:
            # This means its been loaded in through YAML, try to get context
            if self.is_executed_in_metadata_store:
                self._immutable = True
                logger.debug(f'Pipeline {name} loaded and and is immutable.')
            else:
                # if metadata store does not have the pipeline_name, then we
                # can safely execute this again.
                self._immutable = False
                logger.debug(f'Pipeline {name} loaded and can be run.')

            self.pipeline_name = pipeline_name
            self.file_name = self.pipeline_name + '.yaml'
        else:
            # if pipeline_name is None then its a new pipeline
            self._immutable = False
            self.pipeline_name = self.create_pipeline_name_from_name()
            self.file_name = self.pipeline_name + '.yaml'
            # check duplicates here as its a 'new' pipeline
            if self.file_name in \
                    Repository.get_instance().get_pipeline_file_paths(
                        only_file_names=True):
                raise AssertionError(
                    f'Pipeline names must be unique in the repository. There '
                    f'is already a pipeline called {self.name}')
            track(event=CREATE_PIPELINE)
            logger.info(f'Pipeline {name} created.')

        self.enable_cache = enable_cache

        if steps_dict is None:
            self.steps_dict: Dict[Text, BaseStep] = {}
        else:
            self.steps_dict = steps_dict

        # Backends
        if backends_dict is None:
            self.backends_dict: Dict[Text, BaseBackend] = \
                self.get_default_backends()
        else:
            self.backends_dict = backends_dict

        # Artifact store
        if artifact_store:
            self.artifact_store = artifact_store
        else:
            # use default
            self.artifact_store = \
                Repository.get_instance().get_default_artifact_store()

        # Datasource
        if datasource:
            self.datasource = datasource
        else:
            self.datasource = None

    def __str__(self):
        return to_pretty_string(self.to_config())

    def __repr__(self):
        """Visualizes pipeline steps as a basic ASCII flowchart."""
        config = self.to_config()
        steps_config = config[keys.GlobalKeys.STEPS]
        steps = [v[keys.StepKeys.SOURCE] for v in steps_config.values()]
        string_repr_list = []
        for step in steps[:-1]:
            string_repr_list.append(step)
            string_repr_list.append('\t\t\t\t|\t\t\t\t')
            string_repr_list.append('\t\t\t\tv\t\t\t\t')

        string_repr_list.append(steps[-1])
        return '\n'.join(string_repr_list)

    @property
    def is_executed_in_metadata_store(self):
        try:
            # if we find context, then it has been executed
            self.metadata_store.get_pipeline_context(self)
            return True
        except Exception as _:
            return False

    @abstractmethod
    def get_tfx_component_list(self, config: Dict[Text, Any]) -> List:
        """
        Converts config to TFX components list. This is the point in the
        framework where ZenML Steps get translated into TFX pipelines.

        Args:
            config: dict of ZenML config.
        """
        pass

    @abstractmethod
    def steps_completed(self) -> bool:
        """Returns True if all steps complete, else raises exception"""
        pass

    @staticmethod
    def get_type_from_file_name(file_name: Text):
        """
        Gets type of pipeline from file name.

        Args:
            file_name: YAML file name of pipeline.
        """
        return file_name.replace('.yaml', "").split('_')[0]

    @staticmethod
    def get_type_from_pipeline_name(pipeline_name: Text):
        """
        Gets type from pipeline name.

        Args:
            pipeline_name (str): simple string name.
        """
        return pipeline_name.split('_')[0]

    @staticmethod
    def get_name_from_pipeline_name(pipeline_name: Text):
        """
        Gets name from pipeline name.

        Args:
            pipeline_name (str): simple string name.
        """
        return pipeline_name.split('_')[1]

    @classmethod
    def from_config(cls, config: Dict):
        """
        Convert from pipeline config to ZenML Pipeline object.

        All steps are also populated and configuration set to parameters set
        in the config file.

        Args:
            config: a ZenML config in dict-form (probably loaded from YAML).
        """
        # populate steps
        steps_dict: Dict = {}
        for step_key, step_config in config[keys.GlobalKeys.STEPS].items():
            steps_dict[step_key] = BaseStep.from_config(step_config)

        env = config[keys.GlobalKeys.ENV]
        pipeline_name = env[keys.EnvironmentKeys.EXPERIMENT_NAME]
        name = BasePipeline.get_name_from_pipeline_name(
            pipeline_name=pipeline_name)

        backends_dict: Dict = {}
        for backend_key, backend_config in env[
            keys.EnvironmentKeys.BACKENDS].items():
            backends_dict[backend_key] = BaseBackend.from_config(
                backend_key, backend_config)

        artifact_store = ArtifactStore(
            env[keys.EnvironmentKeys.ARTIFACT_STORE])
        metadata_store = ZenMLMetadataStore.from_config(
            config=env[METADATA_KEY]
        )

        datasource = BaseDatasource.from_config(config)

        from zenml.core.pipelines.pipeline_factory import pipeline_factory
        pipeline_type = BasePipeline.get_type_from_pipeline_name(
            pipeline_name)
        class_ = pipeline_factory.get_pipeline_by_type(pipeline_type)

        # TODO: [MEDIUM] Perhaps move some of the logic in the init block here
        #  especially regarding inferring immutability.

        return class_(name=name, pipeline_name=pipeline_name,
                      enable_cache=env[keys.EnvironmentKeys.ENABLE_CACHE],
                      steps_dict=steps_dict,
                      backends_dict=backends_dict,
                      artifact_store=artifact_store,
                      metadata_store=metadata_store,
                      datasource=datasource)

    def add_datasource(self, datasource: BaseDatasource):
        """
        Add datasource to pipeline.

        Args:
            datasource: class of type BaseDatasource
        """
        self.datasource = datasource
        self.steps_dict[keys.TrainingSteps.DATA] = datasource.get_data_step()

    def create_pipeline_name_from_name(self):
        """Creates a unique pipeline name from user-provided name."""
        return self.PIPELINE_TYPE.lower() + '_' + self.name + '_' + str(
            uuid4())

    def get_steps_config(self) -> Dict:
        """Convert Step classes to steps config dict."""
        steps_config = {}
        for step_key, step in self.steps_dict.items():
            steps_config[step_key] = step.to_config()

        return {keys.GlobalKeys.STEPS: steps_config}

    def get_environment(self) -> Dict:
        """Get environment as a dict."""
        backends_config_dict = {}
        for b_name, b in self.backends_dict.items():
            backends_config_dict.update(b.to_config())

        return {
            keys.EnvironmentKeys.EXPERIMENT_NAME: self.pipeline_name,
            keys.EnvironmentKeys.ENABLE_CACHE: self.enable_cache,
            keys.EnvironmentKeys.BACKENDS: backends_config_dict,
            keys.EnvironmentKeys.ARTIFACT_STORE: self.artifact_store.path,
            keys.EnvironmentKeys.METADATA_STORE:
                self.metadata_store.to_config()
        }

    def to_config(self) -> Dict:
        """Converts pipeline to ZenML config."""
        # Create a ZenML pipeline.config.yaml
        steps_config = self.get_steps_config()

        # Add env config to it
        environment = self.get_environment()

        steps_config.update({
            keys.GlobalKeys.ENV: environment,
            keys.GlobalKeys.VERSION: CONFIG_VERSION,
            keys.GlobalKeys.DATASOURCE: self.datasource.to_config()
        })
        return steps_config

    def get_status(self) -> Text:
        """Get status of pipeline."""
        store = self.metadata_store
        return store.get_pipeline_status(self)

    def register_pipeline(self, config: Dict[Text, Any]):
        """
        Registers a pipeline in the artifact store as a YAML file.

        Args:
            config: dict representation of ZenML config.
        """
        Repository.get_instance().register_pipeline(
            file_name=self.file_name, config=config)

    def load_config(self) -> Dict[Text, Any]:
        """Loads a config dict from yaml file."""
        return Repository.get_instance().load_pipeline_config(
            file_name=self.file_name)

    def get_default_backends(self) -> Dict:
        """Gets list of default backends for this pipeline."""
        # For base class, orchestration is always necessary
        return {
            OrchestratorLocalBackend.BACKEND_KEY: OrchestratorLocalBackend()
        }

    @track(event=GET_PIPELINE_ARTIFACTS)
    def get_artifacts_uri_by_component(self, component_name: Text):
        """
        Gets the artifacts of any component within a pipeline. All artifacts
        are resolved locally, even if artifact store is remote.

        Args:
            component_name (str): name of component
        """
        status = self.metadata_store.get_pipeline_status(self)
        if status != PipelineStatusTypes.Succeeded.name:
            AssertionError('Cannot retrieve as pipeline is not succeeded.')
        artifacts = self.metadata_store.get_artifacts_by_component(
            self, component_name)
        # Download if not local
        uris = []
        for a in artifacts:
            uris.append(self.artifact_store.resolve_uri_locally(a.uri))
        return uris

    def copy(self, new_name: Text):
        """
        Deep copy the pipeline and therefore remove mutability requirement.

        Args:
            new_name (str): New name for copied pipeline.
        """
        class_ = self.__class__
        args = self.__dict__

        # Doing this will reset immutability
        args.pop('name')
        args.pop('pipeline_name')
        args['name'] = new_name
        return class_(**args)

    def run_config(self, config: Dict[Text, Any]):
        """
        Gets TFX pipeline from config.

        Args:
            config: dict of ZenML config.
        """
        if OrchestratorLocalBackend.BACKEND_KEY not in self.backends_dict:
            raise AssertionError('Orchestrator backend missing!')
        orch_backend = self.backends_dict[OrchestratorLocalBackend.BACKEND_KEY]

        # TODO: [LOW] Make sure this is subclass of OrchestratorLocalBackend
        orch_backend.run(config)

    @track(event=RUN_PIPELINE)
    def run(self,
            backends: Optional[List[BaseBackend]] = None,
            metadata_store: Optional[ZenMLMetadataStore] = None,
            artifact_store: Optional[ArtifactStore] = None):
        """
        Run the pipeline associated with the datasource.

        Args:
            backends (list): list of backends to use for this
            metadata_store: chosen metadata store, if None use default
            artifact_store: chosen artifact store, if None use default
             """

        # TODO: [HIGH] Important, think about separating register and run
        #  and that way ask user to input name while registering pipeline.

        # Resolve default
        if metadata_store:
            logger.warning('Changing the metadata_store or artifact_store '
                           'might cause your pipelines to be '
                           'non-reproducible and non-comparable.')
            self.metadata_store = metadata_store

        if artifact_store:
            logger.warning('Changing the metadata_store or artifact_store '
                           'might cause your pipelines to be '
                           'non-reproducible and non-comparable.')
            self.artifact_store = artifact_store

        # We do not allow ml metadata to get polluted by repeated runs
        if self.is_executed_in_metadata_store:
            logger.info(f'Pipeline: `{self.name}` has already been executed '
                        f'for the connected metadata store. Pipelines are '
                        f'immutable after they run within the same metadata '
                        f'store.')
            return

        # Check if steps are complete
        self.steps_completed()

        # Resolve backends compatibility
        if backends is None:
            backends = []
        for b in backends:
            if b.BACKEND_KEY not in self.backends_dict:
                raise Exception(f'Backend {b} not supported!')
            self.backends_dict[b.BACKEND_KEY] = b

        if self._immutable:
            # This means its an 'older' pipeline that has been loaded in via
            # YAML but does not exist in the metadata store, so we are safe
            # to run it without inferring new version pins. This will result
            # in a repeated run.
            logger.info('Pipeline is an immutable state: Any changes made '
                        'after loading it will not be reflected in this run.')
            config = self.load_config()
        else:
            # This means its a brand new pipeline
            config = self.to_config()
            # Register in the repository
            self.register_pipeline(config)

        self.run_config(config)

        # After running, pipeline is immutable
        self._immutable = True
