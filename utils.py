import io
import os
import pandas as pd


def formatar_moeda(valor) -> str:
    """Formata um número float/int no padrão monetário brasileiro: R$ 1.234,56"""
    if valor is None or pd.isna(valor):
        return "R$ 0,00"
    try:
        val = float(valor)
        is_negative = val < 0
        val = abs(val)
        # Formata com separador de milhar americano e inverte para o padrão BRL
        texto = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"-R$ {texto}" if is_negative else f"R$ {texto}"
    except (ValueError, TypeError):
        return "R$ 0,00"


def formatar_percentual(valor) -> str:
    """Formata valor percentual no padrão brasileiro: 25,4%"""
    if valor is None or pd.isna(valor):
        return "0,0%"
    try:
        val = float(valor)
        return f"{val:.1f}%".replace(".", ",")
    except (ValueError, TypeError):
        return "0,0%"


def gerar_excel(df: pd.DataFrame) -> bytes:
    """Gera um arquivo Excel formatado com cabeçalhos amigáveis e resumo."""
    output = io.BytesIO()

    df_export = df.copy()

    # Mapeamento de colunas amigáveis
    colunas_map = {
        "id": "ID",
        "data": "Data",
        "tipo": "Tipo",
        "categoria": "Categoria",
        "forma_pagamento": "Forma de Pagamento",
        "status": "Status",
        "qtd_pedidos": "Qtd. Pedidos",
        "valor": "Valor (R$)",
        "descricao": "Observações / Descrição",
    }

    cols_existentes = [c for c in colunas_map.keys() if c in df_export.columns]
    df_export = df_export[cols_existentes].rename(columns=colunas_map)

    if "Data" in df_export.columns:
        df_export["Data"] = pd.to_datetime(df_export["Data"]).dt.strftime("%d/%m/%Y")

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_export.to_excel(writer, sheet_name="Extrato Financeiro", index=False)

        # Ajuste de largura de colunas
        worksheet = writer.sheets["Extrato Financeiro"]
        for col in worksheet.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            col_letter = col[0].column_letter
            worksheet.column_dimensions[col_letter].width = max(max_len + 3, 12)

    return output.getvalue()


def gerar_csv(df: pd.DataFrame) -> bytes:
    """Gera CSV com codificação UTF-8-SIG e separador ponto-e-vírgula para compatibilidade com Excel."""
    df_export = df.copy()

    colunas_map = {
        "id": "ID",
        "data": "Data",
        "tipo": "Tipo",
        "categoria": "Categoria",
        "forma_pagamento": "Forma de Pagamento",
        "status": "Status",
        "qtd_pedidos": "Qtd. Pedidos",
        "valor": "Valor (R$)",
        "descricao": "Observações / Descrição",
    }

    cols_existentes = [c for c in colunas_map.keys() if c in df_export.columns]
    df_export = df_export[cols_existentes].rename(columns=colunas_map)

    if "Data" in df_export.columns:
        df_export["Data"] = pd.to_datetime(df_export["Data"]).dt.strftime("%d/%m/%Y")

    csv_str = df_export.to_csv(index=False, sep=";", decimal=",", encoding="utf-8-sig")
    return csv_str.encode("utf-8-sig")


def obter_backup_db(db_path: str = "financeiro_delivery.db") -> bytes:
    """Lê os bytes do banco de dados SQLite para exportação/backup."""
    if os.path.exists(db_path):
        with open(db_path, "rb") as f:
            return f.read()
    return b""


def restaurar_backup_db(conteudo_bytes: bytes, db_path: str = "financeiro_delivery.db") -> bool:
    """Salva os bytes no arquivo de banco de dados SQLite."""
    try:
        with open(db_path, "wb") as f:
            f.write(conteudo_bytes)
        return True
    except Exception:
        return False
