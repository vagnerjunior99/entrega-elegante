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

# --- NOVO VISUAL IMPERIAL: NOITE DE SÃO JOÃO 99 (GRAFITE, AMARELO E BANDEIRINHAS) ---
st.markdown("""
    <style>
    /* Fundo Escuro Temático (Noite de São João) */
    .stApp {
        background: linear-gradient(180deg, #121212 0%, #1A1A1A 100%) !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Força textos explicativos, labels e spans para Branco/Cinza Claro para dar leitura no fundo escuro */
    .stApp label, .stApp p, .stApp span, .stApp li {
        color: #E0E0E0 !important;
    }
    
    /* Estilização dos Inputs (Campos de Texto) - Branco com borda discreta */
    input, textarea {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 2px solid #333333 !important;
        border-radius: 8px !important;
    }
    input::placeholder, textarea::placeholder {
        color: #888888 !important;
    }
    
    /* Título Principal Estilizado com Linha Amarela e Emojis */
    h1 {
        color: #FFCC00 !important;
        font-weight: 900 !important;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
        margin-bottom: 5px !important;
        padding-top: 10px;
    }
    
    /* Divisor de Bandeirinhas Juninas */
    .divisor-bandeirinhas {
        text-align: center;
        font-size: 1.4rem;
        letter-spacing: 6px;
        margin-bottom: 25px;
        opacity: 0.9;
    }
    
    /* Container do Enunciado / Regras do Arraiá */
    .enunciado-container {
        background-color: #222222 !important;
        border: 2px dashed #FFCC00 !important;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 30px;
        box-shadow: 0px 6px 15px rgba(0,0,0,0.3);
    }
    .enunciado-titulo {
        color: #FFCC00 !important;
        font-weight: bold !important;
        font-size: 1.25rem !important;
        margin-bottom: 12px;
    }
    
    /* Abas Estilizadas (Padrão de App Moderno) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #222222 !important;
        padding: 10px;
        border-radius: 12px;
        box-shadow: inset 0px 2px 5px rgba(0,0,0,0.5);
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 8px;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"] p {
        color: #AAAAAA !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFCC00 !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #1A1A1A !important;
        font-weight: bold !important;
    }

    /* Botões Oficiais 99 (Preto Intenso com borda e texto Amarelo Vibrante) */
    button[data-testid="stBaseButton-secondaryFormSubmit"], 
    button[data-testid="stBaseButton-secondary"],
    .stButton > button {
        background-color: #000000 !important;
        border: 2px solid #FFCC00 !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        box-shadow: 0px 5px 12px rgba(0, 0, 0, 0.4) !important;
        width: 100% !important;
        transition: all 0.2s ease-in-out !important;
    }
    button[data-testid="stBaseButton-secondaryFormSubmit"] p,
    button[data-testid="stBaseButton-secondary"] p,
    .stButton > button p {
        color: #FFCC00 !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
    }
    button[data-testid="stBaseButton-secondaryFormSubmit"]:hover,
    button[data-testid="stBaseButton-secondary"]:hover,
    .stButton > button:hover {
        background-color: #FFCC00 !important;
        border-color: #FFFFFF !important;
        transform: translateY(-2px);
    }
    button[data-testid="stBaseButton-secondaryFormSubmit"]:hover p,
    button[data-testid="stBaseButton-secondary"]:hover p,
    .stButton > button:hover p {
        color: #000000 !important;
    }
    
    /* Cards do Mural Estilizados como Balões Juninos Flutuantes */
    .delivery-card {
        background-color: #FFFFFF !important;
        border-left: 8px solid #FFCC00 !important;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.4);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .delivery-card:hover {
        transform: scale(1.01);
    }
    .delivery-header {
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        color: #1A1A1A !important;
        margin-bottom: 12px;
    }
    .delivery-text {
        font-size: 1.05rem !important;
        font-style: italic !important;
        color: #2D2D2D !important;
        background-color: #F3F4F6 !important;
        padding: 14px;
        border-radius: 10px;
        border-left: 3px solid #E5E7EB;
        margin-bottom: 15px;
    }
    
    /* Ajustes extras para sub-títulos no modo escuro */
    h3 {
        color: #FFCC00 !important;
        font-weight: 700 !important;
        margin-top: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializa o banco de dados de maneira segura
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

# Título Principal e Varal de Bandeirinhas
st.markdown("<h1>🔥 ARRAIÁ 99Food</h1>", unsafe_allow_html=True)
st.markdown('<div class="divisor-bandeirinhas">🎏🍿🌽🔥🌽🍿🎏</div>', unsafe_allow_html=True)

# --- BLOCO DE ENUNCIADO ---
st.markdown("""
<div class="enunciado-container">
    <div class="enunciado-titulo">🍿 🎏 Olha a Entrega Elegante! É verdade!</div>
    <p style="margin-bottom: 8px;">O São João chegou na 99Food! Para celebrar, misturamos a tradição do <strong>Correio Elegante Junino</strong> com a identidade da <strong>99</strong> em um ambiente de reconhecimento corporativo. Veja como participar:</p>
    <ul style="margin-top: 0; padding-left: 20px;">
        <li><strong>Enviar um Recadinho:</strong> Na aba <em>"Enviar Mensagem"</em>, coloque o nome do colega e conte um momento em que essa pessoa foi parceira e "salvou o seu dia". O envio é anônimo!</li>
        <li><strong>Adivinhar no Mural:</strong> Na aba <em>"Mural de Entregas"</em>, ficam expostos os recados. Se achar um para você, tente adivinhar quem mandou. <strong>Cuidado:</strong> você só tem <u>uma única chance</u>!</li>
        <li>⚠️ <strong>Regra do Arraiá:</strong> O mural é exclusivo para quem espalhou carinho. Você só verá as mensagens após enviar pelo menos uma entrega elegante nesta sessão.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Criação das Abas
aba_enviar, aba_mural = st.tabs(["💌 Enviar Mensagem", "📌 Mural de Entregas"])

# --- ABA 1: ENVIAR MENSAGEM ---
with aba_enviar:
    st.markdown("<h3>Prepare seu pedido de agradecimento! 💛</h3>", unsafe_allow_html=True)
    
    with st.form(key="form_correio", clear_on_submit=True):
        remetente = st.text_input("Seu Nome (Ficará escondido no mural para o jogo de adivinhação):").strip()
        destinatario = st.text_input("Para quem é a mensagem? (Nome do Colega):").strip()
        
        st.markdown("<p style='font-weight: bold; margin-bottom: 2px; color:#FFCC00 !important;'>Complete a frase com uma lembrança:</p>", unsafe_allow_html=True)
        texto_base = "Você não é um cupom do 99Food, mas quero te dizer/lembrar que..."
        
        exemplo_emotivo = "Ex: você me deu a maior força quando aquele projeto deu errado. Obrigado por ser essa parceira incrível!"
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
                    "mensagem": message_completa if 'message_completa' in locals() else mensagem_completa,
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
    st.markdown("<h3>👀 Quem recebeu uma entrega hoje?</h3>", unsafe_allow_html=True)
    
    if not st.session_state.ja_enviou:
        st.warning("🔒 Ei, sô! Para conseguir ver o Mural e brincar de adivinhar, você precisa enviar um recadinho primeiro. Vá na aba 'Enviar Mensagem' e colabore com o time!")
    else:
        if len(st.session_state.mensagens) == 0:
            st.info("Nenhuma entrega feita ainda. Seja o primeiro!")
        else:
            for msg in reversed(st.session_state.mensagens):
                orig_id = msg["id"]
                
                card_html = f"""
                <div class="delivery-card">
                    <div class="delivery-header">💛 Para: {msg['destinatario']}</div>
                    <div class="delivery-text">"{msg['mensagem']}"</div>
                    <div style="font-size: 0.8rem; color: #777;">Status: Entregue com sucesso • {msg['data']}</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Se nenhum palpite foi feito, exibe o form de chute
                if not msg["palpite_feito"]:
                    with st.form(key=f"form_palpite_{orig_id}"):
                        st.markdown("<p style='font-weight: bold; margin-bottom: 2px; color: #FFCC00 !important;'>🕵️ Adivinhe quem te mandou esse recado:</p>", unsafe_allow_html=True)
                        
                        identificacao = st.text_input("Seu Nome (Quem está adivinhando):", key=f"id_{orig_id}", placeholder="Digite seu nome para validar...").strip()
                        chute = st.text_input("Quem você acha que enviou?", key=f"chute_{orig_id}", placeholder="Nome do colega do chute...").strip()
                        
                        botao_palpite = st.form_submit_button("Confirmar Palpite (Apenas 1 chance!) 🔒")
                        
                        if botao_palpite:
                            if identificacao and chute:
                                id_limpo = normalizar_nome(identificacao)
                                dest_limpo = normalizar_nome(msg["destinatario"])
                                
                                if id_limpo in dest_limpo or dest_limpo in id_limpo:
                                    remetente_limpo = normalizar_nome(msg["remetente"])
                                    chute_limpo = normalizar_nome(chute)
                                    
                                    acertou_palpite = chute_limpo in remetente_limpo or remetente_limpo in chute_limpo
                                    
                                    for m in st.session_state.mensagens:
                                        if m["id"] == orig_id:
                                            m["quem_palpitou"] = identificacao
                                            m["palpite"] = chute
                                            m["palpite_feito"] = True
                                            m["acertou"] = acertou_palpite
                                    st.rerun()
                                else:
                                    st.warning(f"✋ Ei, sô! Esse recado foi enviado para o(a) {msg['destinatario']}. Mas não tem problema, alguém ainda pode ter te enviado algum recadinho. 😊")
                            else:
                                st.warning("Preencha o seu nome E o nome do seu chute antes de confirmar.")
                # Se o palpite já foi feito, some com o form e mostra o resultado
                else:
                    if msg["acertou"]:
                        st.success(f"🎉 **{msg['quem_palpitou']}, você acertou em cheio!** Foi o(a) **{msg['remetente']}** que te enviou esse recado especial!")
                    else:
                        st.error(f"❌ **Não foi dessa vez, {msg['quem_palpitou']}!** Você chutou '{msg['palpite']}', mas quem assinou esse recado especial na verdade foi o(a) **{msg['remetente']}**!")
                
                st.markdown("<br>", unsafe_allow_html=True)

# --- ÁREA DO ADMINISTRADOR ---
query_params = st.query_params
if query_params.get("adm") == "true":
    st.markdown("---")
    st.markdown("### 🛠️ Área do Administrador (Modo Secreto Ativo)")
    
    senha_adm = st.text_input("Insira a chave master para acessar o banco de dados:", type="password")
    
    if senha_adm == "99food2026":
        st.success("Autenticação efetuada com sucesso!")
        
        if st.button("🧹 Zerar Banco de Dados e Manter Apenas Teste"):
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
            st.success("Mural resetado com sucesso!")
            st.rerun()
        
        if len(st.session_state.mensagens) > 0:
            df = pd.DataFrame(st.session_state.mensagens)
            df['Acertou?'] = df['acertou'].apply(lambda x: "Sim" if x else "Não")
            
            df_relatorio = df[["data", "destinatario", "mensagem", "remetente", "quem_palpitou", "palpite", "Acertou?"]]
            df_relatorio.columns = ["Data/Hora", "Quem Recebeu", "Mensagem", "Remetente Real (Anônimo)", "Quem Deu o Palpite", "Palpite Feito (Chute)", "Acertou o Palpite?"]
            
            st.dataframe(df_relatorio)
            
            csv = df_relatorio.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Baixar Planilha de Acertos (Excel/CSV)",
                data=csv,
                file_name="relatorio_final_entrega_elegante.csv",
                mime="text/csv"
            )
    elif senha_adm != "":
        st.error("Chave inválida. Tentativa registrada.")
