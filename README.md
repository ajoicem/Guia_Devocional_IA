# 📖 Guia Devocional IA

> Assistente inteligente para estudo, compreensão e reflexão bíblica.

O **Guia Devocional IA** é uma aplicação desenvolvida com inteligência artificial para auxiliar no estudo de versículos, passagens e temas bíblicos de forma clara, organizada e acessível.

O projeto combina **IA generativa, interface web e banco de dados**, permitindo que o usuário faça perguntas, receba explicações e mantenha um histórico persistente de conversas.

---

## ✨ Sobre o projeto

O objetivo do Guia Devocional IA é oferecer uma experiência de estudo bíblico assistida por inteligência artificial.

A aplicação foi desenvolvida para:

- explicar passagens bíblicas;
- apresentar contexto dos textos;
- auxiliar na compreensão de temas bíblicos;
- sugerir reflexões e aplicações práticas;
- armazenar conversas anteriores;
- permitir a continuidade dos estudos ao longo do tempo.

A proposta é unir tecnologia e organização de conteúdo em uma interface simples e intuitiva.

---

## 🖥️ Interface

A aplicação possui uma interface desenvolvida em **Streamlit**, com:

- menu lateral;
- criação de novas conversas;
- histórico de estudos;
- chat interativo;
- persistência das mensagens;
- integração com inteligência artificial.

---

## 🤖 Inteligência Artificial

O projeto utiliza a **API da Cohere** para gerar as respostas do assistente.

O modelo é orientado por instruções específicas para atuar como um assistente de estudo bíblico, buscando responder de maneira:

- clara;
- respeitosa;
- contextualizada;
- equilibrada;
- voltada para estudo e reflexão.

---

## 🗄️ Banco de dados

O armazenamento das conversas é realizado através do **Supabase**, utilizando **PostgreSQL**.

Atualmente, o banco armazena informações relacionadas a:

### Conversas

Cada conversa possui informações como:

- identificador;
- título;
- data de criação.

### Mensagens

As mensagens armazenam:

- conversa relacionada;
- tipo de usuário;
- conteúdo da mensagem;
- data de criação.

Isso permite que o histórico permaneça disponível mesmo após atualizar ou fechar a aplicação.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Utilização |
|---|---|
| Python | Linguagem principal |
| Streamlit | Interface web |
| Cohere | Inteligência artificial generativa |
| Supabase | Backend e persistência |
| PostgreSQL | Banco de dados |
| GitHub | Versionamento e hospedagem do código |

---

## 📂 Estrutura do projeto

```text
guia-devocional-ia/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
