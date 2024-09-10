import os
import tkinter as tk
from tkinter import ttk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from log_operations import adicionar_log, atualizar_treeview, verificar_registros
from dotenv import load_dotenv
from tabela import excluir_tabela, criar_tabela

excluir_tabela()
criar_tabela()

# Carregar as variáveis de ambiente
load_dotenv()
caminho = os.getenv('CAMINHO')

# Variáveis globais
popup_aberto = None
registros = False

# Função para criar uma caixa de mensagem personalizada
def mostrar_mensagem_personalizada(fonte, treeview):
    global popup_aberto

    if popup_aberto is None or not popup_aberto.winfo_exists():
        popup_aberto = tk.Toplevel()
        popup_aberto.title("Atenção")
        popup_aberto.geometry("300x150")

        label = tk.Label(popup_aberto, text=f"Há pelo menos 5 registros com a fonte '{fonte}' nos últimos 10 minutos.")
        label.pack(pady=10)

        button = tk.Button(popup_aberto, text="OK", command=lambda: fechar_popup(popup_aberto, treeview))
        button.pack(pady=5)

def fechar_popup(popup, treeview):
    global popup_aberto
    popup_aberto = None
    popup.destroy()
    atualizar_treeview(treeview)  # Atualiza o Treeview ao fechar o pop-up
    global registros
    registros = False

# Classe para manipular eventos do sistema de arquivos
class ManipuladorDeEventos(FileSystemEventHandler):
    def __init__(self):
        super().__init__()

    def on_modified(self, evento):
        global registros
        if not evento.is_directory:
            log = 'Arquivo modificado'
            fonte = evento.src_path
            destino = None
            print(log)
            adicionar_log(log, fonte, destino)
            registros_excedidos = verificar_registros(fonte)
            if registros_excedidos:
                print(f"Há pelo menos 5 registros com a fonte '{fonte}' nos últimos 10 minutos.")
                registros = True
                mostrar_mensagem_personalizada(fonte, app.treeview)
            if not registros:
                atualizar_treeview(app.treeview)

    def on_created(self, evento):
        global registros
        if not evento.is_directory:
            log = 'Arquivo criado'
            fonte = evento.src_path
            destino = None
            print(log)
            adicionar_log(log, fonte, destino)
            if not registros:
                atualizar_treeview(app.treeview)

    def on_deleted(self, evento):
        global registros
        if not evento.is_directory:
            log = 'Arquivo excluído'
            fonte = evento.src_path
            destino = None
            print(log)
            adicionar_log(log, fonte, destino)
            if not registros:
                atualizar_treeview(app.treeview)

    def on_moved(self, evento):
        global registros
        if not evento.is_directory:
            log = 'Arquivo movido ou renomeado'
            fonte = evento.src_path
            destino = evento.dest_path
            print(log)
            adicionar_log(log, fonte, destino)
            if not registros:
                atualizar_treeview(app.treeview)

# Classe principal da aplicação
class MonitoramentoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Monitoramento de Arquivos")
        self.geometry("600x400")
        
        # Configuração do Treeview
        self.treeview = ttk.Treeview(self, columns=("ID", "Log", "Fonte", "Destino", "Data"), show="headings")
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Log", text="Log")
        self.treeview.heading("Fonte", text="Fonte")
        self.treeview.heading("Destino", text="Destino")
        self.treeview.heading("Data", text="Data")
        self.treeview.pack(fill=tk.BOTH, expand=True)
        
        # Botão para sair da aplicação
        self.btn_sair = tk.Button(self, text="Sair", command=self.on_close)
        self.btn_sair.pack(pady=10)
        
        # Inicia o monitoramento do diretório
        self.iniciar_monitoramento()
    
    def iniciar_monitoramento(self):
        if caminho is None:
            print("Erro: A variável de ambiente CAMINHO não está definida.")
            return

        if not os.path.exists(caminho):
            print(f"Erro: O caminho {caminho} não foi encontrado.")
            return

        try:
            manipulador_eventos = ManipuladorDeEventos()
            self.observador = Observer()
            self.observador.schedule(manipulador_eventos, caminho, recursive=True)
            self.observador.start()
            print("Monitoramento iniciado.")
            
            # Carregar dados iniciais
            atualizar_treeview(self.treeview)
        
        except Exception as e:
            print(f"Erro ao iniciar monitoramento: {e}")
    
    def on_close(self):
        # Parar o monitoramento antes de fechar a aplicação
        self.observador.stop()
        self.observador.join()
        self.destroy()

if __name__ == "__main__":
    app = MonitoramentoApp()
    app.mainloop()





