import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Entrega Elegante 99Food", page_icon="🌽", layout="centered")

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
