import os
from dotenv import load_dotenv
from langchain_core.runnables import chain
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import chain


PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

load_dotenv() 

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")


@chain
def search_prompt(question:None):
    
    if question is None:
        return

    question_template = PromptTemplate(
        input_variables=["contexto", "pergunta"],
        template=PROMPT_TEMPLATE
    )

    model = initialize_chat_model(model="gemini-2.5-flash-lite", temperature=0.5)

    embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection_string=DATABASE_URL,
        use_jsonb=True
    )

    results = vector_store.similarity_search(question, k=10)

    contexto = "\n\n".join([result.page_content for result in results])

    chain = contexto | question_template | model

    resposta = chain.invoke({"pergunta": question})

    return resposta.content