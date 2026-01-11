# Gerenciador de Árvore B+ - Trabalho II - Banco de Dados II

## Descrição do Projeto
Este documento apresenta o Trabalho II  da disciplina de Banco de Dados II, feito por Miguel Fellipe de Souza Teixeira, desenvolvido como parte do curso de Engenharia de Computação do Instituto Federal de Minas Gerais de Bambuí (IFMG-Bambuí).

O projeto resultante é um **Visualizador Interativo de Árvore B+**, sendo uma aplicação web que simula o funcionamento interno de estruturas de indexação utilizadas em Sistemas Gerenciadores de Banco de Dados (SGBD). O software foi projetado para demonstrar visualmente operações complexas de estruturas de dados, integrando a lógica de particionamento de páginas com uma interface gráfica moderna e feedbacks sensoriais.


## Demonstração
<div align="center">
  <p>Clique na imagem abaixo para assistir ao vídeo de demonstração:</p>

  <a href="https://www.youtube.com/watch?v=Q_PDM4zifNM">
    <img src="https://i.ytimg.com/vi/Q_PDM4zifNM/hqdefault.jpg?" alt="Demonstração da Arvore B+">
  </a>
</div>

## Funcionalidades Principais
O sistema inclui as seguintes mecânicas e recursos implementados:

* **Renderização Dinâmica de Grafos:** Integração com a biblioteca **Mermaid.js** para desenhar a topologia da árvore em tempo real no navegador, diferenciando visualmente nós internos (índices) e nós folhas (dados).
* **Simulação de Páginas de Disco:** Configuração dinâmica onde o usuário define o tamanho da página (em bytes) e o número de campos, permitindo que o algoritmo calcule a ordem da árvore e simule o estouro de memória (*overflow*).
* **Feedback Sonoro:** Integração com sistema de áudio via **Pygame** que emite sons de confirmação ao inserir novos nós na árvore.
* **Operações CRUD Complexas:** Implementação completa dos algoritmos de Inserção (com *split* de nós), Remoção (com fusão/*merge* e redistribuição) e Busca por igualdade ou intervalo.

## Arquitetura do Sistema

### Componentes Principais
* **Main.py:** Ponto de entrada do programa. Gerencia o servidor Flask, processa as requisições HTTP (POST/GET) e coordena o acionamento dos efeitos sonoros.
* **ArvoreB.py:** O núcleo do sistema (*Model*). Contém as classes `Nodo` e `ArvoreBMais`, implementando a lógica matemática de balanceamento, divisão recursiva de filhos e a exportação do grafo para a sintaxe do Mermaid.
* **Style.css:** Gerencia toda a identidade visual.
* **Interface.html:** O front-end da aplicação, responsável por capturar os dados dos formulários e atualizar o desenho SVG da árvore dinamicamente via JavaScript (AJAX).
* **Pygame Mixer:** Módulo integrado ao controlador principal responsável por carregar e executar os arquivos de áudio `.mp3` de forma assíncrona durante as operações.

## Design de interface
**Toda a reformulação visual e implementação front-end foram desenvolvidas pelo aluno Miguel Teixeira.**


## Tecnologias Utilizadas
* **Linguagem de Programação:** Python 3.x
* **Framework Web:** Flask
* **Visualização de Dados:** Mermaid.js
* **Front-end:** HTML5 / CSS3 / JavaScript
* **Áudio:** Pygame Library
* **Persistência:** CSV (Biblioteca Nativa)

## Instalação e Execução
Para rodar este projeto localmente, é necessário ter instalado o **Python 3.x**. Não é necessário configurar servidores de banco de dados externos (como XAMPP/MySQL), pois a estrutura roda em memória e persiste em CSV.

### 1. Instalação das Dependências
Certifique-se de que todos os arquivos do projeto estão na mesma pasta. Abra o terminal nesta pasta e execute o comando para instalar as bibliotecas listadas no `requirements.txt`:

```bash
pip install -r requirements.txt
```
## Autor
* Miguel Fellipe de Souza Teixeira

---
*Trabalho desenvolvido para a disciplina de Banco de Dados II - IFMG Campus Bambuí.*
