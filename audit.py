import re
from pathlib import Path
from collections import defaultdict

# Get all markdown files
docs_dir = Path("docs")
md_files = sorted(docs_dir.rglob("*.md"))

# Skip .Archive
md_files = [f for f in md_files if ".Archive" not in str(f)]

# Pattern to find markdown links
link_pattern = r'\[([^\]]*)\]\(([^\)]+)\)'

broken_by_severity = {
    'CRITICAL': [],
    'MODERATE': [],
    'MINOR': []
}

broken_by_dir = defaultdict(list)
total_files = 0
total_links = 0

for md_file in md_files:
    total_files += 1
    with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    matches = re.finditer(link_pattern, content)
    
    for match in matches:
        total_links += 1
        link_text = match.group(1)
        link_path = match.group(2)
        
        # Skip external URLs and anchors
        if link_path.startswith(('http://', 'https://', '#')):
            continue
        
        # Skip image links
        if link_path.endswith(('.jpg', '.png', '.gif', '.svg')):
            continue
        
        # Skip template examples
        if 'path/to/' in link_path:
            continue
        
        # Skip computer:/// URLs
        if link_path.startswith('computer://'):
            continue
        
        # Remove anchor if present
        if '#' in link_path:
            target_path = link_path.split('#')[0]
        else:
            target_path = link_path
        
        if not target_path:
            continue
        
        # Resolve path
        file_dir = md_file.parent
        
        if target_path.startswith('../'):
            resolved = (file_dir / target_path).resolve()
        elif target_path.startswith('./'):
            resolved = (file_dir / target_path).resolve()
        elif target_path.startswith('/'):
            resolved = Path(target_path[1:]).resolve()
        else:
            resolved = (file_dir / target_path).resolve()
        
        # Check if target exists
        if not resolved.exists():
            severity = 'MODERATE'
            
            if 'FOR_OMEGA_NOVA' in link_path or '/identity/' in link_path:
                severity = 'CRITICAL'
            
            record = {
                'file': str(md_file),
                'line': content[:match.start()].count('\n') + 1,
                'link_text': link_text[:50],
                'link_path': link_path,
            }
            
            rel_path = str(md_file).split('docs')[1][1:]
            dir_key = rel_path.split('\')[0] if '\' in rel_path else 'root'
            broken_by_dir[dir_key].append(record)
            broken_by_severity[severity].append(record)

# Print results
print("FILES SCANNED:", total_files)
print("LINKS CHECKED:", total_links)
total_broken = sum(len(v) for v in broken_by_severity.values())
print("BROKEN LINKS:", total_broken)
print()

# Critical
print("CRITICAL LINKS (Deleted directories):")
critical = broken_by_severity['CRITICAL']
print(f"Count: {len(critical)}")
if critical:
    for item in critical[:10]:
        print(f"  {item['file'].split('docs')[1][1:]}:{item['line']}")
        print(f"    -> {item['link_path']}")
print()

# Moderate
print("MODERATE LINKS (Incorrect paths):")
moderate = broken_by_severity['MODERATE']
print(f"Count: {len(moderate)}")
print()

# By directory
print("BROKEN LINKS BY DIRECTORY:")
for dir_key in sorted(broken_by_dir.keys()):
    items = broken_by_dir[dir_key]
    print(f"  {dir_key}: {len(items)}")

# Show top problematic files
print()
print("TOP PROBLEMATIC FILES:")
file_counts = defaultdict(int)
for items in broken_by_severity.values():
    for item in items:
        file_counts[item['file']] += 1

for file_path, count in sorted(file_counts.items(), key=lambda x: -x[1])[:15]:
    rel = file_path.split('docs')[1][1:] if 'docs' in file_path else file_path
    print(f"  {rel}: {count}")

