"""
Definition of the :class:`Signed64bitVeryLong` class, representing a single
"SV" data element.
"""

from dicom_parser.data_element import DataElement
from dicom_parser.utils.value_representation import ValueRepresentation


class Signed64bitVeryLong(DataElement):
    #: The VR value of data elements represented by this class.
    VALUE_REPRESENTATION = ValueRepresentation.SV
