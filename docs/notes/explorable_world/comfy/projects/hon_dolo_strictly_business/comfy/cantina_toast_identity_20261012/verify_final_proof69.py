"""Verify a downloaded single Cantina proof locally. Does not generate or alter source media."""
from pathlib import Path
import argparse,datetime,hashlib,json,re,subprocess,wave
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
BASE=Path(__file__).resolve().parent
FF=Path(r'D:\Documents\CFA\.cache\hon_dolo_i2v_20261004\python_packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe')
JOB='569bec13-c8d8-4767-bddf-070b6765708b'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def decode_video(path,label,out):
 r=subprocess.run([str(FF),'-hide_banner','-i',str(path),'-map','0:v:0','-vf','showinfo','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True,check=True)
 log=r.stderr.decode('utf-8',errors='replace');(out/(label+'_VIDEO_SHOWINFO.txt')).write_text(log,encoding='utf-8')
 sizes=set(tuple(map(int,v)) for v in re.findall(r'\bs:(\d+)x(\d+)\b',log))
 if len(sizes)!=1:raise ValueError(f'Changing or unknown dimensions: {sizes}')
 w,h=next(iter(sizes));a=np.frombuffer(r.stdout,dtype=np.uint8).reshape(-1,h,w,3)
 lines=re.findall(r'\bn:\s*(\d+)\s+pts:\s*(-?\d+)\s+pts_time:([0-9.e+-]+)',log)
 tb=re.search(r'config in time_base:\s*(\d+)/(\d+)',log);num,den=map(int,tb.groups());pts=[int(v[1]) for v in lines]
 exact=len(pts)==len(a) and all((p-pts[0])*num*24==i*den for i,p in enumerate(pts))
 meta={'path':str(path),'bytes':path.stat().st_size,'sha256':sha(path),'width':w,'height':h,'decodedFrames':len(a),'timeBase':[num,den],'pts':pts,'startSeconds':pts[0]*num/den,'exact24fpsPTS':exact,'durationAt24fps':len(a)/24,'sourceStreamDescription':[line.strip() for line in log.splitlines() if 'Stream #0:0' in line][:1]}
 return a,meta

def verify_audio(path,out):
 r=subprocess.run([str(FF),'-hide_banner','-i',str(path),'-map','0:a:0','-af','ashowinfo','-ac','2','-ar','48000','-c:a','pcm_s16le','-f','s16le','-'],capture_output=True)
 log=r.stderr.decode('utf-8',errors='replace');(out/'OUTPUT_AUDIO_ASHOWINFO.txt').write_text(log,encoding='utf-8')
 if r.returncode:return {'presentAndDecoded':False,'reason':log[-1800:]}
 a=np.frombuffer(r.stdout,dtype='<i2').reshape(-1,2)
 p=BASE/'SOURCE_FRONTAL_AUDIO_168_236_PCM.wav'
 with wave.open(str(p),'rb') as w:
  assert (w.getframerate(),w.getnchannels(),w.getsampwidth())==(48000,2,2)
  ref=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,2)
 pts=[float(v) for v in re.findall(r'\bpts_time:([0-9.e+-]+)',log)]
 sr=sorted(set(int(v) for v in re.findall(r'\brate:(\d+)\b',log)))
 streams=[line.strip() for line in log.splitlines() if re.search(r'Stream #0:.*Audio:',line)]
 result={'presentAndDecoded':True,'streamDescription':streams[:1],'nativeRatesObserved':sr,'firstDecodedPTSSeconds':pts[0] if pts else None,'comparisonSampleRate':48000,'comparisonChannels':2,'decodedSamples':len(a),'decodedDurationSeconds':len(a)/48000,'expectedSamples':len(ref),'expectedDurationSeconds':len(ref)/48000,'sampleCountDelta':len(a)-len(ref),'referencePath':str(p),'referenceSHA256':sha(p),'crossCorrelationSearchSeconds':[-.25,.25]}
 # Positive lag means output is delayed relative to the source; only +/-250ms searched.
 x=a.astype(np.float64).mean(axis=1);y=ref.astype(np.float64).mean(axis=1)
 x-=x.mean();y-=y.mean();n=1<<(len(x)+len(y)-2).bit_length()
 corr=np.fft.irfft(np.fft.rfft(x,n)*np.conj(np.fft.rfft(y,n)),n)
 lag=np.arange(-12000,12001);start=np.maximum(0,lag);rstart=np.maximum(0,-lag);length=np.minimum(len(x)-start,len(y)-rstart)
 valid=length>0;lag,start,rstart,length=lag[valid],start[valid],rstart[valid],length[valid]
 sx=np.r_[0,np.cumsum(x*x)];sy=np.r_[0,np.cumsum(y*y)]
 norm=np.sqrt((sx[start+length]-sx[start])*(sy[rstart+length]-sy[rstart]));normalized=corr[lag%n]/np.maximum(norm,1e-15)
 best=int(np.argmax(normalized));l=int(lag[best]);i=int(start[best]);j=int(rstart[best]);k=int(length[best]);aa=a[i:i+k].astype(np.float64);rr=ref[j:j+k].astype(np.float64)
 result.update(bestLagSamples=l,bestLagSeconds=l/48000,bestNormalizedCorrelation=float(normalized[best]),zeroLagNormalizedCorrelation=float(normalized[np.flatnonzero(lag==0)[0]]),bestLagAtSearchBoundary=abs(l)==12000,alignedOverlapSamples=k,alignedRMSEPCM16=float(np.sqrt(np.mean((aa-rr)**2))),sourceRMSPCM16=float(np.sqrt(np.mean(rr**2))),outputRMSPCM16=float(np.sqrt(np.mean(aa**2))),caution='AAC priming/padding and lossy coding can alter sample count and PCM values. Correlation and decoded PTS establish evidence, not exact bit identity. A search-boundary lag is inconclusive.')
 return result

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('video',type=Path);parser.add_argument('--output-dir',type=Path,required=True);parser.add_argument('--job-id',default=JOB,help='Cloud job ID for this result; defaults to the original baseline job');a=parser.parse_args()
 src=a.video.resolve(strict=True);out=a.output_dir.resolve()
 if not out.is_relative_to(BASE):raise ValueError('Evidence must stay under the Cantina test folder')
 if out.exists():raise FileExistsError('Use a new evidence directory; never overwrite earlier receipts')
 out.mkdir(parents=True)
 original_hash=sha(src);actual,meta=decode_video(src,'OUTPUT',out)
 report={'createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'jobID':a.job_id,'scope':'Downloaded result verification only; no generation, edits or automatic acceptance.','actualVideo':meta,'expected':{'frames':69,'fps':24,'width':768,'height':432,'durationSeconds':2.875,'sourceFramesInclusive':[168,236]},'videoShapeTimingPass':len(actual)==69 and actual.shape[1:3]==(432,768) and meta['exact24fpsPTS'] and meta['startSeconds']==0,'audio':verify_audio(src,out)}
 if report['videoShapeTimingPass']:
  original,se=decode_video(BASE/'SOURCE_FRONTAL_FRAMES_168_236_24FPS_LOSSLESS.mp4','LOCAL_SOURCE',out)
  expected=np.stack([np.array(Image.fromarray(f).resize((768,432),Image.Resampling.LANCZOS)) for f in original]);del original
  protection,pe=decode_video(BASE/'PROTECTION_FRONTAL_69_768x432_LOSSLESS.mp4','LOCAL_PROTECTION',out)
  assert len(protection)==69 and len(expected)==69
  rows=[]
  for i in range(69):
   allowed=protection[i,...,0]<255;dil=np.array(Image.fromarray(allowed.astype(np.uint8)*255).filter(ImageFilter.MaxFilter(17)))>0;safe=~dil
   target=actual[i].astype(np.int16);delta=np.abs(target-expected[i].astype(np.int16));scores=[{'offset':j-i,'mae':float(np.abs(target-expected[j].astype(np.int16))[safe].mean())} for j in range(max(0,i-2),min(69,i+3))]
   rows.append({'frame':i+1,'sourceFrame':168+i,'maeOutsideEditPlus8px':float(delta[safe].mean()),'p99AbsoluteErrorOutsideEditPlus8px':float(np.percentile(delta[safe],99)),'bestNearbyFrameOffset':min(scores,key=lambda v:v['mae'])['offset'],'nearbyOffsetMAE':scores})
  contacts=[]
  for start in range(0,69,20):
   stop=min(69,start+20);page=Image.new('RGB',(1536,((stop-start+3)//4)*224),(20,24,31));draw=ImageDraw.Draw(page)
   for i in range(start,stop):
    k=i-start;x=(k%4)*384;y=(k//4)*224;draw.text((x+5,y+3),f'{i+1:02d}/69 F{168+i} {(168+i)/24:.3f}s | Source / Proof',fill=(240,240,240))
    for side,arr in enumerate([expected[i],actual[i]]):
     face=Image.fromarray(arr).crop((240,78,468,300)).resize((190,185),Image.Resampling.LANCZOS);page.paste(face,(x+side*192,y+24))
   p=out/f'FACE_SOURCE_PROOF_{168+start}_{167+stop}.jpg';page.save(p,quality=95);contacts.append({'path':str(p),'sourceFramesInclusive':[168+start,167+stop],'sha256':sha(p)})
  report['preservation']={'reference':se,'protectionCap':pe,'expectedResize':'Pillow RGB Lanczos; Cloud scaling/color and H.264 export may differ.','outsideEditMarginPixels':8,'meanFrameMAE':float(np.mean([r['maeOutsideEditPlus8px'] for r in rows])),'maximumFrameMAE':max(r['maeOutsideEditPlus8px'] for r in rows),'allBestNearbyOffsetsZero':all(r['bestNearbyFrameOffset']==0 for r in rows),'diagnosticBaselineMeanFrameMAE':2.1245415793059954,'interpretation':'Compare against the diagnostic baseline; no arbitrary numeric visual-acceptance threshold. Outside-mask alignment confirms source composition, not generated eye/performance alignment inside the edit window.','perFrame':rows}
  report['faceComparisonContacts']=contacts
 report['downloadedSourceUnchanged']=sha(src)==original_hash
 report['visualReviewCompleted']=False;report['accepted']=False
 p=out/'FINAL_PROOF_VERIFICATION.json';p.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'report':str(p),'reportSHA256':sha(p),'videoShapeTimingPass':report['videoShapeTimingPass'],'audio':report['audio'],'preservationSummary':{k:v for k,v in report.get('preservation',{}).items() if k not in ['perFrame','reference','protectionCap']},'contacts':report.get('faceComparisonContacts',[])},indent=2))
if __name__=='__main__':main()
