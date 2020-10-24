import pytesseract
from pytesseract import Output
from PIL import Image, ImageDraw
import pdf2image

from typing import List


__all__ = ("Pruner", )


class Pruner:
    """
    Represents a pruner object. Prunes headers, footers and unneccesary white spaces.

    :param pdf: Bytes-like object of a pdf file.
    :type pdf: bytes

    :param header_portion: The portion of header.
    :type header_portion: float, optional

    :param footer_portion: THe portion of footer.
    :type footer_portion: float, optional
    """
    def __init__(self, pdf: bytes, *, header_portion: float = 0.1, footer_portion: float = 0.1):
        temp_images: List[Image.Image] = pdf2image.convert_from_bytes(pdf)
        self._images = [i.crop((0, i.height*header_portion, i.width, i.height*(1-footer_portion))) for i in temp_images]
        self._pruned_images = []

    def prune(self):
        for i in self._images:
            d = pytesseract.image_to_data(i, output_type=Output.DICT)
            top = min(x for x in d["top"] if x) - 10
            bottom = max(x + d["height"][i] + 10 for i, x in enumerate(d["top"]) if x)
            print(top, bottom)
            # draw = ImageDraw.Draw(i)
            w = i.width
            # draw.line((0, top, w, top), fill=128)
            # draw.line((0, bottom, w, bottom), fill=128)
            c = i.crop((0, top, w, bottom))
            self._pruned_images.append(c)

    @property
    def results(self):
        return self._pruned_images


if __name__ == "__main__":
    with open("/home/hywong2/Python/experiments/.resources/sample-pdf/geo-p1-2019-p3.pdf", "rb") as file:
        f = file.read()

    pruner = Pruner(f)

