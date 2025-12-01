# Gerenciador de Contatos (Python + CustomTkinter)

<img width="1795" height="823" alt="Screenshot_1" src="https://github.com/user-attachments/assets/35f9fe17-ae59-44f9-aaf4-ac18fadd6a42" />

Gerenciador de contatos **moderno e lindo** feito em Python com:
- CustomTkinter (interface dark/light)
- Banco de dados local em JSON
- Validação completa de telefone (11 dígitos) e e-mail
- Busca em tempo real
- Editar/Excluir com duplo clique

## Funcionalidades
- Adicionar, editar e excluir contatos
- Telefone formatado automaticamente: `(11) 98765-4321`
- Só aceita e-mails reais (gmail, hotmail, outlook, yahoo, etc.)
- Evita telefones duplicados
- Totalmente offline (salva em `contatos.json`)

## Como rodar
```bash
pip install customtkinter
python main.py
