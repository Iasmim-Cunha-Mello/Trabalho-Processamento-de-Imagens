import streamlit as st
import requests
import os
from db_sqlite import criar_tabela, salvar_informacoes, listar_registros

criar_tabela()

API_URL = "http://localhost:8000/tipoimagem"

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

st.title("Processamento de Imagens – Integração com Banco de Dados")

st.write("Envie uma imagem para processar via API e salvar o resultado no banco.")

uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    st.image(uploaded_file, caption="Pré-visualização", use_column_width=True)

    if st.button("Enviar para API"):
        st.write("Enviando imagem para a API...")

       
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            
            files = {"file": open(file_path, "rb")}
            response = requests.post(API_URL, files=files)

            resposta_texto = response.text  

            st.subheader("Resposta da API:")
            st.code(resposta_texto)

         
            salvar_informacoes(
                nome_arquivo=uploaded_file.name,
                caminho_arquivo=file_path,
                resposta_api=resposta_texto
            )

            st.success("Informações salvas com sucesso no banco!")

        except Exception as e:
            st.error(f"Erro ao enviar imagem: {e}")


st.header("Histórico de Imagens Processadas")

registros = listar_registros()

if registros:
    for r in registros:
        st.write("---")
        st.write(f"📄 **Arquivo:** {r[1]}")
        st.write(f"📁 Caminho: {r[2]}")
        st.write(f"🕒 Data: {r[4]}")
        st.text_area("Resposta da API", r[3], height=120)
else:
    st.write("Nenhum registro encontrado.")
