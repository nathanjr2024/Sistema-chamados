import json
import os

ARQUIVO_CHAMADOS = 'chamados.json'

dicionario_de_chamados = {}

def carregar_chamados():
    global dicionario_de_chamados
    if os.path.exists(ARQUIVO_CHAMADOS):
        with open(ARQUIVO_CHAMADOS, 'r', encoding='utf-8') as arquivo:
            try:
                dicionario_de_chamados = json.load(arquivo)
            except json.JSONDecodeError:
                print('Erro ao fazer a leitura do Arquivo')
                dicionario_de_chamados = {}

def obter_proximo_codigo():
    if dicionario_de_chamados:
        return max(int(codigo) for codigo in dicionario_de_chamados.keys()) + 1
    return 1

def salvar_dados():
    with open(ARQUIVO_CHAMADOS, 'w') as arquivo:
        json.dump(dicionario_de_chamados, arquivo, indent=4)

def cadastrar_novo_chamado(nome_cliente, prioridade, descricao_do_chamado):
    codigo = str(obter_proximo_codigo())
    chamados = {
        "codigo": codigo,
        "nome_cliente": nome_cliente,
        "nivel_prioridade": prioridade,
        "descricao_do_chamado": descricao_do_chamado,
        "status": "aberto"
    }
    dicionario_de_chamados[codigo] = chamados
    print(f"O chamado do(a) cliente {nome_cliente} foi cadastrado com sucesso!")
    
    with open(ARQUIVO_CHAMADOS, 'w', encoding= 'utf-8') as arquivo:
        json.dump(dicionario_de_chamados, arquivo, indent=4)

def buscar_chamado_codigo(codigo):
    if codigo in dicionario_de_chamados:
        return dicionario_de_chamados[codigo]
    else:
        return None
    
def buscar_chamado_descrição(descricao):
    resultados = []
    for codigo in dicionario_de_chamados:
        if descricao.lower() in dicionario_de_chamados[codigo]['descricao_do_chamado'].lower():
            resultados.append(dicionario_de_chamados[codigo])
    
    return resultados if resultados else "Nenhum chamado encontrado."

def alterar_status_de_chamado(codigo, novo_status):
    if codigo in dicionario_de_chamados:
        dicionario_de_chamados[codigo]['status'] = novo_status
        salvar_dados()
        print(f"Status do chamado alterado para {novo_status}!")
    

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def listar_chamados_prioridade():
    chamados_ordenados = sorted(dicionario_de_chamados.items(), key=lambda x: int(x[1]["nivel_prioridade"]), reverse=True)

    for codigo, dados in chamados_ordenados:
        print(f"Código: {codigo} - Cliente: {dados['nome_cliente']} - Prioridade: {dados['nivel_prioridade']} - Descrição: {dados['descricao_do_chamado']} - Status: {dados['status']}")
        print("\n")

def Lista_invertida():
    chamados_ordenados = sorted(dicionario_de_chamados.items(), key=lambda x: int(x[1]["nivel_prioridade"]), reverse=False)

    for codigo, dados in chamados_ordenados:
        print(f"Código: {codigo} - Cliente: {dados['nome_cliente']} - Prioridade: {dados['nivel_prioridade']} - Descrição: {dados['descricao_do_chamado']} - Status: {dados['status']}")
        print("\n")

def remover_chamado_se_estiver_fechado(codigo):
    if codigo in dicionario_de_chamados and dicionario_de_chamados[codigo]['status'] == "fechado":
        del dicionario_de_chamados[codigo]
        salvar_dados()
        print(f"O chamado {codigo} foi removido com sucesso!")

    elif codigo in dicionario_de_chamados and dicionario_de_chamados[codigo]['status'] == "aberto":
        print("O chamado não pode ser removido pois está aberto!")
    else:
        print(f"O chamado {codigo} não existe!")

def estatisticas():
    total_chamdados = len(dicionario_de_chamados)
    abertos = sum(1 for chamado in dicionario_de_chamados.values() if chamado['status'] == "aberto")
    fechados = total_chamdados - abertos
    print(f"Total de chamados: {total_chamdados}")
    print(f"Chamados abertos: {abertos}")
    print(f"Chamados fechados: {fechados}")

def limpar_lista_de_chamados():
    
    dicionario_de_chamados_vazio_limpa_lista_por_favor = {}
    
    with open ("chamados.json", "w") as arquivo:
        json.dump(dicionario_de_chamados_vazio_limpa_lista_por_favor, arquivo)


def menu():
    while True:
        carregar_chamados()
        print("\nMenu de Chamados")
        print("1- Realizar um novo chamado.")
        print("2- Buscar chamado.")
        print("3- Alterar status de um chamado.")
        print("4- Listar todos os chamados.")
        print("5- Remover chamado.")
        print("6- Exibir estatísticas.")
        print("7- Limpar lista de chamados.")
        print("8- inverter a lista de chamados")

        opcao = input("Escolha uma opção: ")

        try:
            opcao = int(opcao)
        except ValueError:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            continue
        if opcao == 1:
            limpar_tela()
            nome = input("Digite o nome do cliente:\n-->    ")
            prioridade = input("Digite a prioridade do chamado\n(1-Baixa, 2-Média, 3-Urgente)\n-->   ")
            descricao = input("Digite a Descrição do chamado:\n-->  ")
            
            cadastrar_novo_chamado(nome, prioridade, descricao)

        elif opcao == 2:
            print("Como você deseja realizar sua busca?\n")
            print("1- Buscar por código do chamado.")
            print("2- Buscar por descrição.\n")
        
            print("Sendo meu professor digite qualquer coisa kkkkkk\n")
            busca = int(input("Escolha uma opção: "))
        
            if busca == 1:
                codigo = input("Digite o código do chamado: ")
                chamado = buscar_chamado_codigo(str(codigo))
                if chamado:
                    print(f"Chamado encontrado: {chamado}")
                else:
                    print("Chamado não encontrado.")

            elif busca == 2:
                descricao = input("Digite a descrição do chamado: ")
                chamado = buscar_chamado_descrição(descricao)
                if chamado:
                    print(f"Chamado encontrado: {chamado}")
                else:
                    print("Chamado não encontrado.")
        

        elif opcao == 3:
            limpar_tela()
            codigo = input("Digite o código do chamado: ")

            if codigo in dicionario_de_chamados:
                limpar_tela()
                print(buscar_chamado_codigo(codigo))
                new_status = input("Digite o novo status do chamado: ")
                alterar_status_de_chamado(codigo, new_status)
            else:
                print("Chamado não encontrado.")

        
        elif opcao == 4:
            limpar_tela()
            listar_chamados_prioridade()

            
        elif opcao == 5:
            limpar_tela()
            codigo = input("Digite o código do chamado que deseja apagar: ")
            remover_chamado_se_estiver_fechado(codigo)

        elif opcao == 6:
            limpar_tela()
            estatisticas()

        elif opcao == 7:
            limpar_lista_de_chamados()
            print("A lista de chamados foi apagada com sucesso!")

        elif opcao == 8:
            Lista_invertida()

            

menu()
