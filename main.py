from tkinter import Tk, ttk, StringVar, filedialog, messagebox, Listbox, Scrollbar, Entry
import qrcode
import os
from ttkthemes import ThemedStyle

class ThemedHoverButton(ttk.Button):
    def __init__(self, master=None, **kwargs):
        ttk.Button.__init__(self, master=master, **kwargs)

class AplicativoQrCode:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de QR Code")
        self.root.geometry("450x540")
        self.root.configure(bg="#F3F8FF")

        # Defina a fonte padrão para 'Roboto', 12
        self.root.option_add('*Font', 'Roboto 12')

        self.caminhos_pdf = []
        self.diretorio_destino = StringVar()
        self.url_base = StringVar()

        self.inicializar_interface()

    def inicializar_interface(self):
        style = ThemedStyle(self.root)
        style.set_theme("arc")  # Defina o tema para "arc" ou outro tema disponível

        frame = ttk.Frame(self.root, padding=(20, 20), style="TFrame")
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Escolha o arquivo PDF:", style="TLabel").grid(row=0, column=0, pady=10, padx=10, sticky="w")
        ThemedHoverButton(frame, text="Selecionar", command=self.obter_caminhos_pdf, style="TButton").grid(row=1, column=0, pady=5, padx=10, sticky="w")

        # Listbox para exibir os arquivos PDF selecionados
        self.pdf_listbox = Listbox(frame, selectmode="multiple", height=5, width=40)
        self.pdf_listbox.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        # Scrollbar para a listbox
        scrollbar = Scrollbar(frame, orient="vertical")
        scrollbar.config(command=self.pdf_listbox.yview)
        scrollbar.grid(row=2, column=0, padx=380, sticky="nsw")

        self.pdf_listbox.config(yscrollcommand=scrollbar.set)

        ThemedHoverButton(frame, text="Remover Selecionados", command=self.remover_selecionados, style="TButton").grid(row=3, column=0, pady=10, padx=10, sticky="w")
        ThemedHoverButton(frame, text="Remover Todos", command=self.remover_todos, style="TButton").grid(row=3, column=0, pady=10, padx=270, sticky="w")

        ttk.Label(frame, text="Escolha onde salvar os QR Codes:", style="TLabel").grid(row=4, column=0, pady=10, padx=10, sticky="w")
        ttk.Entry(frame, textvariable=self.diretorio_destino, state="readonly", width=28).grid(row=5, column=0, pady=0, padx=10, sticky="w")
        ThemedHoverButton(frame, text="Escolher", command=self.escolher_diretorio_destino, style="TButton").grid(row=5, column=0, pady=10, padx=290, sticky="w")

        ttk.Label(frame, text="Insira a URL base para os QR Codes:", style="TLabel").grid(row=6, column=0, pady=10, padx=10, sticky="w")
        Entry(frame, textvariable=self.url_base, width=28).grid(row=7, column=0, pady=10, padx=10, sticky="w")

        ThemedHoverButton(frame, text="Gerar QR Codes", command=self.gerar_qr_codes, style="TButton").grid(row=8, column=0, pady=10, padx=10, sticky="w")

    def obter_caminhos_pdf(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])

        if file_paths:
            self.caminhos_pdf = list(file_paths)
            self.atualizar_listbox()

    def escolher_diretorio_destino(self):
        selected_directory = filedialog.askdirectory()
        self.diretorio_destino.set(selected_directory)

    def gerar_qr_codes(self):
        diretorio_destino = self.diretorio_destino.get()

        if not diretorio_destino:
            messagebox.showerror("Erro", "Escolha o diretório de destino para os QR Codes.")
            return

        if not self.caminhos_pdf:
            messagebox.showerror("Erro", "Nenhum arquivo PDF selecionado.")
            return

        url_base = self.url_base.get().strip()
        if not url_base:
            messagebox.showerror("Erro", "Insira a URL base para os QR Codes.")
            return

        try:
            for caminho_pdf in self.caminhos_pdf:
                nome_arquivo = os.path.basename(caminho_pdf)
                qr_code_dados = f"{url_base}{nome_arquivo}"

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_code_dados)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")

                caminho_completo = os.path.join(diretorio_destino, f"{nome_arquivo}_qrcode.png")
                img.save(caminho_completo)
                print(f"QR Code gerado com sucesso: {caminho_completo}")

            messagebox.showinfo("Concluído", "QR Codes gerados com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar QR Codes: {str(e)}")

    def atualizar_listbox(self):
        self.pdf_listbox.delete(0, "end")
        for path in self.caminhos_pdf:
            self.pdf_listbox.insert("end", os.path.basename(path))

    def remover_selecionados(self):
        selected_indices = self.pdf_listbox.curselection()
        selected_files = [self.caminhos_pdf[i] for i in selected_indices]

        for file_path in selected_files:
            self.caminhos_pdf.remove(file_path)

        self.atualizar_listbox()

    def remover_todos(self):
        self.caminhos_pdf = []
        self.atualizar_listbox()

if __name__ == "__main__":
    root = Tk()
    app = AplicativoQrCode(root)
    
    root.withdraw()
    root.update_idletasks()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    x_coordinate = (width - root.winfo_reqwidth()) / 2
    y_coordinate = (height - root.winfo_reqheight()) / 2
    root.geometry("+%d+%d" % (x_coordinate, y_coordinate))
    root.deiconify()
    
    root.mainloop()
