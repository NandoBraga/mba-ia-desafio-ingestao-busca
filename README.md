# Desafio MBA Engenharia de Software com IA - Full Cycle

## Configuração do Ambiente

Para configurar o ambiente e instalar as dependências do projeto, siga os passos abaixo:

1. **Criar e ativar um ambiente virtual (`venv`):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

2. **Instalar as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar as variáveis de ambiente:**

   - Duplique o arquivo `.env.example` e renomeie para `.env`
   - Preencher variável OPENAI_API_KEY com sua respectiva chave

4. **Iniciando Docker
   ```bash
   docker compose up -d
   ```
   
## Execução do projeto

1. **Inserindo dados do PDF
    ```bash
    python src/ingest.py
   ```
   - O script irá ler o PDF `document.pdf´, separa em chunks e salva vetorizado no banco

2. **Iniciando o chat
   ```bash
   python src/chat.py
   ```

Perguntas fora do contexto retornam:

```
Não tenho informações necessárias para responder sua pergunta.
```

---