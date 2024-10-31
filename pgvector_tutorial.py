from langchain_postgres import PGVector
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_openai import ChatOpenAI
from uuid import uuid4

# from langchain.globals import set_verbose, set_debug

# set_verbose(True)
# set_debug(True)


docs = [
    Document(
        page_content="A bunch of scientists bring back dinosaurs and mayhem breaks loose",
        metadata={"year": 1993, "rating": 7.7, "genre": "science fiction"},
    ),
    Document(
        page_content="Leo DiCaprio gets lost in a dream within a dream within a dream within a ...",
        metadata={"year": 2010, "director": "Christopher Nolan", "rating": 8.2},
    ),
    Document(
        page_content="A psychologist / detective gets lost in a series of dreams within dreams within dreams and Inception reused the idea",
        metadata={"year": 2006, "director": "Satoshi Kon", "rating": 8.6},
    ),
    Document(
        page_content="A bunch of normal-sized women are supremely wholesome and some men pine after them",
        metadata={"year": 2019, "director": "Greta Gerwig", "rating": 8.3},
    ),
    Document(
        page_content="Toys come alive and have a blast doing so",
        metadata={"year": 1995, "genre": "animated"},
    ),
    Document(
        page_content="Three men walk into the Zone, three men walk out of the Zone",
        metadata={
            "year": 1979,
            "director": "Andrei Tarkovsky",
            "genre": "thriller",
            "rating": 9.9,
        },
    ),
]

connection = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"  # Uses psycopg3!
collection_name = "my_docs"
embeddings_function = OpenAIEmbeddings(model="text-embedding-3-large")

vectorstore = PGVector(
    embeddings=embeddings_function,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)


metadata_field_info = [
    AttributeInfo(
        name="genre",
        description="The genre of the movie. One of ['science fiction', 'comedy', 'drama', 'thriller', 'romance', 'action', 'animated']",
        type="string",
    ),
    AttributeInfo(
        name="year",
        description="The year the movie was released",
        type="integer",
    ),
    AttributeInfo(
        name="director",
        description="The name of the movie director",
        type="string",
    ),
    AttributeInfo(
        name="rating", description="A 1-10 rating for the movie", type="float"
    ),
]

# Essa linha só deve ser executada uma vez, pois é responsável por adicionar os dados no banco. Comente essa linha após a execução do script pela primeira vez
vectorstore.add_documents(docs, ids=[str(uuid4()) for _ in range(len(docs))])

document_content_description = "Brief summary of a movie"
llm = ChatOpenAI(temperature=0)
retriever = SelfQueryRetriever.from_llm(
    llm,
    vectorstore,
    document_content_description,
    metadata_field_info,
)

# This example only specifies a filter
result_1 = retriever.invoke("I want to watch a movie rated lower than 8.0")
print(result_1)

## This example specifies a query and a filter
# result_2 = retriever.invoke("Has Greta Gerwig directed any movies about women")
# print(result_2)

## This example specifies a composite filter
# result_3 = retriever.invoke("What's a highly rated (above 8.5) science fiction film?")
# print(result_3)

## This example specifies a query and composite filter
# result_4 = retriever.invoke(
#     "What's a movie after 1990 but before 2005 that's all about toys, and preferably is animated"
# )
# print(result_4)


## This example only specifies a relevant query
# result_5 = retriever.invoke("What are two movies about dinosaurs")
# print(result_5)