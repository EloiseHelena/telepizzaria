import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

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


def inicializar_interface(root):
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

    # Widgets de Bebida
    bebida_var = tk.StringVar(value=bebidas[0])
    label_preco_unitario_bebida = tk.Label(frame, text="Valor unitário: ", bg='#D2780D', font=('Cascadia Code', 8, 'bold'))
    optionmenu_bebida = tk.OptionMenu(frame, bebida_var, *bebidas, command=lambda _: atualizar_preco_unitario(tamanho_var, label_preco_unitario, precos, bebida_var, label_preco_unitario_bebida, precos_bebidas))
    optionmenu_bebida.config(bg="#807E2A", fg="WHITE", activebackground='#444801')
    optionmenu_bebida.grid(row=9, column=0, padx=5, pady=5)
    label_preco_unitario_bebida.grid(row=10, column=0, columnspan=1, pady=10)

    # Widgets de Ingredientes
    ingredientes_vars = {ing: tk.BooleanVar() for ing in ingredientes}
    for i, ing in enumerate(ingredientes):
        tk.Checkbutton(frame, text=ing, variable=ingredientes_vars[ing], bg='#D2780D', font=('Cascadia Code', 10), bd=3).grid(row=4+i, column=0, sticky="w")
    ingredientes2_vars = {ing: tk.BooleanVar() for ing in ingredientes2}
    for i, ing in enumerate(ingredientes2):
        tk.Checkbutton(frame, text=ing, variable=ingredientes2_vars[ing], bg='#D2780D', font=('Cascadia Code', 10), bd=3).grid(row=4+i, column=1, sticky="w")

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

    # Iniciar a interface gráfica
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    inicializar_interface(root)

