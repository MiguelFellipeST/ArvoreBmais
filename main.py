from flask import Flask, render_template, request, jsonify  # Importa as funcionalidades do Flask
from arvoreB import ArvoreBMais  # Importa a classe ArvoreBMais do módulo arvoreB
import csv  # Importa a biblioteca csv para manipulação de arquivos CSV
from random import randint  # Importa a função randint para gerar números aleatórios
import time  # Importa a biblioteca time para medir o tempo de execução
import pygame  # Importa a biblioteca pygame para som.mp3
import os  # Importa o módulo os para verificação de arquivos

app = Flask(__name__)  # Cria a instância do aplicativo Flask

# Inicializa o mixer de som do Pygame
try:
    pygame.mixer.init()
    CAMINHO_SOM = "som.mp3"  
    print("Som funcionando")
except Exception as e:
    print(f"Erro no áudio: {e}")

# Caminho do arquivo CSV que será carregado
caminho_csv = r"C:\Users\Miguel\Desktop\Trabalho Banco de Dados II\ArvoreB\output.csv"

# Variável global que armazenará a árvore B+
arvore = None

def carregar_dados_csv(caminho):
    """Função que carrega dados de um arquivo CSV para a árvore B+."""  
    global arvore  # Usa a variável global arvore
    try:
        # Abre o arquivo CSV para leitura e garante que o arquivo tenha a codificação correta
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            linhas = csv.reader(arquivo)  # Lê o arquivo CSV
            next(linhas)  # Ignora a primeira linha (cabeçalho)
            for linha in linhas:  # Itera por cada linha do arquivo CSV
                chave, *valores = linha  # Desempacota a linha em chave e valores
                chave = int(chave)  # Converte a chave para inteiro
                valores = list(map(int, valores))  # Converte os valores para inteiros
                arvore.inserir(chave, valores)  # Insere os dados na árvore B+
        print("Dados carregados com sucesso!")  # Mensagem de sucesso
    except FileNotFoundError:
        print(f"Arquivo não encontrado em {caminho}")  # Se o arquivo não for encontrado
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")  # Para qualquer outro erro

def medir_tempo(funcao, *args, **kwargs):
    """Função para medir o tempo de execução de outra função."""
    inicio = time.time()  # Marca o tempo de início
    resultado = funcao(*args, **kwargs)  # Executa a função recebida com os parâmetros passados
    fim = time.time()  # Marca o tempo de fim
    tempo_execucao = fim - inicio  # Calcula a diferença de tempo (tempo de execução)
    return resultado, tempo_execucao  # Retorna o resultado da função e o tempo de execução

@app.route('/')  # Define a rota principal ('/') da aplicação
def index():
    return render_template('interface.html')  # Renderiza o arquivo HTML da interface para o usuário

@app.route('/iniciar', methods=['POST'])  # Define a rota para iniciar a árvore B+ (só aceita POST)
def iniciar():
    global arvore  # Refere-se à variável global arvore
    n_campos = int(request.form['n_campos'])  # Obtém o número de campos a partir do formulário enviado pelo usuário
    tamanho_pagina = int(request.form['tamanho_pagina'])  # Obtém o tamanho da página também a partir do formulário
    arvore = ArvoreBMais(n_campos=n_campos, tamanho_pagina=tamanho_pagina)  # Cria a árvore B+ com os parâmetros

    # Chama a função para carregar os dados do CSV para a árvore
    # ATENÇÃO: Se der erro de arquivo não encontrado, comente a linha abaixo para testar
    carregar_dados_csv(caminho_csv)
    
    # Gera o código Mermaid
    diagrama = arvore.exportar_para_mermaid()
    
    return jsonify({"message": "Árvore B+ iniciada e dados carregados!", "diagrama": diagrama})  # Retorna uma resposta JSON com o diagrama

