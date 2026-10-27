-- =====================================================================
-- IMPÉRIO · banco Supabase (schema public) — exportado em 27/10/2026
-- Projeto Supabase: deebihpvewibzciwwpyc
-- Reconstruído a partir do catálogo (pg_get_functiondef etc.). Serve como
-- referência e para recriar o banco do zero. NÃO contém dados nem os
-- códigos de cadastro das turmas (tabela turmas.codigo) — esses ficam só no banco.
-- Obs.: existe também um trigger em auth.users (AFTER INSERT) que chama
-- public.criar_perfil_novo_usuario() — é ele que cria o perfil no cadastro.
-- =====================================================================

-- TABELAS
create table public.turmas (
  id text not null,               -- '1A','1B','2A','2B','3A' e 'PROF'
  nome text not null,
  tribo text not null,
  serie integer not null,
  codigo text not null            -- código de cadastro da turma (secreto)
);

create table public.perfis (
  id uuid not null,               -- = auth.users.id
  nick text not null,
  personagem integer default 0 not null,
  turma text not null,
  fases integer default 0 not null,
  pontos integer default 0 not null,
  equip jsonb default '{}'::jsonb not null,   -- inventário, equipamento, stats ENEM (equip.enem), guardião (equip.guard), equip.s, equip.manut...
  visual jsonb default '{}'::jsonb not null,  -- aparência do herói (cabelo, pele, cores, arm:{b,a})
  criado_em timestamp with time zone default now() not null,
  atualizado_em timestamp with time zone default now() not null,
  bonus integer default 0 not null,           -- pontos ganhos em simulados
  bonus_dia date,
  bonus_hoje integer default 0 not null,
  simulado_em timestamp with time zone,
  nome text default ''::text not null,
  admin boolean default false not null,       -- professor
  lim_dia date,
  erros_dia integer default 0 not null,       -- limite diário: 20 erros
  pontos_dia integer default 0 not null,      -- limite diário: 400 pontos
  fora_estat boolean default false not null,  -- fora das estatísticas do diretor
  visto_em timestamp with time zone,          -- presença (ping)
  visto_dia date,
  min_hoje integer default 0,
  primeiro_hoje timestamp with time zone
);

create table public.registro (                -- log imutável de tudo
  id bigserial not null,
  criado_em timestamp with time zone default now() not null,
  aluno uuid,
  nick text,
  turma text,
  tipo text not null,                         -- 'cadastro','perfil','simulado','senha_redefinida'...
  dados jsonb default '{}'::jsonb not null
);

create table public.recuperacao (             -- e-mail de recuperação de senha
  id uuid not null,
  email text not null,
  atualizado timestamp with time zone default now()
);

create table public.recup_pedidos (
  nick text not null,
  criado timestamp with time zone default now()
);

create table public.diretor_acesso (          -- hash sha256 do código do Painel do Diretor
  id integer default 1 not null,
  hash text not null,
  criado_em timestamp with time zone default now()
);

-- CONSTRAINTS
alter table diretor_acesso add constraint diretor_acesso_pkey PRIMARY KEY (id);
alter table turmas add constraint turmas_pkey PRIMARY KEY (id);
alter table turmas add constraint turmas_serie_check CHECK (((serie >= 0) AND (serie <= 3)));
alter table perfis add constraint perfis_pkey PRIMARY KEY (id);
alter table perfis add constraint perfis_fases_check CHECK (((fases >= 0) AND (fases <= 24)));
alter table perfis add constraint perfis_personagem_check CHECK (((personagem >= 0) AND (personagem <= 3)));
alter table perfis add constraint perfis_id_fkey FOREIGN KEY (id) REFERENCES auth.users(id) ON DELETE CASCADE;
alter table perfis add constraint perfis_turma_fkey FOREIGN KEY (turma) REFERENCES turmas(id);
alter table recuperacao add constraint recuperacao_pkey PRIMARY KEY (id);
alter table recuperacao add constraint recuperacao_id_fkey FOREIGN KEY (id) REFERENCES perfis(id) ON DELETE CASCADE;
alter table registro add constraint registro_pkey PRIMARY KEY (id);

