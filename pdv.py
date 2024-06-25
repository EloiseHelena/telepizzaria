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
conector.close()

if num_results > 0:
  print('O banco de dados pizzaria_senac existe e esta pronto para uso.')
else:
   
    conector = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password=''
    )

    executor_mysql = conector.cursor()
    executor_mysql.execute('CREATE DATABASE pizzaria_senac;')
    conector.commit()
    
    conector = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='pizzaria_senac' 
    )

    executor_mysql = conector.cursor()
    executor_mysql.execute('CREATE TABLE pedidos (id INT AUTO_INCREMENT PRIMARY KEY, data DATE NOT NULL, tamanho VARCHAR(255),quantidade VARCHAR(255), valor_total DECIMAL(10,2) NOT NULL);')
    executor_mysql.execute('CREATE TABLE clientes (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), telefone VARCHAR(255), email VARCHAR(255));')

    conector.commit()
    conector.close()
    
def novo_pedido():
    def pedido_pizza(root):
        root.title("PIZZARIA SENAC")
        root.geometry("900x900")

        # Carregar e definir a imagem de fundo
        background_image = Image.open("imagens\Pizza-3007395.jpg")
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(root, image=background_photo)
        background_label.place(relwidth=1, relheight=1)
        background_label.image = background_photo  # Manter referência

        # Container para os widgets
        frame = tk.Frame(root, bg='#D2780D', bd=5, relief="ridge")
        frame.place(x=250, y=100)

        # Dicionários de preços e tamanhos
        tamanhos = ["Pequena", "Média", "Grande", "Família"]
        precos = {"Pequena": 25.00, "Média": 35.00, "Grande": 45.00, "Família": 50.00}
        ingredientes = ["Pepperoni: + R$ 3,00", "Bacon: + R$ 4,00", "Calabresa: + R$ 3,00"]
        precos_ingredientes = {"Pepperoni: + R$ 3,00": 3.00, "Bacon: + R$ 4,00": 4.00, "Calabresa: + R$ 3,00": 3.00}
        ingredientes2 = ["Queijo Extra: + R$ 2,00", "Cheddar: + R$ 5,00", "Catupiry: + R$ 5,00"]
        precos_ingredientes2 = {"Queijo Extra: + R$ 2,00": 2.00, "Cheddar: + R$ 5,00": 5.00, "Catupiry: + R$ 5,00": 5.00}
        bebidas = ["Coca-Cola 2l", "Pepsi 2l", "Fruki 2l", "Coca-Cola 350ml", "Pepsi 350ml", "Fruki 350ml", "Suco Delvalle", "Água"]
        precos_bebidas = {"Coca-Cola 2l": 10.00, "Pepsi 2l": 10.00, "Fruki 2l": 8.00, "Coca-Cola 350ml": 5.00, "Pepsi 350ml": 5.00, "Fruki 350ml": 4.00, "Suco Delvalle": 4.00, "Água": 2.00}

        titulo_label = tk.Label(root, text="REALIZE SEU PEDIDO!", font=('Cascadia Code', 20, 'bold'), bg='#D2780D', relief="raised")
        titulo_label.pack(pady=20)
        titulo_label.place(x=320, y=20)
        
        # Widgets de Tamanho e Preço
        tamanho_var = tk.StringVar(value=tamanhos[0])
        label_preco_unitario = tk.Label(frame, text="Valor unitário: ", bg='#D2780D', font=('Cascadia Code', 8, 'bold'))
        optionmenu_tamanho = tk.OptionMenu(frame, tamanho_var, *tamanhos, command=lambda _: atualizar_preco_unitario(tamanho_var, label_preco_unitario, precos, bebida_var, label_preco_unitario_bebida, precos_bebidas))
        optionmenu_tamanho.config(bg="#807E2A", fg="WHITE", activebackground='#444801')
        optionmenu_tamanho.grid(row=1, column=0, padx=10, pady=10)
        label_preco_unitario.grid(row=2, column=0, columnspan=1, pady=10)

        # Widgets de Ingredientes
        ingredientes_vars = {ing: tk.BooleanVar() for ing in ingredientes}
        for i, ing in enumerate(ingredientes):
            tk.Checkbutton(frame, text=ing, variable=ingredientes_vars[ing], bg='#D2780D', font=('Cascadia Code', 10), bd=3).grid(row=4+i, column=0, sticky="w")
        ingredientes2_vars = {ing: tk.BooleanVar() for ing in ingredientes2}
        for i, ing in enumerate(ingredientes2):
            tk.Checkbutton(frame, text=ing, variable=ingredientes2_vars[ing], bg='#D2780D', font=('Cascadia Code', 10), bd=3).grid(row=4+i, column=1, sticky="w")

        # Widgets de Bebida
        bebida_var = tk.StringVar(value=bebidas[0])
        label_preco_unitario_bebida = tk.Label(frame, text="Valor unitário: ", bg='#D2780D', font=('Cascadia Code', 8, 'bold'))
        optionmenu_bebida = tk.OptionMenu(frame, bebida_var, *bebidas, command=lambda _: atualizar_preco_unitario(tamanho_var, label_preco_unitario, precos, bebida_var, label_preco_unitario_bebida, precos_bebidas))
        optionmenu_bebida.config(bg="#807E2A", fg="WHITE", activebackground='#444801')
        optionmenu_bebida.grid(row=9, column=0, padx=5, pady=5)
        label_preco_unitario_bebida.grid(row=10, column=0, columnspan=1, pady=10)

        # Entry para Quantidade
        entry_quantidade = tk.Entry(frame, relief="sunken", bg='#EADAC0')
        entry_quantidade.grid(row=1, column=1, padx=5, pady=5)
        entry_quantidade_bebida = tk.Entry(frame, relief="sunken", bg='#EADAC0')
        entry_quantidade_bebida.grid(row=9, column=1, padx=5, pady=5)

        # Botão Pedir
        label_total = tk.Label(frame, text="Total a Pagar: R$ 0.00", bg='#D2780D', font=('Cascadia Code', 12, 'bold'))
        label_total.grid(row=12, column=0, columnspan=2, pady=10)
        button_pedir = tk.Button(frame, text="Pedir", font=('Cascadia Code', 12, 'bold'), height=2, width=10, borderwidth=5, bg='#807E2A', fg="WHITE", activebackground='#444801', command=lambda: pedir(entry_quantidade, tamanho_var, precos, ingredientes_vars, precos_ingredientes, ingredientes2_vars, precos_ingredientes2, bebida_var, precos_bebidas, entry_quantidade_bebida, label_total))
        button_pedir.grid(row=11, column=0, columnspan=3, pady=35)

        # Atualizar os preços unitários inicialmente
        atualizar_preco_unitario(tamanho_var, label_preco_unitario, precos, bebida_var, label_preco_unitario_bebida, precos_bebidas)
        
        def atualizar_preco_unitario(tamanho_var, label_preco_unitario, precos, bebida_var, label_preco_unitario_bebida, precos_bebidas, *args):
            tamanho_selecionado = tamanho_var.get()
            bebida_selecionada = bebida_var.get()

            preco_tamanho = precos[tamanho_selecionado]
            preco_bebida = precos_bebidas[bebida_selecionada]

            label_preco_unitario.config(text=f"Valor unitário: R$ {preco_tamanho:.2f}")
            label_preco_unitario_bebida.config(text=f"Valor unitário: R$ {preco_bebida:.2f}")

    def pedir(entry_quantidade, tamanho_var, precos, ingredientes_vars, precos_ingredientes, ingredientes2_vars, precos_ingredientes2, bebida_var, precos_bebidas, entry_quantidade_bebida, label_total):
        try:
            quantidade = int(entry_quantidade.get())
            if quantidade <= 0:
                raise ValueError("Quantidade deve ser maior que zero.")

            quantidade_bebida = int(entry_quantidade_bebida.get())
            if quantidade_bebida <= 0:
                raise ValueError("Quantidade deve ser maior que zero.")

            tamanho = tamanho_var.get()
            preco_tamanho = precos[tamanho]

            preco_ingredientes = sum(precos_ingredientes[ing] for ing, var in ingredientes_vars.items() if var.get())
            preco_ingredientes2 = sum(precos_ingredientes2[ing] for ing, var in ingredientes2_vars.items() if var.get())

            bebida = bebida_var.get()
            preco_bebida = precos_bebidas[bebida] * quantidade_bebida

            total = quantidade * (preco_tamanho + preco_ingredientes + preco_ingredientes2) + preco_bebida
            label_total.config(text=f"Total a Pagar: R$ {total:.2f}")

            if messagebox.askyesno("Confirmação", f"Você confirma o pedido de {quantidade} pizza(s) {tamanho} com {bebida} e ingredientes adicionais selecionados?"):
                messagebox.showinfo("Pedido Confirmado", "Seu pedido foi confirmado!")
            else:
                messagebox.showinfo("Pedido Cancelado", "Seu pedido foi cancelado.")

        except ValueError as e:
            messagebox.showerror("Erro", str(e))

      # Iniciar a interface gráfica
        root.mainloop()

    if __name__ == "__main__":
        root = tk.Tk()
        pedido_pizza(root)


