import geopandas as gpd
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

from joblib import load #carregar os dados

from notebooks.src.config import DADOS_GEO_MEDIAN, DADOS_LIMPOS, MODELO_FINAL

#Estamos trabalhando com funções para passar algumas configurações que toda a vez que a gente altera algo ele carrega a pagina, porque ele vai ficar carregando os datas frames e modelos toda a hora que foi carregado e isso pode compremeter o tempo de carregamento
#Conceito de cache
#Decorador é uma função que atua no resultado de uma outra função
#data é destinada para funções e dataframes, essa é uma função do streamlit ele vai pegar o resultado da função pode exemplo: #carregar_dados_limpos e armazenar na memoria

@st.cache_data 
def carregar_dados_limpos():
    return pd.read_parquet(DADOS_LIMPOS)

@st.cache_data
def carregar_dados_geo():
    return gpd.read_parquet(DADOS_GEO_MEDIAN)
    
@st.cache_resource #resource é destinada para modelos
def carregar_modelo():
    return load(MODELO_FINAL)

df = carregar_dados_limpos()
gdf_geo = carregar_dados_geo()
modelo = carregar_modelo()



st.title("Previsão de preços de imóveis") #Titulo Principal

#Agente fez uma mediano dos valores de lat e long de cada condado, ou seja a pessoa não precisa digitar a lat e nem long manualmente ele pode selecionar qual condado ela quer
condados = list(gdf_geo["name"].sort_values())

#Dividir a tela usando um unpacking
coluna1, coluna2 = st.columns(2)

#Gerenciador de contexto
with coluna1:
    selecionar_condado = st.selectbox("Condado", condados)
    
    longitude = gdf_geo.query("name == @selecionar_condado")["longitude"].values#query é busca no pandas
    latitude = gdf_geo.query("name == @selecionar_condado")["latitude"].values
    
    housing_median_age = st.number_input("Idade do imóvel", value=10, min_value=1, max_value=50)
    
    #total_rooms = st.number_input("Total de cômodos", value=800, min_value=6, max_value=11026)
    #total_bedrooms = st.number_input("Total de quartos", value=100, min_value=2, max_value=2205)
    total_rooms = gdf_geo.query("name == @selecionar_condado")["total_rooms"].values
    total_bedrooms = gdf_geo.query("name == @selecionar_condado")["total_bedrooms"].values
    population = gdf_geo.query("name == @selecionar_condado")["population"].values
    households = gdf_geo.query("name == @selecionar_condado")["households"].values
    median_income = st.slider("Renda média (milhares de US$)", 5.0, 100.0, 45.0, 5.0) # O slider é um outro tipo de wiget para pessoa arrastar o valor que ele deseja inputs(valor mim, valor max, valor padrão, step()intervalo)
    
    ocean_proximity = gdf_geo.query("name == @selecionar_condado")["ocean_proximity"].values #selectbox seria uma seleção padrão e de aordo com a documentação eu preciso passar categorias e então estou passando para ele pegar os valores unicos dessa coluna
    
    #tem uma função do numpy que ele verificar se o valor esta dentro de uma categoria e mostra os valores da categoria
    bins_income = [0, 1.5, 3, 4.5, 6, np.inf]
    median_income_cat = np.digitize(median_income / 10, bins=bins_income)
    
    rooms_per_household = gdf_geo.query("name == @selecionar_condado")["rooms_per_household"].values
    bedrooms_per_room = gdf_geo.query("name == @selecionar_condado")["bedrooms_per_room"].values
    population_per_household = gdf_geo.query("name == @selecionar_condado")["population_per_household"].values
    
    #Vamos reunir essas informações em dataframe e ai vamos armazenar essas informações no dicionario que dai teremos chaves e valor e depois eu transformo em um dataframe
    
    entrada_modelo = {
        "longitude": longitude,
        "latitude": latitude,
        "housing_median_age": housing_median_age,
        "total_rooms": total_rooms,
        "total_bedrooms": total_bedrooms,
        "population": population,
        "households": households,
        "median_income": median_income / 10,
        "ocean_proximity": ocean_proximity,
        "median_income_cat": median_income_cat,
        "rooms_per_household": rooms_per_household,
        "bedrooms_per_room": bedrooms_per_room,
        "population_per_household": population_per_household,
    }
    
    df_entrada_modelo = pd.DataFrame(entrada_modelo, index=[0])
    #Variavel para receber a nossa previsão
    
    botao_previsao = st.button("Prever preço")
    #Esse button ele retorna um booleano e podemos checar se esse botão foi precionado
    
    if botao_previsao:
        preco = modelo.predict(df_entrada_modelo)
        st.write(f"Preço previsto: US$ {preco[0][0]:.2f}") #ele retorna um array de arrays

with coluna2:
    view_state = pdk.ViewState(
        #AQui esta dando um erro porque no nosso df quando estavamos otimizando os nossos tipos de dados tem algums tipos de dados que não são compativeis em algumas bibliotecas nesse caso o float32.
        latitude=float(latitude), #estou convertentando para float64 usando float()
        longitude=float(longitude),
        zoom=5,
        min_zoom=5,
        max_zoom=15,
    )

    mapa = pdk.Deck(
        initial_view_state=view_state,
        map_style='light' #Usar um estilo no mapa
    )

    st.pydeck_chart(mapa)


    