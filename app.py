import streamlit as st
import json
import pandas as pd

# Load catálogo
from catalogo_supermercado import catalogo

# Session state init
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []
if "total" not in st.session_state:
    st.session_state.total = 0.0

st.set_page_config(page_title="Supermercado arena", layout="wide")
st.title(" atacadão arena🛒 ")

# Abas por categoria
abas = st.tabs(list(catalogo.keys()))

for i, categoria in enumerate(catalogo.keys()):
    with abas[i]:
        produtos = catalogo[categoria]
        cols = st.columns(2)
        for idx, produto in enumerate(produtos):
            with cols[idx % 2]:
                st.image(produto["imagem"], width=150, caption=produto["nome"])
                st.markdown(f"**Preço:** R${produto['preco']:.2f}")
                st.markdown(f"**Estoque:** {produto['estoque']} unidades")
                quantidade = st.number_input(
                    f"Qtd - {produto['nome']}",
                    min_value=0, max_value=produto["estoque"],
                    step=1, key=f"{categoria}_{produto['nome']}"
                )
                if st.button(f"Adicionar - {produto['nome']}", key=f"btn_{categoria}_{produto['nome']}"):
                    if quantidade > 0:
                        st.session_state.carrinho.append({
                            "Produto": produto["nome"],
                            "Categoria": categoria,
                            "Quantidade": quantidade,
                            "Preço Unitário": produto["preco"],
                            "Subtotal": produto["preco"] * quantidade
                        })
                        st.session_state.total += produto["preco"] * quantidade
                        st.success(f"{quantidade}x {produto['nome']} adicionado(s) ao carrinho.")
                    else:
                        st.warning("Escolha uma quantidade válida.")

# Carrinho lateral
with st.sidebar:
    st.header("🧾 Carrinho de Compras")
    if st.session_state.carrinho:
        df = pd.DataFrame(st.session_state.carrinho)
        st.dataframe(df, use_container_width=True)
        st.markdown(f"### Total: R${st.session_state.total:.2f}")
        if st.button("✅ Finalizar Compra"):
            st.success(f"Compra finalizada! Total: R${st.session_state.total:.2f}")
            st.session_state.carrinho.clear()
            st.session_state.total = 0.0
    else:
        st.write("Carrinho vazio.")

# Rodapé fixo
st.markdown(
    """
    ---
    <style>
        footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #000000
            color: black;
            text-align: center;
        }
    </style>
    <footer>
        <p>Desenvolvido por [Lucas C Vasques] - Supermercado Online</p>
    </footer>
    """,
    unsafe_allow_html=True
)