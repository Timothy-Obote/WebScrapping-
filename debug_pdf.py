import fitz  # PyMuPDF

file_path = "C:/Users/gorti/Downloads/923ec1bc-academic-catalog-2024-2026.pdf"
doc = fitz.open(file_path)

print(f"Total pages: {len(doc)}\n")

# Look at a single page in detail
page_num = 68
page = doc[page_num]
blocks = page.get_text("dict")["blocks"]  # type: ignore[index]

print(f"Page {page_num} - All text blocks:\n")

for block_idx, block in enumerate(blocks):
    if "lines" in block:
        print(f"Block {block_idx}:")
        for line_idx, line in enumerate(block["lines"]): # type: ignore
            for span_idx, span in enumerate(line.get("spans", [])): # type: ignore
                text = span["text"]
                font = span.get("font", "unknown")
                size = span.get("size", 0)
                flags = span["flags"]
                color = span.get("fill", 0)
                is_bold = flags & 2 != 0
                is_italic = flags & 1 != 0
                
                if text.strip():
                    print(f"  {text!r}")
                    print(f"    Font: {font}, Size: {size}, Bold: {is_bold}, Italic: {is_italic}")

doc.close()
