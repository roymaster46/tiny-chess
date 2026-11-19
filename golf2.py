import json,os,urllib.request as U,random
V=[0,100,320,330,500,900,0]
MT=10**5
ND=(31,33,14,18,-31,-33,-14,-18)
DD=(15,17,-15,-17)
SD=(1,-1,16,-16)
KD=SD+DD
PA=(0,0,4,8,14,24,40,0)
PC=(0,0,0,10,15,10,5,0)
KB=(20,25,10,0,0,10,25,20)
PR=(5,4,3,2)
SQS=[q for q in range(128)if not q&8]
PT=[[0]*128 for _ in range(7)]
MG=[0]*128;EG=[0]*128
for q in SQS:
 r,f=q>>4,q&7;c=min(f,7-f)+min(r,7-r)
 PT[1][q]=PA[r]+PC[r]*(3<=f<5)
 PT[2][q]=6*c-20;PT[3][q]=4*c-8
 PT[4][q]=15*(r==6)+5*(r==0 and 3<=f<5)
 PT[5][q]=2*c-6
 MG[q]=KB[f]if r==0 else max(-50,-15*r);EG[q]=8*c-24
g=random.Random(1);R=g.getrandbits
ZP=[[R(64)for _ in range(128)]for _ in range(13)]
ZS=R(64)
ZC=[R(64)for _ in range(16)]
ZE=[R(64)for _ in range(8)]
CM=[15]*128
for i,v in((0,13),(7,14),(4,12),(112,7),(119,11),(116,3)):CM[i]=v
B=[0]*128;S=1;C=0;E=-1;HF=0;H=0;SC=0;PH=0;KW=4;KB2=116;ST=[];MV=[]
def pv(pc,sq):
 return V[pc]+PT[pc][sq] if pc>0 else -(V[-pc]+PT[-pc][sq^0x70])
def rst():
 global B,S,C,E,HF,H,SC,PH,KW,KB2,ST,MV
 B=[0]*128;H=0;ST=[];MV=[]
 for i,p in enumerate((4,2,3,5,6,3,2,4)):
  B[i]=p;B[112+i]=-p;B[16+i]=1;B[96+i]=-1
  H^=ZP[p+6][i]^ZP[-p+6][112+i]^ZP[7][16+i]^ZP[5][96+i]
 S=1;C=15;E=-1;HF=0;SC=0;PH=6400;KW=4;KB2=116;H^=ZC[15]
def atk(sq,by):
 b=B
 for t in(sq-15*by,sq-17*by):
  if not(t&136)and b[t]==by:return 1
 for ds,pt in((ND,2),(KD,6)):
  for d in ds:
   t=sq+d
   if not(t&136)and b[t]==pt*by:return 1
 for d in KD:
  t=sq
  while not((t:=t+d)&136):
   pc=b[t]
   if pc:
    if pc*by>0 and abs(pc)in(5,3+(d in SD)):return 1
    break
 return 0
def chk():return atk(KW if S>0 else KB2,-S)
def gen(cap=0):
 b=B;s=S;ep=E;ms=[];ap=ms.append
 for sq in SQS:
  pc=b[sq]
  if not pc or(pc>0)!=(s>0):continue
  t=abs(pc)
  if t==1:
   f=16*s;st,la=(1,6)if s>0 else(6,1);o=sq+f
   if b[o]==0:
    if(sq>>4)==la:
     for pr in PR:ap(sq+o*128+(pr<<14))
    elif not cap:
     ap(sq+o*128)
     if(sq>>4)==st and b[o+f]==0:ap(sq+(o+f)*128)
   for d in(f-1,f+1):
    to=sq+d
    if to&136:continue
    tg=b[to]
    if tg and(tg>0)!=(s>0):
     if(sq>>4)==la:
      for pr in PR:ap(sq+to*128+(pr<<14))
     else:ap(sq+to*128)
    elif to==ep:ap(sq+to*128)
  elif t==2 or t==6:
   for d in(ND,KD)[t==6]:
    to=sq+d
    if to&136:continue
    tg=b[to]
    if tg:
     if(tg>0)!=(s>0):ap(sq+to*128)
    elif not cap:ap(sq+to*128)
  else:
   ds=(DD,SD,KD)[t-3]
   for d in ds:
    to=sq
    while not((to:=to+d)&136):
     tg=b[to]
     if tg:
      if(tg>0)!=(s>0):ap(sq+to*128)
      break
     if not cap:ap(sq+to*128)
 if not cap:
  if s>0 and(C&3)and not chk():
   if(C&1)and b[5]==b[6]==0 and not atk(5,-1)and not atk(6,-1):ap(4+6*128)
   if(C&2)and b[3]==b[2]==b[1]==0 and not atk(3,-1)and not atk(2,-1):ap(4+2*128)
  elif s<0 and(C&12)and not chk():
   if(C&4)and b[117]==b[118]==0 and not atk(117,1)and not atk(118,1):ap(116+118*128)
   if(C&8)and b[115]==b[114]==b[113]==0 and not atk(115,1)and not atk(114,1):ap(116+114*128)
 return ms
