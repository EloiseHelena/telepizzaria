from tkinter import *
import tkinter as tk
from tkinter import BOTH, messagebox
import datetime
import mysql.connector
import re
from tkinter import ttk
conector = mysql.connector.connect(host='127.0.0.1',user='root',password='')
from tkinter import Tk, Toplevel
from PIL import Image, ImageTk

executor_mysql = conector.cursor()
executor_mysql.execute('SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = "pizzaria_senac";')

num_results = executor_mysql.fetchone()[0]

# Fechar a conexão com o banco de dados
conector.close()

# Se o número de resultados for maior que zero, o banco de dados existe
if num_results > 0:
  print('O banco de dados pizzaria_senac existe e esta pronto para uso.')
else:
    # Conectar-se ao servidor MySQL para criar o banco de dados
    conector = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password=''
    )

    # Criar o banco de dados agenda
    executor_mysql = conector.cursor()
    executor_mysql.execute('CREATE DATABASE pizzaria_senac;')
    conector.commit()

    # Conectar-se ao banco de dados agenda recém-criado
    conector = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='pizzaria_senac'  # Especificar o banco de dados
    )

    
    executor_mysql = conector.cursor()
    executor_mysql.execute('CREATE TABLE pedidos (id INT AUTO_INCREMENT PRIMARY KEY, data DATE NOT NULL, tamanho VARCHAR(255),quantidade VARCHAR(255), valor_total DECIMAL(10,2) NOT NULL);')
    executor_mysql.execute('CREATE TABLE clientes (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), telefone VARCHAR(255), email VARCHAR(255));')
    # Fechar a conexão com o banco de dados
    conector.commit()
    conector.close()
    
