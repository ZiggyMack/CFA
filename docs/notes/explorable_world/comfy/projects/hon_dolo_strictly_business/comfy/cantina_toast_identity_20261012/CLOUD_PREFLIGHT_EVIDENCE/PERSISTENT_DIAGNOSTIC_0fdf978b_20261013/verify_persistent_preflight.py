from pathlib import Path
import hashlib,json,datetime,re,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
E=Path(__file__).resolve().parent
B=E.parent.parent
FF=Path(r'D:\Documents\CFA\.cache\hon_dolo_i2v_20261004\python_packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def decode(path,w,h,label):
 r=subprocess.run([str(FF),'-hide_banner','-i',str(path),'-map','0:v:0','-vf','showinfo','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True,check=True)
 log=r.stderr.decode('utf-8',errors='replace');(E/(label+'_SHOWINFO.txt')).write_text(log,encoding='utf-8')
 sizes=set(tuple(map(int,s)) for s in re.findall(r'\bs:(\d+)x(\d+)\b',log));assert sizes=={(w,h)},sizes
 a=np.frombuffer(r.stdout,dtype=np.uint8).reshape(-1,h,w,3)
 lines=re.findall(r'\bn:\s*(\d+)\s+pts:\s*(-?\d+)\s+pts_time:([0-9.e+-]+)',log)
 tb=re.search(r'config in time_base:\s*(\d+)/(\d+)',log);num,den=map(int,tb.groups())
 pts=[int(v[1]) for v in lines]
 exact= len(pts)==len(a) and all((p-pts[0])*num*24==i*den for i,p in enumerate(pts))
 return a,{'path':str(path),'bytes':path.stat().st_size,'sha256':sha(path),'width':w,'height':h,'decodedFrames':len(a),'inputTimeBase':[num,den],'pts':pts,'allPTSExactly24fps':exact,'startPTS':pts[0],'presentationDurationSeconds':len(a)/24}
mask,me=decode(E/'video/cantina_preflight_finalmask69_v003_00001_.mp4',768,432,'MASK')
over,oe=decode(E/'video/cantina_preflight_sourceoverlay69_v003_00001_.mp4',768,432,'OVERLAY')
protect,pe=decode(B/'PROTECTION_FRONTAL_69_768x432_LOSSLESS.mp4',768,432,'LOCAL_PROTECTION')
orig,se=decode(B/'SOURCE_FRONTAL_FRAMES_168_236_24FPS_LOSSLESS.mp4',1280,720,'LOCAL_SOURCE')
assert all(len(x)==69 for x in [mask,over,protect,orig])
expect=np.stack([np.array(Image.fromarray(f).resize((768,432),Image.Resampling.LANCZOS)) for f in orig]);del orig
actual=mask[...,0].astype(np.int16);cap=255-protect[...,0].astype(np.int16);del protect
maskrows=[];overlayrows=[]
thresholds=[1,8,16]
for i in range(69):
 allowed=cap[i]>0
 dil={n:np.array(Image.fromarray(allowed.astype(np.uint8)*255).filter(ImageFilter.MaxFilter(2*n+1)))>0 for n in [1,2,4,8]}
 row={'frame':i+1,'sourceFrame':168+i,'sourceTimeSeconds':(168+i)/24,'nonzeroPixels':int(np.count_nonzero(actual[i])),'pixelsAbove16':int(np.count_nonzero(actual[i]>16)),'maximumCapExcess':int(max(0,(actual[i]-cap[i]).max()))}
 for t in thresholds:
  row['capExcessAbove'+str(t)]=int(np.count_nonzero(actual[i]-cap[i]>t))
  row['protectedPixelsAbove'+str(t)]=int(np.count_nonzero((~allowed)&(actual[i]>t)))
  for n in [1,2,4]:row[f'protectedBeyond{n}pxAbove{t}']=int(np.count_nonzero((~dil[n])&(actual[i]>t)))
 maskrows.append(row)
 safe=~dil[8];a=over[i].astype(np.int16);expected=expect[i].astype(np.int16);delta=np.abs(a-expected)
 offsets=[]
 for j in range(max(0,i-2),min(69,i+3)):
  offsets.append({'offset':j-i,'meanAbsoluteErrorOutside8px':float(np.mean(np.abs(a-expect[j].astype(np.int16))[safe]))})
 best=min(offsets,key=lambda v:v['meanAbsoluteErrorOutside8px'])
 overlayrows.append({'frame':i+1,'sourceFrame':168+i,'outsideEdit8pxPixels':int(safe.sum()),'meanAbsoluteErrorOutside8px':float(delta[safe].mean()),'p99AbsoluteErrorOutside8px':float(np.percentile(delta[safe],99)),'maximumAbsoluteErrorOutside8px':int(delta[safe].max()),'bestNearbyFrameOffset':best['offset'],'nearbyOffsets':offsets})
contacts=[]
for start in range(0,69,20):
 stop=min(69,start+20);rows=(stop-start+3)//4;page=Image.new('RGB',(1520,rows*405),(20,24,31));draw=ImageDraw.Draw(page)
 for i in range(start,stop):
  k=i-start;x=(k%4)*380;y=(k//4)*405
  face=Image.fromarray(over[i]).crop((240,78,468,300)).resize((380,370),Image.Resampling.LANCZOS)
  page.paste(face,(x,y+35));draw.text((x+7,y+5),f'Cloud {i+1:02d}/69 | Original F{168+i} | {(168+i)/24:.3f}s',fill=(240,240,240));draw.text((x+7,y+20),'Black region = final editable mask',fill=(155,203,224))
 p=E/f'ACTUAL_OVERLAY_{168+start}_{167+stop}.jpg';page.save(p,quality=94);contacts.append({'path':str(p),'sourceFrames':[168+start,167+stop],'sha256':sha(p)})
summary={'countsAndTimingPass':all(r['decodedFrames']==69 and r['allPTSExactly24fps'] and r['startPTS']==0 for r in [me,oe]),'maskRGBChannelsMaximumDifference':int(np.max(np.max(mask,axis=3).astype(np.int16)-np.min(mask,axis=3).astype(np.int16))),'maskAllFramesHaveEditAbove16':all(r['pixelsAbove16']>0 for r in maskrows),'maskMaxCapExcess':max(r['maximumCapExcess'] for r in maskrows),'maskTotals':{key:sum(r[key] for r in maskrows) for key in maskrows[0] if key.startswith(('capExcessAbove','protectedPixelsAbove','protectedBeyond'))},'overlayMeanFrameMAEOutside8px':float(np.mean([r['meanAbsoluteErrorOutside8px'] for r in overlayrows])),'overlayMaximumFrameMAEOutside8px':max(r['meanAbsoluteErrorOutside8px'] for r in overlayrows),'overlayAllBestNearbyOffsetsZero':all(r['bestNearbyFrameOffset']==0 for r in overlayrows),'overlayNonzeroBestOffsets':[{k:r[k] for k in ['frame','sourceFrame','bestNearbyFrameOffset']} for r in overlayrows if r['bestNearbyFrameOffset']]}
report={'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Actual persistent preprocessing outputs only; no generated identity output or production acceptance. Root observed no KSampler.','jobID':'0fdf978b-a29f-471f-99f0-e1a4a1e32f26','actualMask':me,'actualBlackMaskOverlay':oe,'localProtection':pe,'localSource':se,'expectedResize':'Pillow RGB Lanczos, same dimensions as Cloud; implementation/color conversion and lossy export differences remain.','maskRule':'Final editable alpha must be capped by 255-protection. Lossy export can introduce small edge values; thresholds 1/8/16 and distances 1/2/4 are reported separately.','overlayRule':'DrawMaskOnImage color 0,0,0 paints edit region black. Compare unchanged source outside manual allowed-cap dilation of 8 pixels.','summary':summary,'maskPerFrame':maskrows,'overlayPerFrame':overlayrows,'actualOverlayContacts':contacts,'rootActualOverlayReviewCompleted':False}
(E/'PERSISTENT_PREFLIGHT_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'summary':summary,'contacts':contacts},indent=2))
