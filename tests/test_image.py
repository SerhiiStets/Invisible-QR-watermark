"""Test image.py"""

from pytest import raises
from image import QRImage, NoQRImageException


class TestQRImage:

    def test_init(self):
        with raises(NoQRImageException):
            QRImage("random_path")
