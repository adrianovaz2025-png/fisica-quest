import sys
def patch(fn):
    s=open(fn,encoding='utf-8').read()
    def rep(a,b):
        nonlocal s
        assert s.count(a)==1,(fn,a[:50],s.count(a))
        s=s.replace(a,b)
    rep("if(lv>=3&&lv<4&&!G.solo)return;if(lv>=3&&lv<4)return helmGround(G,t,P,lv);","if(lv>=3&&lv<4)return helmGround(G,t,P,lv);")
    rep("function helmGround(G,t,P,lv){const{x,Y}=G;","function helmGround(G,t,P,lv){const{x,Y,back}=G;")
    rep("const hm=mk2(m=>{mEll(m,32,Y(16.6),12.8,10.4);mRect(m,19.2,Y(16.6),25.6,8.6)});cel(x,hm,P.b,{chrome:1});\n cel(x,mk2(m=>{mRect(m,25.4,Y(19.6),13.2,8.4);mEll(m,32,Y(19.8),6.6,2.6)}),'#08060c',{flat:1,dk:0,rim:0});",
        "const hm=mk2(m=>{mEll(m,32,Y(16.6),12.8,10.4);mRect(m,19.2,Y(16.6),25.6,8.6)});if(!back)mSub(hm,mk2(m=>{mRect(m,24.6,Y(19.6),14.8,11);mEll(m,32,Y(19.8),7.4,3)}));cel(x,hm,P.b,{chrome:1});")
    rep(" drawGroundHelm(x,eq,px,py,s);fxFront(F)}"," fxFront(F)}")
    s=s.replace("/* elmo dos níveis altos: viseira aberta + marca do nível (fica pousado no chão ao lado do herói) */","/* elmo dos níveis altos: usado na cabeça, rosto à mostra + marca do nível */")
    open(fn,'w',encoding='utf-8').write(s)
for f in ('index.html','teste.html'): patch(f)
