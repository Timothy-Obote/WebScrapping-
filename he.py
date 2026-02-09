import fitz  # PyMuPDF

file_path = "C:/Users/gorti/Downloads/923ec1bc-academic-catalog-2024-2026.pdf"
doc = fitz.open(file_path)

undergraduate_courses = []
graduate_courses = []
doctoral_courses = []

current_section = None

# Pages are 0-indexed, so page 68 is 67
for page_num in range(67, min(len(doc), 160)):
    page = doc[page_num]
    blocks = page.get_text("dict")["blocks"]  # type: ignore[index]
    
    for block in blocks:
        if "lines" in block:
            for line in block["lines"]: # type: ignore
                for span in line.get("spans", []): # type: ignore
                    text = span["text"].strip()
                    
                    # Track section headers
                    if "UNDERGRADUATE PROGRAMS" in text:
                        current_section = "undergraduate"
                    elif "GRADUATE PROGRAMS" in text:
                        current_section = "graduate"
                    elif "DOCTORAL PROGRAMS" in text:
                        current_section = "doctoral"
                    
                    # Extract courses (lines starting with bullet point)
                    if text.startswith("•"):
                        course_name = text.replace("•", "").strip()
                        # Remove " - Available Online" or " - Online Only" suffix
                        course_name = course_name.split(" - Available Online")[0]
                        course_name = course_name.split(" - Online Only")[0]
                        course_name = course_name.strip()
                        
                        if course_name and current_section:
                            if current_section == "undergraduate":
                                undergraduate_courses.append(course_name)
                            elif current_section == "graduate":
                                graduate_courses.append(course_name)
                            elif current_section == "doctoral":
                                doctoral_courses.append(course_name)

# Remove duplicates
undergraduate_courses = list(dict.fromkeys(undergraduate_courses))  # Preserve order
graduate_courses = list(dict.fromkeys(graduate_courses))
doctoral_courses = list(dict.fromkeys(doctoral_courses))

# Output
print("UNDERGRADUATE COURSES:")
for course in undergraduate_courses:
    print(f"  • {course}")

print(f"\nGRADUATE COURSES:")
for course in graduate_courses:
    print(f"  • {course}")

print(f"\nDOCTORAL COURSES:")
for course in doctoral_courses:
    print(f"  • {course}")

print(f"\n--- Summary ---")
print(f"Undergraduate: {len(undergraduate_courses)}")
print(f"Graduate: {len(graduate_courses)}")
print(f"Doctoral: {len(doctoral_courses)}")

doc.close()
