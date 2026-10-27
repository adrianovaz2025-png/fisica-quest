import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
i=s.find('function buildTribeWorld(levels){');j=s.find('\n/* ===== construções das regiões novas',i);assert i>0 and j>i
s=s[:i]+open('/home/claude/work/btw_cont.js',encoding='utf-8').read().rstrip()+s[j:]
open(f,'w',encoding='utf-8').write(s);print('cont ok')
s=open(f,encoding='utf-8').read()
a="for(let t=.35;t<20;t+=.35){const sx=X+lhx*t,sy=Y+lhy*t;"
s=s.replace(a,"for(let t=.5;t<20;t+=.5){const sx=X+lhx*t,sy=Y+lhy*t;")
open(f,'w',encoding='utf-8').write(s);print('ray ok')
