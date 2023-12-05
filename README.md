# tcc-twitter-bots
Esse repositório contém os resultados obtidos durante o Trabalho de Conclusão de Curso (TCC) do curso de Ciência de Computação na UPM. O objetivo do projeto foi realizar um estudo na análise de identificação de bots no Twitter (ou X) por meio da criação de uma base de dados própria, treinamento de um modelo de machine learning e desenvolvimento de protótipo para aplicação analítica que o utilize.

O objetivo da aplicação é informar alguns dados sobre uma conta no Twitter e, ao clicar no botão de fazer previsão, verificar se a conta é um provável bot e sua respectiva probabilidade.

O trabalho foi produzido por:
- Aluno: Diego Souza Lima Marques
- Orientador: Ivan Carlos Alcântara de Oliveira

A base adaptada também pode ser encontrada no [Kaggle](https://www.kaggle.com/datasets/diegoslmarques/dataset-para-deteco-de-bots-no-twitter).

## dataset
O diretório /dataset possui três arquivos .xlsx, sendo eles:

### base_adaptada.xlsx

Uma versão adaptada da base original construída, com alguns atributos a menos, para não expor nenhuma informação pessoal ou irrelevante (como nome de usuário). Possui 1020 registros com todos os atributos da base original.

### dados_extras.xlsx

Os 20 dados obtidos em uma pequena retroalimentação utilizando o modelo. Como foram unidos com a base após tratamento de dados, seleção de atributos e afins, esses dados possuem apenas os atributos necessários para o modelo (e/ou atributos em diferentes formatos), motivo pelo qual não foram adicionados diretamente no arquivo base_adaptada.xlsx (evitar valores nulos etc.).

### base_retro_adaptada.xlsx

Consolidação dos dados extras da retroalimentação com o restante da base, mas apenas com os atributos obtidos nos dados extras. Possui 1020 registros, ao invés de 1040, por conta de 20 registros terem sido removidos aleatoriamente e estratificadamente para teste ao modelo final do projeto.

## notebook
O diretório /notebook contém uma versão adaptada do processo de otimização de modelos de machine learning realizado durante o projeto. No arquivo TCC_Notebook_Adaptado.ipynb, estão contidos os resultados consolidados e adaptados. Não há garantia que esse notebook será executado com sucesso, nem que os resultados serão os mesmos (visto que é uma versão __adaptada__), mas esse artefato está aqui para dar uma ideia desse processo e servir de referência a quem interessar.

## prototype
O diretório /prototype possui o código-fonte de duas versões da aplicação Flask inicial, versão 1, desenvolvida como protótipo de aplicação analítica. Por ser um protótipo de teste do modelo, todos os atributos precisam ser inseridos manualmente pelo usuário para realizar a predição da categoria de uma conta entre bot ou humano.

### src_forest
Essa versão aplica o modelo final de RandomForest (floresta aleatória) na aplicação.

### src_gradient
Essa versão aplica o modelo final de GradientBoosting na aplicação.

A estrutura geral dentro de cada versão é a seguinte:

```
├───modelo - contém os modelos de ML e normalizadores
├───static
│   ├───css - arquivo .css para estilização do contéudo
│   ├───img - contém imagem da logo antiga do Twitter
│   └───js - arquivos Javascript, se necessários
└───templates - arquivos HTML para construção das páginas
├───bots.py - arquivo Python com Flask para processar os dados da aplicação
```

## prototype_api
O diretório /prototype_api possui o código-fonte de duas versões da aplicação Flask do projeto, versão 2. Seu objetivo segue o mesmo, mas nela há o uso da API do Twitter por meio da biblioteca Tweepy para obter boa parte dos dados antes inseridos manualmente pelo usuário. A estrutura também segue a mesma, com divisão em ``src_forest`` e ``src_gradient``.

No entanto, atualmente, para essa aplicação funcionar, é necessário ter acesso a algum plano na API do Twitter acima do gratuito. <strong>Portanto, recomendamos a utilização da versão 1 para testes, a não ser que você pague algum plano mensal da API do Twitter</strong>.

### <strong>Observações fundamentais</strong>
* Como a versão 2 da aplicação utiliza diretamente a API do Twitter, para ela funcionar na extração e previsão dos dados de uma conta, você precisa ter um [bearer token](https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens) da API do Twitter de um plano acima do gratuito. Caso você o possua, basta criar um arquivo .env dentro do diretório /src_v2 e nele colocar a variável `MY_BEARER_TOKEN` seguido do token em si, entre aspas;
* Também por utilizar a API do Twitter, que em 2023 está em constante modificação, não há maneira de garantir que a versão atual do projeto irá funcionar corretamente para a extração de dados, no caso da versão 2.

## Executando localmente
A aplicação foi construída com base nas seguintes dependências:
* `Python 3.10.10`
* `pip 23.2.1`
* `Flask 2.3.3`

Também foram utilizadas as seguintes bibliotecas: <strong>*os, numpy, pandas, tweepy, scikit-learn e warnings*</strong>. 
Algumas versões importantes a serem utilizadas para execução do projeto sem erros:
* `pandas: 2.1.3`
* `numpy: 1.25.0`
* `scikit-learn: 1.0.2`
* `joblib: 1.3.2`

Talvez seja necessário adicioná-las separadamente por meio do comando:

`pip install nome-do-pacote`

É recomendável instalar as mesmas versões utilizadas, incluindo do Flask, por meio do comando:

`pip install nome-do-pacote==versao`

Exemplo: `pip install pandas==2.1.3`

Feito isso, basta estar no diretório raiz da aplicação e executar o seguinte comando:

`python bots.py`

Dependendo da sua versão e do seu sistema operacional, talvez você precise incluir um "3" ao final dos comandos, como: `python3 bots.py` ou `pip3 install nome-do-pacote`

Essa não é a única maneira, mas é funcional. Caso encontre algum problema, recomendamos olhar a [documentação oficial](https://flask.palletsprojects.com/en/3.0.x/quickstart/) ou o [seguinte tutorial](https://www.geeksforgeeks.org/how-to-run-a-flask-application/).
