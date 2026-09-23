# Previsão do Preço de Imóveis na Califórnia com Linear Regression

![imagem](./relatorios/imagens/capa.jpg)

O mercado imobiliário é dinâmico e complexo, onde o valor de uma propriedade é influenciado por múltiplos fatores geoespaciais e socioeconômicos. Compreender e prever esses preços de forma precisa é fundamental para tomadas de decisão estratégicas por parte de investidores, compradores e corretores de imóveis.O conjunto de dados California Housing é um dataset clássico da área de aprendizado de máquina, originado a partir de dados do censo de 1990 da Califórnia (Estados Unidos). 
Ele reúne informações sobre milhares de blocos residenciais do estado, incluindo variáveis como a renda média dos moradores, a idade média dos imóveis, o número de cômodos e a localização geográfica (latitude e longitude). Para este projeto, utilizou-se o algoritmo de Regressão Linear para mapear a relação entre esses indicadores e estimar o valor mediano das casas.

Para este projeto, foi utilizado conjunto de dados disponível no Kaggle para o ano de 1990.

 [Link do Kaggle](https://https://www.kaggle.com/datasets/camnugent/california-housing-prices)


## Organização do projeto

```
├── ambiente              <- Arquivo de variáveis de ambiente (não versionar)
├── .gitignore         <- Arquivos e diretórios a serem ignorados pelo Git
├── ambiente.yml       <- O arquivo de requisitos para reproduzir o ambiente de análise
├── LICENSE            <- Licença de código aberto se uma for escolhida
├── README.md          <- README principal para desenvolvedores que usam este projeto.
|
├── dados              <- Arquivos de dados para o projeto.
|
├── modelos            <- Modelos treinados e serializados, previsões de modelos ou resumos de modelos
|
├── notebooks          <- Cadernos Jupyter. A convenção de nomenclatura é um número (para ordenação),
│                         as iniciais do criador e uma descrição curta separada por `-`, por exemplo
│                         `01-fb-exploracao-inicial-de-dados`.
│
|   └──src             <- Código-fonte para uso neste projeto.
|      │
|      ├── __init__.py  <- Torna um módulo Python
|      ├── config.py    <- Configurações básicas do projeto
|      └── graficos.py  <- Scripts para criar visualizações exploratórias e orientadas a resultados
|
├── referencias        <- Dicionários de dados, manuais e todos os outros materiais explicativos.
|
├── relatorios         <- Análises geradas em HTML, PDF, LaTeX, etc.
│   └── imagens        <- Gráficos e figuras gerados para serem usados em relatórios
```

## Configuração do ambiente

1. Faça o clone do repositório que será criado a partir deste modelo.

    ```bash
    git clone ENDERECO_DO_REPOSITORIO
    ```

2. Crie um ambiente virtual para o seu projeto utilizando o gerenciador de ambientes de sua preferência.

    a. Caso esteja utilizando o `conda`, exporte as dependências do ambiente para o arquivo `ambiente.yml`:

      ```bash
      conda env export > ambiente.yml
      ```

    b. Caso esteja utilizando outro gerenciador de ambientes, exporte as dependências
    para o arquivo `requirements.txt` ou outro formato de sua preferência. Adicione o
    arquivo ao controle de versão, removendo o arquivo `ambiente.yml`.

Por padrão, o arquivo `.gitignore` já está configurado para ignorar arquivos de dados e
arquivos de Notebook (para aqueles que usam ferramentas como
[Jupytext](https://jupytext.readthedocs.io/en/latest/) e similares). Adicione ou remova
outros arquivos e diretórios do `.gitignore` conforme necessário. Caso deseje adicionar
forçadamente um Notebook ao controle de versão, faça um commit forçado com o
comando `git add --force NOME_DO_ARQUIVO.ipynb`.
