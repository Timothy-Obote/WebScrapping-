import re
from pathlib import Path

def main():
    p=Path('courses_with_names.md').read_text(encoding='utf-8')
    lines=p.splitlines()
    results=[]
    prog=''
    sub=''
    for i,l in enumerate(lines):
        m_prog=re.match(r'^\s*##\s+(.*\S)', l)
        if m_prog:
            prog=m_prog.group(1).strip()
            continue
        m_sub=re.match(r'^\s*###\s+(.*\S)', l)
        if m_sub:
            sub=m_sub.group(1).strip()
            total=None
            for j in range(i+1, i+6):
                if j<len(lines):
                    mtot=re.search(r'Total Courses:\s*(\d+)', lines[j])
                    if mtot:
                        total=int(mtot.group(1))
                        break
            cnt=0
            for j in range(i+1, len(lines)):
                if re.match(r'^\s*##\s+', lines[j]) or re.match(r'^\s*###\s+', lines[j]):
                    break
                if lines[j].strip().startswith('|') and not re.match(r'^\s*\|[-:\s|]+\|\s*$', lines[j]):
                    parts=[p.strip() for p in lines[j].strip().strip('|').split('|')]
                    if len(parts)>=2 and parts[0].lower()!='code' and parts[0]:
                        cnt+=1
            results.append((prog, sub, total, cnt))

    for prog,sub,total,cnt in results:
        if 'Software Engineering' in prog:
            print(f"Program: {prog}\n Subsection: {sub}\n  Declared total: {total}\n  Parsed rows: {cnt}\n")

    mism=[]
    for prog,sub,total,cnt in results:
        if total is None:
            continue
        if total!=cnt:
            mism.append((prog,sub,total,cnt))
    print('\nMismatches (declared vs parsed):', len(mism))
    for prog,sub,total,cnt in mism[:50]:
        print(f"{prog} -> {sub}: declared {total}, parsed {cnt}")

if __name__=='__main__':
    main()
