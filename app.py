import streamlit as st
import pandas as pd
from datetime import datetime
import unicodedata

# Configuração da página
st.set_page_config(page_title="Entrega Elegante 99Food", page_icon="🌽", layout="centered")

# --- FUNÇÃO AUXILIAR PARA NORMALIZAR NOMES (IGNORA MAIÚSCULAS, MINÚSCULAS E ACENTOS) ---
def normalizar_nome(texto):
    if not texto:
        return ""
    # Transforma em minúsculas e remove espaços inúteis nas pontas
    texto = str(texto).lower().strip()
    # Remove acentos (Ex: "Mariana (TI)" ou "Mariana" viram "mariana")
    # Nota: Vamos extrair apenas as primeiras letras/palavras para facilitar a checagem se o nome bate
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto

# --- INJEÇÃO DE IDENTIDADE VISUAL BLINDADA (BOTOES PRETOS + LETRAS AMARELAS) ---
st.markdown("""
    <style>
    /* Cor de fundo geral da página */
    .stApp {
        background-color: #F8F9FA !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Força a cor preta em textos de labels, parágrafos e listas */
    .stApp label, .stApp p, .stApp span, .stApp li {
        color: #1A1A1A !important;
    }
    
    /* Ajusta os campos de entrada de texto */
    input, textarea {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 1px solid #CCCCCC !important;
    }
    
    /* Garante visibilidade do placeholder */
    input::placeholder, textarea::placeholder {
        color: #888888 !important;
    }
    
    /* Customização do Título Principal */
    h1 {
        color: #1A1A1A !important;
        font-weight: 800 !important;
        text-align: center;
        border-bottom: 4px solid #FFCC00;
        padding-bottom: 15px;
        margin-bottom: 10px !important;
    }
    
    /* Bloco do Enunciado / Regras do Arraiá */
    .enunciado-container {
        background-color: #FFFFFF !important;
        border: 2px dashed #FFCC00 !important;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 30px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.02);
    }
    .enunciado-titulo {
        color: #E6B800 !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        margin-bottom: 10px;
    }
    
    /* Abas estilizadas no padrão da marca */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #1A1A1A !important;
        padding: 8px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stTabs [data-baseweb="tab"] p {
        color: #FFFFFF !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFCC00 !important;
    }
    .stTabs [aria-selected="true"] p {
        color: #1A1A1A !important;
    }

    /* --- ALVO GLOBAL EM TODOS OS BOTÕES DA PÁGINA --- */
    button[data-testid="stBaseButton-secondaryFormSubmit"], 
    button[data-testid="stBaseButton-secondary"],
    .stButton > button {
        background-color: #1A1A1A !important;
        border: 2px solid #FFCC00 !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.15) !important;
        width: 100% !important;
    }
    
    /* Força a cor amarela no texto interno de QUALQUER botão */
    button[data-testid="stBaseButton-secondaryFormSubmit"] p,
    button[data-testid="stBaseButton-secondary"] p,
    .stButton > button p {
        color: #FFCC00 !important;
        font-weight: bold !important;
    }
    
    /* Efeito Hover global */
    button[data-testid="stBaseButton-secondaryFormSubmit"]:hover,
    button[data-testid="stBaseButton-secondary"]:hover,
    .stButton > button:hover {
        background-color: #262626 !important;
        border-color: #E6B800 !important;
    }
    
    /* Caixa de Mensagem / Card do Mural */
    .delivery-card {
        background-color: #FFFFFF !important;
        border-left: 8px solid #FFCC00 !important;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .delivery-header {
        font-size: 1.1rem !important;
        font-weight: bold !important;
        color: #1A1A1A !important;
        margin-bottom: 10px;
    }
    .delivery-text {
        font-size: 1rem !important;
        font-style: italic !important;
        color: #4A4A4A !important;
        background-color: #F8F9FA !important;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializa as variáveis da sessão e limpa os dados antigos, deixando apenas o modelo inicial
if 'mensagens' not in st.session_state or st.button("Zerar Mural (Apenas Admin)", key="reset_manual", help="Botão invisível/oculto de suporte", label_visibility="collapsed"):
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

# Título
st.markdown("<h1>🔥 ENTREGA ELEGANTE 99Food</h1>", unsafe_allow_html=True)

# --- BLOCO DE ENUNCIADO ---
st.markdown("""
<div class="enunciado-container">
    <div class="enunciado-titulo">🍿 🎏 Olha a Entrega Elegante! É verdade!</div>
    <p style="margin-bottom: 8px;">O São João chegou na 99Food! Para celebrar, misturamos a tradição do <strong>Correio Elegante Junino</strong> com a agilidade da <strong>99Food</strong> em um arraiá de reconhecimento corporativo. Veja como participar:</p>
    <ul style="margin-top: 0; padding-left: 20px;">
        <li><strong>Enviar um Recadinho:</strong> Pule para a aba <em>"Enviar Mensagem"</em>, coloque o nome do colega e complete a frase lembrando de um momento em que essa pessoa foi uma verdadeira parceira e "salvou o seu dia" na empresa. O envio é 100% anônimo!</li>
        <li><strong>Adivinhar no Mural:</strong> Na aba <em>"Mural de Entregas"</em>, ficam expostos todos os balões e mensagens do nosso time. Se achar um recado para você, clareie a mente e tente adivinhar o remetente. <strong>Cuidado:</strong> você só tem <u>uma única chance</u> para dar o seu palpite!</li>
        <li>⚠️ <strong>Regra do Arraiá:</strong> O mural de entregas é exclusivo para quem também espalhou carinho! Você só conseguirá visualizar os recados e dar seus palpites após enviar pelo menos uma mensagem para um colega nesta sessão.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Criação das Abas
aba_enviar, aba_mural = st.tabs(["💌 Enviar Mensagem", "📌 Mural de Entregas"])

# --- ABA 1: ENVIAR MENSAGEM ---
with aba_enviar:
    st.markdown("<h3 style='color: #1A1A1A;'>Prepare seu pedido de agradecimento! 💛</h3>", unsafe_allow_html=True)
    
    with st.form(key="form_correio", clear_on_submit=True):
        remetente = st.text_input("Seu Nome (Ficará escondido no mural para que a pessoa acerte que você enviou):").strip()
        destinatario = st.text_input("Para quem é a mensagem? (Nome do Colega):").strip()
        
        st.markdown("**Complete a frase com uma lembrança:**")
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
    st.markdown("<h3 style='color: #1A1A1A;'>👀 Quem recebeu um 'pedido' hoje?</h3>", unsafe_allow_html=True)
    
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
                    <div style="font-size: 0.8rem; color: #888;">Status: Entregue com sucesso • {msg['data']}</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
                # SE O CARD NÃO TIVER PALPITE, EXIBE O FORMULÁRIO DE CHUTE
                if not msg["palpite_feito"]:
                    with st.form(key=f"form_palpite_{orig_id}"):
                        st.markdown("<p style='font-weight: bold; margin-bottom: 2px;'>🕵️ Adivinhe quem te mandou esse recado:</p>", unsafe_allow_html=True)
                        
                        identificacao = st.text_input("Seu Nome (Quem está adivinhando):", key=f"id_{orig_id}", placeholder="Digite seu nome para validar...").strip()
                        chute = st.text_input("Quem você acha que enviou?", key=f"chute_{orig_id}", placeholder="Nome do colega do chute...").strip()
                        
                        botao_palpite = st.form_submit_button("Confirmar Palpite (Apenas 1 chance!) 🔒")
                        
                        if botao_palpite:
                            if identificacao and chute:
                                # Normaliza os nomes para fazer a checagem da trava de segurança (Opção B)
                                id_limpo = normalizar_nome(identificacao)
                                dest_limpo = normalizar_nome(msg["destinatario"])
                                
                                # TRAVA DE SEGURANÇA: Só aceita se o nome de quem chuta fizer parte do destinatário do card
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
                                    # Mensagem personalizada solicitada pelo usuário para bloquear bisbilhoteiros
                                    st.warning(f"✋ Ei, sô! Esse recado foi enviado para o(a) {msg['destinatario']}. Mas não tem problema, alguém ainda pode ter te enviado algum recadinho. 😊")
                            else:
                                st.warning("Preencha o seu nome E o nome do seu chute antes de confirmar.")
                # SE JÁ FOI PALPITADO, MOSTRA O RESULTADO IMEDIATAMENTE NA TELA
                else:
                    if msg["acertou"]:
                        # Texto atualizado para "recado especial!"
                        st.success(f"🎉 **{msg['quem_palpitou']}, você acertou em cheio!** Foi o(a) **{msg['remetente']}** que te enviou esse recado especial!")
                    else:
                        st.error(f"❌ **Não foi dessa vez, {msg['quem_palpitou']}!** Você chutou '{msg['palpite']}', mas quem te enviou esse pedido na verdade foi o(a) **{msg['remetente']}**!")
                
                st.markdown("<br>", unsafe_allow_html=True)

# --- ÁREA DO ADMINISTRADOR: DUPLA CAMADA (URL SECRETA + SENHA) ---
query_params = st.query_params
if query_params.get("adm") == "true":
    st.markdown("---")
    st.markdown("### 🛠️ Área do Administrador (Modo Secreto Ativo)")
    
    senha_adm = st.text_input("Insira a chave master para acessar o banco de dados:", type="password")
    
    if senha_adm == "99food2026":
        st.success("Autenticação efetuada com sucesso!")
        
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
