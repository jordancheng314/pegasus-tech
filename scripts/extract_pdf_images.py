# -*- coding: utf-8 -*-
import os
import subprocess
import sys

def ensure_fitz():
    try:
        import fitz
        return fitz
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pymupdf", "-q"])
        import fitz
        return fitz


PDF = r"E:\Pegasus\demo\飛馬先進科技20260515.pdf"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "images")
os.makedirs(OUT, exist_ok=True)


def main() -> None:
    fitz = ensure_fitz()
    doc = fitz.open(PDF)
    print("pages", doc.page_count)
    count = 0
    for i, page in enumerate(doc):
        images = page.get_images(full=True)
        print(f"page {i + 1}: {len(images)} images")
        for j, img in enumerate(images):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n - pix.alpha > 3:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            name = os.path.join(OUT, f"pdf-p{i + 1}-{j + 1}.png")
            pix.save(name)
            print("saved", name, pix.width, pix.height)
            count += 1
    for i, page in enumerate(doc):
        mat = fitz.Matrix(2.0, 2.0)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        name = os.path.join(OUT, f"pdf-page-{i + 1}.jpg")
        pix.save(name)
        print("page-render", name, pix.width, pix.height)
    print("embedded-images", count)


if __name__ == "__main__":
    main()
