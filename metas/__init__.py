from controle_fincanceiro_pessoal.banco.metas_db import (inserir_meta_no_banco, buscar_meta_por_categoria_mes_ano,
                                                         atualizar_meta, obter_metas_com_categorias,
                                                         obter_metas_por_referencia, excluir_meta_por_id)
from datetime import datetime
from time import sleep
from controle_fincanceiro_pessoal.categorias import listar_categorias, exibir_categorias
from controle_fincanceiro_pessoal.utilitarios import cor, padronizar_data
from controle_fincanceiro_pessoal.banco import conectar



def cadastrar_meta():
    print(f'\n{cor("negrito")}{cor("cyan")}==== Cadastrar Nova Meta ===={cor("reset")}')

    # Exibir categorias disponíveis
    exibir_categorias()

    categorias = listar_categorias()
    ids_validos = [str(cat[0]) for cat in categorias]

    while True:
        categoria_id = input(f"\n{cor('verde')}Digite o ID da categoria para a meta: {cor('reset')}")
        if categoria_id in ids_validos:
            categoria_id = int(categoria_id)  # Convertendo para inteiro
            break
        else:
            print(f"⚠️ {cor('Amarelo')}ID inválido! Por favor, escolha um ID da lista.{cor('reset')}")

    while True:
        print(f"\n{cor('negrito')}{cor('cyan')}Qual o tipo da meta?")
        print(f"{cor('amarelo')}1. 📥 Receita")
        print(f"2. 📤 Despesa{cor('reset')}")
        tipo_opcao = input(f"{cor('verde')}Escolha 1 ou 2: {cor('reset')}")

        if tipo_opcao == '1':
            tipo = 'receita'
            break
        elif tipo_opcao == '2':
            tipo = 'despesa'
            break
        else:
            print(f"⚠️ {cor('Amarelo')}Opção inválida. Digite 1 para receita ou 2 para despesa.{cor('reset')}")

    while True:
        valor_str = input(f"\n{cor('negrito')}{cor('verde')}Digite o valor da meta (ex: 1500.00): R$ {cor('reset')}")
        try:
            valor_limite = float(valor_str.replace(',', '.'))
            if valor_limite > 0:
                break
            else:
                print(f"⚠️ {cor('Amarelo')}O valor precisa ser maior que zero.{cor('reset')}")
        except ValueError:
            print(
                f"⚠️ {cor('Amarelo')}Valor inválido. Digite apenas números. Use ponto ou vírgula como separador"
                f" decimal.{cor('reset')}")

    while True:
        resposta = input(
            f"\n{cor('negrito')}{cor('azul')}Essa meta será recorrente todo mês? (s/n): {cor('reset')}").strip().lower()
        if resposta in ['s', 'sim']:
            recorrente = 1
            referencia = f"{int(datetime.now().month):02d}/{datetime.now().year}"
            break
        elif resposta in ['n', 'nao', 'não']:
            recorrente = 0

            referencia = padronizar_data()
            break

        else:
            print(f"❌ {cor('vermelho')}Resposta inválida. Digite 's' para sim ou 'n' para não.{cor('reset')}")

    # Agora chamamos a função para inserir no banco
    if inserir_meta_no_banco(categoria_id, tipo, valor_limite, recorrente, referencia):
        print(f"\n{cor('verde')}Meta cadastrada com sucesso!{cor('reset')}")
        meta = buscar_meta_por_categoria_mes_ano(categoria_id, referencia)
        if meta:
            exibir_meta(meta)
    else:
        print(f"\n❌ {cor('vermelho')}Houve um erro ao cadastrar a meta.{cor('reset')}")

#----------------------------------------------------------
def exibir_meta(meta):
    print(f"🆔 ID: {meta['id']}")
    print(f"📁 Categoria: {meta['categoria']}")
    print(f"📌 Tipo: {meta['tipo'].capitalize()}")
    print(f"💰 Valor Limite: R$ {meta['valor_limite']:.2f}")
    print(f"🗓️ Referência: {meta['referencia'] or 'Recorrente'}")
    print(f"♻️ Recorrente: {'Sim' if meta['recorrente'] else 'Não'}")
    sleep(2)

