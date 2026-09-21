import geopandas as gpd
import numpy as np
import pandas as pd
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

longitude = st.number_input("Longitude", value=-122.33)
latitude = st.number_input("Latitude", value=37.88)

housing_median_age = st.number_input("Idade do imóvel", value=10)

total_rooms = st.number_input("Total de cômodos", value=800)
total_bedrooms = st.number_input("Total de quartos", value=100)
population = st.number_input("População", value=300)
households = st.number_input("Domicílios", value=100)
median_income = st.slider("Renda média (múltiplos de US$ 10k)", 0.5, 15.0, 4.5, 0.5) # O slider é um outro tipo de wiget para pessoa arrastar o valor que ele deseja inputs(valor mim, valor max, valor padrão, step()intervalo)

ocean_proximity = st.selectbox("Proximidade do oceano", df["ocean_proximity"].unique()) #selectbox seria uma seleção padrão e de aordo com a documentação eu preciso passar categorias e então estou passando para ele pegar os valores unicos dessa coluna

median_income_cat = st.number_input("Categoria de renda", value=4)

rooms_per_household = st.number_input("Quartos por domicílio", value=7)
bedrooms_per_room = st.number_input("Quartos por cômodo", value=0.2)
population_per_household = st.number_input("Pessoas por domicílio", value=2)

#Vamos reunir essas informações em dataframe e ai vamos armazenar essas informações no dicionario que dai teremos chaves e valor e depois eu transformo em um dataframe

entrada_modelo = {
    "longitude": longitude,
    "latitude": latitude,
    "housing_median_age": housing_median_age,
    "total_rooms": total_rooms,
    "total_bedrooms": total_bedrooms,
    "population": population,
    "households": households,
    "median_income": median_income,
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
