import datetime
from banco import *
from categorias import (adicionar_categorias, alterar_categoria, excluir_categoria)
from menus import *
from transacoes import *
from relatorios.analises import *
from utilitarios import validar_valor
from metas import *


def main():

    print(f'{cor("negrito")}{cor("magenta")}Antes de adicionar receitas e despesas, adicione categorias para elas.'
          f'{cor("reset")}')

    while True:
        escolha = menu()

        if escolha == '1':
            exibir_categorias()
            categoria = input('Qual categoria você deseja adicionar? ')
            adicionar_categorias(categoria)
            continue

        # ------------------------------------------------------------------
        if escolha == '2':
            menu_metas()
            continue

        # ------------------------------------------------------------------
        if escolha == '3':

            tipo = 'receita'
            data = input('\nData (DD-MM-AA): ')
            try:
                data_formatada = datetime.strptime(data, "%d-%m-%y").strftime("%Y-%m-%d")
            except ValueError:
                print(f"❌{cor("vermelho")} Data inválida. Use o formato DD-MM-AA.{cor('reset')}")
                sleep(1)
                continue

            exibir_descricao()
            descricao = input('Descrição: ')

            while True:
                valor_input = input("Valor: ").strip()
                valor = validar_valor(valor_input)
                if valor is not None:
                    break

            exibir_categorias()
            print(f'\n{cor("amarelo")}⚠️ Se a categoria que deseja não estiver na lista,'
                  f' aperte {cor("verde")}"0"{cor("amarelo")} e adicione-a.{cor('reset')}️')
            while True:
                id_categoria_input = input('Digite o ID da categoria: ').strip()
                try:
                    id_categoria = int(id_categoria_input)
                    break
                except ValueError:
                    print(f"❌{cor('vermelho')} ID inválido. Digite um número inteiro.{cor('reset')}")

            con = conectar()
            cursor = con.cursor()
            cursor.execute('SELECT id FROM categoria WHERE id = ?', (id_categoria,))
            resultado = cursor.fetchone()
            con.close()

            if resultado:
                adicionar_transacao(tipo, data_formatada, descricao, valor, id_categoria)
            else:
                print(f'❌{cor("vermelho")} Categoria não encontrada. Verifique se digitou '
                      f'corretamente ou adicione a categoria.{cor('reset')}')
            sleep(1)

        # ------------------------------------------------------------------
        elif escolha == '4':

            tipo = 'despesa'
            data = input('\nData (DD-MM-AA): ')
            try:
                data_formatada = datetime.strptime(data, "%d-%m-%y").strftime("%Y-%m-%d")
            except ValueError:
                print(f"❌{cor('vermelho')} Data inválida. Use o formato DD-MM-AA.{cor('reset')}")
                sleep(1)
                continue

            exibir_descricao()
            descricao = input('Descrição: ')

            while True:
                valor_input = input("Valor: ").strip()
                valor = validar_valor(valor_input)
                if valor is not None:
                    break

            exibir_categorias()
            print(f'\n{cor("amarelo")}⚠️ Se a categoria que deseja não estiver na lista,'
                  f' aperte {cor("verde")}"0"{cor("amarelo")} e adicione-a.{cor('reset')}️')
            while True:
                id_categoria_input = input('Digite o ID da categoria: ').strip()
                try:
                    id_categoria = int(id_categoria_input)
                    break
                except ValueError:
                    print(f"❌{cor('vermelho')} ID inválido. Digite um número inteiro.{cor('reset')}")

            con = conectar()
            cursor = con.cursor()
            cursor.execute('SELECT id FROM categoria WHERE id = ?', (id_categoria,))
            resultado = cursor.fetchone()
            con.close()

            if resultado:
                adicionar_transacao(tipo, data_formatada, descricao, valor, id_categoria)
            else:
                print(f'❌{cor("vermelho")}Categoria não encontrada. Verifique se digitou '
                      f'corretamente ou adicione a categoria.{cor('reset')}')
            sleep(1)

        # ------------------------------------------------------------------
        elif escolha == '5':

            while True:
                escolha2 = menu_relatorios()

                if escolha2 == '1':
                    exibir_saldo()
                    sleep(1)
                # ------------------------------------------------------------------
                elif escolha2 == '2':
                    resumo_mensal()
                    sleep(1)
                # ------------------------------------------------------------------
                elif escolha2 == '3':
                    menu_filtro()
                    sleep(1)
                # ------------------------------------------------------------------
                elif escolha2 == '4':
                    listar_transacoes()
                    sleep(1)
                # ------------------------------------------------------------------
                elif escolha2 == '5':
                    break

        # ------------------------------------------------------------------
        elif escolha == '6':
            listar_transacoes()

            print(f'\n{cor("magenta")}Dica: Escolha a opção desejada e digite o seu ID{cor("reset")}')

            transacao_id = input("Informe o ID da transação que deseja excluir: ")
            excluir_transacao(transacao_id)
            sleep(1)
        # ------------------------------------------------------------------
        elif escolha == '7':
            listar_transacoes()

            print(f'\n{cor("magenta")}Dica: Escolha a opção desejada e digite o seu ID{cor("reset")}')
            transacao_id = input("Informe o ID da transação que deseja editar: ")
            editar_transacao(transacao_id)
            sleep(1)
        # ------------------------------------------------------------------
        elif escolha == '8':
            exibir_categorias()

            print(f'\n{cor("magenta")}Dica: Escolha a opção desejada e digite o seu ID{cor("reset")}')

            categoria_id = input("Informe o ID da categoria que deseja excluir: ")
            excluir_categoria(categoria_id)
            sleep(1)
        # ------------------------------------------------------------------
        elif escolha == '9':
            exibir_categorias()

            categorias = listar_categorias()
            if not categorias:
                print(f"❌{cor('vermelho')} Nenhuma categoria cadastrada.{cor('reset')}")
                sleep(1)
                return

            print(f'\n{cor("magenta")}Dica: Escolha a opção desejada e digite o seu ID{cor("reset")}')

            categoria_id = input("Digite o ID da categoria que deseja renomear: ").strip()
            novo_nome = input("Digite o novo nome para essa categoria ou 'Enter' para manter o nome atual: ").strip()

            if categoria_id.isdigit():
                alterar_categoria(int(categoria_id), novo_nome)
            else:
                print(f"❌{cor('vermelho')}ID inválido. Deve ser um número.{cor('reset')}")
            sleep(1)
        # ------------------------------------------------------------------
        elif escolha == '10':
            print(f'\n👋 {cor("negrito")}{cor("amarelo")}Saindo do programa...{cor("reset")}')
            break

        else:
            print(f"❌{cor("vermelho")} Opção inválida, tente novamente.{cor('reset')}")
            sleep(1)

inicializar_banco()
resetar_metas_recorrentes()
main()