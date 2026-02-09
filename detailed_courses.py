import fitz  # PyMuPDF
import re
import csv

file_path = "C:/Users/gorti/Downloads/923ec1bc-academic-catalog-2024-2026.pdf"
doc = fitz.open(file_path)

# Store all course information: course_code -> (name, units)
all_courses = {}
program_courses = {}  # program -> [list of course codes]
current_program = None

for page_num in range(67, min(len(doc), 250)):
    page = doc[page_num]
    blocks = page.get_text("dict")["blocks"]  # type: ignore[index]
    
    # Extract full text from page to parse course patterns
    page_text = []
    for block in blocks:
        if "lines" in block:
            for line in block["lines"]: # type: ignore
                line_text = ""
                for span in line.get("spans", []): # type: ignore
                    line_text += span["text"]
                page_text.append(line_text.strip())
    
    # Detect program
    for line in page_text:
        if "Bachelor of" in line and "Master of" not in line:
            current_program = line.replace("Master of", "").strip()
            if current_program not in program_courses:
                program_courses[current_program] = []
    
    # Parse course codes with names and units
    # Pattern: "ACC 101  Accounting Fundamentals (3 UNITS)"
    for i, line in enumerate(page_text):
        # Look for course code pattern
        match = re.search(r'([A-Z]{2,4})\s+(\d{3,4})\s+(.+?)\((\d+)\s+UNIT', line)
        if match:
            course_code = f"{match.group(1)} {match.group(2)}"
            course_name = match.group(3).strip()
            units = int(match.group(4))
            
            all_courses[course_code] = (course_name, units)
            
            if current_program:
                program_courses[current_program].append(course_code)

doc.close()

# Generate CSV report
with open("courses_report.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Program", "Course Code", "Course Name", "Units"])
    
    for program in sorted(program_courses.keys()):
        for course_code in sorted(set(program_courses[program])):
            if course_code in all_courses:
                name, units = all_courses[course_code]
                writer.writerow([program, course_code, name, units])

# Generate Markdown report
with open("courses_report.md", "w", encoding="utf-8") as f:
    f.write("# USIU-Africa Course Catalog\n\n")
    
    total_courses = 0
    total_units = 0
    
    for program in sorted(program_courses.keys()):
        courses = sorted(set(program_courses[program]))
        if not courses:
            continue
        
        f.write(f"## {program}\n\n")
        f.write("| Course Code | Course Name | Units |\n")
        f.write("|---|---|---|\n")
        
        program_units = 0
        for course_code in courses:
            if course_code in all_courses:
                name, units = all_courses[course_code]
                f.write(f"| {course_code} | {name} | {units} |\n")
                program_units += units
                total_courses += 1
                total_units += units
        
        f.write(f"\n**Total: {len(courses)} courses, {program_units} units**\n\n")
    
    f.write(f"\n---\n\n**Grand Total: {total_courses} courses, {total_units} units**\n")

print(f"✓ Generated courses_report.csv")
print(f"✓ Generated courses_report.md")
print(f"\nSummary: {len(all_courses)} unique courses, {len(program_courses)} programs")
print(f"Total Units Offered: {sum(units for _, units in all_courses.values())}")
