from controle_fincanceiro_pessoal.utilitarios import escolher_item_lista, padronizar_data
from controle_fincanceiro_pessoal.relatorios.filtros import (selecionar_data, exibir_filtros,
                                filtrar_transacoes, exibir_descricao)
from controle_fincanceiro_pessoal.relatorios.exportar import exportar_para_csv
from controle_fincanceiro_pessoal.categorias import selecionar_categoria
from controle_fincanceiro_pessoal.metas import *
from controle_fincanceiro_pessoal.banco.metas_db import exibir_metas_com_categorias
from time import sleep

def menu():

    print(f'\n {cor("negrito")}{cor("cyan")}=== CONTROLE FINANCEIRO PESSOAL ===')
    print(f'{cor("amarelo")}1. ➕ {cor("reset")}{cor("negrito")}Adicionar Categoria')
    print(f'{cor("amarelo")}2. 📈 {cor("reset")}{cor("negrito")}Metas')
    print(f'{cor("amarelo")}3. 💰 {cor("reset")}{cor("negrito")}Adicionar Receita')
    print(f'{cor("amarelo")}4. 💸 {cor("reset")}{cor("negrito")}Adicionar Despesa')
    print(f'{cor("amarelo")}5. 📋 {cor("reset")}{cor("negrito")}Relatórios')
    print(f'{cor("amarelo")}6. 🗑️ {cor("reset")}{cor("negrito")}Excluir transação')
    print(f'{cor("amarelo")}7. ✏️ {cor("reset")}{cor("negrito")}Editar transação')
    print(f'{cor("amarelo")}8. ❌ {cor("reset")}{cor("negrito")}Excluir categoria')
    print(f'{cor("amarelo")}9. 🏷️ {cor("reset")}{cor("negrito")}Editar categoria')
    print(f'{cor("amarelo")}10.🚪 {cor("reset")}{cor("negrito")}sair{cor("reset")}')

    print(f'\n{cor("magenta")}Dica: Escolha a opção desejada e digite um número entre 1 a 10')
    escolha = input(f'{cor("verde")}Escolha uma opção: {cor("reset")}')

    return escolha

#------------------------------------------------------------------
def menu_metas():

    while True:
        print(f'\n {cor("negrito")}{cor("cyan")}====== METAS =====')
        print(f'{cor("amarelo")}1. ➕ {cor("reset")}{cor("negrito")}Cadastrar meta')
        print(f'{cor("amarelo")}2. 📈 {cor("reset")}{cor("negrito")}Consultar metas')
        print(f'{cor("amarelo")}3. 💰 {cor("reset")}{cor("negrito")}Alterar metas')
        print(f'{cor("amarelo")}4. 💸 {cor("reset")}{cor("negrito")}Excluir meta')
        print(f'{cor("amarelo")}5. 🔙{cor("reset")}{cor("negrito")} Voltar ao Menu Principal{cor("reset")}')

        print(f'\n{cor("magenta")}Dica: Escolha a opção desejada e digite um número entre 1 a 5')
        opcao = input(f'{cor("verde")}Escolha uma opção: {cor("reset")}')

        if opcao == '1':  # Cadastrar meta
            cadastrar_meta()

        # Consultar metas
        elif opcao == '2':
            # Consulta metas com a referência como argumento
            referencia = padronizar_data()
            exibir_metas_com_categorias(referencia)
            sleep(3)

        elif opcao == '3':
            alterar_meta()

        elif opcao == '4':
            excluir_meta()

        elif opcao == '5':
            print(f'{cor("negrito")}{cor("amarelo")}Voltando ao Menu Principal...{cor("reset")}')
            break

        else:
            print(f"{cor('vermelho')}❌ Opção inválida! Tente novamente.{cor('reset')}")


#------------------------------------------------------------------
def menu_relatorios():

    print(f'\n{cor("negrito")}{cor("cyan")} =============== RELATÓRIOS ==============={cor("reset")}')
    print(f'{cor("negrito")}{cor("amarelo")}1. 🤑{cor("reset")} Visualizar Saldo Atual')
    print(f'{cor("negrito")}{cor("amarelo")}2. 📆{cor("reset")} Resumo Mensal')
    print(f'{cor("negrito")}{cor("amarelo")}3. 🔍{cor("reset")} Filtro de Transações')
    print(f'{cor("negrito")}{cor("amarelo")}4. 📄{cor("reset")} Listar Todas as Transações')
    print(f'{cor("negrito")}{cor("amarelo")}5. 🔙{cor("reset")} Voltar ao Menu Principal')

    print(f'\n{cor("magenta")}Dica: Escolha a opção desejada e digite um número entre 1 a 5')
    return input(f'{cor("verde")}Escolha uma opção: {cor("reset")}')

