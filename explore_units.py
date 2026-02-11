import fitz  # PyMuPDF

file_path = "C:/Users/gorti/Downloads/923ec1bc-academic-catalog-2024-2026.pdf"
doc = fitz.open(file_path)

print(f"Total pages: {len(doc)}\n")

# Explore a few pages to understand unit structure
# Let's start after the programs overview (page 70+)
for page_num in range(70, min(80, len(doc))):
    page = doc[page_num]
    blocks = page.get_text("dict")["blocks"]  # type: ignore[index]
    
    print(f"\n{'='*60}")
    print(f"PAGE {page_num + 1}")
    print(f"{'='*60}\n")
    
    for block in blocks:
        if "lines" in block:
            for line in block["lines"]: # type: ignore
                for span in line.get("spans", []): # type: ignore
                    text = span["text"].strip()
                    font = span.get("font", "")
                    size = span.get("size", 0)
                    
                    if text and len(text.strip()) > 3:
                        # Show structure: course headers, units, etc.
                        if size > 10:
                            print(f"[LARGE {size}] {text}")
                        elif "HelveticaNeue-Bold" in font:
                            print(f"[BOLD] {text}")
                        elif text.startswith("•"):
                            print(f"[BULLET] {text}")
                        elif text.startswith("-"):
                            print(f"[DASH] {text}")

doc.close()
