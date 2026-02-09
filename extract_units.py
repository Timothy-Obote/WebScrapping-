import fitz  # PyMuPDF
import re
import json

file_path = "C:/Users/gorti/Downloads/923ec1bc-academic-catalog-2024-2026.pdf"
doc = fitz.open(file_path)

programs = {}  # {program_name: {sections: {...}, courses: [...]}}
current_program = None
current_section = None
current_requirement = None

# Track pages covered
for page_num in range(67, min(len(doc), 250)):
    page = doc[page_num]
    blocks = page.get_text("dict")["blocks"]  # type: ignore[index]
    
    for block in blocks:
        if "lines" not in block:
            continue
        
        for line in block["lines"]: # type: ignore
            for span in line.get("spans", []): # type: ignore
                text = span["text"].strip()
                font = span.get("font", "")
                size = span.get("size", 0)
                
                # Skip empty text
                if not text or len(text) < 2:
                    continue
                
                # Detect program header (large bold text)
                if size >= 20 and "Bachelor" in text:
                    current_program = text
                    programs[current_program] = {
                        "page": page_num,
                        "requirements": {},
                        "courses": []
                    }
                
                # Detect requirement headers (bold, ~8-12pt)
                elif "BOLD" in font and size <= 12 and current_program:
                    # Look for unit counts like "CORE COURSES (18 UNITS)"
                    if "UNIT" in text.upper():
                        current_requirement = text
                        if current_requirement not in programs[current_program]["requirements"]:
                            programs[current_program]["requirements"][current_requirement] = []
                
                # Detect course codes (format like "ACC 101")
                elif current_program and re.match(r'^[A-Z]{2,4}\s+\d{3}', text):
                    programs[current_program]["courses"].append(text)

print("=" * 80)
print("EXTRACTED COURSE UNITS BY PROGRAM")
print("=" * 80)

for prog_name in sorted(programs.keys()):
    prog_data = programs[prog_name]
    print(f"\n{prog_name}")
    print(f"  Page: {prog_data['page'] + 1}")
    
    if prog_data["requirements"]:
        print(f"  Requirements:")
        for req, courses in prog_data["requirements"].items():
            print(f"    • {req}")
    
    if prog_data["courses"]:
        print(f"  Courses ({len(prog_data['courses'])} found):")
        for course in prog_data["courses"][:10]:  # First 10
            print(f"    - {course}")
        if len(prog_data["courses"]) > 10:
            print(f"    ... and {len(prog_data['courses']) - 10} more")

# Save to JSON for further processing
with open("programs_data.json", "w") as f:
    json.dump(programs, f, indent=2)

print(f"\n✓ Extracted {len(programs)} programs")
print("✓ Saved to programs_data.json")

doc.close()
