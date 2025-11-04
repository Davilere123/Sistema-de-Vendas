while True:
    try:
        operar = float(input("Primeiro número: "))
        operar2 = float(input("Segundo número: "))
    except ValueError:
        print("Só pode digitar números!\n")
        continue  

    opcao = input("Qual operação deseja utilizar? (Soma, Subtração, Multiplicação, Divisão ou Sair): ").lower()

    if opcao == "sair":
        print("Encerrando o programa...")
        break

    try:
        if opcao == "soma":
            resultado = operar + operar2
        elif opcao == "subtração":
            resultado = operar - operar2
        elif opcao == "multiplicação":
            resultado = operar * operar2
        elif opcao == "divisão":
            resultado = operar / operar2
        else:
            print("Opção inválida! Tente novamente.\n")
            continue

        print(f"Resultado: {resultado}\n")

    except ZeroDivisionError:
        print("Erro: não é possível dividir por zero!\n")