def make(m):
 global S,C,E,HF,H,SC,PH,KW,KB2
 MV.append(m)
 fr=m&127;to=(m>>7)&127;pr=(m>>14)&7;pc=B[fr];s=S
 cq=to
 if abs(pc)==1 and to==E and B[to]==0:cq=to-16*s
 cp=B[cq]
 ST.append((m,cp,cq,C,E,HF,H,SC,PH,KW,KB2))
 H^=ZC[C]
 if E>=0:H^=ZE[E&7]
 H^=ZP[pc+6][fr];SC-=pv(pc,fr);B[fr]=0
 if cp:H^=ZP[cp+6][cq];SC-=pv(cp,cq);B[cq]=0;PH-=V[abs(cp)]*(abs(cp)!=1)
 pl=pr*s if pr else pc
 H^=ZP[pl+6][to];SC+=pv(pl,to)
 if pr:PH+=V[pr]-V[1]
 B[to]=pl
 if abs(pc)==6:
  if s>0:KW=to
  else:KB2=to
  if abs(to-fr)==2:
   rf,rt=(fr+3,fr+1)if to>fr else(fr-4,fr-1);rk=B[rf];B[rf]=0;B[rt]=rk;H^=ZP[rk+6][rf]^ZP[rk+6][rt];SC+=pv(rk,rt)-pv(rk,rf)
 C&=CM[fr]&CM[to]
 E=-1
 if abs(pc)==1 and abs(to-fr)==32:E=(fr+to)//2;H^=ZE[E&7]
 H^=ZC[C];HF=0 if abs(pc)==1 or cp else HF+1;S=-s;H^=ZS
def unmake():
 global S,C,E,HF,H,SC,PH,KW,KB2
 m,cp,cq,C,E,HF,H,SC,PH,KW,KB2=ST.pop()
 MV.pop()
 fr=m&127;to=(m>>7)&127;pr=(m>>14)&7;pc=B[to]
 if pr:pc=-S
 if abs(B[to])==6 and abs(to-fr)==2:
  a,b=(fr+1,fr+3)if to>fr else(fr-1,fr-4);B[b]=B[a];B[a]=0
 B[fr]=pc;B[to]=0
 if cp:B[cq]=cp
 S=-S
def ev():
 ph=min(PH,6400);re=6400-ph
 e=SC+(MG[KW]*ph+EG[KW]*re)//6400-(MG[KB2^0x70]*ph+EG[KB2^0x70]*re)//6400
 return e if S>0 else-e
NDS=0;TT={};KL={};P=[]
class AB(Exception):pass
def order(ms,tm,pl):
 b=B;ep=E;sc=[]
 k1,k2=KL.get(pl,(0,0))
 for m in ms:
  to=(m>>7)&127;fr=m&127;fp=abs(b[fr]);tg=b[to];pr=(m>>14)&7
  c=100000+10*V[abs(tg)or 1]-V[fp]if tg or fp==1 and to==ep else 0
  s=1000000 if m==tm else c+200000+V[pr] if pr else 50000 if m==k1 else 40000 if m==k2 else c
  sc.append((-s,m))
 sc.sort();return[m for _,m in sc]
def qs(a,be,pl):
 global NDS
 NDS+=1
 if NDS>=BG:raise AB
 ic=chk()
 if ic:best=-MT-1;lg=0;ms=order(gen(),0,pl)
 else:
  st=ev()
  if st>=be:return st
  if st>a:a=st
  best=st;lg=1;ms=order(gen(1),0,pl)
 for m in ms:
  to=(m>>7)&127
  if not ic and not(m>>14)&7:
   cv=V[abs(B[to])or 1]
   if st+cv+200<a:continue
  make(m)
  if atk(KW if S<0 else KB2,S):unmake();continue
  lg+=1;sc=-qs(-be,-a,pl+1);unmake()
  if sc>best:best=sc
  if sc>=be:return sc
  if sc>a:a=sc
 return -MT+pl if lg==0 else best
