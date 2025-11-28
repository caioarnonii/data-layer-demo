# 📘 Data Layer Demo – API de Consulta e Métricas

Este projeto é um **mini Data Layer** desenvolvido para demonstrar conceitos fundamentais de organização de dados, filtragem, exposições via API e coleta de métricas de uso.
A aplicação foi construída em **Python + FastAPI**, simulando uma camada de consumo de dados estruturados para integrações externas.

---

## 🚀 Funcionalidades

### ✅ Exposição de dados via API

A API lê dados hospedados localmente em um arquivo `sales.json` e os expõe através do endpoint:

* `GET /sales`

Com suporte a:

* **Filtro por status**
* **Filtro por intervalo de datas**
* **Combinação de múltiplos filtros**
* **Retorno com total de itens + dados filtrados**

---

### ✅ Filtros Implementados

#### **Status**

```
/sales?status=paid
```

#### **Intervalo de datas**

```
/sales?start_date=2024-01-01&end_date=2024-02-01
```

#### **Filtros combinados**

```
/sales?status=paid&start_date=2024-01-01
```

---

### ✅ Métricas básicas de uso da API

Um middleware registra:

* Número total de requisições
* Número total de erros
* Endpoint dedicado: `/metrics`

Exemplo de resposta:

```json
{
  "requests_total": 10,
  "errors_total": 1
}
```

---

## 📂 Estrutura do Projeto

```
data-layer-demo/
│── app.py
│── sales.json
│── requirements.txt
└── README.md
```

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **FastAPI**
* **Uvicorn**
* **JSON como fonte de dados**
* Middleware nativo para métricas

---

## ▶️ Como rodar o projeto

### 1. Criar ambiente virtual

```bash
python -m venv venv
```

### 2. Ativar o ambiente virtual

#### Windows:

```bash
venv\Scripts\activate
```

#### Linux/Mac:

```bash
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Rodar a API

```bash
uvicorn app:app --reload --port 8000
```

A API estará disponível em:

```
http://127.0.0.1:8000/sales
```

---

## 📄 Exemplo de Estrutura do `sales.json`

```json
[
  {
    "id": 1,
    "amount": 150.0,
    "status": "paid",
    "date": "2024-01-10"
  },
  {
    "id": 2,
    "amount": 200.0,
    "status": "pending",
    "date": "2024-01-12"
  }
]
```

---

## 📄 Endpoints

# Listar vendas (sem filtros)
GET http://127.0.0.1:8000/sales

# Listar vendas por source
GET "http://127.0.0.1:8000/sales?source=app"

# Listar vendas por status
GET "http://127.0.0.1:8000/sales?status=approved"

# Buscar venda específica
GET http://127.0.0.1:8000/sales/tx_123

# Deletar todas as vendas
DELETE http://127.0.0.1:8000/sales

# Mostrar métricas
GET http://127.0.0.1:8000/metrics


## 🧩 Pontos técnicos demonstrados neste projeto

* Criação de API com FastAPI
* Leitura de dados estruturados em JSON
* Implementação de filtros dinâmicos
* Middleware para observabilidade
* Exposição de métricas de uso da API
* Estrutura simples e organizada para dados
