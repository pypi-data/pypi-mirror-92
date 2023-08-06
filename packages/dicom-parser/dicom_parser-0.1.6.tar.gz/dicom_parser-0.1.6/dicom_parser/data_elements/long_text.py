"""
Definition of the :class:`LongText` class, representing a single "LT" data
element.
"""

from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class LongText(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.LT
