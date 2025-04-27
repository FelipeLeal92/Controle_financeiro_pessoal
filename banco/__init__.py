from controle_fincanceiro_pessoal.banco.conexao  import conectar
from .metas_db import resetar_metas_recorrentes

def inicializar_banco():

    con = conectar()    # Criar um banco de dados
    cursor = con.cursor()   # Cria um cursor para executar comandos SQL
    # Cria a tabela principal: transações.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        id_categoria INTEGER, 
        tipo TEXT,
        FOREIGN KEY (id_categoria) REFERENCES categoria(id)   
    )
    """)
    # Cria auxiliar: categoria.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT
    )    
    """)
    # Cria auxiliar: metas.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria_id INTEGER NOT NULL,
        tipo TEXT CHECK(tipo IN ('despesa', 'receita')) NOT NULL,
        valor_limite REAL NOT NULL,
        progresso REAL DEFAULT 0,
        referencia TEXT NOT NULL,  -- formato 'mm/yyyy'
        recorrente INTEGER DEFAULT 0,
        FOREIGN KEY (categoria_id) REFERENCES categoria(id)
    )    
    """)

    con.commit()
    con.close()