def sr(d,a,be,pl):
 global NDS,E,HF,H,S
 if pl>0 and(HF>=100 or H in HS or H in P):return 0
 if d<=0:return qs(a,be,pl)
 NDS+=1
 if NDS>=BG:raise AB
 ic=chk()
 if ic:d+=1
 if not ic and d>=3 and pl>0 and PH>0:
  e0,f0,h0=E,HF,H
  if E>=0:H^=ZE[E&7]
  E=-1;HF+=1;S=-S;H^=ZS
  sc=-sr(d-3,-be,-be+1,pl+1)
  E,HF,H=e0,f0,h0;S=-S
  if sc>=be:return sc
 e=TT.get(H);tm=e[3]if e else 0
 if e and e[0]>=d and(e[2]==0 or(e[2]==1 and e[1]>=be)or(e[2]==2 and e[1]<=a)):return e[1]
 fut=not ic and d==1 and ev()+150<=a
 ms=order(gen(),tm,pl);best=-MT;bm=0;a0=a;P.append(H);lg=0
 for i,m in enumerate(ms):
  to=(m>>7)&127;cap=B[to]or(m>>14)or(abs(B[m&127])==1 and to==E)
  if fut and not cap:continue
  make(m)
  if atk(KW if S<0 else KB2,S):unmake();continue
  lg+=1
  if i==0:sc=-sr(d-1,-be,-a,pl+1)
  else:
   rd=d-2 if i>=4 and d>=3 and not cap and not ic else d-1
   sc=-sr(rd,-a-1,-a,pl+1)
   if sc>a:sc=-sr(d-1,-be,-a,pl+1)
  unmake()
  if sc>best:best=sc;bm=m
  if sc>=be:
   if not cap:
    k=KL.get(pl,(0,0))
    if m!=k[0]:KL[pl]=(m,k[0])
   break
  if sc>a:a=sc
 P.pop()
 if lg==0:return -MT+pl if ic else ev()if fut else 0
 fl=2 if best<=a0 else 1 if best>=be else 0
 TT[H]=(d,best,fl,bm)
 return best
A='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
BK=['Lb+tKa0sBS9ZMU8+IQZ0OezjFT5qemt8NdjaTa8rJR3vPfraRavmfm1tmu7j','McyiKS+tcktjLbibSbzrGVrkbk5qFa6sBS']
def bk():
 if len(MV)<8:return 0
 for L in BK:
  d=[]
  for j in range(0,len(L),2):
   a=A.index(L[j]);b=A.index(L[j+1])
   d.append((a&7)+(a>>3)*16+(((b&7)+(b>>3)*16)<<7))
  if d[:len(MV)]==MV and len(d)>len(MV):return d[len(MV)]
 return 0
def root():
 global NDS
 b=bk()
 if b:return b
 P[:]=[]
 ms=order(gen(),0,0);lg=[]
 for m in ms:
  make(m)
  if not atk(KW if S<0 else KB2,S):lg.append(m)
  unmake()
 if not lg:return 0
 bm=lg[0];NDS=0
 try:
  for d in range(1,65):
   scs=[];al=-MT
   for m in lg:
    make(m);sc=-sr(d-1,-MT,-al,1);unmake();scs.append((sc,m))
    if sc>al:al=sc
   scs.sort(key=lambda x:-x[0]);bm,lg=scs[0][1],[m for _,m in scs]
 except AB:pass
 return bm
def uc(m):
 fr=m&127;to=(m>>7)&127;pr=(m>>14)&7
 return'%c%d%c%d%s'%(97+fr%8,(fr>>4)+1,97+to%8,(to>>4)+1,'nbrq'[pr-2]if pr else'')
def pu(u):
 fr=ord(u[0])-97+(int(u[1])-1)*16;to=ord(u[2])-97+(int(u[3])-1)*16;pr='nbrq'.index(u[4])+2 if len(u)==5 else 0
 return fr+to*128+(pr<<14)
def post(p,b):
 r=U.Request(EU+p,data=json.dumps(b).encode())
 with U.urlopen(r)as x:return json.load(x)
EU=os.environ.get('MAKEFUN_ENV_URL','')
BG=10**5
def main():
 global HS
 g={}
 while g.get('status')!='done':
  g=post('/game',{})
  while g['status']=='your_move':
   rst();HS={H}
   for u in g['moves']:make(pu(u));HS.add(H)
   g=post('/move',{'game':g['game'],'move':uc(root())})
main()
