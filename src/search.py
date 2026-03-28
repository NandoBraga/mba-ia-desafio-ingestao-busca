import os
from dotenv import load_dotenv
from langchain_core.runnables import chain
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
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
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
DATABASE_URL = os.getenv("DATABASE_URL")

if not all([OPENAI_EMBEDDING_MODEL, PG_VECTOR_COLLECTION_NAME, DATABASE_URL]):
    raise ValueError("Certifique-se de que todas as variáveis de ambiente necessárias estão definidas: OPENAI_EMBEDDING_MODEL, PG_VECTOR_COLLECTION_NAME, DATABASE_URL")

def search_prompt(question:None, k:int=10):

    if question is None:
        return

    embeddings = OpenAIEmbeddings(
        model=OPENAI_EMBEDDING_MODEL
    )

    if not embeddings:
        print("Falha ao criar embeddings. Verifique as configurações do OpenAI.")
        raise SystemExit(0)

    store = PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True
    )

    if not store:
        print("Falha ao conectar ao PGVector. Verifique as configurações do banco de dados.")
        raise SystemExit(0)

    results = store.similarity_search_with_score(question, k=k)

    if not results:
        return "Não tenho informações necessárias para responder sua pergunta."

    output = []
    
    for i, (doc, score) in enumerate(results, start=1):
        output.append("="*50)
        output.append(f"Resultado {i} (score: {score:.2f}):")
        output.append("="*50)

        output.append("\nTexto:\n")
        output.append(doc.page_content.strip())

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["contexto", "pergunta"]
    ).format(contexto="\n\n".join(output), pergunta=question)
    
    llm = ChatOpenAI(
        model="gpt-5-nano", 
        openai_api_key=OPENAI_API_KEY,
        temperature=0)
    
    return llm.invoke(prompt)

if __name__ == "__main__":
    search_prompt()
