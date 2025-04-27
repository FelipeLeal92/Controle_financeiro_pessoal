from controle_fincanceiro_pessoal.banco import conectar
import calendar
from controle_fincanceiro_pessoal.transacoes import exibir_transacoes, calcular_total
from controle_fincanceiro_pessoal.utilitarios import corrigir_valor, cor, padronizar_data

def resumo_mensal():

    # Padronizando a data: "MM-AAAA" para "AAAA-MM"
    referencia = padronizar_data()
    mes, ano = referencia.split('/')
    data_formatada = f"{ano}-{mes.zfill(2)}"  # Ex: '04-2025' para '2025-04'

    con = conectar()
    cursor = con.cursor()

    # ------------------------------------------------------------------
    # Exibição de receitas e despesas
    exibir_transacoes(cursor, 'receita', data_formatada)
    exibir_transacoes(cursor, 'despesa', data_formatada)

    # ------------------------------------------------------------------
    # Cálculo de Totais
    total_receita = calcular_total(cursor, 'receita', data_formatada)
    total_despesa = calcular_total(cursor, 'despesa', data_formatada)
    saldo_mensal = total_receita - total_despesa

    # Exibição do total por categoria
    total_por_categoria(cursor, data_formatada)

    # Exibição do resumo
    print(f"\n{cor('negrito')}-------- Resumo do mês {referencia} --------{cor('reset')}")
    print(f"{cor('azul')}Receitas:{cor('reset')} R$ {cor('verde')}{total_receita:.2f}")
    print(f"{cor('azul')}Despesas:{cor('reset')} R$ {cor('vermelho')}{total_despesa:.2f}")
    # Opção de coloração para saldo positivo ou negativo
    print(f"{cor('azul')}Saldo mensal:{cor('reset')} R$", f'{cor('verde')}' if saldo_mensal >= 0
    else f"{cor('vermelho')}",f"{saldo_mensal:.2f}{cor('reset')}")

    con.close()

#------------------------------------------------------------------
def total_por_categoria(cursor, data_formatada):
    print(f"\n{cor('negrito')}{cor('cyan')}---- Totais por Categoria em {calendar.month_name[int(data_formatada[5:7])]}-"
          f"{data_formatada[:4]} -----{cor('reset')}")
    cursor.execute('''
        SELECT c.nome, t.tipo, SUM(t.valor)
        FROM transacoes t
        JOIN categoria c ON t.id_categoria = c.id
        WHERE strftime('%Y-%m', t.data) = ?
        GROUP BY c.nome, t.tipo
        ORDER BY t.tipo DESC, SUM(t.valor) DESC
    ''', (data_formatada,))
    totais_categoria = cursor.fetchall()

    if totais_categoria:
        print(f"{'Categoria':<20} {'Tipo':<10} {'Total (R$)':>12}")
        print(f"{cor('cyan')}",'-' * 45,f"{cor('reset')}")
        for nome_cat, tipo, total in totais_categoria:
            cor_tipo = f'{cor('verde')}' if tipo == 'receita' else f'{cor('vermelho')}'
            print(f"{nome_cat:<20} {cor_tipo}{tipo:<10} {total:>12.2f}{cor('reset')}")
    else:
        print(f"❌{cor('vermelho')} Nenhuma transação encontrada para este mês.{cor('reset')}")

#------------------------------------------------------------------
def exibir_saldo():
    con = conectar()
    cursor = con.cursor()
    cursor.execute('SELECT SUM(valor) FROM transacoes WHERE tipo = "receita"')
    receita = cursor.fetchone()[0]
    receita = corrigir_valor(receita)
    cursor.execute('SELECT SUM(valor) FROM transacoes WHERE tipo = "despesa"')
    despesa = cursor.fetchone()[0]
    despesa = corrigir_valor(despesa)
    con.close()

    saldo = float(receita) - float(despesa)

    print('\n','-'*14,'Saldo Atual', '-'*14)

    cor_tipo = f"{cor('verde')}" if saldo >= 0 else f"{cor('vermelho')}"
    print(f"{cor('azul')}Saldo:{cor('reset')} R$ {cor_tipo}{saldo:.2f}{cor('reset')}")
    print(f'{cor('azul')}Receitas:{cor('reset')} R$ {cor('verde')}{receita:.2f}{cor('reset')}',
          f'| {cor('azul')}Despesas:{cor('reset')} R$ {cor('vermelho')}{despesa:.2f}{cor('reset')}')
