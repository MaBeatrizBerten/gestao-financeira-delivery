from datetime import datetime
import sqlite3
import pandas as pd

DB_NAME = "financeiro_delivery.db"


def get_connection():
    """Retorna uma conexão SQLite com suporte a timeout e integridade."""
    conn = sqlite3.connect(DB_NAME, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Inicializa as tabelas e executa migrações automáticas de schema se necessário."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Tabela principal de lançamentos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lancamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                tipo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                descricao TEXT,
                valor REAL NOT NULL,
                forma_pagamento TEXT DEFAULT 'Pix',
                status TEXT DEFAULT 'Pago',
                qtd_pedidos INTEGER DEFAULT 1
            )
        """)

        # Migração segura para adicionar novas colunas se o banco já existia
        cursor.execute("PRAGMA table_info(lancamentos)")
        colunas_existentes = [col["name"] for col in cursor.fetchall()]

        if "forma_pagamento" not in colunas_existentes:
            cursor.execute("ALTER TABLE lancamentos ADD COLUMN forma_pagamento TEXT DEFAULT 'Pix'")

        if "status" not in colunas_existentes:
            cursor.execute("ALTER TABLE lancamentos ADD COLUMN status TEXT DEFAULT 'Pago'")

        if "qtd_pedidos" not in colunas_existentes:
            cursor.execute("ALTER TABLE lancamentos ADD COLUMN qtd_pedidos INTEGER DEFAULT 1")

        # Tabela de Fechamento de Caixa Diário
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fechamentos_caixa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                fundo_troco REAL DEFAULT 0,
                dinheiro_gaveta REAL DEFAULT 0,
                total_dinheiro REAL DEFAULT 0,
                total_pix REAL DEFAULT 0,
                total_cartao REAL DEFAULT 0,
                total_ifood REAL DEFAULT 0,
                total_saidas_dinheiro REAL DEFAULT 0,
                sangria REAL DEFAULT 0,
                diferenca REAL DEFAULT 0,
                observacao TEXT,
                criado_em TEXT NOT NULL
            )
        """)

        conn.commit()


def carregar_dados() -> pd.DataFrame:
    """Carrega todos os lançamentos em um DataFrame Pandas com colunas tratadas."""
    with sqlite3.connect(DB_NAME) as conn:
        df = pd.read_sql_query("SELECT * FROM lancamentos ORDER BY data DESC, id DESC", conn)

    if not df.empty:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")
        # Garante valores padrão caso existam nulos
        df["forma_pagamento"] = df["forma_pagamento"].fillna("Pix")
        df["status"] = df["status"].fillna("Pago")
        df["qtd_pedidos"] = df["qtd_pedidos"].fillna(1).astype(int)
        df["descricao"] = df["descricao"].fillna("")
        df["valor"] = df["valor"].fillna(0.0).astype(float)

        # Campos calculados de data
        df["ano"] = df["data"].dt.year
        df["mes_ano"] = df["data"].dt.strftime("%Y-%m")
        df["dia_mes"] = df["data"].dt.strftime("%d/%m")
        df["data_formatada"] = df["data"].dt.strftime("%d/%m/%Y")
    else:
        df = pd.DataFrame(
            columns=[
                "id",
                "data",
                "tipo",
                "categoria",
                "descricao",
                "valor",
                "forma_pagamento",
                "status",
                "qtd_pedidos",
                "ano",
                "mes_ano",
                "dia_mes",
                "data_formatada",
            ]
        )

    return df


def salvar_registro(
    data,
    tipo: str,
    categoria: str,
    descricao: str,
    valor: float,
    forma_pagamento: str = "Pix",
    status: str = "Pago",
    qtd_pedidos: int = 1,
) -> int:
    """Insere um novo lançamento no banco de dados."""
    data_str = data.strftime("%Y-%m-%d") if hasattr(data, "strftime") else str(data)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO lancamentos (
                data, tipo, categoria, descricao, valor, forma_pagamento, status, qtd_pedidos
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data_str,
                tipo,
                categoria,
                descricao or "",
                float(valor),
                forma_pagamento,
                status,
                int(qtd_pedidos),
            ),
        )
        conn.commit()
        return cursor.lastrowid


