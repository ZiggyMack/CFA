"""Read-only local69-frame Cloud evidence comparison. No network or Cloud control."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess
import numpy as np
from PIL import Image
BASE=Path(__file__).resolve().parent
FF=Path(r'D:\Documents\CFA\.cache\hon_dolo_i2v_20261004\python_packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe')
def batch(path,w,h):
 if path.is_dir():
  files=sorted(path.glob('*.png'),key=lambda p:[int(s) if s.isdigit() else s.lower() for s in re.split(r'(\d+)',p.name)])
  if not files: raise ValueError('No individual PNG frames')
  frames=[]
  for f in files:
   with Image.open(f) as im:
    if im.size!=(w,h): raise ValueError(f'Wrong dimensions:{f}; screenshots/contact sheets cannot prove69-frame alignment')
    frames.append(np.array(im.convert('RGB')))
  return np.stack(frames),{'files':[str(f) for f in files],'fps':'unknown from stills','order':'natural filename order; verify exported numbering'}
 r=subprocess.run([str(FF),'-hide_banner','-i',str(path),'-map','0:v:0','-vf','showinfo','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],check=True,capture_output=True)
 log=r.stderr.decode('utf-8',errors='replace');sizes=set(tuple(map(int,s)) for s in re.findall(r'\bs:(\d+)x(\d+)\b',log))
 if sizes!={(w,h)}:raise ValueError(f'Wrong decoded dimensions:{sizes}')
 frames=np.frombuffer(r.stdout,dtype=np.uint8).reshape(-1,h,w,3)
 pts=[float(t) for t in re.findall(r'\bpts_time:([0-9.e+-]+)',log)]
 return frames,{'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'decodedFrames':len(frames),'timestampsUniform24fps':len(pts)==len(frames) and all(abs(t-pts[0]-i/24)<.00002 for i,t in enumerate(pts))}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mask',type=Path);p.add_argument('--mask-kind',choices=['protection','final-edit']);p.add_argument('--source',type=Path);p.add_argument('--report',type=Path,help='Optional NEW JSON report; existing files never overwritten');a=p.parse_args()
 if not a.mask and not a.source:p.error('Actual mask or source evidence required')
 if a.mask and not a.mask_kind:p.error('Explicit --mask-kind required')
 report={'scope':'Local actual-file comparison; no live Cloud compatibility/execution claim'}
 if a.mask:
  actual,evidence=batch(a.mask,768,432);expected,local=batch(BASE/'PROTECTION_FRONTAL_69_768x432_LOSSLESS.mp4',768,432)
  c={'actual':evidence,'local':local,'count69':len(actual)==69,'kind':a.mask_kind,'redChannelUsed':True}
  if len(actual)==69:
   red=actual[...,0].astype(np.int16);protection=expected[...,0].astype(np.int16);c['actualRGBGrayscale']=bool(np.array_equal(actual[...,0],actual[...,1]) and np.array_equal(actual[...,0],actual[...,2]))
   if a.mask_kind=='protection':
    delta=np.abs(red-protection);c.update(redMatchesExactly=bool(not delta.any()),maxAbsoluteDifference=int(delta.max()),meanAbsoluteDifference=float(delta.mean()))
   else:
    excess=red-(255-protection);c.update(pixelsAboveAllowedCapByMoreThanOne8bitLevel=int(np.count_nonzero(excess>1)),maximumCapExcess=int(max(0,excess.max())),nonzeroEditPixelsPerFrame=[int(np.count_nonzero(f)) for f in red],allFramesHaveSomeEdit=bool(all(np.any(f) for f in red)),caution='No overreach does not prove usable identity coverage. All-zero masks are not a successful edit.')
  report['mask']=c
 if a.source:
  actual,evidence=batch(a.source,768,432);original,local=batch(BASE/'SOURCE_FRONTAL_FRAMES_168_236_24FPS_LOSSLESS.mp4',1280,720);expected=np.stack([np.array(Image.fromarray(f).resize((768,432),Image.Resampling.LANCZOS)) for f in original]);c={'actual':evidence,'local':local,'count69':len(actual)==69,'expectedResize':'Pillow RGB Lanczos; Cloud version/color conversion may differ'}
  if len(actual)==69:
   delta=np.abs(actual.astype(np.int16)-expected.astype(np.int16));offsets=[]
   for i,frame in enumerate(actual):
    best=min(range(max(0,i-2),min(69,i+3)),key=lambda j:np.mean(np.abs(frame[::4,::4].astype(np.int16)-expected[j,::4,::4].astype(np.int16))));offsets.append(best-i)
   c.update(exactRGBMatch=bool(not delta.any()),maxAbsoluteDifference=int(delta.max()),meanAbsoluteDifference=float(delta.mean()),bestNearbyFrameOffsets=offsets,caution='Nearby-frame matching is diagnostic; similar frames can tie. Pixel difference alone does not establish temporal misalignment.')
  report['source']=c
 text=json.dumps(report,indent=2)
 if a.report:
  with a.report.open('x',encoding='utf-8') as f:f.write(text)
 print(text)
if __name__=='__main__':main()
