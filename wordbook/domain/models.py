"""Domain models."""


class DomainException(Exception):
    pass


class ModelException(DomainException):
    pass


class ModelValidationError(ModelException):
    pass


class DomainModel(object):
    fields = {}

    # TODO: decorator which builds docstring from fields definitions
    def __init__(self, **kwargs):
        self.data = {}

        for key, value in kwargs.items():
            self.data[key] = value

        self.validate()

    def __getattr__(self, name):
        return self.data[name]

    def validate(self):
        """
        :raises: ModelValidationError
        """
        pass

    def is_valid(self):
        """Checks if domain object is valid.

        :returns: True|False
        :rtype: bool
        """
        return True


class BaseField(object):
    pass


class Translation(DomainModel):
    fields = {
        'from_language': '',
        'into_language': '',
        'word': '',
        'ipa': '',
        'translated': '',
    }
