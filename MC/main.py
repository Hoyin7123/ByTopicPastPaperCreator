from MC.assets import Splitter, Pruner
from docx import Document
from docx.shared import Inches
from PIL import Image

from io import BytesIO
from typing import List


def main():
    with open("../resources/sample_mc/geography/2019.pdf", "rb") as file:
        f = file.read()

    pruner = Pruner(f)
    pruner.prune()
    pruned_images = pruner.results

    splitter = Splitter(pruned_images)
    splitter.gen_breaks()
    splitter.split()
    questions: List[Image] = splitter.results

    doc = Document()

    for q in questions:
        b = BytesIO()
        q.save(b, "PNG")
        doc.add_picture(b, width=Inches(8.5))

    doc.save("../results/test.docx")


if __name__ == "__main__":
    main()
