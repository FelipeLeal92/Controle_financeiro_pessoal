from banco.metas_db import (
    obter_metas_por_referencia,
    exibir_metas_com_categorias
)
from utilitarios import *
from relatorios.filtros import filtrar_transacoes, exibir_filtros
from relatorios.exportar import exportar_para_csv
from metas import calcular_progresso_meta

def menu_debug():
    while True:
        print(f"\n{cor('negrito')}{cor('cyan')}===== MENU DEBUG METAS ====={cor('reset')}")
        print("1. 📜 Exibir metas por referência (ID da categoria)")
        print("2. 🏷️ Exibir metas por referência (Nome da categoria)")
        print("3. 🔍 Filtrar transações por período")
        print("4. 📈 Exibir progresso das metas")
        print("5. 📤 Exportar todas as metas para CSV")
        print("0. ❌ Sair")

        escolha = input(f"{cor('negrito')}Escolha uma opção: {cor('reset')}").strip()

        if escolha == "1":
            ref = input(f"{cor('negrito')}Digite a referência (MM/AAAA): {cor('reset')}").strip()
            metas = obter_metas_por_referencia(ref)
            for meta in metas:
                print(meta)

        elif escolha == "2":
            ref = input(f"{cor('negrito')}Digite a referência (MM/AAAA): {cor('reset')}").strip()
            exibir_metas_com_categorias(ref)

        elif escolha == "3":
            ref = input(f"{cor('negrito')}Digite o mês/ano para filtrar transações (MM-AAAA): {cor('reset')}").strip()
            transacoes = filtrar_transacoes("data", ref)
            exibir_filtros(transacoes)

        elif escolha == "4":
            ref = input(f"{cor('negrito')}Digite a referência da meta para ver progresso (MM-AAAA): {cor('reset')}").strip()
            id_meta = input(f"{cor('negrito')}Digite o ID da meta: {cor('reset')}").strip()
            calcular_progresso_meta(id_meta, ref)

        elif escolha == "5":
            ref = input(f"{cor('negrito')}Digite a referência para exportar metas (MM-AAAA): {cor('reset')}").strip()
            metas = obter_metas_por_referencia(ref)
            exportar_para_csv(metas)
            print(f"{cor('verde')}✅ Metas exportadas para CSV com sucesso!{cor('reset')}")

        elif escolha == "0":
            print(f"{cor('vermelho')}👋 Encerrando menu de debug...{cor('reset')}")
            break

        else:
            print(f"{cor('vermelho')}❌ Opção inválida. Tente novamente.{cor('reset')}")


if __name__ == "__main__":
    menu_debug()
