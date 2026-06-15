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

# --- VISUAL: ARRAIÁ 99 CONSOLIDADO ---
st.markdown("""
    <style>
    /* Fundo Amarelo Oficial da 99 */
    .stApp {
        background: #FFCC00 !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Textos gerais em preto */
    .stApp label, .stApp p, .stApp span, .stApp li {
        color: #1A1A1A !important;
    }
    
    /* Inputs Brancos para leitura perfeita */
    input, textarea {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 2px solid #1A1A1A !important;
        border-radius: 8px !important;
    }
    input::placeholder, textarea::placeholder {
        color: #777777 !important;
    }
    
    /* --- CABEÇALHO PRETO LIMPO (SEM BORDA E SEM SOMBRA) --- */
    .header-box {
        background-color: #1A1A1A !important;
        border: none !important;
        border-radius: 20px;
        padding: 35px 20px;
        text-align: center;
        box-shadow: none !important;
        margin-bottom: 30px;
    }
    
    /* CORREÇÃO DA FONTE E TAMANHO DO TÍTULO INTERNO */
    .header-title {
        color: #FFCC00 !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
        font-weight: 900 !important;
        font-size: 2.5rem !important; /* Aumentado para dar destaque */
        margin-top: 20px !important;
        margin-bottom: 12px !important;
        letter-spacing: -0.5px;
    }
    
    /* Estilização do Divisor de Bandeirinhas Interno */
    .header-divisor {
        font-size: 1.5rem;
        letter-spacing: 8px;
        color: #FFFFFF !important;
        margin-top: 5px;
    }
    
    /* --- CONFIGURAÇÃO DAS ABAS (CENTRALIZADAS E MAIORES) --- */
    .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        justify-content: center !important;
        gap: 15px !important;
        background-color: #1A1A1A !important;
        padding: 10px !important;
        border-radius: 12px !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px !important;
        padding-left: 25px !important;
        padding-right: 25px !important;
        border-radius: 8px !important;
    }
    .stTabs [data-baseweb="tab"] p {
        font-size: 1.05rem !important;
        font-weight: bold !important;
        color: #FFFFFF !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFCC00 !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #1A1A1A !important;
    }

    /* --- ESTILIZAÇÃO DO BOTÃO DE ENVIO (CENTRALIZADO E SEM BORDA) --- */
    div[data-testid="stFormSubmitButton"] {
        text-align: center !important;
        display: flex;
        justify-content: center;
        margin-top: 15px;
    }
    button[data-testid="stBaseButton-secondaryFormSubmit"], 
    button[data-testid="stBaseButton-secondary"],
    .stButton > button {
        background-color: #1A1A1A !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 60px !important;
        min-width: 280px !important;
        width: auto !important;
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
        opacity: 0.95;
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
    
    /* --- CAIXA DE ALERTA DO MURAL BLOQUEADO --- */
    .mural-bloqueado-box {
        background-color: #1A1A1A !important;
        border: 2px dashed #FFFFFF !important;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-top: 10px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
    }
    .mural-bloqueado-box p {
        color: #FFFFFF !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        margin: 0 !important;
    }
    
    /* Cards do Mural em Preto */
    .delivery-card {
        background-color: #1A1A1A !important;
        border-left: 8px solid #FFFFFF !important;
        border-radius: 16px;
        padding: 24px;
        margin-top: 15px !important;
        margin-bottom: 25px !important;
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
    
    /* --- RETÂNGULO BRANCO PARA RESULTADO DE PALPITES E ADVERTÊNCIAS --- */
    .resultado-palpite-box {
        background-color: #FFFFFF !important;
        border: 2px solid #1A1A1A !important;
        border-radius: 12px;
        padding: 18px;
        margin-top: 20px !important;
        margin-bottom: 35px !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        display: block !important;
    }
    .resultado-palpite-box p {
        color: #1A1A1A !important;
        margin: 0 !important;
        font-size: 1.05rem !important;
    }
    
    .centered-title {
        text-align: center !important;
        color: #1A1A1A !important;
        font-weight: 800 !important;
        margin-bottom: 25px !important;
        font-size: 1.4rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inicialização do Banco de Dados
if 'mensagens' not in st.session_state:
    st.session_state.mensagens = [
        {
            "id": 0,
            "remetente": "Carlos",
            "destinatario": "Mariana (TI)",
            "mensagem": "Você não é um cupom do 99Food, mas quero te dizer/lembrar que... você salvou o meu dia quando resolveu o problema do meu acesso logo cedo!",
            "data": "15/06/2026",
            "quem_palpitou": "",
            "palpite": "",
            "palpite_feito": False,
            "acertou": False
        }
    ]
if 'ja_enviou' not in st.session_state:
    st.session_state.ja_enviou = False

# --- CABEÇALHO UNIFICADO COMPLETO EM HTML PURO ---
st.markdown("""
<div class="header-box">
    <img src="https://99app.com/_next/image/?url=https%3A%2F%2Fimages.ctfassets.net%2Fx9sul3ikm35w%2F2kYcs2M15uM3cYchuoDRvG%2Ffd6069a06d44476d143559243510a929%2Fimage.png&w=384&q=75" width="95" style="display: block; margin: 0 auto;">
    <div class="header-title">🔥 ARRAIÁ 99Food</div>
    <div class="header-divisor">🎏🍿🌽🔥🌽🍿🎏</div>
</div>
""", unsafe_allow_html=True)

# --- REGRAS COMPLETAS ---
st.markdown("""
<div class="enunciado-container">
    <div style="font-weight:bold; font-size:1.25rem; color: #1A1A1A; margin-bottom: 12px;">🍿 🎏 Olha a Entrega Elegante! É verdade!</div>
    <p style="margin-bottom: 8px;">O São João chegou na 99Food! Para celebrar, misturamos a tradição do <strong>Correio Elegante Junino</strong> com a agilidade da <strong>99Food</strong> em um arraiá de reconhecimento corporativo. Veja como participar:</p>
    <ul style="margin-top: 0; padding-left: 20px;">
        <li style="margin-bottom: 4px;"><strong>Enviar um Recadinho:</strong> Pule para a aba <em>"Enviar Mensagem"</em>, coloque o nome do colega e complete a frase lembrando de um momento em que essa pessoa foi uma verdadeira parceira e "salvou o seu dia" na empresa. O envio é 100% anônimo!</li>
        <li style="margin-bottom: 4px;"><strong>Adivinhar no Mural:</strong> Na aba <em>"Mural de Entregas"</em>, ficam expostos os balões e mensagens do nosso time. Se achar um recado para você, clareie a mente e tente adivinhar o remetente. <strong>Cuidado:</strong> você só tem <u>uma única chance</u> para dar o seu palpite!</li>
        <li>⚠️ <strong>Regra do Arraiá:</strong> O mural de entregas é exclusive para quem também espalhou carinho! Você só conseguirá visualizar os recados e dar seus palpites após enviar pelo menos uma mensagem para um colega nesta sessão.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

aba_enviar, aba_mural = st.tabs(["💌 Enviar Mensagem", "📌 Mural de Entregas"])

# --- ABA 1: ENVIAR MENSAGEM ---
with aba_enviar:
    st.markdown('<div class="centered-title">Prepare seu pedido de agradecimento! 💌</div>', unsafe_allow_html=True)
    
    with st.form(key="form_correio", clear_on_submit=True):
        remetente = st.text_input("Seu Nome (Ficará escondido no mural para o jogo de adivinhação):").strip()
        destinatario = st.text_input("Para quem é a mensagem? (Nome do Colega):").strip()
        
        st.markdown("<p style='font-weight: bold; margin-bottom: 2px; color:#1A1A1A !important;'>Complete a frase com uma lembrança:</p>", unsafe_allow_html=True)
        texto_base = "Você não é um cupom do 99Food, mas quero te dizer/lembrar que..."
        
        exemplo_emotivo = "Ex: você me deu a maior força quando aquele projeto deu errado e não me deixou desistir. Obrigado por ser essa liderança/parceira incrível, você salva meu dia sempre!"
        lembranca = st.text_area(texto_base, placeholder=exemplo_emotivo)
        
        botao_enviar = st.form_submit_button("Enviar Entrega Elegante 🚀")
        
        if botao_enviar:
            if remetente and destinatario and lembranca:
                mensagem_completa = f"{texto_base} {lembranca}"
                novo_id = len(st.session_state.mensagens)
                nova_msg = {
                    "id": novo_id,
                    "remetente": remetente,
                    "destinatario": destinatario,
                    "mensagem": mensagem_completa,
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "quem_palpitou": "",
                    "palpite": "",
                    "palpite_feito": False,
                    "acertou": False
                }
                st.session_state.mensagens.append(nova_msg)
                st.session_state.ja_enviou = True
                st.success("Mensagem enviada para a cozinha! Seu acesso ao mural foi liberado. 🛵💨")
                st.rerun()
            else:
                st.error("Por favor, preencha todos os campos antes de enviar.")

# --- ABA 2: MURAL DE ENTREGAS ---
with aba_mural:
    st.markdown('<div class="centered-title">👀 Quem recebeu uma entrega hoje?</div>', unsafe_allow_html=True)
    
    if not st.session_state.ja_enviou:
        st.markdown("""
        <div class="mural-bloqueado-box">
            <p>🔒 Ei, sô! Para conseguir ver o Mural e brincar de adivinhar, você precisa enviar um recadinho primeiro. Vá na aba 'Enviar Mensagem' e colabore com o time!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        if len(st.session_state.mensagens) == 0:
            st.info("Nenhuma entrega feita ainda. Seja o primeiro!")
        else:
            for msg in reversed(st.session_state.mensagens):
                orig_id = msg["id"]
                
                st.markdown(f"""
                <div class="delivery-card">
                    <div class="delivery-header">💛 Para: {msg['destinatario']}</div>
                    <div class="delivery-text">"{msg['mensagem']}"</div>
                    <div style="font-size: 0.8rem; color: #999; margin-top:10px;">Status: Entregue com sucesso • {msg['data']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Se o palpite NÃO foi feito, exibe o formulário de chute
                if not msg["palpite_feito"]:
                    with st.form(key=f"form_palpite_{orig_id}"):
                        st.markdown("<p style='font-weight: bold; color: #1A1A1A !important;'>🕵️ Adivinhe quem te mandou esse recado:</p>", unsafe_allow_html=True)
                        identificacao = st.text_input("Seu Nome (Quem está adivinhando):", key=f"id_{orig_id}", placeholder="Digite seu nome para validar...").strip()
                        chute = st.text_input("Quem você acha que enviou?", key=f"chute_{orig_id}", placeholder="Nome do colega do chute...").strip()
                        
                        botao_palpite = st.form_submit_button("Confirmar Palpite (Apenas 1 chance!) 🔒")
                        
                        if botao_palpite:
                            if identificacao and chute:
                                if normalizar_nome(identificacao) in normalizar_nome(msg["destinatario"]):
                                    msg["palpite_feito"] = True
                                    msg["quem_palpitou"] = identificacao
                                    msg["palpite"] = chute
                                    msg["acertou"] = normalizar_nome(chute) in normalizar_nome(msg["remetente"])
                                    st.rerun()
                                else:
                                    st.markdown(f"""
                                    <div class="resultado-palpite-box" style="border-left: 6px solid #FF9900 !important;">
                                        <p>✋ <b>Ei, sô!</b> Esse recado foi enviado para o(a) {msg['destinatario']}. Mas não tem problema, alguém ainda pode ter te enviado algum recadinho. 😊</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.warning("Preencha o seu nome E o nome do seu chute antes de confirmar.")
                
                # SE O PALPITE JÁ FOI FEITO
                else:
                    if msg["acertou"]:
                        st.markdown(f"""
                        <div class="resultado-palpite-box" style="border-left: 6px solid #28a745 !important;">
                            <p>🎉 <b>{msg['quem_palpitou']}, você acertou em cheio!</b> Foi o(a) <b>{msg['remetente']}</b> que te enviou esse recado especial!</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="resultado-palpite-box" style="border-left: 6px solid #dc3545 !important;">
                            <p>❌ <b>Não foi dessa vez, {msg['quem_palpitou']}!</b> Você chutou '{msg['palpite']}', mas quem assinou esse recado especial na verdade foi o(a) <b>{msg['remetente']}</b>!</p>
                        </div>
                        """, unsafe_allow_html=True)

# --- ÁREA DO ADMINISTRADOR ---
if st.query_params.get("adm") == "true":
    st.markdown("---")
    if st.text_input("Senha Master:", type="password") == "99food2026":
        st.dataframe(pd.DataFrame(st.session_state.mensagens))
        if st.button("Limpar Banco"):
            st.session_state.mensagens = []
            st.rerun()
