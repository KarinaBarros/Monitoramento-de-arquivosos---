from db_connection import criar_conexao, liberar_conexao

def excluir_tabela():
    """ Exclui a tabela 'logs' se ela existir. """
    conn = criar_conexao()
    if conn is None:
        return

    try:
        cursor = conn.cursor()

        # Verifica se a tabela 'logs' existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = 'logs'
            );
        """)

        if cursor.fetchone()[0]:
            # Exclui a tabela 'logs'
            cursor.execute("DROP TABLE logs;")
            conn.commit()
            print("Tabela 'logs' excluída com sucesso.")
        else:
            print("A tabela 'logs' não existe.")
    
    except Exception as e:
        print(f"Erro ao executar comando SQL: {e}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)

def criar_tabela():
    """ Cria a tabela 'logs' se não existir. """
    conn = criar_conexao()
    if conn is None:
        return
    
    try:
        cursor = conn.cursor()
        
        # Verifica se a tabela já existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = 'logs'
            );
        """)
        
        if not cursor.fetchone()[0]:
            criar_tabela_sql = """
            CREATE TABLE logs (
                id SERIAL PRIMARY KEY,
                log TEXT NOT NULL,
                fonte TEXT,
                destino TEXT,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(criar_tabela_sql)
            conn.commit()
            print("Tabela 'logs' criada com sucesso.")
        else:
            print("A tabela 'logs' já existe.")
        
    except Exception as e:
        print(f"Erro ao executar comando SQL: {e}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            liberar_conexao(conn)
            


