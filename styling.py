"""
FindOut - Estilos visuales con la paleta de colores de Greenmovil S.A.S.
"""

import streamlit as st

PRIMARIO = "#145A4F"        # Verde institucional Greenmovil
PRIMARIO_OSCURO = "#0D3B34"
SECUNDARIO = "#1F8A73"
FONDO = "#F4F7F6"
BLANCO = "#FFFFFF"
TEXTO = "#1A2E2B"
ALERTA = "#C0392B"
ADVERTENCIA = "#E1A100"
EXITO = "#1F8A73"


def inject_css():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {FONDO};
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {PRIMARIO_OSCURO} 0%, {PRIMARIO} 100%);
        }}
        section[data-testid="stSidebar"] * {{
            color: {BLANCO} !important;
        }}
        .sidebar-brand {{
            font-size: 1.6rem;
            font-weight: 800;
            letter-spacing: 0.5px;
            padding: 0.4rem 0 0.1rem 0;
        }}

        .findout-header {{
            background: linear-gradient(135deg, {PRIMARIO} 0%, {SECUNDARIO} 100%);
            padding: 1.6rem 2rem;
            border-radius: 14px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 14px rgba(20, 90, 79, 0.25);
        }}
        .findout-header h1 {{
            color: {BLANCO};
            margin: 0;
            font-weight: 800;
        }}
        .findout-header p {{
            color: {BLANCO};
            opacity: 0.9;
            margin: 0.2rem 0 0 0;
        }}

        .stButton > button {{
            background-color: {PRIMARIO};
            color: {BLANCO};
            border-radius: 8px;
            border: none;
            font-weight: 600;
        }}
        .stButton > button:hover {{
            background-color: {SECUNDARIO};
            color: {BLANCO};
        }}

        div[data-testid="stMetric"] {{
            background-color: {BLANCO};
            border: 1px solid #E1E8E6;
            border-radius: 12px;
            padding: 0.8rem;
        }}

        div[data-testid="stForm"] {{
            background-color: {BLANCO};
            border: 1px solid #E1E8E6;
            border-radius: 14px;
            padding: 1.2rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
