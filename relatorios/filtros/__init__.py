import sqlite3
from controle_fincanceiro_pessoal.utilitarios import cor
from controle_fincanceiro_pessoal.banco import conectar

def selecionar_data(data_input):
    try:
        mes, ano = data_input.split('-')
        return f"{ano}-{mes.zfill(2)}"
    except ValueError:
        print(f"\n⚠️{cor('amarelo')} Formato inválido. Use MM-AAAA.{cor('reset')}")
        return None

#------------------------------------------------------------------
def selecionar_descricao(descricao):
    if not descricao.strip():
        print(f"\n⚠️{cor('amarelo')} A descrição não pode estar vazia.{cor('reset')}")
        return None
    return descricao.strip()

#------------------------------------------------------------------
def exibir_filtros(transacoes):
    if transacoes:
        print(f'\n{cor("negrito")}{cor("cyan")}','-'*27,'Resultados do filtro:', '-'*27, f'{cor("reset")}')
        print(f"{'Data':<12}{'Descrição':<25}{'Valor (R$)':<12}{'Categoria':<20}{'Tipo':<10}")
        print(f'{cor("cyan")}',"-" * 75, f'{cor("reset")}')
        for data, descricao, valor, categoria, tipo in transacoes:
            cor_tipo = cor('verde') if tipo == 'receita' else cor('vermelho')
            print(f"{data:<12}{cor_tipo}{descricao:<25}{valor:<12.2f}{categoria:<20}{tipo:<10}{cor("reset")}")
    else:
        print(f"\n❌{cor('vermelho')} Nenhuma transação encontrada com os filtros aplicados.")

#------------------------------------------------------------------
def filtrar_transacoes(data_formatada=None, categoria_id=None, descricao=None):
    condicoes = []
    parametros = []

    con = conectar()
    cursor = con.cursor()

    if data_formatada:
        condicoes.append('t.data LIKE ?')
        parametros.append(f'{data_formatada}%')

    if categoria_id:
        condicoes.append('t.id_categoria = ?')
        parametros.append(categoria_id)

    if descricao:
        condicoes.append('t.descricao LIKE ?')
        parametros.append(f"%{descricao}%")

    if not condicoes:
        print(f"\n❌{cor('vermelho')} Nenhum filtro aplicado.{cor('reset')}")
        return

    query = (f"""
    SELECT t.data, t.descricao, t.valor, c.nome AS categoria, t.tipo
    FROM transacoes t
    JOIN categoria c ON t.id_categoria = c.id
    WHERE {' AND '.join(condicoes)}
    ORDER BY t.data
    """)

    cursor.execute(query, parametros)
    transacoes = cursor.fetchall()
    con.close()
    return transacoes

#------------------------------------------------------------------
def exibir_descricao(exibir = False):
    conexao = sqlite3.connect('financas.db')
    cursor = conexao.cursor()

    cursor.execute("SELECT DISTINCT descricao FROM transacoes ORDER BY descricao")
    descricoes = [desc[0] for desc in cursor.fetchall()]
    conexao.close()

    if exibir:
        if descricoes:
            print(f"{cor('negrito')}1mDescrições cadastradas:{cor('reset')}")
            for descricao in descricoes:
                print(f" - {descricao}")
        else:
            print(f"❌{cor('vermelho')} Nenhuma descrição cadastrada ainda.{cor('reset')}")

    return descricoes
