
import os
from supabase import create_client


def conectar():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError(
            "SUPABASE_URL ou SUPABASE_KEY não foram configuradas."
        )

    return create_client(url, key)


def criar_conversa(titulo):
    supabase = conectar()

    resposta = (
        supabase
        .table("conversations")
        .insert({
            "title": titulo
        })
        .execute()
    )

    return resposta.data[0]["id"]


def salvar_mensagem(conversation_id, role, content):
    supabase = conectar()

    supabase.table("messages").insert({
        "conversation_id": conversation_id,
        "role": role,
        "content": content
    }).execute()


def carregar_mensagens(conversation_id):
    supabase = conectar()

    resposta = (
        supabase
        .table("messages")
        .select("*")
        .eq("conversation_id", conversation_id)
        .order("created_at")
        .execute()
    )

    return resposta.data


def listar_conversas():
    supabase = conectar()

    resposta = (
        supabase
        .table("conversations")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return resposta.data


def atualizar_titulo_conversa(conversation_id, titulo):
    supabase = conectar()

    (
        supabase
        .table("conversations")
        .update({
            "title": titulo
        })
        .eq("id", conversation_id)
        .execute()
    )