-- RLS (todas as tabelas com RLS; quase tudo passa por funções SECURITY DEFINER)
alter table public.diretor_acesso enable row level security;
alter table public.perfis enable row level security;
alter table public.recup_pedidos enable row level security;
alter table public.recuperacao enable row level security;
alter table public.registro enable row level security;
alter table public.turmas enable row level security;

create policy "aluno edita o proprio perfil" on public.perfis for UPDATE to authenticated using ((id = auth.uid())) with check ((id = auth.uid()));
create policy "aluno le o proprio perfil" on public.perfis for SELECT to authenticated using ((id = auth.uid()));

-- TRIGGERS
CREATE TRIGGER perfil_log AFTER INSERT OR UPDATE ON public.perfis FOR EACH ROW EXECUTE FUNCTION _perfil_log();
CREATE TRIGGER registro_imutavel BEFORE DELETE OR UPDATE ON public.registro FOR EACH ROW EXECUTE FUNCTION _registro_imutavel();
-- (em auth.users) CREATE TRIGGER ... AFTER INSERT ON auth.users FOR EACH ROW EXECUTE FUNCTION public.criar_perfil_novo_usuario();

-- ============================ FUNÇÕES ============================

CREATE OR REPLACE FUNCTION public._log(p_aluno uuid, p_tipo text, p_dados jsonb)
RETURNS void LANGUAGE sql SECURITY DEFINER SET search_path TO 'public'
AS $function$
insert into registro (aluno, nick, turma, tipo, dados)
select p_aluno, p.nick, p.turma, p_tipo, coalesce(p_dados, '{}'::jsonb) from (select 1) x left join perfis p on p.id = p_aluno
$function$;

CREATE OR REPLACE FUNCTION public._perfil_log()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path TO 'public'
AS $function$
begin
if tg_op = 'INSERT' then
  insert into registro (aluno, nick, turma, tipo, dados)
  values (new.id, new.nick, new.turma, 'cadastro', jsonb_build_object('nome', new.nome));
elsif new.pontos is distinct from old.pontos or new.fases is distinct from old.fases
   or new.turma is distinct from old.turma or new.nome is distinct from old.nome
   or new.admin is distinct from old.admin or new.bonus is distinct from old.bonus then
  insert into registro (aluno, nick, turma, tipo, dados)
  values (new.id, new.nick, new.turma, 'perfil', jsonb_strip_nulls(jsonb_build_object(
    'pontos', case when new.pontos is distinct from old.pontos then jsonb_build_array(old.pontos, new.pontos) end,
    'bonus', case when new.bonus is distinct from old.bonus then jsonb_build_array(old.bonus, new.bonus) end,
    'fases', case when new.fases is distinct from old.fases then jsonb_build_array(old.fases, new.fases) end,
    'turma', case when new.turma is distinct from old.turma then jsonb_build_array(old.turma, new.turma) end,
    'nome', case when new.nome is distinct from old.nome then jsonb_build_array(old.nome, new.nome) end,
    'admin', case when new.admin is distinct from old.admin then jsonb_build_array(old.admin, new.admin) end,
    'por', case when auth.uid() is null then 'painel' when auth.uid() = new.id then 'aluno' else 'outro' end)));
end if;
return new;
end $function$;

CREATE OR REPLACE FUNCTION public._registrar_simulado_base(p_acertos integer, p_total integer)
RETURNS integer LANGUAGE plpgsql SECURITY DEFINER SET search_path TO 'public'
AS $function$
declare p public.perfis; g int; tot int; ac int; motivo text := null; hoje date := (now() at time zone 'America/Sao_Paulo')::date;
begin
select * into p from perfis where id = auth.uid() for update;
if not found then return 0; end if;
tot := greatest(0, least(coalesce(p_total, 0), 45));
ac := greatest(0, least(coalesce(p_acertos, 0), tot));
if p.admin then perform _log(p.id, 'simulado', jsonb_build_object('acertos', ac, 'total', tot, 'ganho', 0, 'motivo', 'professor')); return 0; end if;
if p.simulado_em is not null and p.simulado_em > now() - make_interval(secs => greatest(20, tot * 4)) then
  perform _log(p.id, 'simulado', jsonb_build_object('acertos', ac, 'total', tot, 'ganho', 0, 'motivo', 'rapido_demais',
    'seg_desde_ultimo', round(extract(epoch from now() - p.simulado_em))));
  return 0;
