📊 Dashboard com Streamlit e Docker

Este projeto é um dashboard interativo feito em Python + Streamlit, empacotado em um container Docker.
O app exibe análises visuais e atualiza automaticamente sempre que o código for salvo localmente.

🚀 Tecnologias utilizadas

🐍 Python 3.12

📊 Streamlit

🐋 Docker

📦 Pandas / Plotly Express

📂 Estrutura do projeto
example_01/
├── app.py               # Código principal do dashboard
├── requirements.txt     # Dependências Python
└── Dockerfile           # Configuração da imagem Docker

⚙️ Pré-requisitos

Antes de começar, instale:

Docker Desktop

(Opcional) VS Code
 com a extensão Docker e Python

🧱 1️⃣ Build da imagem

Abra o terminal na pasta do projeto:

cd C:\Users\2402431\Desktop\example_01


E construa a imagem com:

docker build -t meu-dashboard:1.0 .

▶️ 2️⃣ Executar o container
✅ Modo normal (rodar apenas)

Roda o dashboard normalmente:

docker run -d -p 8501:8501 --name dashboard meu-dashboard:1.0


Acesse em: http://localhost:8501

🔁 Modo desenvolvimento (auto reload a cada Ctrl+S)

Para atualizar automaticamente o app ao salvar o arquivo:

docker run --rm -p 8501:8501 ^
  -v "C:\Users\2402431\Desktop\example_01:/app" ^
  meu-dashboard:1.0 ^
  streamlit run app.py --server.address=0.0.0.0 --server.port=8501 --server.runOnSave true


💡 Isso faz o container:

Montar o diretório local /app (permitindo salvar alterações)

Recarregar automaticamente o Streamlit (--server.runOnSave true)

Encerrar sozinho ao fechar o terminal (--rm)

🧰 3️⃣ Parar ou remover o container

Se você rodou no modo normal (-d), pare o container:

docker stop dashboard


E se quiser removê-lo:

docker rm dashboard

🧩 4️⃣ Exemplo do Dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Expor porta para o Streamlit
EXPOSE 8501

# Comando padrão
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]

🧾 5️⃣ Exemplo do requirements.txt
streamlit
pandas
plotly
requests

🌐 Acesso

Abra o navegador em:

👉 http://localhost:8501

# ---------EXEMPLO 04 -----------------

Este projeto é uma aplicação completa de **análise e gerenciamento de vendas** de consoles, assinaturas e acessórios de videogames.  
Ele utiliza uma arquitetura moderna baseada em **microsserviços**, com **FastAPI (back-end)**, **PostgreSQL (banco de dados)** e **Streamlit (dashboard interativo)**, todos orquestrados via **Docker Compose**.

---

## 🧩 Estrutura do Projeto

```
📁 projeto/
│
├── 📁 api/                 # Serviço da API (FastAPI)
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── 📁 dashboard/           # Serviço de Dashboard (Streamlit)
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
│
├── init.sql                # Script para criar tabela e inserir dados iniciais
├── docker-compose.yml      # Arquivo de orquestração dos serviços
└── README.md               # Este arquivo 😄
```

---

## 🐳 Tecnologias Utilizadas

| Componente | Descrição |
|-------------|------------|
| **FastAPI** | Framework Python moderno para criação de APIs RESTful. |
| **Streamlit** | Framework para criação de dashboards e apps de dados. |
| **PostgreSQL** | Banco de dados relacional robusto e confiável. |
| **Docker Compose** | Ferramenta para orquestrar múltiplos containers. |
| **Plotly Express** | Biblioteca para criação de gráficos interativos. |
| **Pandas** | Manipulação e análise de dados em Python. |

---

## ⚙️ Funcionalidades

### 🔹 API (FastAPI)
- Endpoint para listar todas as vendas:  
  `GET /vendas`
- Endpoint para filtrar vendas por categoria:  
  `GET /vendas/categoria/{categoria}`
- Endpoint de análise agregada (por categoria):  
  `GET /vendas/analise`