#------------------------------------------------------------------
def menu_filtro():

    print(f'\n{cor("negrito")}{cor("cyan")} ================== FILTROS =================={cor("reset")}')
    print("Escolha como deseja filtrar as transações:")
    print(f"{cor("negrito")}{cor("amarelo")}1.📆{cor("reset")}     Por data (MM-AAAA)")
    print(f"{cor("negrito")}{cor("amarelo")}2.🏷️{cor("reset")}     Por categoria")
    print(f"{cor("negrito")}{cor("amarelo")}3.📆🏷️{cor("reset")}   Por data + categoria")
    print(f"{cor("negrito")}{cor("amarelo")}4.📝{cor("reset")}     Por descrição")
    print(f"{cor("negrito")}{cor("amarelo")}5.📆📝{cor("reset")}   Por data + descrição")
    print(f"{cor("negrito")}{cor("amarelo")}6.🏷️📝{cor("reset")}   Por categoria + descrição")
    print(f"{cor("negrito")}{cor("amarelo")}7.📆🏷️📝{cor("reset")} Por data + categoria + descrição")
    print(f"{cor("negrito")}{cor("amarelo")}8.🔙{cor("reset")}      Retornar ao menu Relatórios")

    print(f'\n{cor("magenta")}Dica: Escolha a opção desejada e digite um número entre 1 a 8{cor("reset")}')
    opcao_filtro = input("Digite a opção desejada: ")

    while True:

        if opcao_filtro == "1":

            data_input = input('\nInforme o mês e o ano (MM-AAAA): ')
            data_formatada = selecionar_data(data_input)
            if not data_formatada:
                return

            transacoes = filtrar_transacoes(data_formatada=data_formatada)
            exibir_filtros(transacoes)

            if input('Deseja exportar para CSV? (S/N): ').upper().strip() == 'S':
                exportar_para_csv(transacoes)
            break

        # ------------------------------------------------------------------
        elif opcao_filtro == "2":

            exibir_categorias()
            while True:
                categoria_id = input('Digite o ID da categoria que deseja filtrar: ').strip()
                categoria_valida = selecionar_categoria(categoria_id)
                if categoria_valida:
                    break

            transacoes = filtrar_transacoes(categoria_id=categoria_valida)
            exibir_filtros(transacoes)

            if input('Deseja exportar para CSV? (S/N): ').upper().strip() == 'S':
                exportar_para_csv(transacoes)
            break

        # ------------------------------------------------------------------
        elif opcao_filtro == "3":
            # Selecionar data
            data_input = input('\nInforme o mês e o ano (MM-AAAA): ')
            data_formatada = selecionar_data(data_input)
            if not data_formatada:
                return

            # Selecionar categoria
            exibir_categorias()
            while True:
                categoria_id = input('Digite o ID da categoria que deseja filtrar: ').strip()
                categoria_valida = selecionar_categoria(categoria_id)
                if categoria_valida:
                    break

            # Consulta e exibição
            transacoes = filtrar_transacoes(data_formatada, categoria_id)
            exibir_filtros(transacoes)

            if input('Deseja exportar para CSV? (S/N): ').upper().strip() == 'S':
                exportar_para_csv(transacoes)
            break

        # ------------------------------------------------------------------
        elif opcao_filtro == "4":
            descricoes = exibir_descricao()
            if not descricoes:
                print(f"❌{cor('vermelho')} Nenhuma descrição cadastrada.")
                return

            # Usando a função para escolher a descrição com título personalizado
            descricao_nome = escolher_item_lista(descricoes, "Escolha o número da descrição", titulo="Descrições",
                                                 retornar='nome')
            # Certifique-se de que descricao_nome é válido
            if not descricao_nome:
                print(f"❌{cor('vermelho')} Descrição inválida.")
                return

            print(f"🔍 Descrição escolhida: {descricao_nome}")

            transacoes = filtrar_transacoes(descricao=descricao_nome)
            exibir_filtros(transacoes)

            if input('Deseja exportar para CSV? (S/N): ').upper().strip() == 'S':
                exportar_para_csv(transacoes)
            break

        # ------------------------------------------------------------------
        elif opcao_filtro == "5":
            data_input = input('\nInforme o mês e o ano (MM-AAAA): ')
            data_ajustada = selecionar_data(data_input)
            if not data_ajustada:
                return

            descricoes = exibir_descricao()
            if not descricoes:
                print(f"❌{cor('vermelho')} Nenhuma descrição cadastrada.")
                return
            # Usando a função para escolher a descrição com título personalizado
            descricao_nome = escolher_item_lista(descricoes, "Escolha o número da descrição", titulo="Descrições",
                                                 retornar='nome')
            # Certifique-se de que descricao_nome é válido
            if not descricao_nome:
                print(f"❌{cor('vermelho')} Descrição inválida.")
                return
            print(f"🔍 Descrição escolhida: {descricao_nome}")

            transacoes = filtrar_transacoes(data_ajustada, descricao=descricao_nome)
            exibir_filtros(transacoes)

            if input('Deseja exportar para CSV? (S/N): ').upper().strip() == 'S':
                exportar_para_csv(transacoes)
            break

        # ------------------------------------------------------------------
        elif opcao_filtro == "6":

            categorias = listar_categorias()
            if not categorias:
                print(f"❌{cor('vermelho')} Nenhuma categoria cadastrada.")
                return

            # Usando a função para escolher a categoria com título personalizado
            categoria_id = escolher_item_lista(categorias, "Escolha o número da categoria", titulo="Categorias",
                                               retornar='id')
            # Certifique-se de que categoria_id é válido
            if categoria_id is None:
                print(f"❌{cor('vermelho')} Categoria inválida.")

            # Exibir Descrições
            descricoes = exibir_descricao()
            if not descricoes:
                print(f"❌{cor('vermelho')} Nenhuma descrição cadastrada.")
                return

            # Usando a função para escolher a descrição com título personalizado
            descricao_nome = escolher_item_lista(descricoes, "Escolha o número da descrição", titulo="Descrições",
                                                 retornar='nome')
            # Certifique-se de que descricao_nome é válido
            if not descricao_nome:
                print(f"❌{cor('vermelho')} Descrição inválida.")
                return

            print(f"🔍 Descrição escolhida: {descricao_nome}")

            # Filtrar transações com os critérios escolhidos
            transacoes = filtrar_transacoes(categoria_id=categoria_id, descricao=descricao_nome)
            exibir_filtros(transacoes)

            if input('Deseja exportar para CSV? (S/N): ').upper().strip() == 'S':
                exportar_para_csv(transacoes)
            break

        # ------------------------------------------------------------------
        elif opcao_filtro == "7":
            # Input da data (com validação)
            while True:
                data_input = input("\nInforme o mês e o ano (mm-aaaa): ").strip()
                data_formatada = selecionar_data(data_input)
                if data_formatada:
                    break

            # Seleção da categoria
            categorias = listar_categorias()
            if not categorias:
                print(f"❌{cor('vermelho')} Nenhuma categoria cadastrada.")
                return
            # Usando a função para escolher a categoria com título personalizado
            categoria_id = escolher_item_lista(categorias, "Escolha o número da categoria", titulo="Categorias",
                                               retornar='id')
            # Certifique-se de que categoria_id é válido
            if categoria_id is None:
                print(f"❌{cor('vermelho')} Categoria inválida.")

            # Exibir Descrições
            descricoes = exibir_descricao()
            if not descricoes:
                print(f"❌{cor('vermelho')} Nenhuma descrição cadastrada.")
                return
            # Usando a função para escolher a descrição com título personalizado
            descricao_nome = escolher_item_lista(descricoes, "Escolha o número da descrição", titulo="Descrições",
                                                 retornar='nome')
            # Certifique-se de que descricao_nome é válido
            if not descricao_nome:
                print(f"❌{cor('vermelho')} Descrição inválida.")
                return
            print(f"🔍 Descrição escolhida: {descricao_nome}")

            # Filtra e exibe os resultados
            transacoes = filtrar_transacoes(categoria_id=categoria_id, descricao=descricao_nome)
            exibir_filtros(transacoes)

            if input('Deseja exportar para CSV? (S/N): ').upper().strip() == 'S':
                exportar_para_csv(transacoes)
            break

        # ------------------------------------------------------------------
        elif opcao_filtro == "8":
            break
        else:
            print(f"❌{cor("vermelho")} Opção inválida, tente novamente.{cor("reset")}")
