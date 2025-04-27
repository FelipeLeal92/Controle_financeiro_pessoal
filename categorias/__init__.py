from controle_fincanceiro_pessoal.banco.metas_db import conectar
from controle_fincanceiro_pessoal.utilitarios import cor
from time import sleep

def adicionar_categorias(nome):
    print(f'\n{cor("negrito")}----- Adicionar Categoria -----{cor('reset')}')

    con = conectar()
    cursor = con.cursor()
    cursor.execute('SELECT nome FROM categoria WHERE nome LIKE ?',
                   (f'%{nome}%',))
    resultado = cursor.fetchone()

    if resultado:
        print(f"❌{cor('vermelho')} Categoria já está adicionada.{cor('reset')}")
    else:
        cursor.execute("INSERT INTO categoria (nome) VALUES (?)", (nome,))
        print(f"✅{cor('verde')} Categoria adicionada com sucesso{cor('reset')}")
    sleep(1)

    con.commit()
    con.close()

#------------------------------------------------------------------
def listar_categorias():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT id, nome FROM categoria ORDER BY id")
    categorias = cursor.fetchall()
    con.close()
    return categorias

#------------------------------------------------------------------
def exibir_categorias():
    lista_categorias = listar_categorias()

    if lista_categorias:
        print(f'\n',f'{cor("negrito")}{cor("cyan")}-' * 9, 'Categorias', f'-' * 9)
        print(f"{cor("reset")}{'ID':<9} {'Nome':<20}")
        print(f'{cor("cyan")}-'*30)
        for id_categoria, nome in lista_categorias:
            print(f"{cor("negrito")}{cor("amarelo")}{id_categoria:<5} {cor("azul")}{nome:<20}{cor("reset")}")
    else:
        print(f"\n❌{cor('vermelho')} Nenhuma categoria adicionada{cor("reset")}")

#------------------------------------------------------------------
def alterar_categoria(categoria_id, novo_nome):
    con = conectar()
    cursor = con.cursor()

    # Verifica se a categoria existe
    cursor.execute("SELECT * FROM categoria WHERE id = ?", (categoria_id,))
    categoria = cursor.fetchone()

    if not categoria:
        print(f"❌{cor('vermelho')} ID de categoria não encontrado.{cor('reset')}")
    else:
        # Verifica se já existe uma categoria com o novo nome
        cursor.execute("SELECT * FROM categoria WHERE nome = ?", (novo_nome,))
        if cursor.fetchone():
            print(f"⚠️{cor('amarelo')} Já existe uma categoria com o nome '{novo_nome}'. Escolha outro nome."
                  f"{cor('reset')}")
        else:
            cursor.execute("UPDATE categoria SET nome = ? WHERE id = ?", (novo_nome, categoria_id))
            con.commit()
            print(f"✅ {cor('verde')} Categoria atualizada com sucesso para: {cor('amarelo')}{novo_nome}{cor('reset')}")
    sleep(1)

    con.close()

#------------------------------------------------------------------
def excluir_categoria(categoria_id):
    con = conectar()
    cursor = con.cursor()

    # Verifica se a categoria existe
    cursor.execute("SELECT * FROM categoria WHERE id = ?", (categoria_id,))
    categoria = cursor.fetchone()

    if not categoria:
        print(f"⚠️{cor('amarelo')} ID não encontrado.{cor('reset')}")
        con.close()
        return

    # Verifica se há transações associadas à categoria
    cursor.execute("SELECT * FROM transacoes WHERE id_categoria = ?", (categoria_id,))
    transacoes = cursor.fetchall()

    if transacoes:
        print(f"❌{cor('vermelho')} Não é possível excluir a categoria, pois há transações associadas a ela.")
        print(f"{cor('amarelo')}Primeiro delete as transações relacionadas a esta categoria para poder deletá-la"
              f"{cor('reset')}")
    else:
        cursor.execute("DELETE FROM categoria WHERE id = ?", (categoria_id,))
        con.commit()
        print(f"✅ {cor('verde')}Categoria excluída com sucesso.{cor('reset')}")
    sleep(1)

    con.close()

#------------------------------------------------------------------
def selecionar_categoria(categoria_id):
    categorias = listar_categorias()
    if not categorias:
        print(f"❌{cor('vermelho')} Nenhuma categoria cadastrada.{cor('reset')}")
        return None

    if not categoria_id.isdigit():
        print(f"⚠️{cor('amarelo')} O ID da categoria deve ser um número.{cor('reset')}")
        return None

    id_existe = any(str(cat[0]) == categoria_id for cat in categorias)
    if not id_existe:
        print(f"❌{cor('vermelho')} ID inválido. Por favor, escolha um ID da lista.{cor('reset')}")
        return None
    sleep(1)

    return categoria_id
