import psycopg2
from psycopg2 import pool
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

Host =  os.getenv('HOST')
Database =  os.getenv('DATABASE')
Port = os.getenv('PORT')
User = os.getenv('USER')
Password = os.getenv('PASSWORD')

class PostgresConnectionPool:
    def __init__(self, minconn, maxconn, **db_params):
        self._pool = psycopg2.pool.SimpleConnectionPool(minconn, maxconn, **db_params)
    
    def get_connection(self):
        return self._pool.getconn()
    
    def release_connection(self, conn):
        self._pool.putconn(conn)
    
    def close_all_connections(self):
        self._pool.closeall()

# Inicializar o pool de conexões
pool = None

def criar_conexao():
    global pool
    if pool is None:
        pool = PostgresConnectionPool(
            minconn=1,
            maxconn=10,
            dbname=Database,
            user=User,
            password=Password,
            host=Host,
            port=Port
        )
    return pool.get_connection()

def liberar_conexao(conn):
    pool.release_connection(conn)