def novo_pedido():
    class Pedido_Pizza:
        def __init__(self, root):
            self.root = root
            self.root.title("PIZZARIA SENAC")
            self.root.geometry("900x900")
            
            # Carregar e definir a imagem de fundo
            self.background_image = Image.open("imagens\Pizza-3007395.jpg")
            self.background_photo = ImageTk.PhotoImage(self.background_image)
            self.background_label = tk.Label(root, image=self.background_photo)
            self.background_label.place(relwidth=1, relheight=1)

            # Container para os widgets
            self.frame = tk.Frame(root, bg='#D2780D', bd=5, relief="ridge")
            self.frame.place(x=250, y=100)
            
            # Preços das pizzas e ingredientes
            self.tamanhos = ["Pequena", "Média", "Grande", "Família"]
            self.precos = {"Pequena": 25.00, "Média": 35.00, "Grande": 45.00, "Família": 50.00}
            
            self.ingredientes = ["Pepperoni: + R$ 3,00", "Bacon: + R$ 4,00", "Calabresa: + R$ 3,00"]
            self.precos_ingredientes = {"Pepperoni: + R$ 3,00": 3.00, "Bacon: + R$ 4,00": 4.00, "Calabresa: + R$ 3,00": 3.00}
            self.ingredientes2 = ["Queijo Extra: + R$ 2,00", "Cheddar: + R$ 5,00", "Catupiry: + R$ 5,00"]
            self.precos_ingredientes2 = {"Queijo Extra: + R$ 2,00": 2.00, "Cheddar: + R$ 5,00": 5.00, "Catupiry: + R$ 5,00": 5.00}
            
            self.bebidas = ["Coca-Cola 2l", "Pepsi 2l", "Fruki 2l", "Coca-Cola 350ml", "Pepsi 350ml", "Fruki 350ml",  "Suco Delvalle", "Água"]
            self.precos_bebidas = {"Coca-Cola 2l": 10.00, "Pepsi 2l": 10.00, "Fruki 2l": 8.00, "Coca-Cola 350ml": 5.00, "Pepsi 350ml": 5.00, "Fruki 350ml": 4.00, "Suco Delvalle": 4.00, "Água": 2.00}


            titulo_label = tk.Label(root, text="REALIZE SEU PEDIDO!", font=('Cascadia Code', 20, 'bold'), bg='#D2780D', relief="raised")
            titulo_label.pack(pady=20)
            titulo_label.place(x=320, y=20)
            
            # Widget tamanho pizza
            tk.Label(self.frame, text="Tamanho da Pizza:",bg='#D2780D',  font=('Cascadia Code', 12, 'bold')).grid(row=0, column=0, padx=5, pady=5)
            self.tamanho_var = tk.StringVar(value=self.tamanhos[0])
            self.optionmenu_tamanho = tk.OptionMenu(self.frame, self.tamanho_var, *self.tamanhos)
            self.optionmenu_tamanho.config(bg="#807E2A", fg="WHITE", activebackground='#444801')
            self.optionmenu_tamanho.grid(row=1, column=0, padx=10, pady=10)
            
            self.label_preco_unitario = tk.Label(self.frame,  text="Valor unitário: ", bg='#D2780D',  font=('Cascadia Code', 8, 'bold'))
            self.label_preco_unitario.grid(row=2, column=0, columnspan=1, pady=10)

            tk.Label(self.frame,  text="Quantidade:",bg='#D2780D',  font=('Cascadia Code', 12, 'bold')).grid(row=0, column=1, padx=5, pady=5)
            self.entry_quantidade = tk.Entry(self.frame, relief="sunken", bg='#EADAC0'  )
            self.entry_quantidade.grid(row=1, column=1, padx=5, pady=5)
            
            # Widget adicionais
            tk.Label(self.frame,  text="Ingredientes Adicionais:",bg='#D2780D', font=('Cascadia Code', 12, 'bold')).grid(row=3, column=0, padx=5, pady=5)
            self.ingredientes_vars = {}
            for i, ing in enumerate(self.ingredientes):
                var = tk.BooleanVar()
                self.ingredientes_vars[ing] = var
                chk = tk.Checkbutton(self.frame, text=ing, variable=var,bg='#D2780D', font=('Cascadia Code', 10), bd= 3)
                chk.config(activebackground='#91491A')
                chk.grid(row=4+i, column=0, sticky="w")
                
            tk.Label(self.frame)
            self.ingredientes2_vars = {}
            for i, ing in enumerate(self.ingredientes2):
                var = tk.BooleanVar()
                self.ingredientes2_vars[ing] = var
                chk = tk.Checkbutton(self.frame, text=ing, variable=var,bg='#D2780D', font=('Cascadia Code', 10), bd=3)
                chk.config(activebackground='#91491A')
                chk.grid(row=4+i, column=1, sticky="w")

            # Widget bebidas
            tk.Label(self.frame,  text="Escolha a Bebida:",bg='#D2780D', font=('Cascadia Code', 12, 'bold')).grid(row=8, column=0, padx=5, pady=5)
            self.bebida_var = tk.StringVar(value=self.bebidas[0])
            self.optionmenu_bebida = tk.OptionMenu(self.frame, self.bebida_var, *self.bebidas)
            self.optionmenu_bebida.config(bg="#807E2A", fg="WHITE", activebackground='#444801')
            self.optionmenu_bebida.grid(row=9, column=0, padx=5, pady=5)
            
            self.label_preco_unitario_bebida = tk.Label(self.frame,  text="Valor unitário: ", bg='#D2780D',  font=('Cascadia Code', 8, 'bold'))
            self.label_preco_unitario_bebida.grid(row=10, column=0, columnspan=1, pady=10)
            
            tk.Label(self.frame,  text="Quantidade:", bg='#D2780D', font=('Cascadia Code', 12, 'bold')).grid(row=8, column=1, padx=10, pady=10)
            self.entry_quantidade_bebida = tk.Entry(self.frame, relief="sunken", bg='#EADAC0' )
            self.entry_quantidade_bebida.grid(row=9, column=1, padx=5, pady=5)

            # Widget pedir
            self.button_pedir = tk.Button(self.frame,  text="Pedir", font=('Cascadia Code', 12, 'bold'),height= 2, width= 10, borderwidth= 5, bg='#807E2A', fg="WHITE", activebackground='#444801', command=self.pedir)
            self.button_pedir.grid(row=11, column=0, columnspan=3, pady=35)

            self.label_total = tk.Label(self.frame,  text="Total a Pagar: R$ 0.00", bg='#D2780D',  font=('Cascadia Code', 12, 'bold'))
            self.label_total.grid(row=12, column=0, columnspan=2, pady=10)

            #preço unitario label
            self.tamanho_var.trace("w", self.atualizar_preco_unitario)
            self.bebida_var.trace("w", self.atualizar_preco_unitario)
            self.atualizar_preco_unitario()
        def atualizar_preco_unitario(self, *args):
            
            tamanho_selecionado = self.tamanho_var.get()
            bebida_selecionada = self.bebida_var.get()
            
            preco_tamanho = self.precos[tamanho_selecionado]
            preco_bebida = self.precos_bebidas[bebida_selecionada]
            
            self.label_preco_unitario.config(text=f"Valor unitário: R$ {preco_tamanho:.2f}")
            self.label_preco_unitario_bebida.config(text=f"Valor unitário: R$ {preco_bebida:.2f}")

            
        def pedir(self):
            
            try:
                quantidade = int(self.entry_quantidade.get())
                if quantidade <= 0:
                    raise ValueError
                
                quantidade_bebida = int(self.entry_quantidade_bebida.get())
                if quantidade_bebida <= 0:
                    raise ValueError

            
                tamanho = self.tamanho_var.get()
                preco_tamanho = self.precos[tamanho]

                preco_ingredientes = sum(self.precos_ingredientes[ing] for ing in self.ingredientes if self.ingredientes_vars[ing].get())
                preco_ingredientes2 = sum(self.precos_ingredientes2[ing] for ing in self.ingredientes2 if self.ingredientes2_vars[ing].get())

                bebida = self.bebida_var.get()
                preco_bebida = self.precos_bebidas[bebida]*quantidade_bebida

                total = quantidade * preco_tamanho + (preco_ingredientes + preco_ingredientes2 + preco_bebida)
                self.label_total.config(text=f"Total a Pagar: R$ {total:.2f}")

                if messagebox.askyesno("Confirmação", f"Você confirma o pedido de {quantidade} pizza(s) {tamanho} com {bebida} e ingredientes adicionais selecionados?"):
                    messagebox.showinfo("Pedido Confirmado", "Seu pedido foi confirmado!")
                else:
                    messagebox.showinfo("Pedido Cancelado", "Seu pedido foi cancelado.")

            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira um número válido de pizzas.")
                


    if __name__ == "__main__":
        root = tk.Tk()
        app = Pedido_Pizza(root)
        root.mainloop()

    





