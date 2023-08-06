from jsonschema import ValidationError


class ContextException(Exception):
    pass


class TaskNotFoundException(ContextException):
    pass


class InterruptExecution(Exception):
    pass


class TaskException(ContextException):
    pass


class UndefinedEnvironmentVariableUsageError(TaskException):
    pass


class EnvironmentVariableNotUsed(TaskException):
    pass


class EnvironmentVariableNameNotAllowed(TaskException):
    def __init__(self, var_name: str):
        super().__init__('Environment variable with this name "' + var_name + '" cannot be declared, it probably a' +
                         ' commonly reserved name by operating systems')


class UserInputException(Exception):
    pass


class NotSupportedEnvVariableError(UserInputException):
    pass


class YamlParsingException(ContextException):
    """Logic or syntax errors in makefile.yaml"""


class YAMLFileValidationError(YamlParsingException):
    """Errors related to schema validation"""

    def __init__(self, err: ValidationError):
        super().__init__('YAML schema validation failed at path "%s" with error: %s' % (
            '.'.join(list(map(str, list(err.path)))),
            str(err.message)
        ))


class ParsingException(ContextException):
    """Errors related to parsing YAML/Python syntax"""

    @classmethod
    def from_import_error(cls, import_str: str, class_name: str, error: Exception) -> 'ParsingException':
        return cls(
            'Import "%s" is invalid - cannot import class "%s" - error: %s' % (
                import_str, class_name, str(error)
            )
        )

    @classmethod
    def from_class_not_found_in_module_error(cls, import_str: str, class_name: str,
                                             import_path: str) -> 'ParsingException':
        return cls(
            'Import "%s" is invalid. Class or method "%s" not found in module "%s"' % (
                import_str, class_name, import_path
            )
        )


class DeclarationException(ContextException):
    """Something wrong with the makefile.py/makefile.yaml """


class ContextFileNotFoundException(ContextException):
    """When makefile.py, makefile.yaml, makefile.yml not found (at least one needed)"""

    def __init__(self, path: str):
        super().__init__('The directory "%s" should contain at least makefile.py, makefile.yaml or makefile.yml' % path)


class PythonContextFileNotFoundException(ContextFileNotFoundException):
    """When makefile.py is not found"""

    def __init__(self, path: str):
        super().__init__('Python context file not found at "%s"' % path)


class NotImportedClassException(ContextException):
    """When class was not imported"""

    def __init__(self, exc: ImportError):
        super().__init__(
            'Your Makefile contains a reference to not available or not installed Python module "%s"' % str(exc)
        )


class EnvironmentVariablesFileNotFound(ContextException):
    """.env file specified, but not existing"""

    def __init__(self, path: str, lookup_paths: list):
        super().__init__(
            'Specified file "%s" as environment variable provider does not exist. Looked in: %s' % (
                path, str(lookup_paths)
            )
        )


class RuntimeException(Exception):
    pass


class MissingInputException(RuntimeException):
    def __init__(self, arg_name: str, env_name: str):
        super().__init__('Either "%s" switch not used, either "%s" was not defined in environment' % (
            arg_name, env_name
        ))
