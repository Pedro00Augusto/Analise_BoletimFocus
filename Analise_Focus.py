# -*- coding: utf-8 -*-
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

base = requests.get('https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoTop5Anuais?$format=json&$select=Indicador,Data,DataReferencia,tipoCalculo,Media,Mediana')
base_filtrada = base.json()

banco = pd.DataFrame(base_filtrada['value'])
lista_indicadores = list(banco['Indicador'].unique())
i = 0
dicio = {}
lista = []

for l in lista_indicadores:
    indicador = str(lista_indicadores[i])
    x = banco[banco["Indicador"]==indicador]
    dicio[i] = pd.DataFrame(x)   
    i += 1
    

    
banco_PIB, banco_IPCA_ADM, banco_IGP_DI, banco_IGP_M, banco_IPCA, banco_selic, banco_cambio, banco_desocupacao = dicio[0], dicio[1], dicio[2], dicio[3], dicio[4], dicio[5], dicio[6], dicio[7]

def filtrar_tabela(tabela, year, calc, ind):
    tabela = tabela[tabela['DataReferencia']==year]
    tabela[['ano', 'mes', 'dia']] = tabela['Data'].str.split("-", expand = True)
    tabela['periodoAno'] = tabela['ano'] + '/' + tabela['mes']
    tabela = tabela.groupby('periodoAno').mean(numeric_only=True).reset_index()

    if calc == 'C':
        tabela['tipoCalculo'] = 'C'
    elif calc == 'M':
        tabela['tipoCalculo'] = 'M'
    elif calc == 'L':
        tabela['tipoCalculo'] = 'L'
    else:
        tabela = tabela
        
    tabela['Indicador'] = ind    
    return tabela
  

def fazer_grafico(tabela):    
    x = tabela['periodoAno']
    media = tabela['Media']
    mediana = tabela['Mediana']
    prazo = tabela['tipoCalculo'].iloc[0]
    if prazo == 'C':
         prazo = "Curto Prazo"
    elif prazo == 'M':
         prazo = "Médio Prazo"
    elif prazo == "L":
         prazo = "Longo Prazo"
    indic = tabela['Indicador'].iloc[0]
    grafico = plt.figure(figsize=(20,10))
    plt.plot(x, media, label = 'Media')
    plt.plot(x, mediana, label = 'Mediana')
    plt.xlabel('Ano e Mês')
    plt.title(f'Variação {indic} por mês para {prazo}')
    plt.legend()
    plt.xticks(rotation = 'vertical', fontsize = 10)
    lista.append(grafico)    
    return grafico
   

IPCA_C_2023 = filtrar_tabela(banco_IPCA, '2023', 'C', 'IPCA')
graf_ipca_c_23 = fazer_grafico(IPCA_C_2023)

IPCA_M_2023 = filtrar_tabela(banco_IPCA, '2023', 'M', 'IPCA')
graf_ipca_m_23 = fazer_grafico(IPCA_M_2023)

IPCA_L_2023 = filtrar_tabela(banco_IPCA, '2023', 'L', 'IPCA')
graf_ipca_l_23 = fazer_grafico(IPCA_L_2023)

selic_C_2023 = filtrar_tabela(banco_selic, '2023', 'C', 'Selic')
graf_selic_c_23 = fazer_grafico(selic_C_2023)
    
selic_M_2023 = filtrar_tabela(banco_selic, '2023', 'M', 'Selic')
graf_selic_m_23 = fazer_grafico(selic_M_2023)

selic_L_2023 = filtrar_tabela(banco_selic, '2023', 'L', 'Selic')
graf_selic_l_23 = fazer_grafico(selic_L_2023)

cambio_C_2023 = filtrar_tabela(banco_cambio, '2023', 'C', 'Cambio')
graf_cambio_c_23 = fazer_grafico(cambio_C_2023)

cambio_M_2023 = filtrar_tabela(banco_cambio, '2023', 'M', 'Cambio')
graf_cambio_m_23 = fazer_grafico(cambio_M_2023)

cambio_L_2023 = filtrar_tabela(banco_cambio, '2023', 'L', 'Cambio')
graf_cambio_l_23 = fazer_grafico(cambio_L_2023)

desoc_C_2023 = filtrar_tabela(banco_desocupacao, '2023', 'C', 'Taxa de Desocupação')
graf_desoc_c_23 = fazer_grafico(desoc_C_2023)

desoc_M_2023 = filtrar_tabela(banco_desocupacao, '2023', 'M', 'Taxa de Desocupação')
graf_desoc_m_23 = fazer_grafico(desoc_M_2023)

desoc_L_2023 = filtrar_tabela(banco_desocupacao, '2023', 'L', 'Taxa de Desocupação')
graf_desoc_l_23 = fazer_grafico(desoc_L_2023)

pdf = PdfPages('Relatório_Focus.pdf')

for l in range(12):
    pdf.savefig(lista[l])
    
pdf.close()








