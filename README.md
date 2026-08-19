# 🌭 Gestão Financeira — Delivery 

> Sistema web para controle financeiro de pequenos negócios do ramo alimentício, desenvolvido com foco em simplicidade, praticidade e facilidade de uso em dispositivos móveis.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge\&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge\&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge\&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Interactive_Graphics-3F4F75?style=for-the-badge\&logo=plotly)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge\&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📌 Sobre o Projeto

O **Gestão Financeira — Delivery** é uma aplicação web desenvolvida para auxiliar pequenos empreendedores do setor alimentício no controle de suas movimentações financeiras.

A aplicação permite registrar **entradas e saídas**, acompanhar o **lucro líquido**, analisar a **margem de lucro** e visualizar gráficos que facilitam a compreensão dos resultados financeiros do negócio.

O projeto foi pensado especialmente para estabelecimentos como:

* 🌭 Doguerias
* 🍕 Pizzarias
* 🍔 Lanchonetes
* 🛵 Serviços de delivery
* 🍱 Pequenos negócios de alimentação

A interface utiliza um design moderno em **tema escuro**, com elementos visuais inspirados em *post-its*, priorizando uma experiência simples e intuitiva, inclusive em dispositivos móveis.

---

## ✨ Funcionalidades

### 💰 Controle Financeiro

* Cadastro de receitas e despesas.
* Registro de diferentes fontes de entrada, como:

  * WhatsApp
  * iFood
  * MenuDino
  * Vendas presenciais
* Registro de despesas, como:

  * Insumos
  * Embalagens
  * Motoboy
  * Taxas
  * Outros gastos operacionais.

### 📊 Dashboard Financeiro

O painel apresenta automaticamente:

* **Total de Entradas**
* **Total de Saídas**
* **Lucro Líquido**
* **Margem de Lucro (%)**

Os indicadores são atualizados conforme os lançamentos registrados e os filtros selecionados.

### 📈 Gráficos

A aplicação disponibiliza visualizações para facilitar a análise financeira:

* 🍩 **Gráfico de rosca:** distribuição das despesas por categoria.
* 📊 **Gráfico de barras:** comparação entre entradas e saídas ao longo dos meses.

### 🗓️ Filtros

Permite consultar os dados de acordo com:

* Ano
* Mês

Isso facilita a análise do desempenho financeiro em diferentes períodos.

### 📋 Extrato Financeiro

O sistema apresenta as movimentações cadastradas em formato de extrato, permitindo:

* Visualizar os lançamentos.
* Identificar receitas e despesas.
* Consultar valores e categorias.
* Excluir movimentações diretamente pela interface.

### 💾 Persistência de Dados

Os dados são armazenados localmente utilizando **SQLite**, proporcionando uma solução simples e leve, sem necessidade de configurar um servidor de banco de dados externo.

### 📱 Interface

A interface foi desenvolvida pensando também na utilização em dispositivos móveis, priorizando uma experiência simples e acessível durante a rotina do estabelecimento.

---

## 🖥️ Demonstração

> Adicione screenshots ou um GIF da aplicação nesta seção quando disponíveis.

Exemplo de organização:

```text
📊 Dashboard
├── Total de Entradas
├── Total de Saídas
├── Lucro Líquido
└── Margem de Lucro

📋 Movimentações
├── Receitas
├── Despesas
└── Exclusão de lançamentos

📈 Análises
├── Gastos por categoria
└── Entradas x Saídas por mês
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia         | Utilização                       |
| ------------------ | -------------------------------- |
| **Python**         | Linguagem principal              |
| **Streamlit**      | Desenvolvimento da interface web |
| **Pandas**         | Manipulação e análise dos dados  |
| **Plotly Express** | Criação dos gráficos interativos |
| **SQLite3**        | Persistência dos dados           |
| **Git/GitHub**     | Versionamento do projeto         |

---

## 📁 Estrutura do Projeto

```text
gestao-financeira-delivery/
│
├── app.py                  # Aplicação principal
├── requirements.txt        # Dependências do projeto
├── .gitignore              # Arquivos ignorados pelo Git
└── README.md               # Documentação do projeto
```

> O banco de dados SQLite é criado localmente pela aplicação, caso essa seja a configuração utilizada no projeto.

---

## 🚀 Como Executar Localmente

### 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

* [Python 3.9+](https://www.python.org/)
* [Git](https://git-scm.com/)

---

### 1. Clone o repositório

```bash
git clone https://github.com/MaBeatrizBerten/gestao-financeira-delivery.git
```

Entre na pasta do projeto:

```bash
cd gestao-financeira-delivery
```

---

### 2. Crie um ambiente virtual

#### Windows

```bash
python -m venv venv
```

Ative o ambiente virtual:

```bash
venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv venv
```

Ative o ambiente virtual:

```bash
source venv/bin/activate
```

---

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Execute a aplicação

```bash
streamlit run app.py
```

Após executar o comando, o Streamlit disponibilizará a aplicação no navegador.

Acesse:

```text
http://localhost:8501
```

---

## 🔄 Fluxo da Aplicação

O funcionamento básico do sistema segue o seguinte fluxo:

```text
             ┌─────────────────┐
             │     Usuário     │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │   Streamlit     │
             │   Interface     │
             └────────┬────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
   ┌──────────────┐       ┌──────────────┐
   │   Entradas   │       │    Saídas    │
   └──────┬───────┘       └──────┬───────┘
          │                       │
          └───────────┬───────────┘
                      ▼
             ┌─────────────────┐
             │     SQLite      │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │    Pandas /     │
             │     Plotly      │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │    Dashboard    │
             └─────────────────┘
```

---

## 📌 Objetivos do Projeto

O projeto foi desenvolvido com os seguintes objetivos:

* Simplificar o controle financeiro de pequenos negócios.
* Reduzir a dependência de planilhas.
* Facilitar o acompanhamento de receitas e despesas.
* Apresentar informações financeiras de forma visual.
* Permitir acesso rápido pelo celular.
* Praticar o desenvolvimento de aplicações web utilizando Python.

---
