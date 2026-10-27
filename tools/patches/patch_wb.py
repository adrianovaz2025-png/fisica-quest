import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
a="clampCam(W);const Z=ZM(W),RW=Math.ceil(VW/Z),RH=Math.ceil(VH/Z);wb.clearRect"
assert s.count(a)==1
s=s.replace(a,"clampCam(W);const Z=ZM(W),RW=Math.ceil(VW/Z),RH=Math.ceil(VH/Z);if(WB.width<RW+2||WB.height<RH+2){WB.width=Math.max(WB.width,RW+2);WB.height=Math.max(WB.height,RH+2);wb.imageSmoothingEnabled=false}wb.clearRect")
open(f,'w',encoding='utf-8').write(s);print('wb ok',f)
s=open(f,encoding='utf-8').read()
a="wb.imageSmoothingEnabled=false}wb.clearRect(0,0,RW+2,RH+2);"
assert s.count(a)==1
s=s.replace(a,"wb.imageSmoothingEnabled=false}wb.fillStyle=(W.pal&&W.pal.water&&!W.pal.lava)?W.pal.water[4]:'#0b0710';wb.fillRect(0,0,RW+2,RH+2);")
open(f,'w',encoding='utf-8').write(s);print('fill ok')
s=open(f,encoding='utf-8').read()
a="function clampCam(W){const Z=ZM(W);W.cam.x=clamp(W.cam.x,0,W.w-VW/Z);W.cam.y=clamp(W.cam.y,0,W.h-VH/Z)}"
assert s.count(a)==1
s=s.replace(a,"function clampCam(W){const Z=ZM(W),mx=W.w-VW/Z,my=W.h-VH/Z;W.cam.x=mx<0?mx/2:clamp(W.cam.x,0,mx);W.cam.y=my<0?my/2:clamp(W.cam.y,0,my)}")
open(f,'w',encoding='utf-8').write(s);print('cam ok')
