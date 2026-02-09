import fitz  # PyMuPDF
import re
import json

file_path = "C:/Users/gorti/Downloads/923ec1bc-academic-catalog-2024-2026.pdf"
doc = fitz.open(file_path)

programs = {}
current_program = None
current_section = None

for page_num in range(67, min(len(doc), 200)):
    page = doc[page_num]
    blocks = page.get_text("dict")["blocks"]  # type: ignore[index]
    
    for block in blocks:
        if "lines" not in block:
            continue
        
        for line in block["lines"]: # type: ignore
            # Combine all spans in the line
            line_text = ""
            for span in line.get("spans", []): # type: ignore
                line_text += span["text"]
            
            line_text = line_text.strip()
            if not line_text:
                continue
            
            # Detect program header (contains "Bachelor of" or "Master of")
            if re.search(r'(Bachelor|Master|Doctor) of', line_text) and len(line_text) < 100:
                current_program = line_text.strip()
                current_section = None
                if current_program not in programs:
                    programs[current_program] = {
                        "sections": {},
                        "courses": {}
                    }
                continue
            
            # Detect section headers with units (e.g., "Lower Level Courses (18 Units)")
            section_match = re.search(r'(.+?)\((\d+)\s+Unit', line_text)
            if section_match and current_program:
                current_section = section_match.group(1).strip()
                units = int(section_match.group(2))
                
                if current_section not in programs[current_program]["sections"]:
                    programs[current_program]["sections"][current_section] = {
                        "units": units,
                        "courses": []
                    }
                continue
            
            # Detect course codes (e.g., "ACT 1010")
            course_match = re.match(r'^([A-Z]{2,4})\s+(\d{3,4})$', line_text)
            if course_match and current_program:
                course_code = line_text
                # The course name should be in the next line, but we'll capture it if available
                if current_section:
                    programs[current_program]["sections"][current_section]["courses"].append({
                        "code": course_code,
                        "name": ""
                    })
                else:
                    if course_code not in programs[current_program]["courses"]:
                        programs[current_program]["courses"][course_code] = ""

doc.close()

# Save to JSON
with open("programs_courses.json", "w") as f:
    json.dump(programs, f, indent=2)

# Generate report
with open("courses_by_program.md", "w") as f:
    f.write("# USIU-Africa Academic Programs & Courses\n\n")
    
    for program_name in sorted(programs.keys()):
        prog_data = programs[program_name]
        f.write(f"\n## {program_name}\n\n")
        
        for section_name in sorted(prog_data["sections"].keys()):
            section = prog_data["sections"][section_name]
            f.write(f"### {section_name} ({section['units']} Units)\n\n")
            f.write("| Code | Name |\n|---|---|\n")
            
            for course in section["courses"]:
                f.write(f"| {course['code']} | {course['name']} |\n")
            
            f.write("\n")

print(f"✓ Extracted {len(programs)} programs")
print(f"✓ Saved to programs_courses.json")
print(f"✓ Saved to courses_by_program.md")

# Print summary
for prog in list(programs.keys())[:3]:
    print(f"\n{prog}:")
    total_units = sum(s["units"] for s in programs[prog]["sections"].values())
    total_courses = sum(len(s["courses"]) for s in programs[prog]["sections"].values())
    print(f"  {total_courses} courses, {total_units} total units")
