from datetime import datetime

def cor(color):
    """
    Modifica a cor do texto no terminal.
    A função é chamada no formato: cor(cor_name, 'texto')
    Exemplo: cor("vermelho", "Texto em vermelho")
    """
    cores = {
        "reset": "\033[0m",
        "preto": "\033[30m",
        "vermelho": "\033[31m",
        "verde": "\033[32m",
        "amarelo": "\033[33m",
        "azul": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "branco": "\033[37m",
        "negrito": "\033[1m",
    }

    cor_escolhida = cores.get(color.lower())
    return f"{cor_escolhida}"
#------------------------------------------------------------------
def corrigir_valor(valor):
    if valor is None:
        return 0.00
    try:
        valor_corrigido = float(str(valor).replace(",", ".").strip())
        return valor_corrigido
    except ValueError:
        return None

#------------------------------------------------------------------
def validar_valor(valor_input):

    if not valor_input:
        print(f"⚠️{cor("amarelo")} O valor não pode estar em branco.{cor("reset")}")
        return None
    try:
        valor_corrigido = valor_input.replace(",", ".")
        return float(valor_corrigido)
    except ValueError:
        print(f"❌{cor("vermelho")} Valor inválido. Digite um número válido.{cor("reset")}")
        return None

#------------------------------------------------------------------
def escolher_item_lista(lista, mensagem, titulo="LISTA DE ITENS", retornar='id'):
    """
    Exibe uma lista enumerada e permite que o usuário escolha uma opção pelo índice.
    Retorna o item correspondente da lista.
    """
    if not lista:
        print(f"❌{cor('vermelho')} Lista vazia. Nenhuma opção disponível.")
        return None

    print(f"\n{cor('negrito')}{cor('cyan')}--------- {titulo} ---------{cor('reset')}")
    print(f"{'ID':<5} {'Descrição'}")
    print(f"{cor('cyan')}-" * 30)

    # Verifica se a lista contém tuplas ou apenas strings
    if isinstance(lista[0], tuple) and len(lista[0]) == 2:
        itens = lista  # Mantém os IDs originais
    else:
        itens = [(idx + 1, item) for idx, item in enumerate(lista)]  # Transforma em lista de tuplas

    for id_item, nome_item in itens:
        print(f"{cor('negrito')}{cor('amarelo')}{id_item:<5} {cor('azul')}{nome_item}{cor('reset')}")

    while True:
        try:
            escolha = int(input(f"\n{mensagem} ").strip())
            # Verificar se a escolha está dentro da lista real, baseada em IDs
            ids_validos = [item[0] for item in itens]
            if escolha in ids_validos:
                return escolha if retornar == 'id' else dict(itens)[escolha]
            else:
                print(f"❌{cor('vermelho')} Opção inválida. Escolha um número entre 1 e {len(itens)}.")
        except ValueError:
            print(f"❌{cor('vermelho')} Entrada inválida. Digite apenas números.")

#------------------------------------------------------------------
def obter_mes_ano_atual():
    agora = datetime.now()
    return agora.strftime('%m/%Y')

#------------------------------------------------------------------
def calcular_mes_anterior(mes_atual):
    """
    Recebe uma string 'mm/yyyy' e retorna o mês anterior no mesmo formato.
    """
    mes, ano = map(int, mes_atual.split("/"))
    if mes == 1:
        mes_anterior = 12
        ano_anterior = ano - 1
    else:
        mes_anterior = mes - 1
        ano_anterior = ano
    return f"{mes_anterior:02}/{ano_anterior}"

#------------------------------------------------------------------
def padronizar_data():
    while True:
        entrada = input(f"{cor('negrito')}{cor('azul')}📅 Informe o mês e o ano de referencia no formato mm-aaaa "
            f"ou mm-aa: {cor('reset')}").strip()
        partes = entrada.split('-')

        if len(partes) != 2:
            print(f"{cor('vermelho')}❌ Formato inválido. Use mm-aaaa ou mm-aa. Tente novamente.{cor('reset')}")
            continue

        mes, ano = partes[0].zfill(2), partes[1]

        if len(ano) == 2:
            ano = "20" + ano  # converte '25' para '2025'

        if not mes.isdigit() or not ano.isdigit():
            print(
                f"{cor('vermelho')}❌ O mês e o ano devem conter apenas números. Tente novamente.{cor('reset')}")
            continue

        mes = int(mes)
        ano = int(ano)

        if not (1 <= mes <= 12):
            print(f"{cor('vermelho')}❌ Mês inválido. Deve ser entre 01 e 12.{cor('reset')}")
            continue

        if ano < 2000:
            print(f"{cor('vermelho')}❌ Ano inválido. Deve ser igual ou superior a 2000.{cor('reset')}")
            continue

        referencia = f"{mes:02d}/{ano}"
        return referencia
