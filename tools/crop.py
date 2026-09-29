import fitz
import sys

pdf_path = sys.argv[1]
page_no = int(sys.argv[2])  # 1-based
x0, y0, x1, y1 = map(float, sys.argv[3:7])  # fractions 0-1
dpi = int(sys.argv[7]) if len(sys.argv) > 7 else 500
out = sys.argv[8]

doc = fitz.open(pdf_path)
page = doc[page_no - 1]
r = page.rect
clip = fitz.Rect(r.x0 + x0*r.width, r.y0 + y0*r.height, r.x0 + x1*r.width, r.y0 + y1*r.height)
zoom = dpi / 72
mat = fitz.Matrix(zoom, zoom)
pix = page.get_pixmap(matrix=mat, clip=clip)
pix.save(out)
print(out, pix.width, pix.height)
