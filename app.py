import os
import streamlit as st
import cohere

from database import (
    criar_conversa,
    salvar_mensagem,
    carregar_mensagens,
    listar_conversas,
    entrar,
    criar_conta,
    sair
)

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================

st.set_page_config(
    page_title="Guia Devocional IA",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# IDENTIDADE VISUAL
# =====================================================

st.markdown("""
<style>

/* -----------------------------------------------------
   CORES DA MARCA
----------------------------------------------------- */

:root {
    --brand-gold: #C49A4A;
    --brand-gold-hover: #D5B66F;
    --sidebar-bg: #172437;
    --sidebar-button: #223149;
}


/* -----------------------------------------------------
   APLICATIVO
   Usa as cores do próprio tema Light/Dark do Streamlit
----------------------------------------------------- */

html,
body,
[data-testid="stAppViewContainer"],
.stApp {
    background-color: #F8F4EA !important; /* Cor de fundo clara */
    color: #172437 !important;
}

[data-testid="stHeader"] {
    background-color: #F8F4EA !important;
    border-bottom: none !important;
    box-shadow: none !important;
}

/* Força a barra inferior (onde fica o chat_input) a ficar clara */
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"] {
    background-color: #F8F4EA !important;
    border-top: none !important;
    box-shadow: none !important;
}


/* -----------------------------------------------------
   ÁREA PRINCIPAL
----------------------------------------------------- */

.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 2.5rem;
}


/* -----------------------------------------------------
   SIDEBAR
----------------------------------------------------- */

section[data-testid="stSidebar"] {
    background-color: var(--sidebar-bg) !important;

    width: 230px !important;
    min-width: 230px !important;
    max-width: 230px !important;

    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

section[data-testid="stSidebar"] > div {
    width: 230px !important;
}

section[data-testid="stSidebar"] * {
    color: #F8F4EA !important;
}


/* -----------------------------------------------------
   CABEÇALHO DA SIDEBAR
----------------------------------------------------- */

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 8px;

    margin-top: 4px;
    margin-bottom: 2px;

    font-size: 17px;
    line-height: 1.2;
    font-weight: 700;

    color: #F8F4EA !important;
    white-space: nowrap;
}

.sidebar-brand-icon {
    font-size: 19px;
}

.sidebar-subtitle {
    margin-top: 6px;
    margin-bottom: 14px;

    color: #AEB8C6 !important;
    font-size: 10.5px;
    line-height: 1.35;
}


/* -----------------------------------------------------
   BOTÃO DE RECOLHER/ABRIR SIDEBAR
----------------------------------------------------- */

button[data-testid="stSidebarCollapseButton"],
div[data-testid="stSidebarCollapseButton"] button,
button[data-testid="collapsedControl"],
div[data-testid="collapsedControl"] button {
    opacity: 1 !important;
    visibility: visible !important;
    display: flex !important;
}

[data-testid="stSidebarHeader"] {
    opacity: 1 !important;
    visibility: visible !important;
}


/* -----------------------------------------------------
   BOTÕES DA SIDEBAR
----------------------------------------------------- */

.stButton > button {
    background-color: var(--sidebar-button) !important;
    color: #F8F4EA !important;

    border: 1px solid rgba(196, 154, 74, 0.78) !important;
    border-radius: 8px;

    min-height: 38px;
    padding: 0.45rem 0.65rem;

    font-size: 0.82rem;
    transition: all 0.18s ease;
}

.stButton > button:hover {
    background-color: var(--brand-gold) !important;
    color: #172437 !important;
    border-color: var(--brand-gold) !important;
}


/* -----------------------------------------------------
   TÍTULO PRINCIPAL
----------------------------------------------------- */

.devocional-hero {
    text-align: center;
    margin-top: 0.15rem;
    margin-bottom: 1.7rem;
}

.devocional-title {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;

    font-size: 2.35rem;
    line-height: 1.15;
    font-weight: 800;
    letter-spacing: -0.55px;

    color: var(--brand-gold) !important;
}

.devocional-title-icon {
    font-size: 2rem;
    line-height: 1;
}


/* -----------------------------------------------------
   SUBTÍTULO
----------------------------------------------------- */

.devocional-subtitle-box {
    display: inline-block;

    margin-top: 12px;
    padding: 7px 14px;

    border-radius: 8px;
    background: transparent !important;
    border: 1px solid rgba(196, 154, 74, 0.34);

    color: var(--st-text-color) !important;

    font-size: 0.94rem;
    line-height: 1.45;
}


/* -----------------------------------------------------
   TEXTOS E CHAT
----------------------------------------------------- */

.stMarkdown,
.stMarkdown p,
.stMarkdown li,
div[data-testid="stChatMessage"],
div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li {
    color: var(--st-text-color) !important;
}

h1,
h2,
h3 {
    color: var(--st-text-color) !important;
}

div[data-testid="stChatMessage"] {
    background: transparent !important;
    border-radius: 12px;
}


/* -----------------------------------------------------
   CAMPO DE PERGUNTA

   IMPORTANTE:
   Não forçamos nenhuma cor de fundo aqui.
   O próprio Streamlit controla:
   Light = claro
   Dark  = escuro
----------------------------------------------------- */

div[data-testid="stChatInput"] {
    background-color: #F8F4EA !important;
    border: none !important;
    box-shadow: none !important;
}

/* Caixa em volta do campo de texto */
div[data-testid="stChatInput"] > div {
    background-color: #FFFFFF !important; /* Fundo branco interno */
    border: 1px solid var(--brand-gold) !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}

/* Área de texto onde o usuário digita */
div[data-testid="stChatInput"] textarea {
    background-color: transparent !important;
    color: #172437 !important; /* Cor do texto digitado */
    border: none !important;
    box-shadow: none !important;
}

/* Texto de placeholder "Pergunte sobre..." */
div[data-testid="stChatInput"] textarea::placeholder {
    color: #C49A4A !important;
    opacity: 1 !important;
    font-weight: 500 !important;
}

/* Botão de enviar */
div[data-testid="stChatInput"] button {
    background-color: var(--brand-gold) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
}

div[data-testid="stChatInput"] button:hover {
    background-color: var(--brand-gold-hover) !important;
}


/* -----------------------------------------------------
   RODAPÉ / SOBRE O PROJETO
----------------------------------------------------- */

.app-footer {
    max-width: 760px;
    margin: 5rem auto 0 auto;
    padding-top: 1.4rem;
    padding-bottom: 0.5rem;
    text-align: center;
    border-top: 1px solid rgba(196, 154, 74, 0.28);
}

.footer-title {
    color: var(--brand-gold) !important;
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.footer-text {
    color: var(--st-text-color) !important;
    font-size: 0.84rem;
    line-height: 1.6;
    opacity: 0.82;
}


/* -----------------------------------------------------
   LINKEDIN
----------------------------------------------------- */

div[data-testid="stLinkButton"] {
    display: flex;
    justify-content: center;
}

div[data-testid="stLinkButton"] a {
    background-color: #0A66C2 !important;
    color: #FFFFFF !important;

    border: 1px solid #0A66C2 !important;
    border-radius: 8px !important;

    font-weight: 600 !important;
    min-width: 150px;
}

div[data-testid="stLinkButton"] a:hover {
    background-color: #004182 !important;
    border-color: #004182 !important;
    color: #FFFFFF !important;
}


/* -----------------------------------------------------
   MOBILE
----------------------------------------------------- */

@media (max-width: 768px) {

    .devocional-title {
        font-size: 1.9rem;
    }

    .devocional-title-icon {
        font-size: 1.7rem;
    }

    .block-container {
        padding-top: 1.2rem;
    }
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# COHERE
# =====================================================

api_key = os.getenv("Cohere_API_KEY")

if not api_key:
    st.error("A chave Cohere_API_KEY não foi encontrada.")
    st.stop()

co = cohere.Client(api_key)


# =====================================================
# AUTENTICAÇÃO
# =====================================================

if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_email" not in st.session_state:
    st.session_state.user_email = None


def usuario_logado():
    return bool(
        st.session_state.access_token
        and st.session_state.refresh_token
        and st.session_state.user_id
    )


if not usuario_logado():
    st.markdown(
        '<div class="devocional-hero">'
        '<div class="devocional-title">'
        '<span class="devocional-title-icon">📖</span>'
        '<span>Guia Devocional IA</span>'
        '</div>'
        '<div class="devocional-subtitle-box">'
        'Entre para iniciar seus estudos e manter seu histórico privado.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    aba_entrar, aba_cadastrar = st.tabs(["Entrar", "Criar conta"])

    with aba_entrar:
        with st.form("form_login"):
            email_login = st.text_input("E-mail", key="email_login")
            senha_login = st.text_input("Senha", type="password", key="senha_login")
            enviar_login = st.form_submit_button("Entrar", use_container_width=True)

        if enviar_login:
            if not email_login or not senha_login:
                st.warning("Preencha e-mail e senha.")
            else:
                try:
                    resposta = entrar(email_login.strip(), senha_login)

                    if not resposta.session or not resposta.user:
                        st.error("Não foi possível iniciar a sessão.")
                    else:
                        st.session_state.access_token = resposta.session.access_token
                        st.session_state.refresh_token = resposta.session.refresh_token
                        st.session_state.user_id = resposta.user.id
                        st.session_state.user_email = resposta.user.email
                        st.query_params.clear()
                        st.rerun()

                except Exception:
                    st.error("E-mail ou senha inválidos, ou a conta ainda não foi confirmada.")

    with aba_cadastrar:
        with st.form("form_cadastro"):
            email_cadastro = st.text_input("E-mail", key="email_cadastro")
            senha_cadastro = st.text_input(
                "Senha",
                type="password",
                key="senha_cadastro",
                help="Use pelo menos 6 caracteres."
            )
            confirmar_senha = st.text_input(
                "Confirmar senha",
                type="password",
                key="confirmar_senha"
            )
            enviar_cadastro = st.form_submit_button(
                "Criar conta",
                use_container_width=True
            )

        if enviar_cadastro:
            if not email_cadastro or not senha_cadastro:
                st.warning("Preencha e-mail e senha.")
            elif senha_cadastro != confirmar_senha:
                st.warning("As senhas não coincidem.")
            elif len(senha_cadastro) < 6:
                st.warning("A senha precisa ter pelo menos 6 caracteres.")
            else:
                try:
                    resposta = criar_conta(email_cadastro.strip(), senha_cadastro)

                    if resposta.session and resposta.user:
                        st.session_state.access_token = resposta.session.access_token
                        st.session_state.refresh_token = resposta.session.refresh_token
                        st.session_state.user_id = resposta.user.id
                        st.session_state.user_email = resposta.user.email
                        st.success("Conta criada com sucesso.")
                        st.rerun()
                    else:
                        st.success(
                            "Conta criada. Verifique seu e-mail para confirmar o cadastro e depois faça login."
                        )

                except Exception as erro:
                    st.error(f"Não foi possível criar a conta: {erro}")

    st.stop()


# =====================================================
# CONVERSA ATUAL
# =====================================================

conversation_id = st.query_params.get("conversation_id")


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">'
        '<span class="sidebar-brand-icon">📖</span>'
        '<span>Guia Devocional</span>'
        '</div>'
        '<div class="sidebar-subtitle">'
        'Assistente de Estudo Bíblico com IA'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(st.session_state.user_email or "Usuário conectado")

    if st.button("Sair", use_container_width=True):
        try:
            sair(
                st.session_state.access_token,
                st.session_state.refresh_token
            )
        except Exception:
            pass

        st.session_state.access_token = None
        st.session_state.refresh_token = None
        st.session_state.user_id = None
        st.session_state.user_email = None
        st.query_params.clear()
        st.rerun()

    st.divider()

    if st.button(
        "✦ Nova conversa",
        use_container_width=True
    ):
        st.query_params.clear()
        st.rerun()

    st.divider()

    st.subheader("Conversas")

    conversas = listar_conversas(
        st.session_state.user_id,
        st.session_state.access_token,
        st.session_state.refresh_token
    )

    if not conversas:
        st.caption("Nenhuma conversa salva ainda.")

    else:
        for conversa in conversas:

            titulo = conversa["title"] or "Conversa sem título"

            if st.button(
                titulo,
                key=f"conversa_{conversa['id']}",
                use_container_width=True
            ):
                st.query_params["conversation_id"] = conversa["id"]
                st.rerun()


# =====================================================
# CABEÇALHO PRINCIPAL
# =====================================================

if not conversation_id:

    st.markdown(
        '<div class="devocional-hero">'
        '<div class="devocional-title">'
        '<span class="devocional-title-icon">📖</span>'
        '<span>Olá! O que você gostaria de estudar hoje?</span>'
        '</div>'
        '<div class="devocional-subtitle-box">'
        'Seu assistente para estudo, contexto e reflexão bíblica.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

else:

    st.markdown(
        '<div class="devocional-hero">'
        '<div class="devocional-title">'
        '<span class="devocional-title-icon">📖</span>'
        '<span>Guia Devocional IA</span>'
        '</div>'
        '<div class="devocional-subtitle-box">'
        'Estude, compreenda e reflita sobre a Palavra.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


# =====================================================
# CARREGAR HISTÓRICO
# =====================================================

if conversation_id:
    historico = carregar_mensagens(
        conversation_id,
        st.session_state.user_id,
        st.session_state.access_token,
        st.session_state.refresh_token
    )
else:
    historico = []


# =====================================================
# MOSTRAR MENSAGENS
# =====================================================

for mensagem in historico:

    with st.chat_message(mensagem["role"]):
        st.write(mensagem["content"])


# =====================================================
# CAMPO DE PERGUNTA
# =====================================================

pergunta = st.chat_input(
    "Pergunte sobre um versículo, passagem ou tema bíblico..."
)


# =====================================================
# QUANDO O USUÁRIO ENVIA UMA PERGUNTA
# =====================================================

if pergunta:

    if not conversation_id:

        titulo = pergunta.strip()[:50]

        conversation_id = criar_conversa(
            titulo,
            st.session_state.user_id,
            st.session_state.access_token,
            st.session_state.refresh_token
        )

        st.query_params["conversation_id"] = conversation_id

    with st.chat_message("user"):
        st.write(pergunta)

    salvar_mensagem(
        conversation_id,
        "user",
        pergunta,
        st.session_state.access_token,
        st.session_state.refresh_token
    )

    instrucoes = """
    Você é o Guia Devocional, um assistente especializado
    em estudo bíblico e reflexão.

    Responda de maneira clara, respeitosa e acolhedora.

    Quando apropriado:
    - explique o contexto do texto bíblico;
    - apresente uma interpretação equilibrada;
    - sugira aplicações práticas;
    - diferencie interpretação do texto de aplicação pessoal.

    Não invente referências bíblicas.
    """

    mensagem = f"""
    {instrucoes}

    Pergunta do usuário:
    {pergunta}
    """

    try:

        with st.spinner("Preparando seu estudo..."):

            response = co.chat(
                model="command-a-03-2025",
                message=mensagem
            )

            resposta = response.text

    except Exception as erro:

        resposta = f"Erro ao consultar o modelo: {erro}"

    with st.chat_message("assistant"):
        st.write(resposta)

    salvar_mensagem(
        conversation_id,
        "assistant",
        resposta,
        st.session_state.access_token,
        st.session_state.refresh_token
    )

    st.rerun()


# =====================================================
# RODAPÉ / SOBRE O PROJETO
# Exibido somente na tela inicial
# =====================================================

if not conversation_id:
    st.markdown(
        '<div class="app-footer">'
        '<div class="footer-title">Sobre o projeto</div>'
        '<div class="footer-text">'
        'O Guia Devocional IA é um assistente desenvolvido para apoiar o estudo bíblico, '
        'oferecendo contexto, explicações e reflexões com inteligência artificial.<br>'
        'Desenvolvido com Python, Streamlit, Cohere e Supabase/PostgreSQL.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1.5, 1, 1.5])

    with col2:
        st.link_button(
            "in  LinkedIn",
            "https://www.linkedin.com/in/joice-marques-a556a12b0/",
            use_container_width=True
        )
