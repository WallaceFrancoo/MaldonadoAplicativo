import sqlite3
import datetime
from tkinter import messagebox

conn = sqlite3.connect('Z:/Diversos/Projetos T.I/MaldonadoAplicativo/deParaMaldonado.db')

cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS dePara (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    DE TEXT NOT NULL,
    PARA TEXT NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Clientes (
    DESCRICAO TEXT NOT NULL PRIMARY KEY,
    DISTRIBUICAO TEXT NOT NULL,
    CONTA TEXT NOT NULL,
    TARIFA NUMERIC NOT NULL,
    CONTALAKS TEXT,
    CONTAPILI TEXT    
)
''')
def consultarCliente(valor):
    cursor.execute('SELECT * FROM Clientes')
    tabelaClientes = cursor.fetchall()
    if tabelaClientes:
        cursor.execute('SELECT DESCRICAO, DISTRIBUICAO, CONTA, TARIFA FROM Clientes WHERE DESCRICAO = ?',(valor,))
        tabela = cursor.fetchall()
        if tabela:
            return tabela[0][2]
        else:
            return "6"
    else:
        return "6"
def consultarClientePili(valor):
    cursor.execute('SELECT * FROM Clientes')
    tabelaClientes = cursor.fetchall()
    if tabelaClientes:
        cursor.execute('SELECT DESCRICAO, DISTRIBUICAO, CONTA, TARIFA, CONTALAKS, CONTAPILI FROM Clientes WHERE TRIM(LOWER(DESCRICAO)) = TRIM(LOWER(?))', (valor.strip(),))
        tabela = cursor.fetchall()
        if tabela:
            return tabela[0][5]
        else:
            return "6"
    else:
        return "6"
def consultarClienteLaks(valor):
    cursor.execute('SELECT * FROM Clientes')
    tabelaClientes = cursor.fetchall()
    if tabelaClientes:
        cursor.execute('SELECT DESCRICAO, DISTRIBUICAO, CONTA, TARIFA, CONTALAKS, CONTAPILI FROM Clientes WHERE TRIM(LOWER(DESCRICAO)) = TRIM(LOWER(?))', (valor.strip(),))
        tabela = cursor.fetchall()
        if tabela:
            return tabela[0][4]
        else:
            return "6"
    else:
        return "6"
def consultarDistribuicao(valor):
    cursor.execute('SELECT * FROM Clientes')
    tabelaClientes = cursor.fetchall()
    if tabelaClientes:
        cursor.execute('SELECT DESCRICAO, DISTRIBUICAO, CONTA, TARIFA FROM Clientes WHERE DESCRICAO = ?', (valor,))
        tabela = cursor.fetchall()
        if tabela:
            return tabela[0][1]
        else:
            return "Sem DISTRIBUICAO Cadastrada"
    else:
        return "Sem Cadastro do DISTRIBUICAO"
def consultarTarifa(valor):
    cursor.execute('SELECT * FROM Clientes')
    tabelaClientes = cursor.fetchall()
    if tabelaClientes:
        cursor.execute('SELECT DESCRICAO, DISTRIBUICAO, CONTA, TARIFA FROM Clientes WHERE DESCRICAO = ?', (valor,))
        tabela = cursor.fetchall()
        if tabela:
            return tabela[0][3]
        else:
            return "Sem TARIFA Cadastrada"
    else:
        return "Sem Cadastro do TARIFA"
def adicionar_Dados(DE,PARA):
    # Verificar se o par DE e PARA já existe no banco de dados
    cursor.execute('SELECT * FROM dePara WHERE DE = ? AND PARA = ?', (DE, PARA))
    resultado = cursor.fetchone()  # Pega o primeiro resultado, se existir

    if resultado:
        # Se já existir, perguntar se deseja atualizar
        resposta = messagebox.askquestion("Atualizar", "Essa associação DE-PARA já existe. Deseja atualizar os dados?",
                                          icon='warning')

        if resposta == 'yes':
            # Atualizar os dados no banco de dados
            cursor.execute('UPDATE dePara SET PARA = ? WHERE DE = ?', (PARA, DE))
            conn.commit()
            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
        else:
            messagebox.showinfo("Aviso", "Os dados não foram atualizados.")
    else:
        # Se não existir, insere os novos dados
        cursor.execute('INSERT INTO dePara(DE, PARA) VALUES (?, ?)', (DE, PARA))
        conn.commit()
        messagebox.showinfo("Sucesso", "Dados cadastrados com sucesso!")
def adicionar_Clientes(DE,DIST,CONTA,TARIFA,LAKS,PILI):
    # Verificar se o par DE e PARA já existe no banco de dados
    cursor.execute('SELECT * FROM Clientes WHERE DESCRICAO = ? AND DISTRIBUICAO = ? AND CONTA = ? AND TARIFA = ?', (DE, DIST, CONTA, TARIFA))
    resultado = cursor.fetchone()  # Pega o primeiro resultado, se existir

    if resultado:
        # Se já existir, exibir uma mensagem de aviso
        resposta = messagebox.askquestion("Atualizar", "Esse cliente/Fornecedor já existe. Deseja atualizar os dados?", icon='warning')
        if resposta == 'yes':
            # Atualizar os dados existentes no banco de dados
            cursor.execute('UPDATE Clientes SET DESCRICAO = ? WHERE DISTRIBUICAO = ? AND CONTA = ? AND TARIFA = ? AND CONTALAKS = ? AND CONTAPILI = ?', (DE, DIST,CONTA,TARIFA,LAKS,PILI))
            conn.commit()
            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
        else:
            messagebox.showinfo("Aviso", "Os dados não foram atualizados.")
    else:
        # Se não existir, insere os novos dados
        cursor.execute('INSERT INTO Clientes(DESCRICAO, DISTRIBUICAO, CONTA, TARIFA, CONTALAKS, CONTAPILI) VALUES (?, ?, ?, ?, ?, ?)', (DE, DIST, CONTA, TARIFA,LAKS,PILI))
        conn.commit()
        messagebox.showinfo("Sucesso", "Dados cadastrados com sucesso!")
def MostrarTabela():
    cursor.execute('SELECT * FROM dePara')
    todos_dados = cursor.fetchall()
    #print("Todos os dados na tabela:", todos_dados)
    return todos_dados
def TrazerConta(informacao):
    # Executa a consulta inicial para garantir que há dados
    dePara = MostrarTabela()
    if dePara:
        # Executa a consulta para buscar o valor correspondente
        cursor.execute('SELECT DE, PARA FROM dePara WHERE DE LIKE ?', ( informacao,))
        consulta = cursor.fetchall()
        if consulta:
            # Retorna o valor da coluna 'PARA' da primeira linha encontrada
            return consulta[0][1]
        else:
            num_palavras = 3
            palavra = informacao.split()  # Divide a string em uma lista de palavras
            formatada = ' '.join(palavra[:num_palavras])  # Junta as primeiras `num_palavras` palavras
            cursor.execute('SELECT DE, PARA FROM dePara WHERE DE LIKE ?', ('%' + formatada + '%',))
            consultaFormatada = cursor.fetchall()
            if consultaFormatada:
                return consultaFormatada[0][1]
            else:
                return "6"
    else:
        print("Tabela Vazia")
        return "Tabela está vazia"

