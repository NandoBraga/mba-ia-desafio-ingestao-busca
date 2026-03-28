from search import search_prompt

def main():

    print("Olá! Bem-vindo ao assistente de perguntas do Faturamento. Por favor, faça sua pergunta ou digite sair para encerrar a conversa.")

    while True:
        user_input = input("Você: ")

        if user_input.lower() == "sair":
            print("Assistente: Até logo! Se precisar de mais ajuda, estarei aqui.")
            break

        resposta = search_prompt(user_input)

        if not resposta:
            resposta = "Não tenho informações necessárias para responder sua pergunta."

        print(f"Assistente: {resposta}")

if __name__ == "__main__":
    main()