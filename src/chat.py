from langchain.prompts import PromptTemplate
from search import search_prompt


def main():

    template = PromptTemplate(
        input_variables=["question"],
        template="Olá, me faça uma pergunta"
    )
    chain = search_prompt(template)

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    pass

if __name__ == "__main__":
    main()