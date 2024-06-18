import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage



# Função para calcular o total
def calcular_total():
    tamanho = tamanho_var.get()
    quantidade = quantidade_entry.get()
    
    
    # Verificar se a quantidade é um número positivo
    if not quantidade.isdigit() or int(quantidade) <= 0:
        messagebox.showerror("Erro de Entrada", "Por favor, insira uma quantidade válida.")
        return
    
    quantidade = int(quantidade)
    total = precos[tamanho] * quantidade
    
    
    for ingrediente, var in ingredientes_vars.items():
        if var.get():
            total += precos_ingredientes[ingrediente] * quantidade
    
    total_label.config(text=f"Total a pagar: R$ {total:.2f}")

# Função para confirmar o pedido
def confirmar_pedido():
    calcular_total()
    total = total_label.cget("text").split("R$ ")[-1]
    if messagebox.askyesno("Confirmar Pedido", f"O total é R$ {total}. Deseja confirmar o pedido?"):
        messagebox.showinfo("Pedido Confirmado", "Seu pedido foi confirmado!")

# Janela principal
root = tk.Tk()
root.title("Pizzaria SENAC")

root.geometry('500x500')
image_path = "imagens\pngwing.com.png"
img = PhotoImage(file=image_path)
label = tk.Label(root, image=img)
label.pack()


# Título
titulo_label = tk.Label(root, text="Escolha o tamano da pizza e seus adicionais", font=('Cascadia Code', 12, 'bold'))
titulo_label.pack(pady=10)

# Preços das pizzas
precos = {"Pequena": 15.00, "Média": 22.00, "Grande": 28.00}

# OptionMenu para selecionar o tamanho da pizza
tamanho_var = tk.StringVar(root)
tamanho_var.set("Pequena")  # Tamanho padrão
tamanhos = ["Pequena", "Média", "Grande"]
tamanho_menu = tk.OptionMenu(root, tamanho_var, *tamanhos)
tamanho_menu.pack(pady=8)

# Entry para a quantidade de pizzas
quantidade_label = tk.Label(root, text="Quantidade:", font=('Cascadia Code', 12,))
quantidade_label.pack(pady=5)
quantidade_entry = tk.Entry(root)
quantidade_entry.pack(pady=5)


# Ingredientes adicionais
ingredientes = ["Queijo Extra", "Pepperoni", "Bacon", "Cheddar"]
precos_ingredientes = {"Queijo Extra": 2.00, "Pepperoni": 3.00, "Bacon": 4.00, "Cheddar": 4.00}
ingredientes_vars = {}

ingredientes_label = tk.Label(root, text="Ingredientes Adicionais:", font=('Cascadia Code', 12,))
ingredientes_label.pack(pady=5)

for ingrediente in ingredientes:
    var = tk.BooleanVar()
    chk = tk.Checkbutton(root, text=f"{ingrediente} (+R$ {precos_ingredientes[ingrediente]:.2f})", font=('Cascadia Code', 10), variable=var)
    chk.pack(anchor="w")
    ingredientes_vars[ingrediente] = var


# Bebidas
titulo_label = tk.Label(root, text="Escolha sua bebida", font=('Cascadia Code', 12, 'bold'))
titulo_label.pack(pady=10)

precos_bebidas = {"Coca-Cola 2l": 10.00, "Pepsi 2l": 10.00, "Fruki 2l": 9.00, "Coca-Cola 350ml": 5.00, "Pepsi 350ml": 5.00, "Fruki 350ml": 5.00}

bebidas_var = tk.StringVar(root)
bebidas_var.set("Coca-Cola 2l")  
bebidas = ["Coca-Cola 2l", "Pepsi 2l", "Fruki 2l", "Coca-Cola 350ml", "Pepsi 350ml", "Fruki 350ml"]
bebidas_menu = tk.OptionMenu(root, bebidas_var, *bebidas)
bebidas_menu.pack(pady=8)

# Entry para a quantidade de bebidas
quantidade_bebidas_label = tk.Label(root, text="Quantidade:", font=('Cascadia Code', 12,))
quantidade_bebidas_label.pack(pady=5)
quantidade_bebidas_entry = tk.Entry(root)
quantidade_bebidas_entry.pack(pady=5)


# Botão para iniciar o pedido
pedir_button = tk.Button(root, text="Pedir", font=('Cascadia Code', 12, 'bold'), height= 1, width= 10,background='#008000', command=confirmar_pedido)
pedir_button.pack(pady=15)

# Label para exibir o total
total_label = tk.Label(root, text="Total a pagar: R$ 0.00", font=('Cascadia Code', 12, 'bold'), background='#8FBC8F',)
total_label.pack(pady=10)


# Iniciar o loop principal
root.mainloop()