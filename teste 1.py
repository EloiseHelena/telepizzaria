import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Pedido_Pizza:
    def __init__(self, root):
        self.root = root
        self.root.title("PIZZARIA SENAC")
        
         # Carregar e definir a imagem de fundo
        self.background_image = Image.open("imagens\Pizza-3007395.jpg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # Container para os widgets
        self.frame = tk.Frame(root, bg='#C0C0C0', bd=5)
        self.frame.place(relx=0.5, rely=0.1, relwidth=0.3, relheight=0.7, anchor='n')
        
        # Preços das pizzas e ingredientes
        self.tamanhos = ["Pequena", "Média", "Grande"]
        self.precos = {"Pequena": 15.00, "Média": 22.00, "Grande": 28.00}
        self.ingredientes = ["Queijo Extra", "Pepperoni", "Bacon"]
        self.precos_ingredientes = {"Queijo Extra": 2.00, "Pepperoni": 3.00, "Bacon": 4.00}
        self.bebidas = ["Refrigerante", "Suco", "Água"]
        self.precos_bebidas = {"Refrigerante": 5.00, "Suco": 4.00, "Água": 2.00}

        titulo_label = tk.Label(root, text="REALIZE SEU PEDIDO", font=('Cascadia Code', 16, 'bold'))
        titulo_label.pack(pady=10)
        

        # Widgets
        tk.Label(self.frame, text="Tamanho da Pizza:",bg='#C0C0C0',  font=('Cascadia Code', 12, 'bold')).grid(row=0, column=0, padx=5, pady=5)
        self.tamanho_var = tk.StringVar(value=self.tamanhos[0])
        self.optionmenu_tamanho = tk.OptionMenu(self.frame, self.tamanho_var, *self.tamanhos)
        self.optionmenu_tamanho.grid(row=1, column=0, padx=10, pady=10)

        tk.Label(self.frame,  text="Quantidade:",bg='#C0C0C0',  font=('Cascadia Code', 12, 'bold')).grid(row=0, column=1, padx=5, pady=5)
        self.entry_quantidade = tk.Entry(self.frame )
        self.entry_quantidade.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.frame,  text="Ingredientes Adicionais:",bg='#C0C0C0', font=('Cascadia Code', 12, 'bold')).grid(row=2, column=0, padx=5, pady=5)
        self.ingredientes_vars = {}
        for i, ing in enumerate(self.ingredientes):
            var = tk.BooleanVar()
            self.ingredientes_vars[ing] = var
            chk = tk.Checkbutton(self.frame, text=ing, variable=var,bg='#C0C0C0', font=('Cascadia Code', 10))
            chk.grid(row=3+i, column=0, sticky="w")

        tk.Label(self.frame,  text="Escolha a Bebida:",bg='#C0C0C0', font=('Cascadia Code', 12, 'bold')).grid(row=6, column=0, padx=5, pady=5)
        self.bebida_var = tk.StringVar(value=self.bebidas[0])
        self.optionmenu_bebida = tk.OptionMenu(self.frame, self.bebida_var, *self.bebidas)
        self.optionmenu_bebida.grid(row=7, column=0, padx=5, pady=5)
        
        tk.Label(self.frame,  text="Quantidade:", bg='#C0C0C0', font=('Cascadia Code', 12, 'bold')).grid(row=6, column=1, padx=10, pady=10)
        self.entry_quantidade_bebida = tk.Entry(self.frame, )
        self.entry_quantidade_bebida.grid(row=7, column=1, padx=5, pady=5)

        self.button_pedir = tk.Button(self.frame,  text="Pedir", font=('Cascadia Code', 12, 'bold'),height= 2, width= 10, borderwidth= 5, command=self.pedir)
        self.button_pedir.grid(row=8, column=0, columnspan=3, pady=35)

        self.label_total = tk.Label(self.frame,  text="Total a Pagar: R$ 0.00", bg='#C0C0C0',  font=('Cascadia Code', 12, 'bold'))
        self.label_total.grid(row=9, column=0, columnspan=2, pady=10)

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

            bebida = self.bebida_var.get()
            preco_bebida = self.precos_bebidas[bebida]*quantidade_bebida

            total = quantidade * (preco_tamanho + preco_ingredientes + preco_bebida)
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