def tela_addicinar_dados():
       
        janela_cadastro = Toplevel(janela_principal)
        janela_cadastro.title('Adicionar Cliente')

        # Entradas para adicionar dados
        nome_rotulo = tk.Label(janela_cadastro, text='Nome:')
        nome_rotulo.grid(row=0, column=0, padx=10, pady=10)
        nome_entrada =  tk.Entry(janela_cadastro)
        nome_entrada.grid(row=0, column=1, padx=10, pady=10)

        telefone_rotulo =  tk.Label(janela_cadastro, text='Telefone:')
        telefone_rotulo.grid(row=1, column=0, padx=10, pady=10)
        telefone_entrada =  tk.Entry(janela_cadastro)
        telefone_entrada.grid(row=1, column=1, padx=10, pady=10)

        email_rotulo =  tk.Label(janela_cadastro, text='Email:')
        email_rotulo.grid(row=2, column=0, padx=10, pady=10)
        email_entrada =  tk.Entry(janela_cadastro)
        email_entrada.grid(row=2, column=1, padx=10, pady=10)

        # Botão para confirmar a adição
        confirm_btn = tk.Button(janela_cadastro, text='Adicionar', command=lambda: adicionar_dados(nome_entrada.get(), telefone_entrada.get(), email_entrada.get(),janela_cadastro))
        confirm_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
def adicionar_dados(nome, telefone, email,janela_cadastro):
         if nome == '' or telefone == '' or email == '':
            messagebox.showerror('Erro', 'Todos os campos devem ser preenchidos.')
            return False

         if not re.match(r'^[0-9]+$', telefone):
            messagebox.showerror('Erro', 'O número de telefone deve conter apenas números.')
            return False

         if '@' not in email:
            messagebox.showerror('Erro', 'O e-mail deve conter um @.')
            return False

    # Adicionar dados ao banco de dados
         cnx = mysql.connector.connect(
                        host='127.0.0.1',
                        user='root',
                        password='',
                        database='telepizza'
                        )
                    
         cursor = cnx.cursor()
         cursor.execute('INSERT INTO clientes (nome, telefone, email) VALUES (%s, %s, %s)', (nome, telefone, email))
         cnx.commit()
         cnx.close()
         janela_cadastro.destroy()
         
