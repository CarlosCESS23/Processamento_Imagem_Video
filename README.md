# Ferramenta de processamento de imagem e video

## Programa de processamento de imagens e video com Visão Computacional

Este projeto utiliza o Python, usando a biblioteca de visão computacional para fazer o processamento de imagem e video

## Conteúdo

- [Pré-requisito](#pré-requisito)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Como Começar](#como-começar)
  - [1. Instalação de Python](#1-InstalacaoPython)
  - [2.Instalação das bibliotecas necessárias](#2-bibliotecas_necessárias)
- [Clone ou baixe os arquivos](#clone-ou-baixe-os-arquivos)
- [Objetivos do Programa](#objetivo_programa)
- [Funcionalidade do Programa](#funcionalidade_do_programa)
- [Forma de Execução](#forma-execucao)
- [Referências](#referencias)


  ## Pré-requisito:

  - Sistema Operacional: Linux, Windows e Mac
  - Anaconda instalado[Instrução de Instalação do Anaconda](https://www.anaconda.com/download)
  - Versão do Python: acima de 3.10
  - Bibliotecas:
    - OpenCV: Processamento de imagens e vídeos.
    - Customtkinter: Interface gráfica moderna
    - Numpy: Manipulações de vetores/Matrizes (Usado para o OpenCV)
    - PIL: Conversão de imagens OpenCV

  ## Estrutura do Projeto

  ```
   .
   └── ProcessamentoImagemVideo.py
   └── README.md
   └── Mídia
          └── <arquivos_imagem>
  
  ```

  ## Como Começar

### 1. Instalação de Python

Se optou por instalar o **Anaconda**, o Python já vem íncluido, caso não queira utilizar a versão incluída, pode criar novo ambiente com a versão que você deseja, mas lembrando de instalar a versão superior à 3.10, segue o código para o novo ambiente (Opcional)

Abrindo o terminal, execute o seguintes comandos:

```bash 
#Criando um novo ambiente Conda (É opcional, mas recomendado)
conda create -n Py311 python=3.11

#Após criar o ambiente, ative o ambiente

conda activate Py311
```

### 2. Instalação das bibliotecas necessárias

Com Anaconda instalado e o ambiente já criado que é uma forma de instalar as bibliotecas de forma isolada, evitando o conflito com outros projetos, novamente com terminal aberto, execute os seguintes comandos para instalar as bibliotecas necessários:

```bash

pip install opencv-python customtkinter numpy Pillow 

```

## Clona ou baixar os arquivos

Para obter o código do projeto,você pode clonar o repositório utilizando Git

```bash
git clone https://github.com/CarlosCESS23/Processamento_Imagem_Video

```

Ou, se preferir, pode baixar o arquivo do tipo `.zip` do repositório e faça extração

## Objetivos do Programa

Este programa foi desenvolvido com os seguintes objetivos:

* Fornecer uma ferramenta acessível para o **processamento básico e avançado de imagens e vídeos** 
* Oferece uma **interface gŕafica intuitiva** para facilitar a interação com as funcionalidade do programa
* Servir como base para **projetos futuros envolvendo análise e manipulação de midia visual**
* Demonstrar uma aplicação prática de **conceitos de visão computacional** utilizando a biblioteca OpenCV

## Funcionalidade do programa

- ### **Abrir e processar**:
O programa oferece variedade de tipos de arquivos para abrir, os **arquivos de imagem** (`.png`,`.jpg`,`.jpeg`,`.bmp``.gif`)
arquivos tipos video (`.mp4`) e também faz a **captura de stream da webcam**

- ### Aplicação de filtros:

O programa oferece várias aplcaições de filtros, como:

- **Shapen:** Aumenta a nitidez da imagem.
- **Blur:** Suaviza a imagem e remove ruídos
- **Emboss:** Cria um efeito de relevo
- **Laplacian:** Destaca as bordas na imagem
- **Canny:** Realiza detecção de bordas com alta precisão
- **Gray:** Converte a imagem para tons de cinza
- **Sobel:** Detecta gradientes e bordas verticais/horizontais
- **Binary:** Converte a imagem para preto e branco (binário)
- **Cores Normais:** Retorna a imagem às cores originais
- **Desfazer os filtros:** Remove o último filtro aplicado, permitindo experimentar e corrigir.

- ### Região de interesse (ROI)

Permite selecionar uma **área específica da imagem/video** para aplicar os filtros

## Forma de execução

Depois de seguir os passos de instalação e ter os arquivos do projeto, execute o programa dessa forma:

1. Ative o ambiente Conda que contém as bibliotecas necessárias:

```bash

conda activate py311

```

2. Execute o Script Python:
   Navegue até diretorio onde você salvou o arquivo e execute seguinte comando com o Python

```bash

python processamentoImagemVideo.py
   
```

## Guia de orientação do uso:

### Interface Principal

<img src="https://github.com/CarlosCESS23/Processamento_Imagem_Video/blob/main/ImagemAplicativ.png" alt="Interface Gráfica preta">

Imagem acima mostra como é a interface criada!!!

A interface da aplicação é dividida em algumas seções:

- **Controle superiores**:
  - **"Abrir Imagem":** Clique para selecionar e carregar um arquivo de imagem
  - **"Abrir a Webcam":** Inicia a transmissão pela sua webcam
  - **"Abrir Video":** Clique para selecionar e carregar um arquivo de video

- **Área de Visualização** (Canva) 
  - A região preta central onde a imagem ou video é exibido

- **Controle Inferiores** (Filtors e Ações)
  - **"Selecionar ROI:"** Ativa/desativa o modo de seleção de Região de Interesse
  - **"Botões de Filtro:"** Cada botão aplica um filtro específico à imagem ou à ROI
  - **"Desfazer":** Remove o último filtro aplicado
  - **"Salvar":** Salva a imagem atual ( ou a ROI, caso seja selecionada) como um arquivo PNG









  
  

  

