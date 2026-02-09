import fitz  # PyMuPDF
import re

file_path = "C:/Users/gorti/Downloads/923ec1bc-academic-catalog-2024-2026.pdf"
doc = fitz.open(file_path)

programs = {}
current_program = None
current_section = None

for page_num in range(67, min(len(doc), 200)):
    page = doc[page_num]
    blocks = page.get_text("dict")["blocks"]  # type: ignore[index]
    
    # Collect all text lines from page
    page_lines = []
    for block in blocks:
        if "lines" not in block:
            continue
        
        for line in block["lines"]: # type: ignore
            line_text = ""
            for span in line.get("spans", []): # type: ignore
                line_text += span["text"]
            
            line_text = line_text.strip()
            if line_text:
                page_lines.append(line_text)
    
    # Now process lines with lookahead for course names
    i = 0
    while i < len(page_lines):
        line = page_lines[i]
        
        # Detect program
        if re.search(r'(Bachelor|Master|Doctor) of', line) and len(line) < 100:
            current_program = line
            current_section = None
            if current_program not in programs:
                programs[current_program] = {
                    "sections": {},
                    "courses_list": []
                }
            i += 1
            continue
        
        # Detect section headers with units
        section_match = re.search(r'(.+?)\((\d+)\s+Unit', line)
        if section_match and current_program:
            current_section = section_match.group(1).strip()
            units = int(section_match.group(2))
            
            if current_section not in programs[current_program]["sections"]:
                programs[current_program]["sections"][current_section] = {
                    "total_units": units,
                    "courses": []
                }
            i += 1
            continue
        
        # Detect course code and look for name in next line
        course_match = re.match(r'^([A-Z]{2,4})\s+(\d{3,4})$', line)
        if course_match and current_program and current_section:
            code = line
            # Look for course name in next line
            name = ""
            if i + 1 < len(page_lines):
                next_line = page_lines[i + 1]
                # If next line is not a course code, it's likely the name
                if not re.match(r'^[A-Z]{2,4}\s+\d{3,4}', next_line):
                    name = next_line
                    i += 2
                    programs[current_program]["sections"][current_section]["courses"].append({
                        "code": code,
                        "name": name
                    })
                    continue
        
        i += 1

doc.close()

# Generate markdown report
output = "# USIU-Africa Programs, Courses & Units\n\n"

for program_name in sorted(programs.keys()):
    if not programs[program_name]["sections"]:
        continue
    
    output += f"## {program_name}\n\n"
    
    for section_name in sorted(programs[program_name]["sections"].keys()):
        section = programs[program_name]["sections"][section_name]
        total_units = section["total_units"]
        courses = section["courses"]
        
        output += f"### {section_name} ({total_units} Units)\n\n"
        output += f"**Total Courses: {len(courses)}**\n\n"
        output += "| Code | Course Name |\n|---|---|\n"
        
        for course in courses:
            code = course["code"].strip()
            name = course["name"].strip()
            output += f"| {code} | {name} |\n"
        
        output += "\n"

with open("courses_with_names.md", "w") as f:
    f.write(output)

print("✓ Generated courses_with_names.md")

# Also count totals
total_progs = len([p for p in programs.values() if p["sections"]])
total_sections = sum(len(p["sections"]) for p in programs.values())
total_courses = sum(len(s["courses"]) for p in programs.values() for s in p["sections"].values())
total_units = sum(s["total_units"] for p in programs.values() for s in p["sections"].values())

print(f"Summary:")
print(f"  Programs: {total_progs}")
print(f"  Sections: {total_sections}")
print(f"  Courses: {total_courses}")
print(f"  Total Units: {total_units}")