@app.route('/inserir', methods=['POST'])  # Define a rota para inserir dados na árvore (só aceita POST)
def inserir():
    global arvore  # Refere-se à variável global arvore
    if not arvore:  # Verifica se a árvore não foi inicializada
        return jsonify({"error": "Árvore não iniciada!"}), 400  # Se não foi, retorna um erro 400
    
    chave = int(request.form['chave'])  # Pega a chave do formulário enviado pelo usuário
    # Cria um dicionário com valores aleatórios para os campos da árvore
    valor = {f"A{i+1}": randint(0, 1000) for i in range(arvore.n_campos)}

    # Mede o tempo de inserção do novo valor na árvore
    resultado, tempo_insercao = medir_tempo(arvore.inserir, chave, valor)
    
    # Toca o som de inserção
    try:
        if os.path.exists(CAMINHO_SOM):
            pygame.mixer.music.load(CAMINHO_SOM)
            pygame.mixer.music.play()
    except Exception as e:
        print(f"Erro ao tocar som: {e}")

    # Gera o código Mermaid atualizado
    diagrama = arvore.exportar_para_mermaid()

    return jsonify({"message": f"Chave {chave} inserida em {tempo_insercao:.4f} segundos.", "diagrama": diagrama})  # Retorna uma resposta com o diagrama

@app.route('/remover', methods=['POST'])  # Define a rota para remover dados da árvore (só aceita POST)
def remover():
    global arvore  # Refere-se à variável global arvore
    if not arvore:  # Verifica se a árvore não foi inicializada
        return jsonify({"error": "Árvore não iniciada!"}), 400  # Se não foi, retorna um erro 400
    
    chave = int(request.form['chave'])  # Pega a chave do formulário

    # Mede o tempo para remover a chave da árvore
    resultado, tempo_remocao = medir_tempo(arvore.remover, chave)
    
    # Gera o código Mermaid atualizado
    diagrama = arvore.exportar_para_mermaid()

    return jsonify({"message": f"Chave {chave} removida em {tempo_remocao:.4f} segundos.", "diagrama": diagrama})  # Retorna o tempo e o diagrama

@app.route('/buscar', methods=['POST'])  # Define a rota para buscar dados na árvore (só aceita POST)
def buscar():
    global arvore  # Variável global arvore
    if not arvore:  # Verifica se a árvore não foi inicializada
        return jsonify({"error": "Árvore não iniciada!"}), 400  # Se não foi, retorna um erro 400
    
    chave = int(request.form['chave'])  # Pega a chave do formulário

    # Mede o tempo para buscar a chave na árvore
    resultado, tempo_busca = medir_tempo(arvore.buscar, chave)
    if resultado:
        return jsonify({"message": f"Chave {chave} encontrada com valor: {resultado} em {tempo_busca:.4f} segundos."})
    else:
        return jsonify({"error": f"Chave {chave} não encontrada!"}), 404  # Se não encontrar a chave retorna erro 404

@app.route('/busca_intervalo', methods=['POST'])  # Define a rota para busca em intervalo 
def busca_intervalo():
    global arvore  # Variável global arvore
    if not arvore:  # Verifica se a árvore não foi inicializada
        return jsonify({"error": "Árvore não iniciada!"}), 400  # Se não foi, retorna um erro 400
    
    inicio = int(request.form['inicio'])  # Pega o início do intervalo do formulário
    fim = int(request.form['fim'])  # Pega o fim do intervalo do formulário

    # Mede o tempo de busca no intervalo da árvore
    resultados, tempo_busca_intervalo = medir_tempo(arvore.busca_intervalo, inicio, fim)
    if resultados:
        return jsonify({"resultados": resultados, "tempo_busca_intervalo": f"{tempo_busca_intervalo:.4f} segundos"})
    else:
        return jsonify({"error": "Nenhuma chave encontrada no intervalo!"}), 404  # Se não encontrar nada no intervalo retorna erro 404

if __name__ == '__main__':
    app.run(debug=True)  # Inicia o servidor Flask