#!/usr/bin/env python3
"""
Extract all units (courses) for each program from courses.csv and output to a new CSV.

Usage:
  python extract_by_program.py courses.csv programs_output.csv
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

def main():
    input_csv = sys.argv[1] if len(sys.argv) > 1 else 'courses.csv'
    output_csv = sys.argv[2] if len(sys.argv) > 2 else 'programs_with_units.csv'
    
    programs = defaultdict(list)
    
    # Read courses.csv and group by program
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            prog = row['program']
            code = row['code']
            name = row['name']
            programs[prog].append((code, name))
    
    # Write grouped output
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['program', 'total_units', 'code', 'name'])
        
        for prog in sorted(programs.keys()):
            courses_list = programs[prog]
            total = len(courses_list)
            for code, name in courses_list:
                writer.writerow([prog, total, code, name])
    
    print(f'Extracted {len(programs)} programs -> {output_csv}')
    for prog in sorted(programs.keys()):
        print(f'  {prog}: {len(programs[prog])} units')

if __name__ == '__main__':
    main()
