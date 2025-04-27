from controle_fincanceiro_pessoal.utilitarios import corrigir_valor
from controle_fincanceiro_pessoal.metas import *

def adicionar_transacao(tipo, data_formatada, descricao, valor, id_categoria, mes=None, ano=None):
    print(f'\n{cor("negrito")}--- Adicionar {tipo} ---{cor('reset')}')

    # Conexão com o banco de dados
    con = conectar()
    cursor = con.cursor()

    try:
        # Inserção da transação no banco
        cursor.execute(
            'INSERT INTO transacoes (data, descricao, valor, tipo, id_categoria) VALUES (?, ?, ?, ?, ?)',
            (data_formatada, descricao, valor, tipo, id_categoria)
        )
        print(f'{cor("verde")}✅ {tipo.capitalize()} adicionado com sucesso.{cor("reset")}')

        # Determina o mês e ano atuais, caso não sejam passados
        data_atual = datetime.now()
        mes = int(mes) if mes else data_atual.month
        ano = int(ano) if ano else data_atual.year

        # Consulta a meta relacionada
        cursor.execute("""
                SELECT m.id
                FROM metas m
                WHERE m.categoria_id = ? AND m.referencia = ?
            """, (id_categoria, f"{mes:02d}/{ano}"))

        id_meta = cursor.fetchone()
        con.commit()

    except Exception as e:
        con.rollback()
        print(f"{cor('vermelho')}❌ Erro ao adicionar transação: {e}{cor('reset')}")
        id_meta = None

    finally:
        cursor.close()
        con.close()

    # Chama cálculo de progresso, se meta foi encontrada
    if id_meta:
        id_meta = id_meta[0]
        calcular_progresso_meta(id_meta, f"{mes:02d}/{ano}")
    else:
        print(f"❌{cor('vermelho')} Meta não encontrada para a categoria {id_categoria} no mês {mes}/{ano}.{cor('reset')}")

#------------------------------------------------------------------
def editar_transacao(transacao_id):
    con = conectar()
    cursor = con.cursor()

    # Buscar transação atual
    cursor.execute("""
        SELECT data, descricao, valor, tipo, id_categoria 
        FROM transacoes 
        WHERE id = ?
    """, (transacao_id,))
    transacao = cursor.fetchone()

    if not transacao:
        print(f"❌ {cor('vermelho')} Transação não encontrada.{cor('reset')}")
        con.close()
        return

    data_atual, descricao_atual, valor_atual, tipo_atual, categoria_atual = transacao

    print(f"\n{cor('negrito')}{cor('cyan')}--- Editar Transação ---{cor('reset')}")
    print(f"\nData atual: {cor("amarelo")}{data_atual}")

    # O usuario define o dia da transação
    dia = input(f"{cor('negrito')}{cor('azul')}📅 Informe o dia (Enter se não lembra o dia): {cor('reset')}").strip()

    if dia == "":
        dia = '01'  # Mantém o dia atual se o usuário apertar Enter
    elif not dia.isdigit() or not (1 <= int(dia) <= 31):
        print(f"{cor('vermelho')}❌ Dia inválido. Use um valor entre 01 e 31.{cor('reset')}")
        return

    if not dia.isdigit() or not (1 <= int(dia) <= 31):
        print(f"{cor('vermelho')}❌ Dia inválido. Use um valor entre 01 e 31.{cor('reset')}")
        return

    nova_data = padronizar_data() or data_atual

    mes, ano = nova_data.split('/')  # Separando mês e ano
    nova_data = f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"  # Formatando para AAAA-MM-DD


    print(f"\nDescrição atual: {cor("amarelo")}{descricao_atual}{cor('reset')}")
    nova_descricao = input("Nova descrição ou Enter para manter: ") or descricao_atual

    print(f"\nValor atual: {cor("amarelo")}{valor_atual}{cor('reset')}")
    novo_valor = input("Novo valor ou Enter para manter: ")
    if novo_valor:
        try:
            novo_valor = float(novo_valor)
        except ValueError:
            print(f"❌{cor('vermelho')} Valor inválido. Edição cancelada.{cor('reset')}")
            con.close()
            return
    else:
        novo_valor = valor_atual

    print(f"\nTipo atual: {cor("amarelo")}{tipo_atual}{cor('reset')}")
    while True:
        novo_tipo = input("Novo tipo (receita/despesa) ou Enter para manter: ") or tipo_atual
        if novo_tipo.lower() in ['receita', 'despesa']:
            break
        print(f"❌{cor('vermelho')} Tipo inválido. Digite 'receita' ou 'despesa'.{cor('reset')}")

    print(f"\nID da categoria atual: {cor("amarelo")}{categoria_atual}")
    exibir_categorias()
    novo_categoria_id = input("Novo ID da categoria ou Enter para manter: ") or categoria_atual

    if novo_categoria_id != categoria_atual:
        cursor.execute("SELECT id FROM categoria WHERE id = ?", (novo_categoria_id,))
        if not cursor.fetchone():
            print(f"❌{cor('vermelho')} ID de categoria inválido. Edição cancelada.{cor('reset')}")
            con.close()
            return

    # Atualizar no banco
    cursor.execute("""
        UPDATE transacoes 
        SET data = ?, descricao = ?, valor = ?, tipo = ?, id_categoria = ?
        WHERE id = ?
    """, (nova_data, nova_descricao, novo_valor, novo_tipo, novo_categoria_id, transacao_id))

    con.commit()
    con.close()

    print(f"✅{cor('verde')} Transação atualizada com sucesso!{cor('reset')}")

