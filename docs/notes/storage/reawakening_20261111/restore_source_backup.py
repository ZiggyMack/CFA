"""Restore a verified CFA source snapshot into a new empty directory. Never overwrites."""
import argparse,hashlib,json,shutil,sys,os
from pathlib import Path,PurePosixPath
import zipfile

def diskpath(p):
 return Path(chr(92)*2+'?'+chr(92)+os.path.abspath(p)) if os.name=='nt' else Path(p)
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  while block:=f.read(8*1024*1024):h.update(block)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True,type=Path);p.add_argument('--target',required=True,type=Path);p.add_argument('--only',action='append',default=[],help='Restore exact source path; repeat as needed for probes. Default all.');a=p.parse_args()
 root=a.source.resolve();target=a.target.resolve()
 if diskpath(target).exists():raise SystemExit('Choose a new target directory; existing targets are never overwritten.')
 manifest_path=root/'source_manifest.json';receipt=json.loads((root/'verification_receipt.json').read_text(encoding='utf8'))
 if digest(manifest_path)!=receipt['sourceManifestSHA256']:raise SystemExit('Manifest SHA256 mismatch')
 m=json.loads(manifest_path.read_text(encoding='utf8'))
 if m.get('format')!='cfa-recovery-source-parts-v1':raise SystemExit('Unsupported manifest format')
 entries=[x for x in m['sourceFiles'] if not a.only or x['path'] in a.only]
 if a.only and set(a.only)!={x['path'] for x in entries}:raise SystemExit('Requested path absent from manifest')
 parts={x['name']:x for x in m['parts']};needed=sorted({x['part'] for x in entries})
 for name in needed:
  if Path(name).name!=name or name not in parts:raise SystemExit('Unsafe/missing part name')
  path=root/name
  if not path.is_file() or path.stat().st_size!=parts[name]['bytes'] or digest(path)!=parts[name]['sha256']:raise SystemExit('Archive checksum mismatch or missing: '+name)
 diskpath(target).mkdir(parents=True);count=0
 for name in needed:
  with zipfile.ZipFile(root/name) as z:
   for x in entries:
    if x['part']!=name:continue
    rel=PurePosixPath(x['path'])
    if rel.is_absolute() or any(k in ('','..','.') for k in rel.parts) or '\\' in x['path'] or ':' in x['path']:raise SystemExit('Unsafe source path')
    if x['member']!='CFA/'+x['path']:raise SystemExit('Unexpected ZIP member')
    plain_output=target.joinpath(*rel.parts);output=diskpath(plain_output);output.parent.mkdir(parents=True,exist_ok=True)
    if not plain_output.is_relative_to(target):raise SystemExit('Destination escaped target')
    with z.open(x['member']) as src,output.open('xb') as dest:shutil.copyfileobj(src,dest,8*1024*1024)
    if output.stat().st_size!=x['bytes'] or digest(output)!=x['sha256']:raise SystemExit('Restored source checksum mismatch: '+x['path'])
    count+=1
 print(json.dumps({'restoredFiles':count,'target':str(target),'allSelectedFilesSHA256Matched':True},indent=2))
if __name__=='__main__':main()

