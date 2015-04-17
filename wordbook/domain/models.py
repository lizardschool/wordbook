"""Domain models."""
from wordbook import secure


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
            self.__setattr__(key, value)

        self.validate()

    def __repr__(self):
        fields = ", ".join(['%s=%s' % (fn, getattr(self, fn)) for fn in sorted(self.fields.keys())])
        value = "".join(['<', self.__class__.__name__, ": ", fields, '>'])
        return value

    def __setattr__(self, name, value):
        if name == 'data':
            super().__setattr__(name, value)
        elif name not in self.fields:
            raise AttributeError('Unknown field %s in %s' % (name, self))
        else:
            super().__setattr__(name, value)

    def __getattr__(self, name):
        try:
            return self.data[name]
        except KeyError:
            if name in self.fields:
                return None
            raise AttributeError('Unknown field %s in %s' % (name, self))

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


class List(DomainModel):
    fields = {
        'id': '',
        'name': '',
    }

    @property
    def hash(self):
        return secure.id_to_hash(self.id)

    @staticmethod
    def hash2id(list_hash):
        decoded = secure.hash_to_id(list_hash)
        assert len(decoded) == 1
        return decoded[0]


class Translation(DomainModel):
    fields = {
        'id': '',
        'from_language': '',
        'into_language': '',
        'word': '',
        'ipa': '',
        'translated': '',
    }

    def dto_autocomplete(self):
        return dict(
            id=self.id,
            word=self.word,
            translation=self.translated or '',
            ipa=self.ipa or ''
        )


class Card(DomainModel):
    fields = {
        'translation_id': '',
        'list_id': '',
    }

    def dto(self):
        return dict(
            translation_id=self.translation_id,
            list_id=self.list_id,
        )
