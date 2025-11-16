import sqlite3
from datetime import datetime

DB_NAME = "imagens.db"

def criar_tabela():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS imagens_enviadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_arquivo TEXT NOT NULL,
            caminho_arquivo TEXT NOT NULL,
            resposta_api TEXT NOT NULL,
            criado_em DATETIME NOT NULL
        );
    """)

    conn.commit()
    conn.close()


def salvar_informacoes(nome_arquivo, caminho_arquivo, resposta_api):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO imagens_enviadas (nome_arquivo, caminho_arquivo, resposta_api, criado_em)
        VALUES (?, ?, ?, ?);
    """, (nome_arquivo, caminho_arquivo, resposta_api, datetime.now()))

    conn.commit()
    conn.close()


def listar_registros():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM imagens_enviadas ORDER BY criado_em DESC;")
    registros = cursor.fetchall()

    conn.close()
    return registros
