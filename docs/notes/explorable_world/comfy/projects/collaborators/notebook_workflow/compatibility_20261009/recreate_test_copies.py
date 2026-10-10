"""Reproduce the two bounded compatibility containers without modifying the JPEG.

This creates local temporary files only. It never uploads or alters a catalog.
Run explicitly with Python containing Pillow, reportlab and pypdf.
PDF metadata timestamps may change its file hash; the embedded JPEG must not.
"""
from pathlib import Path
import hashlib

from PIL import Image
from reportlab.pdfgen import canvas
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parents[2] / "lisan_al_gaib/01_Flagship_References/LAG-LOCK-FACE-NATURAL.jpg"
EXPECTED_SHA = "602a9fd4021dc356086728a781aee985741811b3b401a52d9e85869652bb944f"


def main():
    original = SOURCE.read_bytes()
    assert hashlib.sha256(original).hexdigest() == EXPECTED_SHA
    temporary = ROOT / "temporary"
    temporary.mkdir(exist_ok=True)
    png = temporary / "LAG_FACE_source_compatibility_v1.png"
    pdf = temporary / "LAG_FACE_source_compatibility_v1.pdf"
    if png.exists() or pdf.exists():
        raise FileExistsError("Review or clear existing temporary tests before rebuilding.")
    with Image.open(SOURCE) as image:
        image.load()
        image.save(png, format="PNG", compress_level=6)
        with Image.open(png) as check:
            check.load()
            assert (check.mode, check.size, check.tobytes()) == (image.mode, image.size, image.tobytes())
        document = canvas.Canvas(str(pdf), pagesize=image.size)
        document.setTitle("Lisan - visual reference compatibility copy")
        document.drawImage(str(SOURCE), 0, 0, width=image.width, height=image.height)
        document.showPage()
        document.save()
    page = PdfReader(pdf).pages[0]
    images = [x.get_object() for x in page["/Resources"]["/XObject"].values() if x.get_object().get("/Subtype") == "/Image"]
    assert len(images) == 1 and images[0].get_data() == original
    assert SOURCE.read_bytes() == original
    print("Temporary PNG and PDF created; source unchanged. Record new hashes before any test.")


if __name__ == "__main__":
    main()