def tela_clientes():
    janela_clientes =Toplevel(janela_principal)
    janela_clientes.title('Clientes')
    janela_clientes.focus_force()
         
    tabela = ttk.Treeview(janela_clientes, columns=('ID', 'Nome', 'Telefone', 'Email'), show='headings')
        
    tabela.heading('ID', text='ID')
    tabela.heading('Nome', text='Nome')
    tabela.heading('Telefone', text='Telefone')
    tabela.heading('Email', text='Email')
        
    tabela.pack(fill=BOTH, expand=True)
    tabela.bind('<Map>', lambda event: atualiza())
    
    def atualiza_cliente():
            if tabela.selection():
                # Janela para atualizar dados
               
                janela_cadastro = Toplevel(janela_clientes)
                janela_cadastro.title('Atualiza cliente')

                # Entradas para adicionar dados
                nome_rotulo = tk.Label(janela_cadastro, text='Nome:')
                nome_rotulo.grid(row=0, column=0, padx=10, pady=10)
                nome_entrada =  tk.Entry(janela_cadastro)
                nome_entrada.grid(row=0, column=1, padx=10, pady=10)

                telefone_rotulo =  tk.Label(janela_cadastro, text='Telefone:')
                telefone_rotulo.grid(row=1, column=0, padx=10, pady=10)
                telefone_entrada =  tk.Entry(janela_cadastro)
                telefone_entrada.grid(row=1, column=1, padx=10, pady=10)
                
                
                

                email_rotulo =  tk.Label(janela_cadastro, text='Email:')
                email_rotulo.grid(row=2, column=0, padx=10, pady=10)
                email_entrada =  tk.Entry(janela_cadastro)
                email_entrada.grid(row=2, column=1, padx=10, pady=10)

                # Botão para confirmar a adição
                confirm_btn = tk.Button(janela_cadastro, text='Adicionar', command=lambda: atualiza_banco(nome_entrada.get(), telefone_entrada.get(), email_entrada.get(),janela_cadastro))
                confirm_btn.grid(row=3, column=0, columnspan=2, pady=10)
                        
            else:
                # Nenhum item selecionado, mostre uma mensagem de erro ou faça outra ação
                messagebox.showerror('Erro', 'Nenhum registro selecionado.')
                return
            
    def atualiza_banco(novo_nome, novo_telefone, novo_email, janela_cadastro):
            if novo_nome == '' or novo_telefone == '' or novo_email == '':
                messagebox.showerror('Erro', 'Todos os campos devem ser preenchidos.')
                return 

            if not re.match(r'^[0-9]+$', novo_telefone):
                messagebox.showerror('Erro', 'O número de telefone deve conter apenas números.')
                return 

            if '@' not in novo_email:
                messagebox.showerror('Erro', 'O e-mail deve conter um @.')
                return 
        
            item = tabela.selection()[0]
            data = tabela.item(item, 'values')
            id = data[0]
            # Atualizar dados no banco de dados
            # o objeto 'cursor' é utilizado para executar a instrução SQL
            cnx = mysql.connector.connect(
                            host='127.0.0.1',
                            user='root',
                            password='',
                            database='telepizza')
            # Buscar dados do banco de dados e popular a tabela treeview
            cursor = cnx.cursor()
            cursor.execute('UPDATE clientes SET nome=%s, telefone=%s, email=%s WHERE id=%s', (novo_nome, novo_telefone, novo_email, id))
            # Confirma a alteração no banco de dados usando a função commit
            cnx.commit()
            # Fecha a janela de atualização
            atualiza()
            janela_cadastro.destroy()
           
    def deleta_cliente():
                if tabela.selection():  # Verifica se há algum item selecionado
                    item = tabela.selection()[0]
                    # Pegar o ID do contato selecionado
                    data = tabela.item(item, 'values')
                    id = data[0]
        
            
            
                # Verificar se o usuário realmente deseja excluir o registro
                    if messagebox.askyesno('Confirmação', 'Tem certeza de que deseja excluir o registro?'):
                         
                    # Deletar dados do banco de dados
                        cnx = mysql.connector.connect(
                            host='127.0.0.1',
                            user='root',
                            password='',
                            database='telepizza')
            # Buscar dados do banco de dados e popular a tabela treeview
                        cursor = cnx.cursor()
                       
                        cursor.execute('DELETE FROM clientes WHERE id=%s', (id,))  # Passe o ID como uma tupla de um elemento
                        cnx.commit()
                        atualiza()
                        
                else:
            # Nenhum item selecionado, mostre uma mensagem de erro ou faça outra ação
                    messagebox.showerror('Erro', 'Nenhum registro selecionado.')
                    return
            
            
                # Obter o item selecionado   
    def atualiza():
        cnx = mysql.connector.connect(
                            host='127.0.0.1',
                            user='root',
                            password='',
                            database='telepizza')
            # Buscar dados do banco de dados e popular a tabela treeview
        cursor =  cursor = cnx.cursor()
        cursor.execute('SELECT * FROM clientes')
        rows = cursor.fetchall()

            # Limpar dados anteriores
        for row in tabela.get_children():
            tabela.delete(row)

            # Adicionar novos dados
        for row in rows:
            tabela.insert('', 'end', values=row)

            # Adicionar um evento de seleção
        tabela.bind('<<TreeviewSelect>>', selecao_unica)
            # Botões para atualizar e deletar
    def selecao_unica(event):
            # Obter o item selecionado
            item = tabela.selection()[0]

            # Pegar os dados do item selecionado
            data = tabela.item(item, 'values')
            id = data[0]
            nome = data[1]
            telefone = data[2]
            email = data[3]
            # Fazer algo com os dados
    botao_atualizar = tk.Button(janela_clientes, text="Atualizar", command=atualiza_cliente)
    botao_excluir = tk.Button(janela_clientes, text="Excluir", command=deleta_cliente)

    # Posicionando os botões lado a lado na mesma linha
    botao_atualizar.pack(side=LEFT) 
    botao_excluir.pack(side=LEFT) 
   
   

