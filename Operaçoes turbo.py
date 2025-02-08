from datetime import datetime 

def sacar(*, saldo, valor, limite, numero_saque, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saque = numero_saque >= limite_saques

    if excedeu_saldo:
        return f'\nSaldo insuficiente', numero_saque
    elif excedeu_saque:
        return 'Limite de saque diário atingido', numero_saque
    elif excedeu_limite:
        return 'Não é possível sacar esse valor, tente um valor abaixo de R$500.00', numero_saque
    elif valor > 0:
        saldo -= valor
        numero_saque += 1
        return f'Saque de R${valor:.2f} realizado com sucesso', numero_saque
    else:
        return 'Operação falhou! Valor inválido', numero_saque


def depositar(saldo, valor):
    saldo += valor
    return saldo


def exibir_extrato(saldo, *, extrato):
    print('Extrato')
    for operacao, valor in extrato:
        print(f'{operacao}: R${valor:.2f}')
    print(f'Saldo: R${saldo:.2f}')
    return saldo, extrato


def criar_user(usuarios):
    cpf = input('Insira seu CPF (somente números): ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('Já existe usuário com esse CPF!')
        return

    nome = input('Informe seu nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Insira seu endereço (logradouro, número, bairro, cidade/estado em sigla): ')
    usuarios.append({'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco})
    print('Usuário cadastrado com sucesso')


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta_corrente(agencia, numero_conta, usuarios):
    cpf = input('Insira seu CPF (somente números): ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('Conta criada com sucesso')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario}
    print('Usuário não encontrado')


def listar_contas(contas):
    for conta in contas:
        print(f"""\
            Agência: {conta['agencia']}
            C/C: {conta['numero_conta']}
            Titular: {conta['usuario']['nome']}
        """)
    print('='*100)


def main():
    menu = f"""
            Bem-vindo de volta! 
        Dia: {datetime.now()} 
        
        Escolha uma das opções abaixo:

        1 - Exibir o saldo da sua conta
        2 - Depósito
        3 - Saque
        4 - Exibir extrato
        5 - Criar Novo usuário
        6 - Nova conta
        7 - Listar contas
        8 - Sair
    """

    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    limite_saque = 3
    usuarios = []
    contas = []
    numero_conta = 1
    agencia = '0001'

    while True:
        print(menu)
        decisao_usuario = int(input('Sua escolha: '))

        match decisao_usuario:
            case 1:
                print(f'Seu saldo atual é: R${saldo:.2f}')
            
            case 2:  # Depósito
                valor = float(input('Valor que você gostaria de depositar: R$ '))
                if valor > 0:
                    saldo = depositar(saldo, valor)
                    extrato.append(('Depósito', valor))
                    print(f'Depósito de R${valor:.2f} realizado com sucesso')
                else:
                    print('Valor inválido para depósito.')

            case 3:  # Saque
                valor = float(input('Valor que você gostaria de sacar: R$ '))
                mensagem, numero_saques = sacar(
                    saldo=saldo,
                    valor=valor,
                    limite=limite,
                    numero_saque=numero_saques,
                    limite_saques=limite_saque
                )
                print(mensagem)
                if 'realizado' in mensagem:  # Só adiciona o saque ao extrato se foi realizado com sucesso
                    extrato.append(('Saque', valor))

            case 4:  # Exibir Extrato
                exibir_extrato(saldo, extrato=extrato)
            
            case 5:  # Criar Novo Usuário
                criar_user(usuarios)
            
            case 6:  # Nova Conta
                numero_conta = len(contas) + 1
                conta = criar_conta_corrente(agencia, numero_conta, usuarios)
                if conta:
                    contas.append(conta)
            
            case 7:  # Listar Contas
                listar_contas(contas)
            
            case 8:  # Sair
                print('Até mais ;)')
                break
main()