end if;
if p.lim_dia is distinct from hoje then p.erros_dia := 0; p.pontos_dia := 0; end if;
if p.erros_dia >= 20 then g := 0; motivo := 'limite_erros'; else g := ac * 2; end if;
if g > greatest(0, 400 - p.pontos_dia) then g := greatest(0, 400 - p.pontos_dia); motivo := coalesce(motivo, 'limite_pontos'); end if;
update perfis
   set bonus = bonus + g, simulado_em = now(),
       pontos = fases * 10 + (fases / 6) * 50 + bonus + g,
       lim_dia = hoje, erros_dia = p.erros_dia + (tot - ac), pontos_dia = p.pontos_dia + g
 where id = auth.uid();
perform _log(p.id, 'simulado', jsonb_strip_nulls(jsonb_build_object('acertos', ac, 'total', tot, 'ganho', g, 'motivo', motivo,
  'erros_dia', p.erros_dia + (tot - ac), 'pontos_dia', p.pontos_dia + g,
  'seg_desde_ultimo', case when p.simulado_em is null then null else round(extract(epoch from now() - p.simulado_em)) end)));
return g;
end $function$;

CREATE OR REPLACE FUNCTION public._registro_imutavel()
RETURNS trigger LANGUAGE plpgsql
AS $function$ begin raise exception 'registro_imutavel'; end $function$;

CREATE OR REPLACE FUNCTION public.admin_alunos()
RETURNS TABLE(nome text, nick text, turma text, pontos integer, simulados integer, criado_em timestamp with time zone)
LANGUAGE plpgsql STABLE SECURITY DEFINER SET search_path TO 'public'
AS $function$
begin
if not exists (select 1 from perfis where id = auth.uid() and admin) then raise exception 'sem_permissao'; end if;
return query
  select p.nome, p.nick, p.turma, p.pontos, coalesce((p.equip->'enem'->>'n')::int, 0), p.criado_em
    from perfis p where not p.admin order by p.pontos desc, p.nick;
end $function$;

CREATE OR REPLACE FUNCTION public.admin_ao_vivo()
RETURNS TABLE(nick text, nome text, turma text, visto_em timestamp with time zone, primeiro_hoje timestamp with time zone, min_hoje integer, simulados integer, questoes integer, acertos integer, pontos_dia integer, ult_simulado timestamp with time zone)
LANGUAGE plpgsql SECURITY DEFINER SET search_path TO 'public'
AS $function$
declare hoje date := (now() at time zone 'America/Sao_Paulo')::date;
begin
if not exists (select 1 from perfis a where a.id = auth.uid() and a.admin) then raise exception 'sem permissao'; end if;
return query
select p.nick, p.nome, p.turma, p.visto_em,
       case when p.visto_dia = hoje then p.primeiro_hoje end,
       case when p.visto_dia = hoje then coalesce(p.min_hoje,0) else 0 end,
       coalesce(r.n,0)::int, coalesce(r.q,0)::int, coalesce(r.a,0)::int,
       case when p.lim_dia = hoje then coalesce(p.pontos_dia,0) else 0 end,
       r.ult
  from perfis p
  left join (select g.aluno, count(*) n, sum((g.dados->>'total')::int) q, sum((g.dados->>'acertos')::int) a, max(g.criado_em) ult
               from registro g where g.tipo='simulado' and (g.criado_em at time zone 'America/Sao_Paulo')::date = hoje group by g.aluno) r on r.aluno = p.id
 where not coalesce(p.admin,false) and p.turma <> 'PROF';
