"""Test image.py"""

from PIL import Image
from pytest import raises

from image import QRImage, EmptyQRTextError, NoQRImageError, QRSizeError, NoQRError


class TestQRImage:
    """Tests QRImage class."""

    def test_init(self):
        """Tests init method of QRImage"""
        with raises(NoQRImageError):
            QRImage("random_path")

    def test_encode(self):
        """Tests encode method of QRImage."""
        new_img = QRImage('img/ex3.png')
        with raises(EmptyQRTextError):
            new_img.encode("")

        with raises(QRSizeError):
            new_img.encode("a very long message that is generates QR bigger then original image")

        assert isinstance(new_img.encode("random text"), Image.Image), "Should return PIL Image instance"
        new_img = QRImage('img/ex1.jpg')
        assert isinstance(new_img.encode("random text"), Image.Image), "Should return PIL Image instance"

    def test_decode(self):
        """Tests decode method of QRImage."""
        new_img = QRImage('img/ex3.png')

        with raises(NoQRError):
            new_img.decode()

        encoded_img = new_img.encode("random_text")
        encoded_img.save('img/qr_ex1.png')

        new_img = QRImage('img/qr_ex1.png')
        decoded_text = new_img.decode()
        assert isinstance(decoded_text, str), "Should return str test"
        assert decoded_text == "random_text", "Should return 'random text'"
