import sqlite3
from datetime import datetime

def conectar_db():
    return sqlite3.connect('produtos.db')

def criar_tabelas():
    conexao = conectar_db()
    cursor = conexao.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produto INTEGER NOT NULL,
            quantidade_vendida INTEGER NOT NULL,
            data_venda TEXT NOT NULL,
            FOREIGN KEY (id_produto) REFERENCES produtos(id)
        )
    ''')
    
    conexao.commit()
    conexao.close()

def criar_produto(nome: str, descricao: str, quantidade: int, preco: float):
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO produtos(nome, descricao, quantidade, preco)
        VALUES (?, ?, ?, ?)
    ''', (nome, descricao, quantidade, preco))
    conexao.commit()
    conexao.close()

def deletar_produto(id_produto: int):
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute('''
        DELETE FROM produtos WHERE id = ?
    ''', (id_produto,))
    conexao.commit()
    conexao.close()

def listar_produtos():
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    for produto in produtos:
        print(f'ID: {produto[0]}, Nome: {produto[1]}, Quantidade: {produto[3]}, Preço: {produto[4]}')
    conexao.close()

class Venda:
    def __init__(self, id_produto: int, quantidade_vendida: int):
        self.id_produto = id_produto
        self.quantidade_vendida = quantidade_vendida
        self.data_venda = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def registrar_venda(self):
        conexao = conectar_db()
        cursor = conexao.cursor()
        cursor.execute('''
            INSERT INTO vendas(id_produto, quantidade_vendida, data_venda)
            VALUES (?, ?, ?)
        ''', (self.id_produto, self.quantidade_vendida, self.data_venda))
        conexao.commit()
        conexao.close()
        self.atualizar_quantidade_produto()

    def atualizar_quantidade_produto(self):
        conexao = conectar_db()
        cursor = conexao.cursor()
        cursor.execute('''
            UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?
        ''', (self.quantidade_vendida, self.id_produto))
        conexao.commit()
        conexao.close()

def registrar_venda(id_produto: int, quantidade_vendida: int):
    venda = Venda(id_produto, quantidade_vendida)
    venda.registrar_venda()
    print(f'Venda registrada para o produto ID {id_produto}, Quantidade: {quantidade_vendida}')

def listar_vendas():
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM vendas')
    vendas = cursor.fetchall()
    for venda in vendas:
        print(f'ID da Venda: {venda[0]}, Produto ID: {venda[1]}, Quantidade Vendida: {venda[2]}, Data da Venda: {venda[3]}')
    conexao.close()

def menu():
    while True:
        texto = """Escolha:
        [1] Inserir produto
        [2] Deletar produto
        [3] Registrar venda
        [4] Listar produtos
        [5] Listar vendas
        [6] Sair"""

        print(texto)
        opc = int(input("Digite sua escolha:"))
        
        match opc:
            case 1:
                nome = input("Digite o nome do produto: ")
                descricao = input("Digite a descrição do produto: ")
                quant = int(input("Digite a quantidade do produto: "))
                preco = float(input("Digite o preço do produto: "))
                criar_produto(nome, descricao, quant, preco)
            case 2:
                id_produto = int(input("Digite o ID do produto que deseja excluir: "))
                deletar_produto(id_produto)
            case 3:
                id_produto = int(input("Digite o ID do produto: "))
                quantidade = int(input("Digite a quantidade vendida: "))
                registrar_venda(id_produto, quantidade)
            case 4:
                listar_produtos()
            case 5:
                listar_vendas()
            case 6:
                break

criar_tabelas()
menu()