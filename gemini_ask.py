#!/usr/bin/env python3
import google.generativeai as genai
import os
import sys

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# ------- Ferramentas ----------


def read_file(filename: str) -> str:
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"Erro: Arquivo '{filename}' não encontrado."
    except Exception as e:
        return f"Erro ao ler o arquivo '{filename}': {e}"
    
def write_file(filename: str, content: str) -> str:
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f"Arquivo '{filename}' escrito com sucesso."
    except Exception as e:
        return f"Erro ao escrever no arquivo '{filename}': {e}"

#--------- Função principal ------------


def ask_gemini(prompt_text):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash', 
                                      tools=[read_file, write_file])
        chat = model.start_chat()

        response = chat.send_message(prompt_text)

        while True:
            if response.text:
                print(response.text)
                break
                
            if response.parts:
                too_called = False
                for part in response.parts:
                    if part.function_call:
                        too_called = True
                        function_call = part.function_call
                        function_name = function_call.name
                        function_args = function_call.args

                        print(f"DEBUG: Gemini Chamou a ferramenta '{function_name}' com argumentos: {function_args}", file=sys.stderr)

                        result_of_tool = None
                        if function_name == "read_file":
                            result_of_tool = read_file(**function_args)
                        elif function_name == "write_file":
                            result_of_tool = write_file(**function_args)
                        else:
                            print(f"Erro: Função '{function_name}' não reconhecida pelo script", file=sys.stderr)
                            sys.exit(1)
                
                        response = chat.send_message(
                            genai.GenerativeModel.response.FunctionResponse(
                                name = function_name,
                                response={'result': result_of_tool}
                            )
                        )
                        break

                if not too_called:
                    print("DEBUG: Nenhuma Chamada de ferramenta ou texto na resposta. Resposta inesperada.", file=sys.stderr)
                    break
            else:
                print(f"DEBUG: Resposta Vazia ou estrutura inesperada do Gemini.", file=sys.stderr)
                print(response)
                break
    
    except Exception as e:
        print(f'Erro ao interagir com o Gemini: {e}', file=sys.stderr)
        print('Certifique-se de que o GOOGLE_API_KEY está configurada corretamente e há conexão com a internet.', file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: gemini_ask \"Sua pergunta para o Gemini\"", file=sys.stderr)
        sys.exit(1)
    
    prompt = ' '.join(sys.argv[1:])
    ask_gemini(prompt)
