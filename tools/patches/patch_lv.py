import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:60]);s=s.replace(a,b)
rep("NIVEIS:[0,100,300,700,1300,2200,3500,5000,7000,10000],","NIVEIS:[0,500,1500,3000,5000,8000,12000,17000,23000,30000],")
rep("const mw=96,CX0=W.w*.2","const mw=66,CX0=W.w*.2")
rep("x0=VW-mw-44,y0=28;","x0=VW-mw-44,y0=26;")
open(f,'w',encoding='utf-8').write(s);print('lv ok')