#----------------------------------------------------------
def calcular_progresso_meta(id_meta, referencia):
    """
       Calcula o progresso de uma meta com base nas transações realizadas em porcentagem.
       """
    if id_meta is None or referencia is None:
        print(f"❌ {cor('vermelho')}Erro: 'id_meta' e 'referencia' são obrigatórios para calcular o progresso da meta."
              f"{cor('reset')}")
        return

    con = None

    try:
        con = conectar()
        cursor = con.cursor()

        # Recupera o valor total gasto da categoria naquele mês
        cursor.execute("""
                   SELECT SUM(valor)
                   FROM transacoes
                   WHERE id_categoria = (
                       SELECT categoria_id FROM metas WHERE id = ?
                   ) AND strftime('%m/%Y', data) = ?
               """, (id_meta, referencia))
        total_gasto = cursor.fetchone()[0] or 0.0

        # Atualiza o progresso da meta
        cursor.execute("SELECT valor_limite FROM metas WHERE id = ?", (id_meta,))
        valor_meta = cursor.fetchone()[0]

        progresso_percentual = (total_gasto / valor_meta) * 100
        cursor.execute("UPDATE metas SET progresso = ? WHERE id = ?", (progresso_percentual, id_meta))
        con.commit()
        print(
            f"✅ Progresso da meta para a categoria {id_meta} no período {referencia} atualizado: {progresso_percentual:.2f}%")

    except Exception as e:
        print(f"❌ {cor('vermelho')}Erro ao calcular o progresso da meta: {e}{cor('reset')}")

    finally:
        if con:
            con.close()

#--------------------------------------------------------
def exibir_metas_por_referencia(referencia: str):
    metas = obter_metas_por_referencia(referencia)
    if metas:
        print(f"📊 Metas para {referencia}:")
        for meta in metas:
            print(meta)
    else:
        print(f"⚠️ Nenhuma meta encontrada para {referencia}.")