end $function$;

CREATE OR REPLACE FUNCTION public.admin_codigo_diretor(p_novo text)
RETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path TO 'public'
AS $function$
begin
if not exists (select 1 from perfis where id = auth.uid() and admin) then raise exception 'nao_autorizado'; end if;
if length(coalesce(p_novo,'')) < 8 then raise exception 'codigo_curto'; end if;
insert into diretor_acesso (id, hash) values (1, encode(sha256(convert_to(p_novo,'UTF8')),'hex'))
on conflict (id) do update set hash = excluded.hash, criado_em = now();
end $function$;

CREATE OR REPLACE FUNCTION public.admin_emails_recup()
RETURNS TABLE(nick text, tem_email boolean) LANGUAGE plpgsql STABLE SECURITY DEFINER SET search_path TO 'public'
AS $function$
begin
if not exists (select 1 from perfis where id = auth.uid() and admin) then raise exception 'nao_autorizado'; end if;
return query select p.nick::text, (r.id is not null) from perfis p left join recuperacao r on r.id = p.id where not p.admin;
end $function$;

CREATE OR REPLACE FUNCTION public.admin_enem()
RETURNS TABLE(nick text, turma text, enem jsonb, fora boolean) LANGUAGE plpgsql STABLE SECURITY DEFINER SET search_path TO 'public'
AS $function$
begin
if not exists (select 1 from perfis where id = auth.uid() and admin) then raise exception 'nao_autorizado'; end if;
return query select p.nick::text, p.turma::text, coalesce(p.equip->'enem','{}'::jsonb), p.fora_estat from perfis p where not p.admin;
end $function$;

CREATE OR REPLACE FUNCTION public.admin_fora_estat(p_nick text, p_fora boolean)
RETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path TO 'public'
AS $function$
begin
if not exists (select 1 from perfis where id = auth.uid() and admin) then raise exception 'nao_autorizado'; end if;
update perfis set fora_estat = coalesce(p_fora,false) where lower(nick) = lower(p_nick) and not admin;
end $function$;

CREATE OR REPLACE FUNCTION public.admin_redefinir_senha(p_nick text, p_senha text)
RETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path TO 'public', 'extensions', 'auth'
AS $function$
declare v_id uuid;
begin
if not exists (select 1 from public.perfis where id = auth.uid() and admin) then raise exception 'nao_autorizado'; end if;
if length(coalesce(p_senha,'')) < 6 then raise exception 'senha_curta'; end if;
select id into v_id from public.perfis where lower(nick) = lower(p_nick) and not admin;
if v_id is null then raise exception 'aluno_nao_encontrado'; end if;
update auth.users set encrypted_password = extensions.crypt(p_senha, extensions.gen_salt('bf')), updated_at = now() where id = v_id;
perform public._log(v_id, 'senha_redefinida', jsonb_build_object('por','professor'));
exception when undefined_function then
update auth.users set encrypted_password = extensions.crypt(p_senha, extensions.gen_salt('bf')), updated_at = now() where id = v_id;
end $function$;

CREATE OR REPLACE FUNCTION public.admin_registro(p_nick text DEFAULT NULL::text, p_limite integer DEFAULT 300)
RETURNS TABLE(quando text, nick text, turma text, tipo text, dados jsonb) LANGUAGE plpgsql STABLE SECURITY DEFINER SET search_path TO 'public'
AS $function$
begin
if not exists (select 1 from perfis where id = auth.uid() and admin) then raise exception 'sem_permissao'; end if;
return query select to_char(r.criado_em at time zone 'America/Sao_Paulo', 'DD/MM HH24:MI:SS'), r.nick, r.turma, r.tipo, r.dados
  from registro r where p_nick is null or lower(r.nick) = lower(p_nick)
 order by r.criado_em desc limit least(greatest(coalesce(p_limite, 300), 1), 5000);
end $function$;

