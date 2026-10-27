import pdfplumber
import pandas as pd
import os
import re

def extrair_dados_pdf(caminho_arquivo):
        dados_extraidos = {}
        with pdfplumber.open(caminho_arquivo) as pdf:
                texto_completo = ""
                for pagina in pdf.pages:
                        texto_completo += pagina.extract_text() + "\n"

        nome = re.search(r"Nome:\s*(.*)", texto_completo, re.IGNORECASE)
        email= re.search(r"Email:\s*(.*)", texto_completo, re.IGNORECASE)

        dados_extraidos['Arquivo Original'] = os.path.basename(caminho_arquivo)
        dados_extraidos['Nome'] = nome.group(1).strip() if nome else "Não encontrado"
        dados_extraidos['Email'] = email.group(1).strip() if email else "Não encontrado"
        
        return dados_extraidos

pasta_pdfs = "pdfs"
lista_de_dados = []

for nome_arquivo in os.listdir(pasta_pdfs):
        if nome_arquivo.endswith(".pdf"):
                caminho_completo =os.path.join(pasta_pdfs, nome_arquivo)
                dados = extrair_dados_pdf(caminho_completo)
                lista_de_dados.append(dados)

planilha = pd.DataFrame(lista_de_dados)
planilha.to_excel("fichas_consolidadas.xlsx", index=False)

print("Extração concluída! Verifique o arquivo fichas_consolidadas.xlsx")