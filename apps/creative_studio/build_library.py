"""Build the hosted review library from local CFA masters; no network or source edits.

Run from any directory: python apps/creative_studio/build_library.py
Optional --ffmpeg selects an installed FFmpeg binary. Pillow is required.
"""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
import hashlib
from io import BytesIO
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import unquote

from PIL import Image, ImageOps, __version__ as pillow_version

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'docs/notes/explorable_world/comfy/projects/visual_library/catalog.js'
OUT = Path(__file__).resolve().parent / 'library'
SETTINGS = {'image_long_edge':1280, 'image_quality':82, 'thumb_long_edge':480,
            'thumb_quality':85, 'video_max_width':854, 'video_crf':28,
            'video_preset':'medium', 'audio_bitrate':'96k'}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--ffmpeg', help='FFmpeg executable; bundled local fallback or PATH by default')
args = parser.parse_args()
bundled = ROOT / '.cache/hon_dolo_i2v_20261004/python_packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
FF = args.ffmpeg or (str(bundled) if bundled.is_file() else shutil.which('ffmpeg'))
if not FF:
    raise SystemExit('FFmpeg is required: use --ffmpeg PATH or install it locally. No automatic download is attempted.')
TOOLS = {'pillow':pillow_version,'ffmpeg':subprocess.run([FF,'-version'],capture_output=True,text=True,check=True).stdout.splitlines()[0]}
assert OUT.resolve().is_relative_to(ROOT), 'Output must remain inside CFA'
OUT.mkdir(parents=True, exist_ok=True)
for folder in ('images','thumbs','videos','animations','docs'):
    (OUT/folder).mkdir(exist_ok=True)

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def source_path(relative: str) -> Path:
    p = (SOURCE.parent/unquote(relative)).resolve()
    if not p.is_relative_to(ROOT) or not p.is_file():
        raise ValueError(f'Missing or out-of-workspace source: {relative}')
    return p

