import streamlit as st
import google.generativeai as genai
import PyPDF2
# 1. Configuração da Interface
st.set_page_config(page_title="Auditor de Compliance IA", page_icon=" ")
st.title(" Auditor Digital de Contratos")
st.markdown("### Análise de Conformidade - Lei 14.133/2021")
# 2. Configuração da API (Sidebar)
with st.sidebar:
st.header("Configurações Técnicas")
api_key = st.text_input("Cole sua Gemini API Key:", type="password")
st.info("Obtenha uma chave gratuita em: aistudio.google.com")
# 3. Upload do Documento
uploaded_file = st.file_uploader("Arraste o contrato em PDF aqui",
type="pdf")
if uploaded_file and api_key:
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
# Extração do Texto
pdf_reader = PyPDF2.PdfReader(uploaded_file)
content = ""
for page in pdf_reader.pages:
content += page.extract_text()
if st.button("Executar Auditoria de Compliance"):
with st.spinner("A IA está analisando as cláusulas..."):
prompt = f"""
Você é um Auditor de Compliance sênior. Analise o contrato
abaixo com base na Lei 14.133/2021.
CONTRATO: {content[:15000]}
Gere um relatório estruturado em tabela contendo:
- Item Analisado (ex: Anticorrupção, Reajuste, Matriz de Risco)
- Status ( Conforme | Não Conforme)
- Justificativa (Cite o artigo da lei se possível)
- Recomendação (O que o gestor deve fazer)
"""
response = model.generate_content(prompt)
st.success("Auditoria Concluída!")
st.markdown(response.text)
elif not api_key:
st.warning("Aguardando a chave da API para habilitar o motor de auditoria.")