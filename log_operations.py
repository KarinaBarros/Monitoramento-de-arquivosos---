from db_connection import criar_conexao, liberar_conexao
from datetime import datetime, timedelta

def adicionar_log(log, fonte, destino):
    """ Adiciona um log à tabela 'logs' no banco de dados. """
    conn = criar_conexao()
    if conn is None:
        return
    
    cursor = None
    try:
        cursor = conn.cursor()
        comando_sql = "INSERT INTO logs (log, data, fonte, destino) VALUES (%s, %s, %s, %s);"
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(comando_sql, (log, data_atual, fonte, destino))
        conn.commit()
        print(f"Log adicionado: {log}")
        
    except Exception as e:
        print(f"Erro ao adicionar log: {e}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)
            
# Função para carregar dados do banco de dados e atualizar o Treeview
def atualizar_treeview(treeview):
    conn = criar_conexao()
    if conn is None:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, log, fonte, destino, data FROM logs ORDER BY id DESC")
        rows = cursor.fetchall()
        
        # Limpa o Treeview antes de adicionar novos dados
        for row in treeview.get_children():
            treeview.delete(row)
        
        # Insere os dados no Treeview
        for row in rows:
            treeview.insert("", "end", values=row)
    
    except Exception as e:
        print(f"Erro ao atualizar Treeview: {e}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)
            
            
def verificar_registros(fonte):
    """ Verifica se foram inseridos 5 registros com a mesma fonte nos últimos 10 minutos. """
    conn = criar_conexao()
    if conn is None:
        return False
    
    cursor = None
    try:
        cursor = conn.cursor()
        tempo_limite = datetime.now() - timedelta(minutes=10)
        comando_sql = """
            SELECT COUNT(*)
            FROM logs
            WHERE fonte = %s AND data >= %s;
        """
        cursor.execute(comando_sql, (fonte, tempo_limite.strftime('%Y-%m-%d %H:%M:%S')))
        resultado = cursor.fetchone()
        
        if resultado[0] >= 5:
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Erro ao verificar registros: {e}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)
    
            