CREATE OR REPLACE FUNCTION public.concluir_fase(p_fase integer)
RETURNS perfis LANGUAGE plpgsql SECURITY DEFINER SET search_path TO 'public'
AS $function$
declare p public.perfis;
begin
update perfis
   set fases = fases + 1, pontos = (fases + 1) * 10 + ((fases + 1) / 6) * 50 + bonus, atualizado_em = now()
 where id = auth.uid() and fases = p_fase and p_fase < 24 and atualizado_em < now() - interval '5 seconds'
returning * into p;
if not found then select * into p from perfis where id = auth.uid(); end if;
return p;
end $function$;

CREATE OR REPLACE FUNCTION public.criar_perfil_novo_usuario()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path TO 'public'
AS $function$
declare m jsonb := new.raw_user_meta_data; t public.turmas;
begin
select * into t from public.turmas where id = m->>'turma';
if not found or upper(trim(coalesce(m->>'codigo',''))) <> upper(t.codigo) then raise exception 'codigo_invalido'; end if;
if coalesce(m->>'nick','') !~ '^[A-Za-z0-9_]{3,16}$' then raise exception 'nick_invalido'; end if;
if t.id = 'PROF' and lower(m->>'nick') <> 'adrianovaz' then raise exception 'codigo_invalido'; end if;
if t.id <> 'PROF' and lower(m->>'nick') = 'adrianovaz' then raise exception 'nick_invalido'; end if;
insert into public.perfis (id, nick, nome, admin, personagem, turma, visual)
values (new.id, m->>'nick', left(trim(coalesce(m->>'nome','')), 60), t.id = 'PROF',
        least(greatest(coalesce((m->>'personagem')::int, 0), 0), 3), t.id,
        case when jsonb_typeof(m->'visual') = 'object' then m->'visual' else '{}'::jsonb end);
return new;
end $function$;

CREATE OR REPLACE FUNCTION public.limites_hoje()
RETURNS json LANGUAGE sql STABLE SECURITY DEFINER SET search_path TO 'public'
AS $function$
select json_build_object(
  'erros', case when lim_dia = (now() at time zone 'America/Sao_Paulo')::date then erros_dia else 0 end,
  'pontos', case when lim_dia = (now() at time zone 'America/Sao_Paulo')::date then pontos_dia else 0 end,
  'max_erros', 20, 'max_pontos', 400)
from perfis where id = auth.uid()
$function$;

CREATE OR REPLACE FUNCTION public.membros_tribo(p_turma text)
RETURNS TABLE(nick text, personagem integer, pontos integer, fases integer, visual jsonb, equip jsonb)
LANGUAGE sql STABLE SECURITY DEFINER SET search_path TO 'public'
AS $function$
select nick, personagem, pontos, fases, visual, equip from perfis where turma = p_turma order by pontos desc, nick limit 60;
$function$;

CREATE OR REPLACE FUNCTION public.mestre()
RETURNS json LANGUAGE sql STABLE SECURITY DEFINER SET search_path TO 'public'
AS $function$
select json_build_object('nick', nick, 'visual', visual, 'equip', coalesce(equip->'s', '{}'::jsonb), 'guard', coalesce(equip->'guard', '{}'::jsonb), 'manut', coalesce((equip->>'manut')::boolean, false))
from perfis where admin order by nick limit 1
$function$;

CREATE OR REPLACE FUNCTION public.meu_email_recup()
RETURNS text LANGUAGE sql STABLE SECURITY DEFINER SET search_path TO 'public'
AS $function$ select email from recuperacao where id = auth.uid() $function$;

CREATE OR REPLACE FUNCTION public.painel_diretor(p_codigo text)
RETURNS TABLE(turma text, enem jsonb) LANGUAGE plpgsql STABLE SECURITY DEFINER SET search_path TO 'public'
AS $function$
begin
if not exists (select 1 from diretor_acesso where hash = encode(sha256(convert_to(coalesce(p_codigo,''),'UTF8')),'hex')) then
  perform pg_sleep(1); raise exception 'codigo_invalido';