#----------------------------------------------------------
def alterar_meta():
    from datetime import datetime

    print(f"\n{cor('negrito')}{cor('azul')}🔧 ALTERAÇÃO DE META{cor('reset')}")

    # Identificar a meta pelo ID, categoria ou outro critério
    exibir_categorias()
    categoria_id = input(f"{cor('negrito')}Digite o ID da categoria da meta que deseja alterar: {cor('reset')}").strip()

    referencia = padronizar_data()

    meta = buscar_meta_por_categoria_mes_ano(categoria_id, referencia)

    if not meta:
        print(f"{cor('vermelho')}❌ Meta não encontrada com os critérios informados.{cor('reset')}")
        return

    print(f"\n{cor('negrito')}📝 Meta atual:{cor('reset')}")
    exibir_meta(meta)

    print(f"\n{cor('negrito')}{cor('azul')}Pressione Enter para manter o valor atual.{cor('reset')}")

    # Novo valor limite
    novo_valor = input(f"{cor('negrito')}Novo valor limite (atual: R${meta['valor_limite']:.2f}): {cor('reset')}")
    if novo_valor.strip() == "":
        novo_valor = meta['valor_limite']
    else:
        try:
            novo_valor = float(novo_valor.replace(",", "."))
        except ValueError:
            print(f"{cor('vermelho')}❌ Valor inválido. Operação cancelada.{cor('reset')}")
            return

    # Garantindo que recorrente e referencia sejam definidos corretamente
    recorrente = meta["recorrente"]  # Mantém o valor atual da recorrência
    nova_referencia = referencia  # Mantém a referência original

    # Nova recorrência
    nova_recorrencia = input(
        f"{cor('negrito')}Meta será recorrente? (s/n) (atual: {'sim' if meta['recorrente'] else 'não'}): "
        f"{cor('reset')}").strip().lower()
    if nova_recorrencia in ["", "s", "sim", "n", "nao", "não"]:
        if nova_recorrencia in ["", "s", "sim"]:
            recorrente = 1
            nova_referencia = f"{int(datetime.now().month):02d}/{datetime.now().year}"
        elif nova_recorrencia in ["n", "nao", "não"]:
            recorrente = 0
            # Solicitar nova referência
            print(f"{cor('negrito')}Referência atual: {meta['referencia']}). Nova referência:{cor('reset')}")
            nova_referencia = padronizar_data()

    else:
        print(f"{cor('vermelho')}❌ Resposta inválida. Operação cancelada.{cor('reset')}")
        return

    # Novo tipo
    tipo_atual = meta['tipo']
    print(f"\n{cor('negrito')}Tipo atual da meta: {tipo_atual.capitalize()}{cor('reset')}")
    while True:
        print(f"{cor('amarelo')}1. 📥 Receita")
        print(f"2. 📤 Despesa{cor('reset')}")
        novo_tipo = input(
            f"{cor('negrito')}Novo tipo (receita/despesa) ou Enter para manter: {cor('reset')}").strip().lower()

        if novo_tipo == '1':
            novo_tipo = 'receita'
            break
        elif novo_tipo == '2':
            novo_tipo = 'despesa'
            break
        elif novo_tipo == "":
            novo_tipo = tipo_atual
            break
        else:
            print(f"❌ {cor('vermelho')}Opção inválida. Digite 1 para receita ou 2 para despesa.{cor('reset')}")
            return

    # Atualizar no banco
    atualizar_meta(
        categoria_id=categoria_id,
        tipo=novo_tipo,
        valor_limite=novo_valor,
        recorrente=recorrente,
        referencia=nova_referencia
    )

    print(f"\n{cor('verde')}✅ Meta alterada com sucesso!{cor('reset')}")
    nova_meta = buscar_meta_por_categoria_mes_ano(categoria_id, nova_referencia)
    if nova_meta:
        exibir_meta(nova_meta)

#----------------------------------------------------------
def excluir_meta():
    """Função para excluir uma meta do banco de dados."""
    print(f"\n{cor('negrito')}{cor('vermelho')}🗑️ EXCLUSÃO DE META{cor('reset')}")

    referencia = padronizar_data()
    # Consulta as metas disponíveis
    metas_encontradas = obter_metas_com_categorias(referencia)

    if not metas_encontradas:
        print(f"{cor('vermelho')}❌ Nenhuma meta encontrada para a referência informada.{cor('reset')}")
        return

    print(f"\n{cor('negrito')}📜 Metas disponíveis para {referencia}:{cor('reset')}")
    print(f"{'ID':<4} {'Categoria':<18} {'Tipo':<10} {'Meta (R$)':<12} {'Referencia':<10} {'Recorrente':<10}")
    print("-" * 60)

    for id_meta, categoria, tipo, valor_limite, referencia, recorrente in metas_encontradas:
        print(f"{id_meta:<4} {categoria:<18} {tipo:<10} R${valor_limite:<10.2f} {referencia:<10} {'🔁' if recorrente else '📌'}")

    # Usuário escolhe qual meta excluir
    id_excluir = input(f"\n{cor('negrito')}Digite o ID da meta que deseja excluir: {cor('reset')}").strip()

    if not any(str(meta[0]) == id_excluir for meta in metas_encontradas):
        print(f"{cor('vermelho')}❌ ID inválido. Operação cancelada.{cor('reset')}")
        return

    confirmacao = input(
        f"{cor('vermelho')}Tem certeza que deseja excluir esta meta? (s/n): {cor('reset')}").strip().lower()
    if confirmacao in ["s", "sim"]:
        if excluir_meta_por_id(id_excluir):
            print(f"\n{cor('verde')}✅ Meta excluída com sucesso!{cor('reset')}")
    else:
        print(f"\n{cor('amarelo')}❌ Operação cancelada.{cor('reset')}")