def repo_path(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()

def clean_text(value: str) -> str:
    # Source documents are retained locally. Hosted text avoids machine-specific user paths.
    for root in (str(ROOT), ROOT.as_posix()):
        value = re.sub(re.escape(root)+r'[\\/]*', '', value, flags=re.I)
    return re.sub(r'(?i)\b[A-Z]:[\\/][^\s"<>|]+', '[local path]', value)

def clean_values(value):
    if isinstance(value,str): return clean_text(value)
    if isinstance(value,list): return [clean_values(x) for x in value]
    if isinstance(value,dict): return {k:clean_values(v) for k,v in value.items()}
    return value

catalog_bytes = SOURCE.read_bytes()
catalog = json.loads(catalog_bytes.decode('utf-8-sig').split('=',1)[1].strip().rstrip(';'))
old_manifest = json.loads((OUT/'manifest.json').read_text(encoding='utf-8')) if (OUT/'manifest.json').exists() else {}
old_outputs = {r['path']:r for r in old_manifest.get('outputs',[])} if old_manifest.get('settings')==SETTINGS and old_manifest.get('tools')==TOOLS else {}
sources={}
assets=[]
for asset in catalog['assets']:
    a=dict(asset)
    p=source_path(a['src']); raw=p.read_bytes(); digest=sha(raw)
    if a.get('sha256') and a['sha256']!=digest:
        raise ValueError(f'Registered source hash changed: {a["filename"]}')
    sources.setdefault(repo_path(p), {'path':repo_path(p),'sha256':digest,'bytes':len(raw),'role':'master_or_unchanged_review_copy'})
    a['_source']=p; a['_hash']=digest
    if a.get('thumb'):
        tp=source_path(a['thumb']);tr=tp.read_bytes()
        sources.setdefault(repo_path(tp), {'path':repo_path(tp),'sha256':sha(tr),'bytes':len(tr),'role':'existing_display_thumbnail_or_reference'})
        a['_thumb_source']=tp
    assets.append(a)

def cached(path: Path, original_sha: str) -> bool:
    old=old_outputs.get(path.relative_to(OUT).as_posix())
    return bool(old and old['source_sha256']==original_sha and path.is_file() and sha(path.read_bytes())==old['sha256'])

def output_record(path:Path, source_sha:str, role:str, **extra):
    raw=path.read_bytes()
    return {'path':path.relative_to(OUT).as_posix(),'sha256':sha(raw),'bytes':len(raw),
            'source_sha256':source_sha,'role':role,**extra}

def jpeg(source:Path, target:Path, edge:int, quality:int, digest:str, role:str):
    if not cached(target,digest):
        with Image.open(source) as image:
            image=ImageOps.exif_transpose(image).convert('RGB')
            image.thumbnail((edge,edge),Image.Resampling.LANCZOS)
            image.save(target,format='JPEG',quality=quality,optimize=True)
    with Image.open(target) as image:
        image.load(); width,height=image.size
    if max(width,height)>edge: raise ValueError('Oversized display JPEG')
    return output_record(target,digest,role,width=width,height=height,decode='passed')

def frame_audit(path:Path):
    cmd=[FF,'-hide_banner','-v','info','-i',str(path),'-map','0:v:0','-map','0:a?', '-f','framemd5','pipe:1']
    result=subprocess.run(cmd,capture_output=True,check=True)
    text=result.stdout.decode('utf-8','replace');log=result.stderr.decode('utf-8','replace')
    timebases={int(k):Fraction(v) for k,v in re.findall(r'^#tb (\d+): (\S+)',text,re.M)}
    streams={}
    for line in text.splitlines():
        if not line or line.startswith('#'):continue
        parts=[p.strip() for p in line.split(',')]
        n=int(parts[0]);dt=int(parts[3]);s=streams.setdefault(n,{'frames':0,'ticks':0,'first_pts':int(parts[2]),'end_pts':0})
        s['frames']+=1;s['ticks']+=dt;s['end_pts']=int(parts[2])+dt
    for n,s in streams.items():
        s['duration_seconds']=float(s['ticks']*timebases[n]);s['time_base']=str(timebases[n])
    video_line=next(x for x in log.splitlines() if 'Stream #0:' in x and 'Video:' in x)
    dim=re.search(r'(\d{2,5})x(\d{2,5})',video_line)
    return {'width':int(dim[1]),'height':int(dim[2]),'streams':streams,'decode':'passed'}

def video_dimensions(width:int,height:int):
    # Use an even integer multiple of the exact source aspect ratio. 1280x720 -> 832x468.
    g=math.gcd(width,height);unit_w,unit_h=width//g,height//g
    step=2 if unit_w%2 or unit_h%2 else 1
    count=min(g,SETTINGS['video_max_width']//unit_w);count-=count%step
    if count<step:raise ValueError('Source aspect ratio has no exact even proxy below configured width')
    return unit_w*count,unit_h*count

unique={}
for a in assets: unique.setdefault((a['kind'],a['_hash']),a)

def build_one(a):
    kind=a['kind'];digest=a['_hash'];source=a['_source'];records=[]
    if kind=='image':
        dest=OUT/'images'/f'{digest}.jpg'
        records.append(jpeg(source,dest,1280,82,digest,'full_view_image_preview'))
    elif kind=='video':
        # Keep the supplied video basename, with a content-hash directory avoiding collisions.
        dest=OUT/'videos'/digest/source.name;dest.parent.mkdir(exist_ok=True)
        previous=old_outputs.get(dest.relative_to(OUT).as_posix())
        if cached(dest,digest) and previous.get('source_probe') and previous.get('proxy_probe'):
            # Both complete files were rehashed; retain their measured decode/timing receipt.
            records.append(dict(previous))
        else:
            original=frame_audit(source)
            width,height=video_dimensions(original['width'],original['height'])
            subprocess.run([FF,'-hide_banner','-v','error','-y','-i',str(source),'-map','0:v:0','-map','0:a?',
                            '-vf',f'scale={width}:{height}:flags=lanczos','-c:v','libx264','-preset','medium','-crf','28',
                            '-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-movflags','+faststart','-map_metadata','-1',str(dest)],check=True)
            proxy=frame_audit(dest)
            if original['streams'][0]['frames']!=proxy['streams'][0]['frames']:
                raise ValueError(f'Video frame count changed: {source.name}')
            if abs(original['streams'][0]['duration_seconds']-proxy['streams'][0]['duration_seconds'])>1e-7:
                raise ValueError(f'Video timing changed: {source.name}')
            if original['width']*proxy['height']!=original['height']*proxy['width']:
                raise ValueError(f'Aspect ratio changed: {source.name}')
            if set(original['streams'])!=set(proxy['streams']):raise ValueError('Audio track disappeared')
            for n in original['streams']:
                if n and abs(original['streams'][n]['duration_seconds']-proxy['streams'][n]['duration_seconds'])>0.022:
                    raise ValueError(f'Audio duration changed beyond one AAC frame: {source.name}')
            records.append(output_record(dest,digest,'video_proxy_full_duration_full_audio',source_probe=original,proxy_probe=proxy))
    elif kind in ('gif','pdf'):
        dest=OUT/('animations' if kind=='gif' else 'docs')/(digest+('.gif' if kind=='gif' else '.pdf'))
        if not cached(dest,digest):shutil.copyfile(source,dest)
        if sha(dest.read_bytes())!=digest:raise ValueError('Unchanged copy mismatch')
        extra={}
        if kind=='gif':
            with Image.open(dest) as image:
                for i in range(image.n_frames):image.seek(i);image.load()
                extra={'frames':image.n_frames,'width':image.width,'height':image.height,'decode':'passed'}
        records.append(output_record(dest,digest,'unchanged_animation' if kind=='gif' else 'unchanged_pdf',**extra))
    else:
        dest=OUT/'docs'/f'{digest}.txt'
        text=clean_text(source.read_text(encoding='utf-8-sig',errors='replace'))
        if not cached(dest,digest):dest.write_text(text,encoding='utf-8')
        records.append(output_record(dest,digest,'inert_text_preview',inert_helper=bool(a.get('inert'))))
    thumb=None
    if a.get('_thumb_source'):
        thumb=OUT/'thumbs'/f'{digest}.jpg';tp=a['_thumb_source']
        with Image.open(tp) as image:is_ready=image.format=='JPEG' and max(image.size)<=480
        if is_ready:
            if not cached(thumb,digest):shutil.copyfile(tp,thumb)
            with Image.open(thumb) as image:image.load();w,h=image.size
            records.append(output_record(thumb,digest,'thumbnail',width=w,height=h,decode='passed'))
        else:records.append(jpeg(tp,thumb,480,85,digest,'thumbnail'))
    return (kind,digest),{'src':dest.relative_to(OUT).as_posix(),'thumb':thumb.relative_to(OUT).as_posix() if thumb else None,'records':records}

built={}
with ThreadPoolExecutor(max_workers=3) as pool:
    futures=[pool.submit(build_one,a) for a in unique.values()]
    for f in as_completed(futures):
        key,result=f.result();built[key]=result
        if key[0]=='video':print('Verified video proxy:',Path(result['src']).name,flush=True)

packaged=[]
for a in assets:
    result=built[(a['kind'],a['_hash'])]
    item={k:v for k,v in a.items() if not k.startswith('_')}
    item['src']=result['src']
    if result['thumb']:item['thumb']=result['thumb']
    item['sha256']=a['_hash']
    item['previewStatus']='Hosted review preview; local original remains the master.'
    if a['kind']=='document':
        item['text']=clean_text(item.get('text',''))
        if item.get('inert'):item['downloadFilename']=a['filename']+'.txt'
    packaged.append(clean_values(item))
catalog['assets']=packaged
catalog=clean_values(catalog)
output_catalog=OUT/'catalog.json'
output_catalog.write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
outputs={r['path']:r for result in built.values() for r in result['records']}
for a in packaged:
    for key in ('src','thumb'):
        if a.get(key):
            p=(OUT/a[key]).resolve()
            if not p.is_relative_to(OUT.resolve()) or not p.is_file():raise ValueError('Invalid package path')
for record in sources.values():
    if sha((ROOT/record['path']).read_bytes())!=record['sha256']:raise ValueError('Source changed during build')
if SOURCE.read_bytes()!=catalog_bytes:raise ValueError('Source catalog changed during build; rerun with the new snapshot')
manifest={'schema_version':1,'purpose':'Hosted review proxies, not production masters.','settings':SETTINGS,
          'source_catalog':{'path':repo_path(SOURCE),'sha256':sha(catalog_bytes)},
          'tools':TOOLS,
          'builder_sha256':sha(Path(__file__).read_bytes()),
          'asset_count':len(packaged),'asset_kinds':dict(Counter(a['kind'] for a in packaged)),
          'output_file_count':len(outputs),'output_bytes':sum(r['bytes'] for r in outputs.values()),
          'catalog_sha256':sha(output_catalog.read_bytes()),'sources_preserved':True,'sources':list(sources.values()),'outputs':list(outputs.values())}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({k:manifest[k] for k in ('asset_count','asset_kinds','output_file_count','output_bytes','sources_preserved')},indent=2))
