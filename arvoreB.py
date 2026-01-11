import csv  # Importa o módulo CSV para manipulação de arquivos CSV

class Nodo:
    def __init__(self, eh_folha=True):
        # Inicializa um nodo com o parâmetro 'eh_folha' (se o nodo é folha ou não)
        # 'chaves' são as chaves do nodo, e 'filhos' são os filhos do nodo.
        self.eh_folha = eh_folha  # Define se o nodo é uma folha (por padrão, True)
        self.chaves = []  # Lista de chaves armazenadas no nodo
        self.filhos = []  # Lista de filhos do nodo

class ArvoreBMais:
    def __init__(self, n_campos=1, tamanho_pagina=4096):
        # Inicializa a árvore B+ com o número de campos por chave e o tamanho da página
        self.raiz = Nodo()  # Inicializa a raiz como um nodo
        self.n_campos = n_campos  # Define o número de campos por chave
        self.tamanho_pagina = tamanho_pagina  # Define o tamanho da página da árvore
        self.ordem = self.calcular_ordem()  # Calcula a ordem da árvore com base no tamanho da página

    def calcular_ordem(self):
        #Calcula o número máximo de chaves baseado no tamanho da página e nos campos.#
        tamanho_chave = 4  # Supondo que cada chave é um inteiro (4 bytes)
        tamanho_registro = tamanho_chave * self.n_campos  # Calcula o tamanho do registro por chave
        tamanho_metadata = 16  # Sobrecarga para ponteiros/metadata
        max_registros = (self.tamanho_pagina - tamanho_metadata) // tamanho_registro  # Calcula o número máximo de registros
        return max(2, max_registros)  # Retorna a ordem mínima de 2

    def chave_existe(self, chave):
        #Verifica se a chave já existe na árvore.#
        return self._buscar(self.raiz, chave) is not None  # Retorna True se a chave for encontrada, False caso contrário

    def inserir(self, chave, valor):
        if self.chave_existe(chave):  # Verifica se a chave já existe
            print(f"Chave {chave} já existe na árvore!")  # Exibe mensagem de erro se a chave já existir
            return  # Não insere a chave se ela já existir

        raiz = self.raiz  # Obtém a raiz da árvore
        if len(raiz.chaves) == self.ordem - 1:  # Verifica se a raiz está cheia
            nova_raiz = Nodo(eh_folha=False)  # Cria uma nova raiz que não é folha
            nova_raiz.filhos.append(self.raiz)  # Adiciona a raiz antiga como filho da nova raiz
            self.dividir_filho(nova_raiz, 0)  # Divide o filho da nova raiz
            self.raiz = nova_raiz  # Atualiza a raiz da árvore
        self._inserir_nao_cheio(self.raiz, chave, valor)  # Insere a chave e o valor na árvore

    def _inserir_nao_cheio(self, nodo, chave, valor):
        if nodo.eh_folha:  # Se o nodo for folha, insere a chave e o valor
            nodo.chaves.append((chave, valor))  # Adiciona a chave e o valor no nodo
            nodo.chaves.sort()  # Ordena as chaves
        else:
            i = len(nodo.chaves) - 1  # Começa da última chave
            while i >= 0 and chave < nodo.chaves[i][0]:  # Procura o lugar correto para inserir
                i -= 1
            i += 1  # Avança o índice para o filho adequado
            filho = nodo.filhos[i]  # Obtém o filho correspondente
            if len(filho.chaves) == self.ordem - 1:  # Se o filho está cheio, divide-o
                self.dividir_filho(nodo, i)
                if chave > nodo.chaves[i][0]:  # Verifica se a chave é maior que a chave no nodo pai
                    i += 1
            self._inserir_nao_cheio(nodo.filhos[i], chave, valor)  # Chama recursivamente para o filho

    def dividir_filho(self, pai, indice):
        nodo = pai.filhos[indice]  # Obtém o filho que será dividido
        meio = len(nodo.chaves) // 2  # Encontra o índice do meio da chave
        chave_divisao = nodo.chaves[meio][0]  # A chave de divisão será a chave no meio

        # Cria os filhos esquerdo e direito da divisão
        filho_esquerdo = Nodo(eh_folha=nodo.eh_folha)  
        filho_esquerdo.chaves = nodo.chaves[:meio]  # Chaves do filho esquerdo

        filho_direito = Nodo(eh_folha=nodo.eh_folha)
        filho_direito.chaves = nodo.chaves[meio + 1:]  # Chaves do filho direito

        if not nodo.eh_folha:  # Se o nodo não for folha, divide também os filhos
            filho_esquerdo.filhos = nodo.filhos[:meio + 1]
            filho_direito.filhos = nodo.filhos[meio + 1:]

        # Atualiza o nodo pai com a chave de divisão
        pai.chaves.insert(indice, (chave_divisao, None))  # Insere a chave de divisão no pai
        pai.filhos[indice] = filho_esquerdo  # Atualiza o filho esquerdo no pai
        pai.filhos.insert(indice + 1, filho_direito)  # Insere o filho direito no pai

    def buscar(self, chave):
        return self._buscar(self.raiz, chave)  # Chama o método recursivo de busca

    def _buscar(self, nodo, chave):
        if nodo.eh_folha:  # Se o nodo for folha, busca na lista de chaves
            for k, v in nodo.chaves:
                if k == chave:
                    return v  # Retorna o valor associado à chave
            return None  # Retorna None se a chave não for encontrada
        else:
            i = 0
            while i < len(nodo.chaves) and chave > nodo.chaves[i][0]:  # Percorre as chaves
                i += 1
            return self._buscar(nodo.filhos[i], chave)  # Chama recursivamente para o filho adequado

    def busca_intervalo(self, inicio, fim):
        resultados = []  # Lista para armazenar os resultados da busca
        self._busca_intervalo(self.raiz, inicio, fim, resultados)  # Chama o método recursivo para o intervalo
        return resultados  # Retorna os resultados da busca

    def _busca_intervalo(self, nodo, inicio, fim, resultados):
        if nodo.eh_folha:  # Se o nodo for folha, busca no intervalo
            for k, v in nodo.chaves:
                if inicio <= k <= fim:
                    resultados.append((k, v))  # Adiciona a chave e valor aos resultados
        else:
            for i, (k, _) in enumerate(nodo.chaves):
                if inicio <= k:
                    self._busca_intervalo(nodo.filhos[i], inicio, fim, resultados)  # Busca no filho correspondente
                if k > fim:
                    return
            self._busca_intervalo(nodo.filhos[-1], inicio, fim, resultados)  # Busca no último filho

    def remover(self, chave):
        print(f"Operação de remoção para a chave {chave} iniciada.")
        if self.raiz is None:
            print("Árvore vazia.")
            return

        self._remover(self.raiz, chave)
        if len(self.raiz.chaves) == 0 and not self.raiz.eh_folha:
            self.raiz = self.raiz.filhos[0]
            print("Altura da árvore diminuiu, nova raiz definida") 

    def _remover(self, nodo, chave):
        if nodo.eh_folha:  # Se o nodo for folha, remove a chave diretamente
            if chave in [k for k, v in nodo.chaves]:
                nodo.chaves = [kv for kv in nodo.chaves if kv[0] != chave]  # Remove a chave
                if len(nodo.chaves) == 0 and nodo == self.raiz:  # Se a raiz ficar vazia
                    self.raiz = Nodo()  # Torna a raiz um novo nodo vazio
                return True  # Retorna True se a chave for removida
            return False  # Retorna False se a chave não for encontrada
        else:
            i = 0
            while i < len(nodo.chaves) and chave > nodo.chaves[i][0]:  # Procura a chave no nodo
                i += 1
            if i < len(nodo.chaves) and chave == nodo.chaves[i][0]:  # Se a chave estiver no nodo interno
                # A chave está em um nodo interno, substitui por chave de maior valor à esquerda ou direita
                if len(nodo.filhos[i].chaves) >= self.ordem // 2:
                    maior_chave = self._remover_max(nodo.filhos[i])
                    nodo.chaves[i] = (maior_chave, None)
                    return True
                elif len(nodo.filhos[i + 1].chaves) >= self.ordem // 2:
                    menor_chave = self._remover_min(nodo.filhos[i + 1])
                    nodo.chaves[i] = (menor_chave, None)
                    return True
                else:
                    self._fundir(nodo, i)  # Se os filhos tiverem menos da metade das chaves, funde nós
                    return self._remover(nodo.filhos[i], chave)
            else:
                if self._remover(nodo.filhos[i], chave):  # Se a chave estiver no filho
                    if len(nodo.filhos[i].chaves) < self.ordem // 2:  # Verifica se o filho ficou com poucas chaves
                        self._fundir(nodo, i)
                    return True
            return False  # Retorna False se a chave não for encontrada

    def _remover_max(self, nodo):
        #Remove a chave máxima de um nodo e retorna seu valor.
        if nodo.eh_folha:
            return nodo.chaves[-1][0]
        return self._remover_max(nodo.filhos[-1])  # Chama recursivamente para o último filho

    def _remover_min(self, nodo):
        #Remove a chave mínima de um nodo e retorna seu valor.
        if nodo.eh_folha:
            return nodo.chaves[0][0]
        return self._remover_min(nodo.filhos[0])  # Chama recursivamente para o primeiro filho

    def _fundir(self, nodo, indice):
        #Funde dois filhos de um nodo.# 
        filho_esquerdo = nodo.filhos[indice]  # Filho esquerdo
        filho_direito = nodo.filhos[indice + 1]  # Filho direito
        chave_pai = nodo.chaves[indice][0]  # Chave do pai a ser movida para o meio

        # Junta os filhos
        filho_esquerdo.chaves.append((chave_pai, None))  # Adiciona a chave do pai no filho esquerdo
        filho_esquerdo.chaves.extend(filho_direito.chaves)  # Junta as chaves do filho direito
        filho_esquerdo.filhos.extend(filho_direito.filhos)  # Junta os filhos do filho direito

        # Atualiza o nodo pai
        nodo.chaves = [kv for i, kv in enumerate(nodo.chaves) if i != indice]
        nodo.filhos = [filho for i, filho in enumerate(nodo.filhos) if i != indice + 1]

    def exportar_para_mermaid(self):
        if self.raiz is None or len(self.raiz.chaves) == 0:
            return "graph TD;\nMinhaArvore[Árvore Vazia];"

        linhas = ["graph TD"]
        fila = [self.raiz]
        
        ids_nodos = {id(self.raiz): "Raiz"}
        contador = 0

        while fila:
            nodo_atual = fila.pop(0)
            id_atual = ids_nodos[id(nodo_atual)]
            
            chaves_str = " | ".join([str(k[0]) for k in nodo_atual.chaves])
            label = f'"{chaves_str}"'
            
            linhas.append(f'{id_atual}[{label}]')
            
            if nodo_atual.eh_folha:
                 linhas.append(f'style {id_atual} fill:#fbf5ef,stroke:#8b6d9c,stroke-width:2px,color:#272744')
            else:
                 linhas.append(f'style {id_atual} fill:#494d7e,stroke:#272744,stroke-width:2px,color:#fff')

            if not nodo_atual.eh_folha:
                for i, filho in enumerate(nodo_atual.filhos):
                    contador += 1
                    id_filho = f"No{contador}"
                    ids_nodos[id(filho)] = id_filho
                    
                    linhas.append(f'{id_atual} --o {id_filho}')
                    fila.append(filho)
        
        return "\n".join(linhas)