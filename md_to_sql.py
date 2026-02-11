#!/usr/bin/env python3
"""Convert `courses_with_names.md` into `courses.csv` and `courses.sql`.

Usage:
  python md_to_sql.py courses_with_names.md
  python md_to_sql.py --csv out.csv --sql out.sql
"""
import re
import csv
import argparse

def parse(md_path):
    rows = []
    program = ''
    with open(md_path, encoding='utf-8') as f:
        for raw in f:
            line = raw.rstrip('\n')
            # Program heading: level-2 headings (##)
            m_prog = re.match(r'^\s*##\s+(.*\S)', line)
            if m_prog:
                program = m_prog.group(1).strip()
                continue
            # skip markdown table separator lines
            if re.match(r'^\s*\|[-:\s|]+\|\s*$', line):
                continue
            # parse table rows like: | CODE | Course Name |
            if line.strip().startswith('|'):
                parts = [p.strip() for p in line.strip().strip('|').split('|')]
                if len(parts) >= 2:
                    code, name = parts[0], parts[1]
                    if not code or code.lower() == 'code':
                        continue
                    # normalize whitespace
                    name = ' '.join(name.split())
                    rows.append((program, code, name))
    return rows

def write_csv(rows, out_path):
    with open(out_path, 'w', newline='', encoding='utf-8') as fp:
        w = csv.writer(fp)
        w.writerow(['program', 'code', 'name'])
        for r in rows:
            w.writerow(r)

def write_sql(rows, out_path, table='courses'):
    def esc(s):
        return s.replace("'", "''")
    with open(out_path, 'w', encoding='utf-8') as fp:
        fp.write(f"CREATE TABLE IF NOT EXISTS {table} (\n  id INTEGER PRIMARY KEY AUTOINCREMENT,\n  program TEXT,\n  code TEXT,\n  name TEXT\n);\n\n")
        for program, code, name in rows:
            fp.write("INSERT INTO {} (program, code, name) VALUES ('{}','{}','{}');\n".format(
                table, esc(program), esc(code), esc(name)
            ))

def main():
    p = argparse.ArgumentParser(description='Convert courses markdown to CSV and SQL')
    p.add_argument('md', nargs='?', default='courses_with_names.md', help='markdown file')
    p.add_argument('--csv', default='courses.csv', help='output CSV file')
    p.add_argument('--sql', default='courses.sql', help='output SQL file')
    args = p.parse_args()

    rows = parse(args.md)
    write_csv(rows, args.csv)
    write_sql(rows, args.sql)
    print(f'Wrote {len(rows)} rows -> {args.csv}, {args.sql}')

if __name__ == '__main__':
    main()
