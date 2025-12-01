import customtkinter as ctk
import json
import os
import re
from datetime import datetime
from tkinter import ttk, messagebox as tkmsg

# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DB_FILE = "contatos.json"

# Domínios de e-mail permitidos
DOMINIOS_PERMITIDOS = {
    "gmail.com", "outlook.com", "hotmail.com", "yahoo.com", "yahoo.com.br",
    "uol.com.br", "bol.com.br", "live.com", "icloud.com", "protonmail.com",
    "globomail.com", "terra.com.br", "ig.com.br", "mail.com", "aol.com"
}

def validar_email(email):
    if not email.strip():
        return True  # Email é opcional
    email = email.strip().lower()
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(padrao, email):
        return False
    dominio = email.split('@')[-1]
    return dominio in DOMINIOS_PERMITIDOS

def formatar_telefone(telefone):
    telefone = re.sub(r'\D', '', telefone)  # Remove tudo que não é número
    if len(telefone) == 11:
        return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
    return telefone

def validar_telefone(telefone):
    telefone_limpo = re.sub(r'\D', '', telefone)
    return len(telefone_limpo) == 11 and telefone_limpo.isdigit()

# Carregar e salvar contatos
def carregar_contatos():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_contatos(contatos):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(contatos, f, indent=4, ensure_ascii=False)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Contatos Moderno")
        self.geometry("1800x800")
        self.resizable(False, False)
        self.contatos = carregar_contatos()
        self.criar_interface()

    def criar_interface(self):
        # Frame esquerdo - Formulário
        frame_esq = ctk.CTkFrame(self, width=380, corner_radius=20)
        frame_esq.pack(side="left", fill="y", padx=25, pady=25)

        ctk.CTkLabel(frame_esq, text="Novo Contato", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=25)

        self.entry_nome = ctk.CTkEntry(frame_esq, placeholder_text="Nome completo *", height=45, font=("Arial", 13))
        self.entry_nome.pack(pady=12, padx=40, fill="x")

        self.entry_telefone = ctk.CTkEntry(frame_esq, placeholder_text="Telefone com DDD (11 dígitos) *", height=45, font=("Arial", 13))
        self.entry_telefone.pack(pady=12, padx=40, fill="x")

        self.entry_email = ctk.CTkEntry(frame_esq, placeholder_text="E-mail (opcional)", height=45, font=("Arial", 13))
        self.entry_email.pack(pady=12, padx=40, fill="x")

        self.entry_anotacoes = ctk.CTkTextbox(frame_esq, height=120, font=("Arial", 12))
        self.entry_anotacoes.pack(pady=12, padx=40, fill="x")
        self.entry_anotacoes.insert("0.0", "Anotações (opcional)")

        btn_frame = ctk.CTkFrame(frame_esq)
        btn_frame.pack(pady=25)

        ctk.CTkButton(btn_frame, text="Adicionar Contato", width=160, height=40,
                      fg_color="#1f6aa5", hover_color="#144870",
                      command=self.adicionar_contato).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Limpar Campos", width=120, height=40,
                      fg_color="#555555", command=self.limpar_form).pack(side="left", padx=10)

        # Frame direito - Lista
        frame_dir = ctk.CTkFrame(self)
        frame_dir.pack(side="right", fill="both", expand=True, padx=25, pady=25)

        # Busca
        busca_frame = ctk.CTkFrame(frame_dir)
        busca_frame.pack(fill="x", pady=(0, 15))

        self.entry_busca = ctk.CTkEntry(busca_frame, placeholder_text="Pesquisar por nome ou telefone...", height=40)
        self.entry_busca.pack(side="left", fill="x", expand=True, padx=(15, 8))
        self.entry_busca.bind("<KeyRelease>", self.filtrar_contatos)

        ctk.CTkButton(busca_frame, text="Atualizar", width=100, command=self.atualizar_lista).pack(side="right", padx=15)

        # Tabela estilizada
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white",
                        fieldbackground="#2b2b2b", rowheight=40, font=("Segoe UI", 12))
        style.configure("Treeview.Heading", font=("Segoe UI", 14, "bold"), background="#1f6aa5", foreground="white")
        style.map("Treeview", background=[("selected", "#1f6aa5")])

        colunas = ("nome", "telefone", "email")
        self.tree = ttk.Treeview(frame_dir, columns=colunas, show="headings", style="Treeview")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("email", text="E-mail")
        self.tree.column("nome", width=300, anchor="w")
        self.tree.column("telefone", width=180, anchor="center")
        self.tree.column("email", width=350, anchor="w")

        scrollbar = ttk.Scrollbar(frame_dir, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        # Botões de ação
        action_frame = ctk.CTkFrame(frame_dir)
        action_frame.pack(fill="x", pady=15)

        ctk.CTkButton(action_frame, text="Editar Selecionado", fg_color="#2b8a3e", width=160,
                      command=self.editar_contato).pack(side="left", padx=15)
        ctk.CTkButton(action_frame, text="Excluir Contato", fg_color="#c92a2a", width=160,
                      command=self.excluir_contato).pack(side="left", padx=15)

        self.tree.bind("<Double-1>", lambda e: self.editar_contato())
        self.atualizar_lista()

    def adicionar_contato(self):
        nome = self.entry_nome.get().strip()
        tel_raw = self.entry_telefone.get()
        email = self.entry_email.get().strip().lower()
        anotacoes = self.entry_anotacoes.get("0.0", "end").strip()

        if not nome:
            tkmsg.showerror("Erro", "O nome é obrigatório!")
            return
        if not tel_raw:
            tkmsg.showerror("Erro", "O telefone é obrigatório!")
            return

        if not validar_telefone(tel_raw):
            tkmsg.showerror("Telefone Inválido", "Digite um número com 11 dígitos!\nEx: (11) 98765-4321")
            return

        if email and not validar_email(email):
            dominio = email.split('@')[-1] if '@' in email else "inválido"
            tkmsg.showerror("E-mail Inválido", f"O domínio '{dominio}' não é permitido.\n"
                                              "Use: gmail.com, hotmail.com, outlook.com, yahoo.com etc.")
            return

        telefone_formatado = formatar_telefone(tel_raw)

        # Verifica duplicidade
        if any(c["telefone"] == telefone_formatado for c in self.contatos):
            if not tkmsg.askyesno("Atenção", "Este telefone já está cadastrado.\nDeseja adicionar mesmo assim?"):
                return

        novo = {
            "id": len(self.contatos) + 1,
            "nome": nome.title(),
            "telefone": telefone_formatado,
            "email": email or "Não informado",
            "anotacoes": anotacoes or "Sem anotações",
            "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M")
        }

        self.contatos.append(novo)
        salvar_contatos(self.contatos)
        self.atualizar_lista()
        self.limpar_form()
        tkmsg.showinfo("Sucesso!", f"Contato '{nome}' adicionado com sucesso!")

    def atualizar_lista(self, dados=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
        lista = dados or self.contatos
        for c in lista:
            self.tree.insert("", "end", values=(c["nome"], c["telefone"], c["email"]), tags=(c["id"],))

    def filtrar_contatos(self, event=None):
        termo = self.entry_busca.get().lower()
        filtrados = [c for c in self.contatos if termo in c["nome"].lower() or termo in c["telefone"]]
        self.atualizar_lista(filtrados)

    def limpar_form(self):
        self.entry_nome.delete(0, "end")
        self.entry_telefone.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.entry_anotacoes.delete("0.0", "end")

    def editar_contato(self):
        sel = self.tree.selection()
        if not sel:
            tkmsg.showwarning("Atenção", "Selecione um contato para editar!")
            return

        item = self.tree.item(sel[0])
        contato_id = int(item["tags"][0])
        contato = next(c for c in self.contatos if c["id"] == contato_id)

        self.limpar_form()
        self.entry_nome.insert(0, contato["nome"])
        self.entry_telefone.insert(0, contato["telefone"])
        self.entry_email.insert(0, contato["email"] if contato["email"] != "Não informado" else "")
        self.entry_anotacoes.insert("0.0", contato["anotacoes"])

        def salvar():
            if not validar_telefone(self.entry_telefone.get()):
                tkmsg.showerror("Erro", "Telefone deve ter 11 dígitos!")
                return
            if self.entry_email.get() and not validar_email(self.entry_email.get()):
                tkmsg.showerror("Erro", "E-mail com domínio inválido!")
                return

            contato.update({
                "nome": self.entry_nome.get().strip().title(),
                "telefone": formatar_telefone(self.entry_telefone.get()),
                "email": self.entry_email.get().strip().lower() or "Não informado",
                "anotacoes": self.entry_anotacoes.get("0.0", "end").strip() or "Sem anotações"
            })
            salvar_contatos(self.contatos)
            self.atualizar_lista()
            self.limpar_form()
            btn.destroy()
            tkmsg.showinfo("Atualizado", "Contato editado com sucesso!")

        btn = ctk.CTkButton(self, text="Salvar Alterações", fg_color="#ff0000", hover_color="#ff0000",
                            command=salvar, width=200, height=45, font=("Arial", 12, "bold"))
        btn.place(x=35, y=535)

    def excluir_contato(self):
        sel = self.tree.selection()
        if not sel:
            return
        if tkmsg.askyesno("Excluir", "Tem certeza que deseja excluir este contato permanentemente?"):
            cid = int(self.tree.item(sel[0])["tags"][0])
            self.contatos = [c for c in self.contatos if c["id"] != cid]
            salvar_contatos(self.contatos)
            self.atualizar_lista()
            tkmsg.showinfo("Excluído", "Contato removido com sucesso.")

if __name__ == "__main__":
    app = App()
    app.mainloop()