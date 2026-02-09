import fitz  # PyMuPDF

file_path = "C:/Users/gorti/Downloads/923ec1bc-academic-catalog-2024-2026.pdf"
doc = fitz.open(file_path)

# Look at a specific page to understand course listing format
page_num = 71  # Bachelor of Science in Accounting
page = doc[page_num]
blocks = page.get_text("dict")["blocks"]  # type: ignore[index]

print(f"PAGE {page_num + 1} - Full text extraction\n")
print("="*80)

for block_idx, block in enumerate(blocks):
    if "lines" not in block:
        continue
    
    print(f"\nBLOCK {block_idx}:")
    for line_idx, line in enumerate(block["lines"]):
        line_text = ""
        for span in line.get("spans", []):
            text = span["text"]
            line_text += text
        
        if line_text.strip():
            print(f"  {line_text}")

doc.close()