def atualizar_registro(
    id_registro: int,
    data,
    tipo: str,
    categoria: str,
    descricao: str,
    valor: float,
    forma_pagamento: str = "Pix",
    status: str = "Pago",
    qtd_pedidos: int = 1,
) -> bool:
    """Atualiza um registro existente."""
    data_str = data.strftime("%Y-%m-%d") if hasattr(data, "strftime") else str(data)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE lancamentos
            SET data = ?,
                tipo = ?,
                categoria = ?,
                descricao = ?,
                valor = ?,
                forma_pagamento = ?,
                status = ?,
                qtd_pedidos = ?
            WHERE id = ?
            """,
            (
                data_str,
                tipo,
                categoria,
                descricao or "",
                float(valor),
                forma_pagamento,
                status,
                int(qtd_pedidos),
                id_registro,
            ),
        )
        conn.commit()
        return cursor.rowcount > 0


def deletar_registro(id_registro: int) -> bool:
    """Exclui um registro pelo ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM lancamentos WHERE id = ?", (id_registro,))
        conn.commit()
        return cursor.rowcount > 0


def obter_registro_por_id(id_registro: int):
    """Busca um único registro pelo seu ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lancamentos WHERE id = ?", (id_registro,))
        row = cursor.fetchone()
        return dict(row) if row else None


def obter_resumo_dia(data_str: str) -> dict:
    """Calcula os totais de vendas e saídas por meio de pagamento para a data especificada."""
    with sqlite3.connect(DB_NAME) as conn:
        query = "SELECT * FROM lancamentos WHERE data = ?"
        df_dia = pd.read_sql_query(query, conn, params=(data_str,))

    if df_dia.empty:
        return {
            "vendas_dinheiro": 0.0,
            "vendas_pix": 0.0,
            "vendas_cartao": 0.0,
            "vendas_ifood": 0.0,
            "total_vendas": 0.0,
            "saidas_dinheiro": 0.0,
            "total_saidas": 0.0,
            "qtd_pedidos": 0,
        }

    entradas = df_dia[df_dia["tipo"] == "Entrada"]
    saidas = df_dia[df_dia["tipo"] == "Saída"]

    vendas_dinheiro = entradas[entradas["forma_pagamento"] == "Dinheiro"]["valor"].sum()
    vendas_pix = entradas[entradas["forma_pagamento"] == "Pix"]["valor"].sum()
    vendas_cartao = entradas[
        entradas["forma_pagamento"].isin(["Cartão de Débito", "Cartão de Crédito", "Cartão"])
    ]["valor"].sum()
    vendas_ifood = entradas[
        entradas["forma_pagamento"].isin(["iFood / Repasse", "iFood", "MenuDino"])
    ]["valor"].sum()

    saidas_dinheiro = saidas[saidas["forma_pagamento"] == "Dinheiro"]["valor"].sum()

    return {
        "vendas_dinheiro": float(vendas_dinheiro),
        "vendas_pix": float(vendas_pix),
        "vendas_cartao": float(vendas_cartao),
        "vendas_ifood": float(vendas_ifood),
        "total_vendas": float(entradas["valor"].sum()),
        "saidas_dinheiro": float(saidas_dinheiro),
        "total_saidas": float(saidas["valor"].sum()),
        "qtd_pedidos": int(entradas["qtd_pedidos"].fillna(1).sum()) if "qtd_pedidos" in entradas else len(entradas),
    }


def salvar_fechamento_caixa(
    data_str: str,
    fundo_troco: float,
    dinheiro_gaveta: float,
    total_dinheiro: float,
    total_pix: float,
    total_cartao: float,
    total_ifood: float,
    total_saidas_dinheiro: float,
    sangria: float,
    diferenca: float,
    observacao: str = "",
) -> int:
    """Registra um fechamento de caixa."""
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO fechamentos_caixa (
                data, fundo_troco, dinheiro_gaveta, total_dinheiro, total_pix,
                total_cartao, total_ifood, total_saidas_dinheiro, sangria, diferenca,
                observacao, criado_em
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data_str,
                float(fundo_troco),
                float(dinheiro_gaveta),
                float(total_dinheiro),
                float(total_pix),
                float(total_cartao),
                float(total_ifood),
                float(total_saidas_dinheiro),
                float(sangria),
                float(diferenca),
                observacao or "",
                agora,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def carregar_fechamentos_caixa() -> pd.DataFrame:
    """Carrega o histórico de fechamentos de caixa."""
    with sqlite3.connect(DB_NAME) as conn:
        df = pd.read_sql_query("SELECT * FROM fechamentos_caixa ORDER BY data DESC, id DESC", conn)
    return df
