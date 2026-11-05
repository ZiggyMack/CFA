import cv2,numpy as np,hashlib,json,os
from PIL import Image,ImageDraw,ImageFont
SRC='/workspace/james_edit/v004pkg/957897bd45c4__HIP-COAT-01_JAMES-CLEAN_v004.png'
im=cv2.imread(SRC); g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
F=lambda s:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',s)
Fr=lambda s:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',s)
def line(crop,bs=15,C=6):
    c=cv2.createCLAHE(3,(4,4)).apply(crop); c=cv2.bilateralFilter(c,7,40,7)
    t=cv2.adaptiveThreshold(c,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,bs,C)
    return cv2.medianBlur(t,3)
def up(a,s=3): return cv2.resize(a,None,fx=s,fy=s,interpolation=cv2.INTER_CUBIC)
# silhouette via grabcut
mask=np.zeros(g.shape,np.uint8); bg=np.zeros((1,65));fg=np.zeros((1,65))
cv2.grabCut(im,mask,(360,0,430,720),bg,fg,6,cv2.GC_INIT_WITH_RECT)
person=np.where((mask==1)|(mask==3),255,0).astype(np.uint8)
person=cv2.morphologyEx(person,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
n,lab,st,_=cv2.connectedComponentsWithStats(person); k=1+np.argmax(st[1:,4]); person=np.where(lab==k,255,0).astype(np.uint8)
ff=person.copy(); fm=np.zeros((722,1282),np.uint8); cv2.floodFill(ff,fm,(0,0),255); person=cv2.bitwise_or(person,cv2.bitwise_not(ff))
feat={}
hx0,hy0,hx1,hy1=440,0,625,175
face=line(up(g[hy0:hy1,hx0:hx1]),25,9)
def clean(b,mn=40):
    inv=255-b; n,l,st,_=cv2.connectedComponentsWithStats(inv)
    out=np.full_like(b,255)
    for i in range(1,n):
        if st[i,4]>=mn: out[l==i]=0
    return out
pm=cv2.dilate(up(person[hy0:hy1,hx0:hx1]),np.ones((7,7),np.uint8)); face[pm==0]=255; face=clean(face,60); feat['FACE']=face
hc=up(g[hy0:hy1,hx0:hx1]); hp=up(person[hy0:hy1,hx0:hx1])
hair=np.full_like(hc,255); hm=(hc<55)&(hp>0); hm[int(hc.shape[0]*0.62):]=False
H,Wd=hc.shape; xs_=np.arange(Wd); cut=(H*0.34+H*0.32*np.clip(np.abs(xs_-Wd*0.5)/(Wd*0.5),0,1)**2.2).astype(int)
rows=np.arange(H)[:,None]; hm&=rows<cut[None,:]
hair[hm]=0; hair=cv2.medianBlur(hair,5); feat['HAIR']=hair
sil=np.full_like(g,255); sil[person>0]=0; cnt,_=cv2.findContours(person,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
sil=cv2.cvtColor(sil,cv2.COLOR_GRAY2BGR); s2=np.full(g.shape,255,np.uint8); s2[person>0]=200; cv2.drawContours(s2,cnt,-1,0,3)
feat['SILHOUETTE']=s2[0:720,340:810]
tz={'CHEST':(470,175,650,400),'NECK':(505,140,605,250),'FACE-INK':(470,40,600,165),'ABDOMEN':(470,380,640,470),'R-FOREARM-HAND':(680,440,775,640)}
tc=tz['CHEST']; fl=cv2.imread('flash/JAMES-TATTOO-CHEST-ASTROLABE-flash.jpg',0); fl=np.where(fl<150,0,255).astype(np.uint8)
yy,xx=np.where(fl==0); fl=fl[max(yy.min()-20,0):yy.max()+20,max(xx.min()-20,0):xx.max()+20]; feat['TATTOO']=fl
oz=cv2.imread('flash/JAMES-TATTOO-OTHER-ZONES-flash.jpg',0); oz=np.where(oz<150,0,255).astype(np.uint8); Hh,Ww=oz.shape
def tight(a):
    yy,xx=np.where(a==0); return a[max(yy.min()-10,0):yy.max()+10,max(xx.min()-10,0):xx.max()+10]
ink={'CHEST':fl,'NECK':tight(oz[:Hh*2//5,:Ww//2]),'FACE-INK':tight(oz[:Hh*2//5,Ww//2:]),'ABDOMEN':tight(oz[Hh*2//5:,:Ww//2]),'R-FOREARM-HAND':tight(oz[Hh*2//5:,Ww//2:])}
def var(a,dx,dy,sc,rot):
    h,w=a.shape[:2]; M=cv2.getRotationMatrix2D((w/2,h/2),rot,sc); M[0,2]+=dx*w; M[1,2]+=dy*h
    return cv2.warpAffine(a,M,(w,h),borderValue=255,flags=cv2.INTER_LINEAR)
VARS=[('M00','master',0,0,1,0),('V01','shift L 4% / rot -3deg',-.04,0,1,-3),('V02','shift R 4% / rot +3deg',.04,0,1,3),('V03','scale 95% / up 2%',0,-.02,.95,0),('V04','scale 105% / down 2%',0,.02,1.05,0),('V05','combo R3% 97% rot -5deg',.03,.01,.97,-5)]
man={}
for name,a in feat.items():
    tiles=[]
    for vid,desc,dx,dy,sc,r in VARS:
        v=var(a,dx,dy,sc,r) if vid!='M00' else a
        fn=f'individual/JAMES-STENCIL-{name}-{vid}.png'; cv2.imwrite(fn,v); tiles.append((vid,desc,fn))
        man[fn]={'feature':name,'variant':vid,'transform':desc,'sha256':hashlib.sha256(open(fn,'rb').read()).hexdigest()}
    # sheet 3x2 uniform tiles
    TW,TH=600,560 if name!='SILHOUETTE' else 760
    W=3*TW+4*30; H=140+2*(TH+70)+30
    S=Image.new('RGB',(W,H),(246,243,236)); d=ImageDraw.Draw(S)
    d.rectangle([0,0,W,110],fill=(28,28,32)); d.text((W//2,55),f'JAMES  STENCIL SET  /  {name}  /  master + 5 tolerance variants',font=F(40),fill=(232,200,120),anchor='mm')
    for i,(vid,desc,fn) in enumerate(tiles):
        r,c=divmod(i,3); x=30+c*(TW+30); y=140+r*(TH+70)
        t=Image.open(fn).convert('RGB'); t.thumbnail((TW-20,TH-20)); bx=Image.new('RGB',(TW,TH),'white'); bx.paste(t,((TW-t.width)//2,(TH-t.height)//2))
        S.paste(bx,(x,y)); d.rectangle([x,y,x+TW,y+TH],outline=(200,160,60) if vid=='M00' else (90,90,90),width=6 if vid=='M00' else 2)
        d.text((x+TW//2,y+TH+33),f'{vid}  {desc}',font=F(24),fill=(30,30,30),anchor='mm')
    S.save(f'sheets/JAMES-STENCIL-SHEET-{name}.png')
# tattoo callout diagram
base=Image.fromarray(cv2.cvtColor(im[0:720,340:810],cv2.COLOR_BGR2RGB)).resize((940,1440))
W,H=2200,1560; D=Image.new('RGB',(W,H),(246,243,236)); d=ImageDraw.Draw(D)
d.rectangle([0,0,W,100],fill=(28,28,32)); d.text((W//2,50),'JAMES  TATTOO PLACEMENT MAP  (source: v004 clean reference: no gun, no holster)',font=F(42),fill=(232,200,120),anchor='mm')
bx0=(W-940)//2; D.paste(base,(bx0,110)); sx=940/470; sy=1440/720
cols=[(214,64,52),(52,120,214),(40,160,90),(200,130,20),(150,60,190)]
labels={'CHEST':'Chest: circular astrolabe / compass dial, sternum-centred','NECK':'Neck and throat: script and filigree, under the jaw','FACE-INK':'Face: small marks on the cheeks, temples and brow','ABDOMEN':'Abdomen: line work below the astrolabe, above the belt','R-FOREARM-HAND':'Forearm and hand (viewer-right): sleeve down to the knuckles'}
side=['L','R','L','R','L']
for i,(k,b) in enumerate(tz.items()):
    x0=bx0+(b[0]-340)*sx; y0=110+b[1]*sy; x1=bx0+(b[2]-340)*sx; y1=110+b[3]*sy
    d.rectangle([x0,y0,x1,y1],outline=cols[i],width=6)
    th=ink[k]; t=Image.fromarray(th).convert('RGB'); t.thumbnail((380,230))
    ly=150+i*280; lx=40 if side[i]=='L' else W-40-560
    d.rectangle([lx,ly,lx+560,ly+260],fill='white',outline=cols[i],width=5)
    D.paste(t,(lx+10,ly+20)); d.text((lx+400,ly+20),k,font=F(26),fill=cols[i])
    import textwrap
    for j,ln in enumerate(textwrap.wrap(labels[k].split(': ',1)[1],14)): d.text((lx+400,ly+60+j*28),ln,font=Fr(22),fill=(30,30,30))
    ax=lx+560 if side[i]=='L' else lx; tx=x0 if side[i]=='L' else x1
    d.line([ax,ly+130,tx,(y0+y1)/2],fill=cols[i],width=5); d.ellipse([tx-9,(y0+y1)/2-9,tx+9,(y0+y1)/2+9],fill=cols[i])
D.save('sheets/JAMES-TATTOO-PLACEMENT-MAP.png')
for k,a in ink.items(): cv2.imwrite(f'individual/JAMES-TATTOO-ZONE-{k}.png',a)
json.dump(man,open('manifest_partial.json','w'),indent=1)
