from hashids import Hashids

# TODO: read hashids_salt from config file (it shouldn't be in repository)
HASHIDS_SALT = 'Oyps9OcZa'
HASHIDS_LEN = 5

__all__ = (
    'id_to_hash',
    'hash_to_id',
)


def id_to_hash(identifier):
    hashids = Hashids(salt=HASHIDS_SALT, min_length=HASHIDS_LEN)
    return hashids.encode(identifier)


def hash_to_id(url_hash):
    hashids = Hashids(salt=HASHIDS_SALT, min_length=HASHIDS_LEN)
    return hashids.decode(url_hash)
