from controle_fincanceiro_pessoal.utilitarios import cor, obter_mes_ano_atual, calcular_mes_anterior
from controle_fincanceiro_pessoal.banco.conexao  import conectar


def criar_nova_meta(categoria_id, tipo, valor_limite, recorrente, referencia):
    # Conectar ao banco de dados
    con = conectar()
    cursor = con.cursor()

    # Inserir a nova meta no banco de dados
    query = """
    INSERT INTO metas (categoria_id, tipo, valor_limite, recorrente, referencia)
    VALUES (?, ?, ?, ?, ?);
    """
    cursor.execute(query, (categoria_id, tipo, valor_limite, recorrente, referencia))

    con.commit()  # Comitar a inserção
    con.close()

    print(f"✅ {cor('verde')}Nova meta para {referencia} foi criada com sucesso!{cor('reset')}")
    return True

#----------------------------------------------------------
def buscar_meta_por_categoria_mes_ano(categoria_id, referencia):
    # Conectar ao banco de dados
    con = conectar()
    cursor = con.cursor()

    # Consulta para verificar se já existe uma meta para a categoria e o mês/ano
    cursor.execute("""
            SELECT 
                m.id, c.nome AS nome_categoria, m.tipo, m.valor_limite, m.referencia, m.recorrente
            FROM 
                metas m
            JOIN 
                categoria c ON m.categoria_id = c.id
            WHERE 
                m.categoria_id = ? 
                AND (m.referencia = ? OR m.recorrente = 1)
        """, (categoria_id, referencia))

    resultado = cursor.fetchone()
    con.close()

    if resultado:
        meta = {
            'id': resultado[0],
            'categoria': resultado[1],
            'tipo': resultado[2],
            'valor_limite': resultado[3],
            'referencia': resultado[4],
            'recorrente': bool(resultado[5])
        }
        return meta
    else:
        return None  # Retorna None se não encontrar

#----------------------------------------------------------
def inserir_meta_no_banco(categoria_id, tipo, valor_limite, recorrente, referencia=None):

    # Caso a meta seja recorrente, precisamos verificar se já existe um registro para o mês/ano
    if recorrente == 1:
        # Verificar se já existe uma meta para o mês/ano atual (se já existir, atualizamos, senão criamos uma nova)
        resultado = buscar_meta_por_categoria_mes_ano(categoria_id,
                                                      referencia)  # Função para buscar no banco

        if resultado:  # Já existe uma meta para esse mês/ano
            # Atualizar a meta existente
            print(f"⚠️ {cor('amarelo')}Meta já existente para {referencia}.{cor('reset')} Atualizando a meta...")

            return atualizar_meta(categoria_id, tipo, valor_limite, referencia) # função de atualização

        else:
            # Se não houver meta existente, cria uma nova meta para esse mês/ano
            print(f"{cor('verde')}Criando uma nova meta para {referencia}...")
            return criar_nova_meta(categoria_id, tipo, valor_limite, recorrente, referencia)

    else:  # Para metas não recorrentes, o processo permanece o mesmo
        print(f"{cor('verde')}Criando uma nova meta não recorrente para {referencia}...")
        return criar_nova_meta(categoria_id, tipo, valor_limite, recorrente, referencia)

#----------------------------------------------------------
def resetar_metas_recorrentes():
    """
    Duplica metas recorrentes do mês anterior para o mês atual, com progressão zerada.
    """
    mes_atual = obter_mes_ano_atual()
    mes_anterior = calcular_mes_anterior(mes_atual)  # Nova função para calcular o mês anterior

    con = conectar()
    cursor = con.cursor()

    # Verifica se já existem metas recorrentes cadastradas para o mês anterior
    cursor.execute("""
        SELECT id, categoria_id, tipo, valor_limite
        FROM metas
        WHERE referencia = ? AND recorrente = 1
    """, (mes_anterior,))
    metas_recorrentes = cursor.fetchall()

    if not metas_recorrentes:
        print(f"🔴 Não há metas recorrentes para o mês anterior ({mes_anterior}). Nenhuma meta será duplicada.")
        con.close()
        return

    # Duplica as metas recorrentes para o mês atual
    for meta in metas_recorrentes:
        id_meta, categoria_id, tipo, valor_limite = meta

        cursor.execute("""
            INSERT INTO metas (categoria_id, tipo, valor_limite, referencia, recorrente)
            VALUES (?, ?, ?, ?, ?)
        """, (categoria_id, tipo, valor_limite, mes_atual, 1))

    con.commit()
    con.close()

#--------------------------------------------------------
def obter_metas_por_referencia(referencia: str):
    """
    Retorna todas as metas cadastradas para o mês/ano informado com o seu número de ID.
    """
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        SELECT * FROM metas
        WHERE referencia = ?
    """, (referencia,))
    resultados = cursor.fetchall()
    con.close()
    return resultados

#--------------------------------------------------------
def obter_metas_com_categorias(referencia: str):
    """
    Retorna todas as metas do mês com nome da categoria.
    """
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
        SELECT m.id, c.nome AS categoria, m.tipo, m.valor_limite, m.referencia, m.recorrente
        FROM metas m
        JOIN categoria c ON m.categoria_id = c.id
        WHERE m.referencia = ?
    """, (referencia,))
    resultados = cursor.fetchall()
    con.close()
    return resultados

