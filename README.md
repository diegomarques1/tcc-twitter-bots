# tcc-twitter-bots
Esse repositório contém os resultados obtidos durante o Trabalho de Conclusão de Curso (TCC) do curso de Ciência de Computação na UPM. O objetivo do projeto foi realizar um estudo na análise de identificação de bots no Twitter (ou X) por meio da criação de uma base de dados própria, treinamento de um modelo de machine learning e desenvolvimento de protótipo para aplicação analítica que o utilize.

O trabalho foi produzido por:
- Aluno: Diego Souza Lima Marques
- Orientador: Ivan Carlos Alcântara de Oliveira

## dataset
O diretório /dataset possui dois arquivos .xlsx, sendo eles:

### base_adaptada.xlsx

Uma versão adaptada da base original construída, com alguns atributos a menos, para não expor nenhuma informação pessoal ou irrelevante (como nome de usuário). Possui 1020 registros com todos os atributos da base original.

### dados_extras.xlsx

Os 20 dados obtidos na pequena retroalimentação final. Como foram unidos com a base após tratamento de dados, seleção de atributos e afins, possuem apenas os atributos necessários para o modelo (ou atributos em diferentes formatos), motivo pelo qual não foram adicionados diretamente no arquivo base_adaptada.xlsx (evitar valores nulos etc.).

## src
O diretório /src possui o código-fonte da aplicação Flask desenvolvida como protótipo de aplicação analítica.
```
├───modelo - contém os modelos de ML e normalizadores
├───static
│   ├───css - arquivo .css para estilização do contéudo
│   ├───img - contém imagem da logo antiga do Twitter
│   └───js - arquivos Javascript, se necessários
└───templates - arquivos HTML para construção das páginas
├───bots.py - arquivo Python com Flask para processar os dados da aplicação
```

### Executando localmente
A aplicação foi construída com base nas seguintes dependências:
* ```Python 3.10.10```
* ```pip 23.2.1```
* ```Flask 2.3.3```

Também foram utilizadas as seguintes bibliotecas: <strong>*os, dotenv, numpy, pandas, tweepy e warnings*</strong>. Talvez seja necessário adicioná-las separadamente por meio do comando:

```pip install nome-do-pacote```

Feito isso, basta estar no diretório raiz da aplicação e executar o seguinte comando:

```python bots.py```

## <strong>Observações fundamentais</strong>
* Como a aplicação utiliza diretamente a API do Twitter, para ela funcionar na extração e previsão dos dados de uma conta, você precisa ter um [bearer token](https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens) da API do Twitter. Se você o possuir, basta criar um arquivo .env no diretório raiz e nele colocar a variável MY_BEARER_TOKEN seguido do token em si;
* Também por utilizar a API do Twitter, que está em constante modificação, não há maneira de garantir que a versão atual do projeto irá funcionar corretamente para a extração de dados.