import streamlit as st
import base64

def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    set_background("9cc298341615defaecd24a5ac87388e8.jpg")  # imagem de fundo

    st.set_page_config(page_title="GastoDrive 💸🚗", layout="centered")
    st.title("💸 GastoDrive - Calculadora de Gasolina")

    with st.sidebar:
        st.header("⛽ Parâmetros do Veículo")
        consumo_cidade = st.number_input("Consumo na cidade (km/l)", min_value=1.0, value=10.0, step=0.1)
        consumo_estrada = st.number_input("Consumo na estrada (km/l)", min_value=1.0, value=14.0, step=0.1)
        consumo_misto = st.number_input("Consumo misto (km/l)", min_value=1.0, value=12.0, step=0.1)
        preco_litro = st.number_input("Preço da gasolina (R$)", min_value=0.01, value=5.49, step=0.01)

    st.subheader("🛣️ Adicionar Trechos")

    if "trechos" not in st.session_state:
        st.session_state.trechos = []

    with st.form("form_trajeto"):
        origem = st.text_input("Origem")
        destino = st.text_input("Destino")
        distancia = st.number_input("Distância entre os pontos (ida, em km)", min_value=0.1, value=10.0, step=0.1)
        tipo = st.selectbox("Tipo de trajeto", ["cidade", "estrada", "misto"])
        adicionar = st.form_submit_button("Adicionar trecho")

        if adicionar:
            st.session_state.trechos.append({
                "origem": origem,
                "destino": destino,
                "distancia": distancia * 2,  # ida e volta
                "tipo": tipo
            })
            st.success(f"Trecho {origem} → {destino} adicionado com sucesso!")

    if st.session_state.trechos:
        st.subheader("📋 Trechos Adicionados")
        total_km = 0
        total_custo = 0

        consumo = {
            "cidade": consumo_cidade,
            "estrada": consumo_estrada,
            "misto": consumo_misto
        }

        for i, trecho in enumerate(st.session_state.trechos):
            km_l = consumo[trecho["tipo"]]
            litros = trecho["distancia"] / km_l
            custo = litros * preco_litro

            st.markdown(f"**{i+1}. {trecho['origem']} → {trecho['destino']}** - {trecho['distancia']} km ({trecho['tipo']}): R$ {custo:.2f}")
            total_km += trecho["distancia"]
            total_custo += custo

        st.write("---")
        st.subheader("📊 Resumo Final")
        st.write(f"**Distância total:** {total_km:.2f} km")
        st.write(f"**Custo total estimado:** R$ {total_custo:.2f}")

        if st.button("🧹 Limpar todos os trechos"):
            st.session_state.trechos = []
            st.success("Todos os trechos foram removidos.")

if __name__ == "__main__":
    main()
