# Instruções de como rodar a aplicação 

## Preparação do ambiente

### Instale o pipenv 
- Abra o terminal com privilégios de adminstrador e instale o pipenv

```
pip install pipenv
```

### Crie um arquivo .env e coloque a chave de API da OpenAI

```
OPENAI_API_KEY=**********************
```

### Ative o ambiente virtual

```
pipenv shell
```

### Instale as dependências

```
pipenv install
```

## Tutorial com o Chroma (Site do langchain)

### Execute o script para rodar a aplicação

```
python chroma_tutorial.py
```

## Tutorial com o Pgvector (Solução customizada)

### Inicie um container docker com o pgvector

```
docker run --name pgvector-container -e POSTGRES_USER=langchain -e POSTGRES_PASSWORD=langchain -e POSTGRES_DB=langchain -p 6024:5432 -d pgvector/pgvector:pg16
```

### Execute o script para rodar a aplicação

```
python pgvector_tutorial.py
```

## Observações
- O Chroma é um banco de dados vetorial embarcado baseado em Sqlite, que permite o armazenamento em memória e/ou em arquivo.
- O Pgvector é uma extensão do banco de dados PostgreSQL, portanto não é possível armazenar os dados em memória ou arquivo. No momento em que a
variável de vectorstore é iniciada é criada uma tabela chamada 'langchain_pg_embedding' no banco de dados
que pode ser visualizada por um cliente SQL.

## Credenciais de acesso ao banco
```
USUARIO=langchain
SENHA=langchain
BANCO=langchain
PORTA=6024
```