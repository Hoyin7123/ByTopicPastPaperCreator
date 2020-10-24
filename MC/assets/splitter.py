import pytesseract
from PIL import Image, ImageDraw
from pytesseract.pytesseract import Output
import pdf2image

import typing
import re
import pprint


__all__ = ("Splitter", )


class Splitter:
    def __init__(self, images: typing.List[Image.Image]):
        self.images = images
        self.breaks = {}
        self._splitted_images = []

    def gen_breaks(self):
        for page, i in enumerate(self.images):
            d = pytesseract.image_to_data(i, output_type=Output.DICT)
            for index, j in enumerate(d["text"]):
                if re.match(r"^[0-9]+\.$", j):
                    if page not in self.breaks:
                        self.breaks.update({page: []})
                    self.breaks[page].append((d["top"][index] - 10))

    def print_breaks(self):
        for page, breaks in self.breaks.items():
            img = self.images[page]
            for i in breaks:
                w = img.width
                draw = ImageDraw.Draw(img)
                draw.line((0, i, w, i), fill=128)
            img.show(title=str(page))

    def split(self):
        for page, breaks in self.breaks.items():
            img = self.images[page]
            bks = breaks[1:]

            # If that page only has one question
            if not bks:
                self._splitted_images.append(img)
            else:
                for count, b in enumerate(bks):
                    top = 0 if count == 0 else bks[count-1]
                    bottom = img.height if count == len(breaks)-1 else b
                    self._splitted_images.append(img.crop((0, top, img.width, bottom)))
                self._splitted_images.append(img.crop((0, bks[-1], img.width, img.height)))

    @staticmethod
    def _invert_height(y, image: Image.Image):
        return image.height - y
    
    @property
    def results(self):
        return self._splitted_images


if __name__ == "__main__":
    with open("/home/hywong2/Python/experiments/.resources/sample-pdf/geo-p1-2019-p3.pdf", "rb") as file:
        f = file.read()

    parser = Splitter(pdf2image.convert_from_bytes(f))
    parser.gen_breaks()
    print(parser.breaks)
    parser.split()
    for i in parser._splitted_images:
        i.show()