#------------------------------------------------------------------
def excluir_transacao(transacao_id):
    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM transacoes WHERE id = ?", (transacao_id,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM transacoes WHERE id = ?", (transacao_id,))
        con.commit()
        print(f"✅{cor('verde')} Transação excluída com sucesso.{cor('reset')}")
    else:
        print(f"⚠️{cor('amarelo')} ID não encontrado.{cor('reset')}")

    con.close()

#------------------------------------------------------------------
def exibir_transacoes(cursor, tipo=None, data_formatada=None):

    # Cabeçalho com variação de cor a depender do tipo de transação
    cor_tipo = cor('verde') if tipo == 'receita' else cor('vermelho')
    titulo = 'Receitas' if tipo == 'receita' else 'Despesas'

    print(f'\n{cor_tipo}{"-" * 28} {titulo} {"-" * 28}{cor("reset")}')

    # Coleta das informações das transações
    cursor.execute('''
            SELECT t.data, t.descricao, t.valor, c.nome
            FROM transacoes t
            JOIN categoria c ON t.id_categoria = c.id
            WHERE tipo = ? AND data LIKE ?
        ''', (tipo, f"{data_formatada}%"))

    transacoes = cursor.fetchall()

    # Saída dos resultados coletados
    if transacoes:
        print(f"{cor('negrito')}{'Data':<12}{'Descrição':<25}{'Valor (R$)':<12}{'Categoria':<20}{cor('reset')}")
        print(f"{cor_tipo}","-" * 65, f"{cor('reset')}")
        for data, descricao, valor, categoria in transacoes:
            print(f"{data:<12}{cor_tipo}{descricao:<25}{valor:<12.2f}{categoria:<20}{cor('reset')}")
    else:
        print(f"❌{cor('vermelho')} Nenhuma {titulo.lower()} encontrada para o período.{cor('reset')}")

#------------------------------------------------------------------
def listar_transacoes():

    con = conectar()
    cursor = con.cursor()

    cursor.execute("""SELECT t.id, t.data, t.descricao, t.valor, c.nome AS categoria, t.tipo 
    FROM transacoes t
    JOIN categoria c ON t.id_categoria = c.id
    ORDER BY t.data ASC, t.tipo ASC
    """)
    transacoes = cursor.fetchall()
    con.close()

    if transacoes:
        print(f"{cor('negrito')}{cor('cyan')}\n{'-' * 30} TODAS AS TRANSAÇÕES {'-' * 30}{cor('reset')}")
        print(f"{cor('negrito')}{'ID':<5}{'Data':<12}{'Descrição':<25}{'Valor (R$)':<12}{'Categoria':<20}{'Tipo':<10}")
        print(f"{cor('cyan')}{'-'*80}{cor('reset')}")

        for id_categoria, data, descricao, valor, categoria, tipo in transacoes:
            cor_tipo = cor('verde') if tipo == 'receita' else cor('vermelho')
            print(f"{cor('negrito')}{cor('amarelo')}{id_categoria:<5}{cor('reset')}"
                  f"{data:<12}"
                  f"{cor_tipo}{descricao:<25}"
                  f"{valor:<12}"
                  f"{categoria:<20}"
                  f"{tipo:<10}{cor('reset')}")
    else:
        print(f"❌{cor('vermelho')} Nenhuma transação encontrada.{cor('reset')}")

#------------------------------------------------------------------
def calcular_total(cursor, tipo, data_formatada):

    # Calculando o total de um tipo de transação
    cursor.execute('''
            SELECT SUM(valor) FROM transacoes
            WHERE tipo = ? AND data LIKE ?
        ''', (tipo, f"{data_formatada}%"))

    total = cursor.fetchone()[0]
    return corrigir_valor(total)
