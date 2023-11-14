# Faz os imports utilizados
import os
from dotenv import load_dotenv
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import tweepy
import warnings
warnings.filterwarnings('ignore')

# Importa as variáveis de ambiente
load_dotenv()

# Importa o deserializador de objetos
import joblib

# Carrega a classe de predição do diretório local
# Carregando o modelo em disco para a memória da nossa aplicação.
modelo = joblib.load('modelo/tcc_bots_modelo_rand_forest_retro.sav')
scaler = joblib.load('modelo/min_max_scaler.save')
scaler_v2 = joblib.load('modelo/min_max_scaler_v2.save')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def get_acc_info():
    # Coloque seu bearer token da API do Twitter em um arquivo .env associado ao nome MY_BEARER_TOKEN
    bearer_token = os.getenv("MY_BEARER_TOKEN")

    auth = tweepy.OAuth2BearerHandler(bearer_token)
    api = tweepy.API(auth)

    user = api.get_user(screen_name=str(request.form['username']))
    print(user)
    # timeline = user.timeline(include_rts=False, count=5)
    # timeline = api.user_timeline(screen_name=str(request.form['username']), include_rts=False, count=5)
    dados = dict()

    dados['username'] = str(request.form['username'])
    dados['follower_count'] = int(user.followers_count)
    dados['followings_count'] = int(user.friends_count)
    dados['favourites_count'] = int(user.favourites_count)
    dados['statuses_count'] = int(user.statuses_count)

    followers_followings_ratio = 0
    if user.friends_count != 0:
        followers_followings_ratio =  user.followers_count / user.friends_count
    
    dados['followers_followings_ratio'] = followers_followings_ratio

    dados['rts_mean'] = float(request.form['rts_mean'])
    dados['favs_mean'] = float(request.form['favs_mean'])

    rts_favs_ratio = 0
    if dados['favs_mean'] != 0:
        rts_favs_ratio = dados['rts_mean'] / dados['favs_mean']

    dados['rts_favs_ratio'] = rts_favs_ratio

    # dados['is_verified'] = 1 if user.verified == True else 0 # não está funcionando por algum motivo
    dados['is_verified'] = int(request.form['is_verified'])
    try:
        dados['has_url'] = 0 if user.entities['url']['urls'][0]['display_url'] == '' else 1
    except:
        dados['has_url'] = 0

    dados['more_than_once'] = int(request.form['more_than_once'])
    dados['by_other'] = int(request.form['by_other'])

    return dados


# Função acima quebrou do nada - 13/11/2023 - Provavelmente mudanças internas na API
# https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-me#tab0

# Tentativa de solução alternativa - não funcionou
# bearer_token = os.getenv("MY_BEARER_TOKEN")
# # auth = tweepy.OAuth2BearerHandler(bearer_token)
# client = tweepy.Client(bearer_token=bearer_token)
# user_fields = ["created_at", "entities", "username", "public_metrics", "url", "verified"]
# user = client.get_me(screen_name=str(request.form['username']))

def obtem_dados_form():
    dados = dict()

    dados['username'] = str(request.form['username'])
    dados['follower_count'] = int(request.form['follower_count'])
    dados['followings_count'] = int(request.form['followings_count'])
    dados['favourites_count'] = int(request.form['favourites_count'])
    dados['statuses_count'] = int(request.form['statuses_count'])
    dados['followers_followings_ratio'] = float(request.form['followers_followings_ratio'])
    dados['rts_mean'] = float(request.form['rts_mean'])
    dados['favs_mean'] = float(request.form['favs_mean'])
    dados['rts_favs_ratio'] = float(request.form['rts_favs_ratio'])
    dados['is_verified'] = int(request.form['is_verified'])
    dados['has_url'] = int(request.form['has_url'])
    dados['more_than_once'] = int(request.form['more_than_once'])
    dados['by_other'] = int(request.form['by_other'])

    return dados

def monta_dicionario_resposta(dados, classe, res_proba):
    resposta = dict()
    resposta['username'] = str(dados['username'])
    resposta['follower_count'] = dados['follower_count']
    resposta['followings_count'] = dados['followings_count']
    resposta['favourites_count'] = dados['favourites_count']
    resposta['statuses_count'] = dados['statuses_count']
    
    resposta['followers_followings_ratio'] = dados['followers_followings_ratio']
    resposta['rts_mean'] = dados['rts_mean']
    resposta['favs_mean'] = dados['favs_mean']
    resposta['rts_favs_ratio'] = dados['rts_favs_ratio']

    resposta['is_verified'] = 'Sim' if dados['is_verified'] == 1 else 'Não'
    resposta['has_url'] = 'Sim' if dados['has_url'] == 1 else 'Não'
    resposta['more_than_once'] = 'Sim' if dados['more_than_once'] == 1 else 'Não'
    resposta['by_other'] = 'Sim' if dados['by_other'] == 1 else 'Não'

    resposta["classe"] = classe
    resposta["res_proba"] = res_proba

    return resposta


def normaliza_resposta(dados):
    to_be_scaled = pd.DataFrame([{
        'author_follower_count': dados['follower_count'],
        'author_followings_count': dados['followings_count'],
        'author_favourites_count': dados['favourites_count'],
        'author_statuses_count': dados['statuses_count'],
        'followers_followings_ratio': dados['followers_followings_ratio'],
        # 'last_five_tweets_rts_mean': dados['rts_mean'],
        'last_five_tweets_favs_mean': dados['favs_mean'],
        'last_five_rts_favs_ratio': dados['rts_favs_ratio']
    }])

    # df_scaled = scaler.transform(to_be_scaled)
    df_scaled = scaler_v2.transform(to_be_scaled)

    retro_scaled = pd.DataFrame(df_scaled, columns=to_be_scaled.columns)

    dados_normalizados = {
    'author_follower_count': retro_scaled['author_follower_count'].values[0],
    'author_favourites_count': retro_scaled['author_favourites_count'].values[0],
    'author_verified': dados['is_verified'],
    'account_has_url': dados['has_url'],
    'last_five_tweets_favs_mean': retro_scaled['last_five_tweets_favs_mean'].values[0],
    'last_five_rts_favs_ratio': retro_scaled['last_five_rts_favs_ratio'].values[0],
    'posted_more_than_once': dados['more_than_once'],
    'posted_by_other': dados['by_other']
    }

    return dados_normalizados

    

@app.route('/verificar', methods=['POST'])
def verificar():
    # Obtém os valores dos atributos obtidos no formulário do index.html
    dados = get_acc_info() # dados = obtem_dados_form()

    print(":::::: Mostra alguns dados de teste ::::::")
    print("username: {}".format(dados["username"]))
    print("follower_count: {}".format(dados["follower_count"]))
    print("is_verified: {}".format(dados["is_verified"]))
    print("by_other: {}".format(dados["by_other"]))

    # Normaliza a entrada
    dados_normalizados = normaliza_resposta(dados)

    # Cria array numpy para teste
    teste = np.array([list(dados_normalizados.values())])

    # Faz a predição:
    classe = modelo.predict(teste)[0]
    proba = modelo.predict_proba(teste)
    res_proba = "%5.2f"%(proba[0][1]*100)

    print("Classe Predita: {}".format(str(classe)))
    # Mostra na aplicação qual foi o retorno do modelo
    if classe == 0:
        classe = 'Não'
    else:
        classe = 'Sim'

    # Monta a resposta da predição para a página resultado.html
    resposta = monta_dicionario_resposta(dados, classe, res_proba)

    return render_template('resultado.html', resultado=resposta)

# Executa a aplição na porta 80 (localhost)
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
