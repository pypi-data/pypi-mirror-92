"""
*dicom_parser* facilitates access to DICOM header information using the
subpackages and submodules documented below.
"""

from dicom_parser.header import Header
from dicom_parser.image import Image
from dicom_parser.series import Series
from dicom_parser.utils.read_file import read_file
