import streamlit as st
import pandas as pd
from datetime import datetime
import unicodedata

# Configuração da página
st.set_page_config(page_title="Entrega Elegante 99Food", page_icon="🌽", layout="centered")

# --- FUNÇÃO AUXILIAR PARA NORMALIZAR NOMES ---
def normalizar_nome(texto):
    if not texto:
        return ""
    texto = str(texto).lower().strip()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto

# --- VISUAL: ARRAIÁ 99 CONSOLIDADO (AMARELO, PRETO E CENTRALIZAÇÃO) ---
st.markdown("""
    <style>
    /* Fundo Amarelo Vibrante Oficial da 99 */
    .stApp {
        background: #FFCC00 !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Textos gerais em preto */
    .stApp label, .stApp p, .stApp span, .stApp li {
        color: #1A1A1A !important;
    }
    
    /* Inputs Brancos para leitura */
    input, textarea {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 2px solid #1A1A1A !important;
        border-radius: 8px !important;
    }
    
    /* --- CABEÇALHO PRETO UNIFICADO --- */
    .header-box {
        background-color: #1A1A1A !important;
        border: 2px solid #FFFFFF;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.3);
        margin-bottom: 30px;
    }
    .header-box h1 {
        color: #FFCC00 !important;
        font-weight: 900 !important;
        margin: 0 !important;
        font-size: 2.3rem !important;
    }
    .header-box .divisor-bandeirinhas {
        font-size: 1.5rem;
        letter-spacing: 8px;
        margin-top: 10px;
    }
    
    /* --- CENTRALIZAÇÃO E TAMANHO DAS ABAS --- */
    .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        justify-content: center !important; /* Centraliza as abas */
        gap: 20px !important;
        background-color: #1A1A1A !important;
        padding: 12px !important;
        border-radius: 15px !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px !important; /* Deixa a aba mais alta */
        padding-left: 30px !important;
        padding-right: 30px !important;
        border-radius: 10px !important;
    }
    .stTabs [data-baseweb="tab"] p {
        font-size: 1.1rem !important;
        font-weight: bold !important;
        color: #FFFFFF !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFCC00 !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #1A1A1A !important;
    }

    /* --- BOTÃO DE ENVIO CENTRALIZADO E LARGO --- */
    div[data-testid="stFormSubmitButton"] {
        text-align: center !important;
        display: flex;
        justify-content: center;
    }
    
    button[data-testid="stBaseButton-secondaryFormSubmit"], 
    button[data-testid="stBaseButton-secondary"],
    .stButton > button {
        background-color: #1A1A1A !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 12px !important;
        padding: 12px 60px !important; /* Aumenta a largura horizontal */
        box-shadow: 0px 5px 15px rgba(0,0,0,0.2) !important;
        width: auto !important; /* Impede que o botão estique 100% sem controle */
        min-width: 280px !important;
        transition: all 0.2s ease !important;
    }
    button[data-testid="stBaseButton-secondaryFormSubmit"] p,
    .stButton > button p {
        color: #FFCC00 !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }
    button[data-testid="stBaseButton-secondaryFormSubmit"]:hover,
    .stButton > button:hover {
        border-color: #FFCC00 !important;
        transform: translateY(-2px);
    }
    
    /* Container do Enunciado */
    .enunciado-container {
        background-color: #FFFFFF !important;
        border: 2px dashed #1A1A1A !important;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 30px;
    }
    
    /* Cards do Mural em Preto */
    .delivery-card {
        background-color: #1A1A1A !important;
        border-left: 8px solid #FFFFFF !important;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .delivery-card .delivery-header {
        font-weight: 800;
        color: #FFCC00 !important;
        margin-bottom: 10px;
    }
    .delivery-card .delivery-text {
        color: #FFFFFF !important;
        background-color: #2D2D2D !important;
        padding: 14px;
        border-radius: 10px;
        border-left: 3px solid #FFCC00;
    }
    
    /* Força centralização dos títulos internos das abas */
    .centered-title {
        text-align: center !important;
        color: #1A1A1A !important;
        font-weight: 800 !important;
        margin-bottom: 20px !important;
        font-size: 1.5rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inicialização segura
if 'mensagens' not in st.session_state:
    st.session_state.mensagens = [
        {
            "id": 0, "remetente": "Carlos", "destinatario": "Mariana (TI)",
            "mensagem": "Você não é um cupom do 99Food, mas quero te dizer/lembrar que... você salvou o meu dia quando resolveu o problema do meu acesso logo cedo!",
            "data": "15/06/2026", "quem_palpitou": "", "palpite": "", "palpite_feito": False, "acertou": False
        }
    ]
if 'ja_enviou' not in st.session_state:
    st.session_state.ja_enviou = False

# --- CABEÇALHO ---
st.markdown("""
<div class="header-box">
    <img src="https://99app.com/_next/image/?url=https%3A%2F%2Fimages.ctfassets.net%2Fx9sul3ikm35w%2F2kYcs2M15uM3cYchuoDRvG%2Ffd6069a06d44476d143559243510a929%2Fimage.png&w=384&q=75" width="95">
    <h1>🔥 ARRAIÁ 99Food</h1>
    <div class="divisor-bandeirinhas">🎏🍿🌽🔥🌽🍿🎏</div>
</div>
""", unsafe_allow_html=True)

# --- REGRAS ---
st.markdown("""
<div class="enunciado-container">
    <div style="font-weight:bold; font-size:1.2rem;">🍿 🎏 Olha a Entrega Elegante! É verdade!</div>
    <p>O São João chegou na 99Food! Envie mensagens anônimas de reconhecimento e tente adivinhar quem te enviou um recado. <strong>Regra:</strong> Você só vê o mural após enviar uma mensagem!</p>
</div>
""", unsafe_allow_html=True)

aba_enviar, aba_mural = st.tabs(["💌 Enviar Mensagem", "📌 Mural de Entregas"])

# --- ABA 1: ENVIAR ---
with aba_enviar:
    st.markdown('<div class="centered-title">Prepare seu pedido de agradecimento! 💌</div>', unsafe_allow_html=True)
    
    with st.form(key="form_correio", clear_on_submit=True):
        remetente = st.text_input("Seu Nome (Ficará escondido):").strip()
        destinatario = st.text_input("Para quem é a mensagem? (Nome do Colega):").strip()
        
        texto_base = "Você não é um cupom do 99Food, mas quero te dizer/lembrar que..."
        lembranca = st.text_area(texto_base, placeholder="Ex: você me ajudou muito no projeto X...")
        
        st.form_submit_button("Enviar Entrega Elegante 🚀")
        
        if st.session_state.get('form_correio'): # Simulação do clique
            pass # Lógica abaixo

    # Verificação de envio fora do form para evitar bugs de Rerun
    if st.button("Clique aqui para confirmar o envio acima 🚀", key="trigger_envio", help="Finalize o envio da sua mensagem"):
        if remetente and destinatario and lembranca:
            nova_msg = {
                "id": len(st.session_state.mensagens),
                "remetente": remetente, "destinatario": destinatario,
                "mensagem": f"{texto_base} {lembranca}",
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "quem_palpitou": "", "palpite": "", "palpite_feito": False, "acertou": False
            }
            st.session_state.mensagens.append(nova_msg)
            st.session_state.ja_enviou = True
            st.success("Mensagem enviada! Mural liberado. 🛵💨")
            st.rerun()

# --- ABA 2: MURAL ---
with aba_mural:
    st.markdown('<div class="centered-title">👀 Quem recebeu uma entrega hoje?</div>', unsafe_allow_html=True)
    
    if not st.session_state.ja_enviou:
        st.warning("🔒 Envie uma mensagem primeiro para liberar o mural!")
    else:
        for msg in reversed(st.session_state.mensagens):
            st.markdown(f"""
            <div class="delivery-card">
                <div class="delivery-header">💛 Para: {msg['destinatario']}</div>
                <div class="delivery-text">"{msg['mensagem']}"</div>
                <div style="font-size: 0.8rem; color: #777; margin-top:10px;">Entregue em {msg['data']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if not msg["palpite_feito"]:
                with st.form(key=f"palpite_{msg['id']}"):
                    ident = st.text_input("Seu Nome:", key=f"id_{msg['id']}").strip()
                    chute = st.text_input("Quem mandou?", key=f"ch_{msg['id']}").strip()
                    if st.form_submit_button("Confirmar Palpite 🔒"):
                        if normalizar_nome(ident) in normalizar_nome(msg['destinatario']):
                            msg["palpite_feito"] = True
                            msg["quem_palpitou"] = ident
                            msg["palpite"] = chute
                            msg["acertou"] = normalizar_nome(chute) in normalizar_nome(msg['remetente'])
                            st.rerun()
                        else:
                            st.error("Ei! Esse recado não é para você. 😉")
            else:
                if msg["acertou"]:
                    st.success(f"🎉 Acertou! Foi o(a) {msg['remetente']}!")
                else:
                    st.error(f"❌ Não foi dessa vez! Quem assinou foi o(a) {msg['remetente']}!")

# --- ADM ---
if st.query_params.get("adm") == "true":
    st.markdown("---")
    if st.text_input("Senha Master:", type="password") == "99food2026":
        st.dataframe(pd.DataFrame(st.session_state.mensagens))
        if st.button("Limpar Banco"):
            st.session_state.mensagens = []; st.rerun()