- Endpoint para adicionar novas vendas:  
  `POST /vendas`

### 🔹 Dashboard (Streamlit)
- Exibe **indicadores (KPIs)** de desempenho:
  - Receita total 💰  
  - Total de vendas 🛒  
  - Ticket médio 🏷️  
- Gráficos interativos:
  - Receita total por categoria (barras)
  - Proporção de vendas (pizza)
  - Evolução temporal das receitas (linha)
- Tabela detalhada das vendas
- Filtro por categoria
- Exportação dos dados em CSV
- Formulário para inserir novas vendas diretamente do dashboard

---

## 🗃️ Estrutura do Banco de Dados

```sql
CREATE TABLE vendas (
    id SERIAL PRIMARY KEY,
    data_venda DATE NOT NULL,
    produto VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    quantidade INT NOT NULL
);
```

### 🧠 Dados iniciais
O arquivo `init.sql` é executado automaticamente no primeiro build e insere alguns registros de exemplo no banco, como:

| Produto | Categoria | Valor | Quantidade |
|----------|------------|--------|-------------|
| Xbox Series S | Console | 1970.00 | 45 |
| PS5 | Console | 3200.00 | 15 |
| PS Plus | Assinatura | 95.00 | 425 |
| Headset Gamer | Acessórios | 350.00 | 21 |

---

## 🚀 Como Executar o Projeto

### 1️⃣ Pré-requisitos
Certifique-se de ter instalado:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

---

### 2️⃣ Subir os containers

No diretório raiz do projeto, execute:

```bash
docker-compose up --build
```

Esse comando irá:
- Criar o banco PostgreSQL com dados iniciais (`init.sql`)
- Iniciar a API FastAPI (porta `8000`)
- Iniciar o dashboard Streamlit (porta `8501`)

---

### 3️⃣ Acessar os serviços

| Serviço | URL | Descrição |
|----------|------|-----------|
| **Dashboard (Streamlit)** | [http://localhost:8501](http://localhost:8501) | Interface interativa para análise das vendas |
| **API FastAPI** | [http://localhost:8000/docs](http://localhost:8000/docs) | Documentação interativa da API (Swagger) |
| **Banco de Dados (PostgreSQL)** | `localhost:5432` | Pode ser acessado via PgAdmin ou DBeaver |

## ---

## 🔄 Atualização automática de código

Durante o desenvolvimento:
- O **Streamlit** e a **API FastAPI** possuem volumes montados (`volumes: ./api:/app` e `./dashboard:/app`), permitindo **recarregamento automático** sem rebuild do container.

---

## 🧰 Variáveis de Ambiente

| Serviço | Variável | Descrição | Valor Padrão |
|----------|-----------|------------|---------------|
| **db** | `POSTGRES_USER` | Usuário do banco | `analista` |
| | `POSTGRES_PASSWORD` | Senha do banco | `segredo` |
| | `POSTGRES_DB` | Nome do banco | `datawarehouse` |
| **api** | `DATABASE_URL` | URL de conexão | `postgresql://analista:segredo@db:5432/datawarehouse` |
| **dashboard** | `API_URL` | URL da API | `http://api:8000` |

---

## 📊 Exemplo de Dashboard

- **Gráfico de barras** mostrando receita total por categoria  
- **Gráfico de pizza** com a proporção de vendas  
- **Gráfico temporal** com evolução das receitas  
- **Cards com métricas de desempenho (KPIs)**  
- **Tabela interativa** com todos os registros

---

## 💾 Persistência de Dados

Os dados são armazenados em um volume Docker:

```yaml
volumes:
  postgres_data:
```

Assim, mesmo que os containers sejam reiniciados, as informações permanecem salvas.

---

## 🧑‍💻 Autor

**FIilipe Machado** <br/>
**Guilherme Oliveira** <br/>
**Carlos Eduardo**  
💼 Projeto desenvolvido para fins de estudo e prática de integração entre **Docker, FastAPI, PostgreSQL e Streamlit**.

----
