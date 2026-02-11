#!/usr/bin/env python3
"""
Create a comprehensive CSV with all programs from Courses.md and their units from courses_with_names.md.

Usage:
  python all_programs_units.py Courses.md programs_with_units.csv all_courses_complete.csv
"""
import csv
import re
import sys
from pathlib import Path

def parse_courses_md(file_path):
    """Extract all programs by level from Courses.md"""
    text = Path(file_path).read_text(encoding='utf-8')
    
    levels = {'Undergraduate': [], 'Graduate': [], 'Doctoral': []}
    current_level = None
    
    for line in text.splitlines():
        # Check for level headers
        if 'UNDERGRADUATE COURSES:' in line:
            current_level = 'Undergraduate'
        elif 'GRADUATE COURSES:' in line:
            current_level = 'Graduate'
        elif 'DOCTORAL COURSES:' in line:
            current_level = 'Doctoral'
        
        # Parse bullet points
        if line.strip().startswith('•') and current_level:
            prog = line.strip().lstrip('•').strip()
            # Skip lines that look like descriptions (no degree name pattern)
            if any(word in prog.lower() for word in ['bachelor', 'master', 'doctor', 'phd', 'dba', 'psyd']):
                levels[current_level].append(prog)
    
    return levels

def load_existing_courses(csv_path):
    """Load existing course data and create a program->units mapping"""
    prog_units = {}
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            prog = row['program']
            if prog not in prog_units:
                prog_units[prog] = []
            prog_units[prog].append({
                'code': row['code'],
                'name': row['name'],
                'total': row['total_units']
            })
    
    return prog_units

def fuzzy_match(prog_name, existing_progs):
    """Try to match a program name from Courses.md with existing programs"""
    # Normalize: lowercase, remove special chars and suffixes
    norm_prog = prog_name.lower().replace('–', '-').replace(' & ', ' and ').split('(')[0].strip()
    
    for existing in existing_progs:
        norm_exist = existing.lower().replace('–', '-').replace(' & ', ' and ').split('(')[0].strip()
        
        # Exact match
        if norm_prog == norm_exist:
            return existing
        
        # Remove "Online only" and other suffixes
        norm_prog_clean = ' '.join(norm_prog.split())
        norm_exist_clean = ' '.join(norm_exist.split())
        
        if norm_prog_clean == norm_exist_clean:
            return existing
        
        # Partial/fuzzy match (at least 5 words should match)
        prog_words = set(norm_prog_clean.split())
        exist_words = set(norm_exist_clean.split())
        if len(prog_words & exist_words) >= len(prog_words) - 1:
            return existing
    
    return None

def main():
    courses_md = sys.argv[1] if len(sys.argv) > 1 else 'Courses.md'
    units_csv = sys.argv[2] if len(sys.argv) > 2 else 'programs_with_units.csv'
    output_csv = sys.argv[3] if len(sys.argv) > 3 else 'all_courses_complete.csv'
    
    # Parse Courses.md
    levels = parse_courses_md(courses_md)
    
    # Load existing course data
    prog_units = load_existing_courses(units_csv)
    existing_progs = list(prog_units.keys())
    
    # Write output CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['level', 'program', 'total_units', 'code', 'name', 'status'])
        
        matched = 0
        unmatched = 0
        
        for level in ['Undergraduate', 'Graduate', 'Doctoral']:
            for prog in levels[level]:
                # Try to find matching courses
                found = fuzzy_match(prog, existing_progs)
                
                if found and found in prog_units:
                    # Write all units for this program
                    for unit in prog_units[found]:
                        writer.writerow([level, prog, unit['total'], unit['code'], unit['name'], 'Matched'])
                    matched += 1
                else:
                    # Write placeholder row for programs without course details
                    writer.writerow([level, prog, 'N/A', '', '', 'No Units Found'])
                    unmatched += 1
        
        total = matched + unmatched
        print(f'\nOutput: {output_csv}')
        print(f'Programs with units: {matched}')
        print(f'Programs without units: {unmatched}')
        print(f'Total programs: {total}')

if __name__ == '__main__':
    main()
