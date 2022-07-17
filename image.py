""""""

import qrcode
import qrtools

import numpy as np

from PIL import Image


class NoQRImageException(BaseException):
    """No Image received Error."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class EmptyQRText(BaseException):
    """No text to convert to QR Error."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class QRImage:
    """"""

    def __init__(self, img_path: str) -> None:
        """
        Initialize QRImage instance

        Parameters
        ----------
        img_path : str
            path to the image
        """
        try:
            self.image = Image.open(img_path, 'r')
            self.image_rgba = np.asarray(self.image.convert('L'))
            print(self.image_rgba)
        except OSError as error:
            raise NoQRImageException(f"{img_path}, Couldn't find or open the image") from error

    def __flatten_image(self) -> None:
        """Flatten the image, so that every red chanel has even number."""
        for i, val in enumerate(self.image_rgba):
            red, green, blue = val
            if red % 2:
                if red == 255:
                    self.image_rgba[i] = red - 1, green, blue
                else:
                    self.image_rgba[i] = red + 1, green, blue

    def encode(self, text: str) -> Image:
        """_summary_

        Parameters
        ----------
        text : str
            _description_

        Returns
        -------
        Image
            _description_
        """
        if not text:
            raise EmptyQRText("Text can't be empty")

        self.__flatten_image()

        qr = qrcode.QRCode()
        qr.add_data(text)
        qr_code = qrcode.make()
        qr_rgba = np.asarray(qr_code.convert('L'))
        # new_img = Image.new("RGB", qr_code.size)
        # new_img.putdata(qr_code_rgba)
        # new_img.save("QR2.png")
        print()

        # print(qr_code_rgba)
        for i, val in enumerate(qr_rgba):
            if val == 0:
                self.image_rgba[i] = self.image_rgba[i][0] - 100, self.image_rgba[i][1], self.image_rgba[i][2]
        new_img = Image.new("RGB", self.image.size)
        new_img.putdata(self.image_rgba)
        return new_img

    def decode(self) -> str:
        qr_rgba = []
        for i, val in enumerate(self.image_rgba):
            red, green, blue = val
            if red % 2:
                qr_rgba.append((0, 0, 0))
            else:
                qr_rgba.append((255, 255, 255))
        # print(qr_rgba)
        new_img = Image.new("RGB", self.image.size)
        new_img.putdata(qr_rgba)
        new_img.save("Qr.png")
        #qr = qrtools.QR()
        # qr.decode()
        # return qr.data


if __name__ == "__main__":
    new_img = QRImage("img/ex1.jpg")
    #new_img = QRImage("img/ex3.png")
    new = new_img.encode("asdsadasdsadsad")
    new.save("New_img.png")
    new_img.decode()
