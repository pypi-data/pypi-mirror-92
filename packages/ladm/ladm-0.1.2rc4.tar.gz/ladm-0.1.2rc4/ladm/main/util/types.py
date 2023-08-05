from typing import List, Union

LanguageDependenciesInput = List[List[str]]
SystemDependenciesInput = List[List[str]]
DataDependenciesInput = List[str]
DependenciesInput = Union[LanguageDependenciesInput, SystemDependenciesInput, DataDependenciesInput]

LanguageDependenciesOutput = List[str]
SystemDependenciesOutput = List[str]
DataDependenciesOutput = List[str]
DependenciesOutput = Union[LanguageDependenciesOutput, SystemDependenciesOutput, DataDependenciesOutput]