def tela_adicionar_dados():
       
        janela_cadastro = Toplevel(janela_principal)
        janela_cadastro.title('Adicionar Cliente')

        nome_rotulo = tk.Label(janela_cadastro, text='Nome:', font=('Cascadia Code', 12, 'bold'))
        nome_rotulo.grid(row=0, column=0, padx=10, pady=10)
        nome_entrada =  tk.Entry(janela_cadastro)
        nome_entrada.grid(row=0, column=1, padx=10, pady=10)

        telefone_rotulo =  tk.Label(janela_cadastro, text='Telefone:', font=('Cascadia Code', 12, 'bold'))
        telefone_rotulo.grid(row=1, column=0, padx=10, pady=10)
        telefone_entrada =  tk.Entry(janela_cadastro)
        telefone_entrada.grid(row=1, column=1, padx=10, pady=10)

        email_rotulo =  tk.Label(janela_cadastro, text='Email:', font=('Cascadia Code', 12, 'bold'))
        email_rotulo.grid(row=2, column=0, padx=10, pady=10)
        email_entrada =  tk.Entry(janela_cadastro)
        email_entrada.grid(row=2, column=1, padx=10, pady=10)
        
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

         conector = mysql.connector.connect(
                        host='127.0.0.1',
                        user='root',
                        password='',
                        database='pizzaria_senac'
                        )
                    
         executor_mysql = conector.cursor()
         executor_mysql.execute('INSERT INTO clientes (nome, telefone, email) VALUES (%s, %s, %s)', (nome, telefone, email))
         conector.commit()
         conector.close()
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
               
                janela_cadastro = Toplevel(janela_clientes)
                janela_cadastro.title('Atualiza cliente')

                nome_rotulo = tk.Label(janela_cadastro, text='Nome:', font=('Cascadia Code', 12, 'bold'))
                nome_rotulo.grid(row=0, column=0, padx=10, pady=10)
                nome_entrada =  tk.Entry(janela_cadastro)
                nome_entrada.grid(row=0, column=1, padx=10, pady=10)

                telefone_rotulo =  tk.Label(janela_cadastro, text='Telefone:', font=('Cascadia Code', 12, 'bold'))
                telefone_rotulo.grid(row=1, column=0, padx=10, pady=10)
                telefone_entrada =  tk.Entry(janela_cadastro)
                telefone_entrada.grid(row=1, column=1, padx=10, pady=10)
                
                email_rotulo =  tk.Label(janela_cadastro, text='Email:',font=('Cascadia Code', 12, 'bold'))
                email_rotulo.grid(row=2, column=0, padx=10, pady=10)
                email_entrada =  tk.Entry(janela_cadastro)
                email_entrada.grid(row=2, column=1, padx=10, pady=10)

                confirm_btn = tk.Button(janela_cadastro, text='Adicionar', font=('Cascadia Code', 12, 'bold'), command=lambda: atualiza_banco(nome_entrada.get(), telefone_entrada.get(), email_entrada.get(),janela_cadastro))
                confirm_btn.grid(row=3, column=0, columnspan=2, pady=10)
                        
            else:
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

            conector = mysql.connector.connect(
                            host='127.0.0.1',
                            user='root',
                            password='',
                            database='pizzaria_senac')
            
            executor_mysql = conector.cursor()
            executor_mysql.execute('UPDATE clientes SET nome=%s, telefone=%s, email=%s WHERE id=%s', (novo_nome, novo_telefone, novo_email, id))
            conector.commit()
            atualiza()
            janela_cadastro.destroy()
           
    def deleta_cliente():
                if tabela.selection(): 
                    item = tabela.selection()[0]
                    data = tabela.item(item, 'values')
                    id = data[0]
        
                    if messagebox.askyesno('Confirmação', 'Tem certeza de que deseja excluir o registro?'):
                        conector = mysql.connector.connect(
                            host='127.0.0.1',
                            user='root',
                            password='',
                            database='pizzaria_senac')

                        executor_mysql = conector.cursor()
                        executor_mysql.execute('DELETE FROM clientes WHERE id=%s', (id,))  # Passe o ID como uma tupla de um elemento
                        conector.commit()
                        atualiza()     
                else:
                    messagebox.showerror('Erro', 'Nenhum registro selecionado.')
                    return
            
    def atualiza():
        conector = mysql.connector.connect(
                            host='127.0.0.1',
                            user='root',
                            password='',
                            database='pizzaria_senac')

        executor_mysql =  executor_mysql = conector.cursor()
        executor_mysql.execute('SELECT * FROM clientes')
        rows =executor_mysql.fetchall()

 
        for row in tabela.get_children():
            tabela.delete(row)

        for row in rows:
            tabela.insert('', 'end', values=row)

        tabela.bind('<<TreeviewSelect>>', selecao_unica)

    def selecao_unica(event):
            item = tabela.selection()[0]
            data = tabela.item(item, 'values')
            id = data[0]
            nome = data[1]
            telefone = data[2]
            email = data[3]

    botao_atualizar = tk.Button(janela_clientes, text="Atualizar", font=('Cascadia Code', 12, 'bold'),command=atualiza_cliente)
    botao_excluir = tk.Button(janela_clientes, text="Excluir", font=('Cascadia Code', 12, 'bold'), command=deleta_cliente)
    botao_atualizar.pack(side=LEFT) 
    botao_excluir.pack(side=LEFT) 
   