# Cria a janela principal
janela_principal = tk.Tk()

# Define o título da janela principal
janela_principal.title("Menu Principal")
janela_principal.geometry("400x200")
# Cria o menu principal
barra_de_menus = tk.Menu(janela_principal)

# Configura a janela principal para usar o menu criado
janela_principal.config(menu=barra_de_menus)

# Cria um menu suspenso com o rótulo "Cadastro"
menu_cadastro = tk.Menu(barra_de_menus, tearoff=0)

# Adiciona o menu "Cadastro" ao menu principal
barra_de_menus.add_cascade(label="Cadastro", menu=menu_cadastro)

# Adiciona uma opção "Cliente" ao menu "Cadastro"
menu_cadastro.add_command(label="Cliente", command=tela_addicinar_dados)

# Adiciona uma opção "Produto" ao menu "Cadastro"
menu_cadastro.add_command(label="Clientes", command=tela_clientes)

# Cria um menu suspenso com o rótulo "Pedido"
menu_pedido = tk.Menu(barra_de_menus, tearoff=0)

# Adiciona o menu "Pedido" ao menu principal
barra_de_menus.add_cascade(label="Pedido", menu=menu_pedido)

# Adiciona uma opção "Novo Pedido" ao menu "Pedido"
menu_pedido.add_command(label="Novo Pedido", command=novo_pedido)

# Adiciona uma opção "Consultar Pedidos" ao menu "Pedido"
menu_pedido.add_command(label="Consultar Pedidos", command=lambda: print("Consultando pedidos..."))

# Cria um menu suspenso com o rótulo "Relatório"
menu_relatorio = tk.Menu(barra_de_menus, tearoff=0)

# Adiciona o menu "Relatório" ao menu principal
barra_de_menus.add_cascade(label="Relatório", menu=menu_relatorio)

# Adiciona uma opção "Vendas por Período" ao menu "Relatório"
menu_relatorio.add_command(label="Vendas por Período", command=lambda: print("Gerando relatório de vendas por período..."))

# Adiciona uma opção "Produtos Mais Vendidos" ao menu "Relatório"
menu_relatorio.add_command(label="Produtos Mais Vendidos", command=lambda: print("Gerando relatório de produtos mais vendidos..."))

# Cria um menu suspenso com o rótulo "Configuração"
menu_configuracao = tk.Menu(barra_de_menus, tearoff=0)


janela_principal.mainloop()