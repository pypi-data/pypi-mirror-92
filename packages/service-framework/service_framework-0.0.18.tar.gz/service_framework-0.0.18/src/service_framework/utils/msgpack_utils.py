""" File to House a Custom Msgpack Wrapper """

from decimal import Decimal
from uuid import UUID
from msgpack import packb, unpackb
import numpy


def custom_encode(obj):
    """
    Custom function to enhance msgpack encoding.
    obj::Object An object
    return::{} Stringified object in a msgpack dict if a custom object
    """
    if isinstance(obj, Decimal):
        return {'__decimal__': True, 'as_str': str(obj)}

    if isinstance(obj, set):
        return {'__set__': True, 'value': list(obj)}

    if isinstance(obj, UUID):
        return {'__uuid__': True, 'as_str': str(obj)}

    if isinstance(obj, numpy.ndarray):
        return {'__numpy.ndarray__': True, 'as_bytes': obj.tobytes()}

    return obj


def custom_decode(obj):
    """
    Custom function to enchance msgpack decoding.
    obj::{} A dictionary representition of an object already unwrapped by msgpack
    return::Object The decoded object if a custom object
    """
    if '__decimal__' in obj:
        return Decimal(obj['as_str'])

    if '__set__' in obj:
        return set(obj['value'])

    if '__uuid__' in obj:
        return UUID(obj['as_str'])

    if '__numpy.ndarray__' in obj:
        return numpy.frombuffer(obj['as_bytes'])

    return obj


def msg_pack(obj):
    """
    Custom msgpack packing method
    """
    return packb(obj, default=custom_encode, use_bin_type=True)


def msg_unpack(packb_obj):
    """
    Custom msgpack unpacking method
    """
    return unpackb(packb_obj, object_hook=custom_decode, raw=False)
