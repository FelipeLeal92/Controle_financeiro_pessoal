import csv
from controle_fincanceiro_pessoal.utilitarios import cor

def exportar_para_csv(transacoes):
    if transacoes:
        with open('transacoes.csv', 'w', newline='', encoding='utf-8') as arquivo:
            cabecalho = ['Data', 'Descrição', 'Valor', 'Categoria', 'Tipo']
            escritor = csv.writer(arquivo)
            escritor.writerow(cabecalho)
            escritor.writerows(transacoes)
        print(f'📁 {cor('verde')}Arquivo exportado com sucesso.{cor('reset')}')
    else:
        print(f"⚠️ {cor('amarelo')}Nada para exportar.{cor('reset')}")