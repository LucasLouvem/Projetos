import json

ARQUIVO_JSON = "usuarios.json"
cadastro = []

#--------- Função Para cadastrar os Usuarios. ---------------------

def cadastrarPessoa(nome, idade, cidade, curso):
    novo_cadastro = {
        "nome": nome,
        "idade": idade,
        "cidade": cidade,
        "curso": curso
    }

    cadastro.append(novo_cadastro)
    print("Cadastro realizado com sucesso!")

#--------- Função de Listar Usuários no sistema -----------------

def listarPessoas(cadastro):
    for usuario in cadastro:
            print("RESUMO DO CADASTRO:")
            print(f"Nome: {usuario['nome']}")
            print(f"Idade: {usuario['idade']}")
            print(f"Cidade: {usuario['cidade']}")
            print(f"Curso: {usuario['curso']}")
            print("-" * 33)

#----------- Função para procurar Pessoas no sistema -------------

def buscarUsuario(nome_a_localizar):
    resultados_encontrados = []
    termo_busca_lower = nome_a_localizar.lower()

    for usuario in cadastro:
        nome_usuario_lower = usuario['nome'].lower()
        if termo_busca_lower in nome_usuario_lower:
            resultados_encontrados.append(usuario)

    if resultados_encontrados:
        for usuario_econtrado in resultados_encontrados:
            print("Usuário encontrado!")
            print("*"*33)
            print(f"Nome: {usuario_econtrado['nome']}")
            print(f"idade: {usuario_econtrado['idade']}")
            print(f"Cidade: {usuario_econtrado['cidade']}")
            print(f"Curso: {usuario_econtrado['curso']}")
            print('*'*33)
            print("---- Fim dos Resultado -----")
    else:
        print(f"Usuário {nome_a_localizar} não encontrado no sistema.")

#----------- Função Para remover um usuario ---------------------
 
def removerUsuario(nome_a_remover):
    encontrado = False
    for usuario in list(cadastro):
        if nome_a_remover.lower() == usuario['nome'].lower():
            cadastro.remove(usuario)
            print(f"Pessoa {usuario['nome']} Removida com sucesso.")
            encontrado = True
            break
    if not encontrado:
        print(f"Usuário {nome_a_remover} não encontrado no sistema.")

#------------ Função para o Json Ler o arquivo ---------------

def carregarDados():
    try:
        with open(ARQUIVO_JSON, 'r', encoding="utf-8") as arquivo:
            usuariosCarregados = json.load(arquivo)
        print("Usuarios Carregados com sucesso!")
        return usuariosCarregados
    except FileNotFoundError:
        print("Arquivo não encontrado. Criando uma Lista vazia.")
        usuariosCarregados = []
        return usuariosCarregados
    except json.JSONDecodeError:
        print("Erro ao ler o JSON, Arquivo corrompido ou vazio!")
        return []
    except Exception as e:
        print(f"Erro inesperado: {e}")
        usuariosCarregados = []
        return usuariosCarregados


#---------- Função para Salvar o arquivo em um JSON ------------

def salvarDados(cadastro):
    try:
        with open(ARQUIVO_JSON, 'w', encoding="utf-8") as arquivo:
            json.dump(cadastro, arquivo, indent=4, ensure_ascii=False)
        print("Dados salvos com Sucesso no arquivo!")
    except Exception as e:
        print(f"erro ao salvar os dados: {e}")

cadastro = carregarDados()

#------------ Programa Principal -----------

while True:
    print("-" * 33)
    print("MENU DE CADASTRO:")
    print("1 - Cadastrar Nova Pessoa")
    print("2 - Listar Usuários Cadastrados")
    print("3 - Remover Usuário Cadastrado")
    print("4 - Buscar Usuário")
    print("5 - Salva e Sair do Programa")
    print("-" * 33)
    decisao = int(input("Escolha uma opção: "))
   
    if decisao == 1:
        
        nome = input("Digite seu nome completo: ")
        idade = int(input("Digite sua idade: "))
        cidade = input("Em que cidade você mora? ")
        curso = input("Qual curso você faz? ")
        cadastrarPessoa(nome, idade, cidade, curso)
        
    elif decisao == 2:
        print('--- Pessoas Cadastradas ---')
        print("-" * 33)
        listarPessoas(cadastro)
        print("--- Fim da Lista ---")

    elif decisao == 3:
        nome_a_remover = input("Digite o nome completo do usuario a ser removido: ")
        removerUsuario(nome_a_remover)

    elif decisao == 4:
        print("-"*30)
        nome_a_localizar = input("Digite o nome do Usuário para pesquisa: ")
        print("-"*30)
        print(f"Buscando Usuário {nome_a_localizar}")
        print("-"*30)
        buscarUsuario(nome_a_localizar)
        
    elif decisao == 5:
        print("Salvando cadastros...")
        salvarDados(cadastro)
        print("Saindo do programa, até mais!")
        break
    else:
        print("Opção inválida. Tente novamente.")