#--------------------------------------------------------
def exibir_metas_com_categorias(referencia: str):
    """
    Exibe as metas no banco de dados em uma tabela formatada, com cores e valores acumulados reais.
    """
    con = conectar()
    cursor = con.cursor()

    cursor.execute("""
        SELECT m.id, m.categoria_id, c.nome, m.tipo, m.valor_limite, m.referencia, m.recorrente
        FROM metas m
        JOIN categoria c ON m.categoria_id = c.id
        WHERE m.referencia = ?
    """, (referencia,))
    metas = cursor.fetchall()

    if not metas:
        print(f"⚠️ {cor('amarelo')}Nenhuma meta encontrada para {referencia}.{cor('reset')}")
        con.close()
        return

    print(f"\n{cor('negrito')}📅 Metas para {referencia}:{cor('reset')}")
    print(
        f"{cor('negrito')}{'ID':<4} {'Categoria':<18} {'Tipo':<10} {'Meta (R$)':<12} {'Acumulado (R$)':<17} "
        f"{'Restante (R$)':<15} {'Progresso':<15} {'Recorrente'}{cor('reset')}")
    print("-" * 108)

    alertas = []

    for id_meta, categoria_id, categoria, tipo, valor_limite, referencia, recorrente in metas:
        # Consulta o total acumulado real nas transações
        cursor.execute("""
            SELECT COALESCE(SUM(
            valor), 0)
            FROM transacoes
            WHERE id_categoria = ? AND strftime('%m/%Y', data) = ?
        """, (categoria_id, referencia))
        acumulado = cursor.fetchone()[0]

        try:
            valor_limite = float(valor_limite)
            acumulado = float(acumulado)
            restante = valor_limite - acumulado
            percentual = (acumulado / valor_limite) * 100 if valor_limite > 0 else 0
        except ValueError:
            print(f"{cor('vermelho')}❌ Erro ao converter valores da meta '{categoria}'.{cor('reset')}")
            continue

        # Emoji e alerta
        if percentual >= 100:
            progresso_emoji = "🚨" if tipo.lower() == "despesa" else "🎉"
            alerta = f"{progresso_emoji} A meta de {tipo.upper()} '{categoria}' foi ULTRAPASSADA!"
        elif percentual >= 80:
            progresso_emoji = "⚠️"
            alerta = f"⚠️ A meta de {tipo.upper()} '{categoria}' ultrapassou 80%!"
        else:
            progresso_emoji = ""
            alerta = None

        if alerta:
            if tipo.lower() == 'despesa' and percentual >= 100:
                alertas.append(cor("vermelho") + alerta + cor("reset"))
            elif tipo.lower() == 'despesa' and percentual >= 80:
                alertas.append(cor("amarelo") + alerta + cor("reset"))
            elif tipo.lower() == 'receita' and percentual >= 100:
                alertas.append(cor("verde") + alerta + cor("reset"))

        # Cor da linha
        if tipo.lower() == 'despesa':
            if percentual >= 100:
                cor_linha = cor("vermelho")
            elif percentual >= 80:
                cor_linha = cor("amarelo")
            else:
                cor_linha = cor("reset")
        elif tipo.lower() == 'receita' and percentual >= 100:
            cor_linha = cor("verde")
        else:
            cor_linha = cor("reset")

        progresso_formatado = f"{percentual:.2f}% {progresso_emoji}"
        print(
            f"{cor_linha}{id_meta:<4} {categoria:<18} {tipo:<10} R${valor_limite:<10.2f} R${acumulado:<15.2f} R${restante:<15.2f} {progresso_formatado:<15} {'🔁' if recorrente else '📌'}{cor('reset')}"
        )

    print(f"\n{cor('negrito')}📢 Alertas:{cor('reset')}")
    if alertas:
        for alerta in alertas:
            print(alerta)
    else:
        print(f"👌 {cor('amarelo')}Nenhum alerta para exibir.{cor('reset')}")

    con.close()

#--------------------------------------------------------
def atualizar_meta(categoria_id, tipo, valor_limite, referencia, recorrente=None):
    """Atualiza uma meta no banco de dados.
    Se 'recorrente' for None, apenas 'tipo' e 'valor_limite' serão atualizados.
    Caso contrário, todos os campos serão atualizados."""

    con = conectar()
    cursor = con.cursor()

    if recorrente is None:  # Atualização parcial
        query = """
        UPDATE metas 
        SET tipo = ?, valor_limite = ? 
        WHERE categoria_id = ? AND referencia = ?;
        """
        cursor.execute(query, (tipo, valor_limite, categoria_id, referencia))
    else:  # Atualização completa
        query = """
        UPDATE metas 
        SET tipo = ?, valor_limite = ?, recorrente = ?, referencia = ? 
        WHERE categoria_id = ?;
        """
        cursor.execute(query, (tipo, valor_limite, recorrente, referencia, categoria_id))

    con.commit()
    con.close()

    print(f"✅ {cor('verde')}Meta para {referencia} foi atualizada com sucesso!{cor('reset')}")
    return True

#--------------------------------------------------------
def excluir_meta_por_id(id_meta):
    """Exclui uma meta pelo ID."""
    con = conectar()
    cursor = con.cursor()

    query = "DELETE FROM metas WHERE id = ?"
    cursor.execute(query, (id_meta,))

    con.commit()
    con.close()
    return True
