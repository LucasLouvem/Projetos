senha = "root"
tentativas = 0
senha_user = ""

while senha_user != senha:
    senha_user = input("Senha: ")
    if senha_user != senha:
        print("Senha Errada!")
        tentativas = tentativas + 1
        if tentativas == 3:
            print("Tentativas Excedidas!. Saindo do programa...")
            quit()
        else:
            continue
    elif senha_user == senha:
        print("Acesso autorizado")
        continue
    else:
        print("Dados incorretos")

print("dados")

