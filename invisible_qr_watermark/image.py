"""Module for endodin and decoding invisible QR into Images"""

import qrcode
import numpy as np

from PIL import Image
from pyzbar.pyzbar import decode


class NoQRImageError(BaseException):
    """No Image received Error."""


class EmptyQRTextError(BaseException):
    """No text to convert to QR Error."""


class QRSizeError(BaseException):
    """QR image is bigger then Image Error."""


class NoQRError(BaseException):
    """No QR code in given Image Error."""


class QRImage:
    """Class to work with Image (encode, decode)."""

    def __init__(self, img_path: str) -> None:
        """
        Initialize QRImage instance.

        Parameters
        ----------
        img_path : str
            path to the image
        """
        try:
            self.image = Image.open(img_path, 'r')
            self.image_rgba = np.array(self.image)
        except OSError as error:
            raise NoQRImageError(f"{img_path}, Couldn't find or open the image") from error

    def __flatten_image(self) -> None:
        """Flatten the image, so that every red chanel has even number."""
        for iy, ix, iz in np.ndindex(self.image_rgba.shape):
            red = self.image_rgba[iy][ix][0]
            if red % 2:
                if red == 255:
                    self.image_rgba[iy][ix][0] = self.image_rgba[iy][ix][0] - 1
                else:
                    self.image_rgba[iy][ix][0] = self.image_rgba[iy][ix][0] + 1

    def encode(self, text: str) -> Image.Image:
        """
        Encodes given text to image in a form of invisible QR code.

        Parameters
        ----------
        text : str
            given text to encode

        Returns
        -------
        Image.Image
            PIL Image instance
        """
        if not text:
            raise EmptyQRTextError("Text can't be empty")

        self.__flatten_image()

        # TODO: version QR Code

        qr = qrcode.QRCode()
        qr.add_data(text)
        qr.make()
        qr_rgba = np.array(qr.make_image().convert('RGB'))

        if qr_rgba.shape > self.image_rgba.shape:
            raise QRSizeError("Generated QR is bigger then original image")

        for iy, ix, iz in np.ndindex(qr_rgba.shape):
            if qr_rgba[iy][ix][0] == 0:
                if self.image_rgba[iy][ix][0] == 255:
                    self.image_rgba[iy][ix][0] = self.image_rgba[iy][ix][0] - 1
                else:
                    self.image_rgba[iy][ix][0] = self.image_rgba[iy][ix][0] + 1
        PIL_image = Image.fromarray(np.uint8(self.image_rgba)).convert('RGB')
        return PIL_image

    def decode(self) -> str:
        """
        Decodes given image by returning encoded in
        invisible QR text.

        Returns
        -------
        str
            decoded message from hidden QR
        """
        qr_rgba = np.empty(self.image_rgba.shape)
        for iy, ix, iz in np.ndindex(self.image_rgba.shape):
            red = self.image_rgba[iy][ix][0]
            if red % 2:
                qr_rgba[iy][ix] = [0, 0, 0]
            else:
                qr_rgba[iy][ix] = [255, 255, 255]

        PIL_image = Image.fromarray(np.uint8(qr_rgba)).convert('RGB')

        # decode returns a list of pyzbar.pyzbar.Decoded type instances
        # every instance contains a data key which stores byte version of QR text
        # decode("utf-8") return str instead of byte
        data = decode(PIL_image)

        if not data:
            # if list is empty, then decoder couldn't find a QR code
            raise NoQRError("There's no QR code in given Image, nothing to decode")

        return data[0].data.decode("utf-8")