janela_principal = tk.Tk()

janela_principal.title("PDV PIZZARIA SENAC")
janela_principal.geometry("400x200")
barra_de_menus = tk.Menu(janela_principal)
janela_principal.config(menu=barra_de_menus)

menu_cadastro = tk.Menu(barra_de_menus, tearoff=0)
barra_de_menus.add_cascade(label="Cadastro", menu=menu_cadastro)
menu_cadastro.add_command(label="Cliente", command=tela_adicionar_dados)
menu_cadastro.add_command(label="Clientes", command=tela_clientes)

menu_pedido = tk.Menu(barra_de_menus, tearoff=0)
barra_de_menus.add_cascade(label="Pedido", menu=menu_pedido)
menu_pedido.add_command(label="Novo Pedido", command=novo_pedido)
menu_pedido.add_command(label="Consultar Pedidos", command=lambda: print("Consultando pedidos..."))
menu_relatorio = tk.Menu(barra_de_menus, tearoff=0)

barra_de_menus.add_cascade(label="Relatório", menu=menu_relatorio)
menu_relatorio.add_command(label="Vendas por Período", command=lambda: print("Gerando relatório de vendas por período..."))
menu_relatorio.add_command(label="Produtos Mais Vendidos", command=lambda: print("Gerando relatório de produtos mais vendidos..."))
menu_configuracao = tk.Menu(barra_de_menus, tearoff=0)


janela_principal.mainloop()