end if;
return query select p.turma::text, coalesce(p.equip->'enem','{}'::jsonb) from perfis p where not p.admin and not p.fora_estat;
end $function$;

CREATE OR REPLACE FUNCTION public.ping(p_ativo boolean DEFAULT true)
RETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path TO 'public'
AS $function$
declare hoje date := (now() at time zone 'America/Sao_Paulo')::date;
begin
update perfis set
  min_hoje = case when visto_dia is distinct from hoje then 1 when p_ativo and (visto_em is null or visto_em < now() - interval '50 seconds') then coalesce(min_hoje,0)+1 else min_hoje end,
  primeiro_hoje = case when visto_dia is distinct from hoje then now() else primeiro_hoje end,
  visto_dia = hoje,
  visto_em = case when p_ativo then now() else visto_em end
where id = auth.uid() and (visto_em is null or visto_em < now() - interval '40 seconds' or visto_dia is distinct from hoje);
end $function$;

CREATE OR REPLACE FUNCTION public.placar_tribos()
RETURNS TABLE(id text, nome text, tribo text, serie integer, pontos bigint, membros bigint)
LANGUAGE sql STABLE SECURITY DEFINER SET search_path TO 'public'
AS $function$
select t.id, t.nome, t.tribo, t.serie, coalesce(sum(p.pontos), 0), count(p.id)
from turmas t left join perfis p on p.turma = t.id where t.id <> 'PROF' group by t.id order by t.id;
$function$;

CREATE OR REPLACE FUNCTION public.registrar_simulado(p_acertos integer, p_total integer, p_fonte text DEFAULT NULL::text)
RETURNS integer LANGUAGE plpgsql SECURITY DEFINER SET search_path TO 'public'
AS $function$
begin
if coalesce(p_fonte, '') <> 'enem' then
  begin
    perform _log(auth.uid(), 'simulado', jsonb_build_object('acertos', p_acertos, 'total', p_total, 'ganho', 0, 'motivo', case when p_fonte is null then 'versao_antiga_do_jogo' else 'questoes_rapidas_sem_pontos' end));
  exception when others then null; end;
  return 0;
end if;
return public._registrar_simulado_base(p_acertos, p_total);
end $function$;

CREATE OR REPLACE FUNCTION public.salvar_email_recup(p_email text)
RETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path TO 'public'
AS $function$
begin
if auth.uid() is null then raise exception 'nao_autorizado'; end if;
if coalesce(p_email,'') !~* '^[^@\s]+@[^@\s]+\.[^@\s]+$' or length(p_email) > 120 then raise exception 'email_invalido'; end if;
insert into recuperacao (id, email) values (auth.uid(), lower(trim(p_email)))
on conflict (id) do update set email = excluded.email, atualizado = now();
end $function$;

CREATE OR REPLACE FUNCTION public.validar_cadastro(p_turma text, p_codigo text, p_nick text)
RETURNS text LANGUAGE plpgsql STABLE SECURITY DEFINER SET search_path TO 'public'
AS $function$
begin
if not exists (select 1 from turmas where id = p_turma and upper(codigo) = upper(trim(p_codigo))) then return 'codigo'; end if;
if p_turma = 'PROF' and lower(p_nick) <> 'adrianovaz' then return 'codigo'; end if;
if p_turma <> 'PROF' and lower(p_nick) = 'adrianovaz' then return 'nick'; end if;
if exists (select 1 from perfis where lower(nick) = lower(p_nick)) then return 'nick'; end if;
return 'ok';
end $function$;

-- EXECUTE (quem pode chamar)
-- funções _* : só postgres/service_role (internas)
-- authenticated: admin_* (checam perfis.admin), concluir_fase, limites_hoje, membros_tribo, meu_email_recup, registrar_simulado, salvar_email_recup
-- anon+authenticated: mestre, painel_diretor (protegido por código), ping, placar_tribos, validar_cadastro, admin_ao_vivo (checa admin)
