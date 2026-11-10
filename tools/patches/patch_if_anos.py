def patch(fn):
    s=open(fn,encoding='utf-8').read()
    def rep(a,b):
        nonlocal s
        assert s.count(a)==1,(fn,a[:50],s.count(a)); s=s.replace(a,b)
    rep("Processo seletivo dos cursos técnicos integrados · provas de 2025 e 2026","Processo seletivo dos cursos técnicos integrados · provas de 2020, 2023, 2024, 2025 e 2026")
    rep("'Prova inteira · 25 de Língua Portuguesa e 25 de Matemática'","'Prova inteira · 50 questões (Português, Matemática e, em 2020, Ciências, Geografia e História)'")
    open(fn,'w',encoding='utf-8').write(s)
for f in ('index.html','teste.html'): patch(f)
