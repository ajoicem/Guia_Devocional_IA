import os
from supabase import create_client


def conectar(access_token=None, refresh_token=None):
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError(
            "SUPABASE_URL ou SUPABASE_KEY não foram configuradas."
        )

    supabase = create_client(url, key)

    if access_token and refresh_token:
        supabase.auth.set_session(access_token, refresh_token)

    return supabase


def entrar(email, senha):
    supabase = conectar()

    return supabase.auth.sign_in_with_password({
        "email": email,
        "password": senha
    })


def criar_conta(email, senha):
    supabase = conectar()

    return supabase.auth.sign_up({
        "email": email,
        "password": senha
    })


def sair(access_token=None, refresh_token=None):
    supabase = conectar(access_token, refresh_token)
    return supabase.auth.sign_out()


def criar_conversa(
    titulo,
    user_id,
    access_token,
    refresh_token
):
    supabase = conectar(access_token, refresh_token)

    resposta = (
        supabase.table("conversations")
        .insert({
            "title": titulo,
            "user_id": user_id
        })
        .execute()
    )

    return resposta.data[0]["id"]


def salvar_mensagem(
    conversation_id,
    role,
    content,
    access_token,
    refresh_token
):
    supabase = conectar(access_token, refresh_token)

    supabase.table("messages").insert({
        "conversation_id": conversation_id,
        "role": role,
        "content": content
    }).execute()


def carregar_mensagens(
    conversation_id,
    user_id,
    access_token,
    refresh_token
):
    supabase = conectar(access_token, refresh_token)

    # Confirma primeiro que a conversa pertence ao usuário logado.
    conversa = (
        supabase.table("conversations")
        .select("id")
        .eq("id", conversation_id)
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )

    if not conversa.data:
        return []

    resposta = (
        supabase.table("messages")
        .select("*")
        .eq("conversation_id", conversation_id)
        .order("created_at")
        .execute()
    )

    return resposta.data


def listar_conversas(
    user_id,
    access_token,
    refresh_token
):
    supabase = conectar(access_token, refresh_token)

    resposta = (
        supabase.table("conversations")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    return resposta.data
