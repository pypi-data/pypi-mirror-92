import logging
import yaml
from typing import List, Tuple

from ladm.main.generator_context import GeneratorContext
from ladm.main.generator_strategy import LanguageGeneratorStrategy, SystemGeneratorStrategy, DataGeneratorStrategy
from ladm.main.util.custom_exceptions import LADMError
from ladm.main.util.types import LanguageDependenciesOutput, SystemDependenciesOutput, DataDependenciesOutput


class LADM:
    logger = logging.getLogger('LADM')

    def __init__(self, input_filepath: str, language: str = None):
        """
        :param input_filepath: File path and name of the skill.yml file containing the dependencies
                               (Or any other file containing dependencies in the correct format)
        :param language: For which language to generate the output, python => requirements.txt format, java => .gradle
        """
        self._input_filepath: str = input_filepath
        self._language: str = language

    def generate_dependencies_from_file(self,
                                        do_language: bool = True,
                                        do_system: bool = True,
                                        do_data: bool = True) -> Tuple[LanguageDependenciesOutput,
                                                                       SystemDependenciesOutput,
                                                                       DataDependenciesOutput]:
        """
        Main method to call from this class. Generates three lists.
        :param do_language: generate language libraries dependencies
        :param do_system: generate system dependencies
        :param do_data: generate data dependencies
        :return: Language library dependencies, system-level dependencies, data dependencies
        """
        self.logger.info(f"Generating with args{list(vars().items())[1:]} and language {self._language}")

        with open(self._input_filepath, 'r') as stream:
            try:
                dependencies_yaml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                self.logger.error(exc)
                raise LADMError(f"The supplied YAML in {self._input_filepath} cannot be parsed.")

            if 'dependencies' not in dependencies_yaml:
                self.logger.warning("\'dependencies\' is not specified in skill.yml.")
                self.logger.warning("No additional dependencies will be installed.")
                return [], [], []

            language_libraries = dependencies_yaml['dependencies'].get('libraries')
            system_dependencies = dependencies_yaml['dependencies'].get('system')
            data = dependencies_yaml['dependencies'].get('data')

            language_libraries_results: LanguageDependenciesOutput = []
            system_dependencies_results: SystemDependenciesOutput = []
            data_results: DataDependenciesOutput = []

            context = GeneratorContext()
            if do_language:
                context.strategy = LanguageGeneratorStrategy(self._language)
                language_libraries_results = context.execute_strategy(language_libraries)
            if do_system:
                context.strategy = SystemGeneratorStrategy()
                system_dependencies_results = context.execute_strategy(system_dependencies)
            if do_data:
                context.strategy = DataGeneratorStrategy()
                data_results = context.execute_strategy(data)

            return language_libraries_results, system_dependencies_results, data_results
