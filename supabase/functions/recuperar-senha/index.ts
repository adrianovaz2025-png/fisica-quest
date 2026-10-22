// Recuperação de senha do IMPÉRIO por e-mail.
// O aluno digita o nick; se ele cadastrou um e-mail de recuperação, enviamos um link
// para criar senha nova. Envio pelo Brevo (API HTTPS). Segredos necessários:
//   BREVO_KEY    – chave de API do Brevo
//   SENDER_EMAIL – e-mail remetente verificado no Brevo
import { createClient } from "jsr:@supabase/supabase-js@2";

const SITE = "https://adrianovaz2025-png.github.io/fisica-quest/";
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const ok = (body: Record<string, unknown>, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...CORS, "Content-Type": "application/json" } });

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  try {
    const { nick } = await req.json();
    const n = String(nick || "").trim();
    if (!/^[A-Za-z0-9_]{3,16}$/.test(n)) return ok({ ok: true });
    const sb = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);

    // no máximo 3 pedidos por nick a cada hora
    const desde = new Date(Date.now() - 3600_000).toISOString();
    const { count } = await sb.from("recup_pedidos").select("*", { count: "exact", head: true }).ilike("nick", n).gte("criado", desde);
    if ((count ?? 0) >= 3) return ok({ ok: true, limite: true });
    await sb.from("recup_pedidos").insert({ nick: n });

    const { data: p } = await sb.from("perfis").select("id,nick,nome").ilike("nick", n).maybeSingle();
    if (!p) return ok({ ok: true });
    const { data: r } = await sb.from("recuperacao").select("email").eq("id", p.id).maybeSingle();
    if (!r?.email) return ok({ ok: true, semEmail: true });
    const { data: u } = await sb.auth.admin.getUserById(p.id);
    if (!u?.user?.email) return ok({ ok: true });
    const { data: link, error } = await sb.auth.admin.generateLink({ type: "recovery", email: u.user.email });
    if (error || !link?.properties?.hashed_token) throw error || new Error("sem token");
    const url = `${SITE}?recup=${encodeURIComponent(link.properties.hashed_token)}`;

    const nome = (p.nome || p.nick).split(" ")[0];
    const html = `<div style="font-family:Arial,sans-serif;max-width:520px;margin:auto;background:#2a1d14;color:#f4e4c0;padding:24px;border:4px solid #e8c070">
      <h2 style="color:#f8d870;margin-top:0">IMPÉRIO · Nova senha</h2>
      <p>Olá, ${nome}! Recebemos um pedido para criar uma senha nova para o nick <b>${p.nick}</b>.</p>
      <p style="text-align:center;margin:28px 0"><a href="${url}" style="background:#e8c070;color:#2a1d14;padding:14px 22px;text-decoration:none;font-weight:bold">CRIAR SENHA NOVA</a></p>
      <p style="font-size:13px;color:#c8b898">O link vale por 1 hora e só funciona uma vez. Se não foi você que pediu, ignore este e-mail: sua senha continua a mesma.</p></div>`;
    const res = await fetch("https://api.brevo.com/v3/smtp/email", {
      method: "POST",
      headers: { "api-key": Deno.env.get("BREVO_KEY")!, "Content-Type": "application/json", accept: "application/json" },
      body: JSON.stringify({
        sender: { name: "Império – Física", email: Deno.env.get("SENDER_EMAIL")! },
        to: [{ email: r.email }],
        subject: "Império: crie sua senha nova",
        htmlContent: html,
      }),
    });
    if (!res.ok) throw new Error("brevo " + res.status + " " + (await res.text()).slice(0, 200));
    return ok({ ok: true, enviado: true });
  } catch (e) {
    console.error(e);
    return ok({ ok: false, erro: String((e as Error)?.message || e).slice(0, 200) }, 500);
  }
});
