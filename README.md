# Gerenciador de Contatos (Python + CustomTkinter)

![preview](https://prnt.sc/2KP4tsNQyO5Nraw=true)

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
