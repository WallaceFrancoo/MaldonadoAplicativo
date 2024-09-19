import tkinter as tk
from tkinter import *
import os
from PyPDF2 import PdfReader
import parametros
import BancoDeDados
import main
from PIL import Image
import customtkinter
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import re
import tabula


self = customtkinter.CTk()
self.title("Conversão PDF para Maldonado v1")
self.geometry("950x450")

# Função para inserir o placeholder quando o campo estiver vazio e perder o foco

# set grid layout 1x2
self.grid_rowconfigure(0, weight=1)
self.grid_columnconfigure(1, weight=1)

def abrir_janela_depara():
    # Criar uma nova janela
    janela_depara = customtkinter.CTkToplevel()
    janela_depara.title("Cadastrar dePara")
    janela_depara.geometry("350x200")

    # Trazer a janela para frente e focá-la
    janela_depara.focus_force()
    janela_depara.grab_set()

    # Label e campo de entrada para "DE"
    label_de = customtkinter.CTkLabel(janela_depara, text="DE:")
    label_de.grid(row=0, column=0, padx=20, pady=10)
    entry_de = customtkinter.CTkEntry(janela_depara, width=200)
    entry_de.grid(row=0, column=1, padx=20, pady=10)

    # Label e campo de entrada para "PARA"
    label_para = customtkinter.CTkLabel(janela_depara, text="PARA:")
    label_para.grid(row=1, column=0, padx=20, pady=10)
    entry_para = customtkinter.CTkEntry(janela_depara, width=200)
    entry_para.grid(row=1, column=1, padx=20, pady=10)

    # Função para pegar os valores das entradas e chamar adicionar_Dados
    def cadastrar():
        DE = entry_de.get()
        PARA = entry_para.get()
        if DE and PARA:
            # Pergunta de confirmação
            confirmar = messagebox.askokcancel(
                "Confirmação",
                f"Você digitou o historico {DE} para ir para a conta {PARA}. Deseja confirmar?"
            )
            if confirmar:
                BancoDeDados.adicionar_Dados(DE, PARA)
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")

    # Botão de Cadastrar
    botao_cadastrar = customtkinter.CTkButton(janela_depara, text="Cadastrar", command=cadastrar)
    botao_cadastrar.grid(row=2, column=0, columnspan=2, pady=20)
def abrir_janela_clientes():
    # Criar uma nova janela
    janela_clientes = customtkinter.CTkToplevel()
    janela_clientes.title("Cadastrar Clientes")
    janela_clientes.geometry("600x450")

    # Trazer a janela para frente e focá-la
    janela_clientes.focus_force()
    janela_clientes.grab_set()

    # Label e campo de entrada para "DE"
    label_de = customtkinter.CTkLabel(janela_clientes, text="DE:")
    label_de.grid(row=0, column=0, padx=20, pady=10)
    entry_de = customtkinter.CTkEntry(janela_clientes, width=300, placeholder_text="Coloca apenas o nome do Cliente")
    entry_de.grid(row=0, column=1, padx=20, pady=10)

    # Label e campo de entrada para "PARA"
    label_dist = customtkinter.CTkLabel(janela_clientes, text="DISTRUBICAO (1/2) :")
    label_dist.grid(row=1, column=0, padx=20, pady=10)
    entry_dist = customtkinter.CTkEntry(janela_clientes, width=300, placeholder_text="1- Sem Distribuição 2- Com distribuição")
    entry_dist.grid(row=1, column=1, padx=20, pady=10)

    # Label e campo de entrada para "PARA"
    label_conta = customtkinter.CTkLabel(janela_clientes, text="CONTA:")
    label_conta.grid(row=2, column=0, padx=20, pady=10)
    entry_conta = customtkinter.CTkEntry(janela_clientes, width=300, placeholder_text="Incluir a conta contabil do cliente ou destinatario")
    entry_conta.grid(row=2, column=1, padx=20, pady=10)

    label_tarifa = customtkinter.CTkLabel(janela_clientes, text="TARIFA:")
    label_tarifa.grid(row=3, column=0, padx=20, pady=10)
    entry_tarifa = customtkinter.CTkEntry(janela_clientes, width=300, placeholder_text="0- Sem Tarifa 1- Sem Tarifa")
    entry_tarifa.grid(row=3, column=1, padx=20, pady=10)
    # Função para pegar os valores das entradas e chamar adicionar_Dados

    label_contalaks = customtkinter.CTkLabel(janela_clientes, text="Conta na Lakshmi")
    label_contalaks.grid(row=4, column=0, padx=20, pady=10)
    entry_contaLaks = customtkinter.CTkEntry(janela_clientes, width=300, placeholder_text="Conta Contabil do Cliente na empresa Lakshmi")
    entry_contaLaks.grid(row=4, column=1, padx=20, pady=10)

    label_contapili = customtkinter.CTkLabel(janela_clientes, text="Conta na Pilipili")
    label_contapili.grid(row=5, column=0, padx=20, pady=10)
    entry_contapili = customtkinter.CTkEntry(janela_clientes, width=300,placeholder_text="Conta Contabil do Cliente na empresa Pilipili")
    entry_contapili.grid(row=5, column=1, padx=20, pady=10)

    # Botão de Cadastrar
    botao_cadastrar = customtkinter.CTkButton(janela_clientes, text="Cadastrar", command=cadastrar)
    botao_cadastrar.grid(row=6, column=0, columnspan=2, pady=20)
def cadastrar():
        DE = entry_de.get()
        DIST = entry_dist.get()
        CONTA = entry_conta.get()
        TARIFA = entry_tarifa.get()
        LAKS = entry_contalaks.get()
        PILI = entry_contapili.get()

        if DE and DIST and CONTA and TARIFA:
            distribuicao = ''
            if DIST == "1":
                distribuicao = "Não tem separação"
            elif DIST == "2":
                distribuicao = "Tem Separacao"

            tarifa = ''
            if TARIFA == "1":
                tarifa = "Tem tarifa"
            elif TARIFA == "0":
                tarifa = "Sem Tarifa"
            # Pergunta de confirmação
            confirmar = messagebox.askokcancel(
                "Confirmação",
                f"Você digitou as seguintes informações:\nCliente: {DE}\nDistribuicao: {distribuicao}\nPara a conta: {CONTA}. e {tarifa}\nLaks:{LAKS} e Pili {PILI}\nDeseja confirmar?"
            )
            if confirmar:
                BancoDeDados.adicionar_Clientes(DE,DIST, CONTA, TARIFA,LAKS,PILI)
                janela_depara.destroy()  # Fechar a janela após cadastrar
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
# load images with light and dark mode image
image_path = "Z:/Diversos/Projetos T.I/MaldonadoAplicativo/imagens"
logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Transparente2.png")), size=(26, 26))
large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Simbolo.png")), size=(150, 100))
image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "pdf.png")), size=(20, 20))
image_icon_image2 = customtkinter.CTkImage(Image.open(os.path.join(image_path, "excel.png")), size=(20, 20))

# create navigation frame = column 0
navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
navigation_frame.grid(row=0, column=0, sticky="nsew")
navigation_frame.grid_rowconfigure(6, weight=1)
navigation_frame_label = customtkinter.CTkLabel(navigation_frame, text="  Sergecont Contabilidade", image=logo_image,
                                                compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

# create textbox
textbox = customtkinter.CTkTextbox(navigation_frame,
                                   corner_radius=10,
                                   width=100,
                                   fg_color="transparent",
                                   wrap="word")
textbox.grid(row=1, column=0, rowspan=6, padx=(10, 10), pady=(10, 10), sticky="nsew")
textbox.insert("0.0", "Segue passo a passo para conversão do PDF do extrato bancario da MALDONADO!\n\n\n"
                      "1. Clique no botão 'Selecionar arquivo'.\n\n"
                      "2. Selecione o arquivo desejado!\n\n"
                      "3. Clique no botão Salvar, irá abrir opção para incluir o nome do arquivo e onde irá salvar\n\n"
                      "4. Caso tenha historico de boleto em acerto, verificar como será feita a distribuição do cliente!\n\n"
                      "5. Obs Complementar: Tem clientes que pagam 2x uma tem tarifa e a outra não, verificar de acordo com a planilha!\n\n"
               )

# create home frame column 1
home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
home_frame.grid_columnconfigure(0, weight=1)
home_frame_large_image_label = customtkinter.CTkLabel(home_frame, text="", image=large_test_image)
home_frame_large_image_label.grid(row=0, column=0, columnspan=2, padx=10, pady=15)

# Botão Selecionar arquivo PDF
botao_pdf = customtkinter.CTkButton(home_frame, text="Selecionar Arquivo", image=image_icon_image, compound="right",
                                    command=main.buscarArquivo)
botao_pdf.grid(row=2, column=0, pady=5, columnspan=2)

botao_repasse = customtkinter.CTkButton(home_frame, text="Gerar Repasses", compound="right", command=main.buscarRepasse)
botao_repasse.grid(row=4,column=0,pady=35, columnspan=2)
# Botão onde salvar Excel
botao_gerar = customtkinter.CTkButton(home_frame, text="Gerar Arquivo", compound="right",
                                      command=main.gerarArquivos)
botao_gerar.grid(row=3, column=0, pady=10, columnspan=2)

# Frame para os botões de cadastro
frame_cadastro = customtkinter.CTkFrame(home_frame,fg_color="transparent")
frame_cadastro.grid(row=5, column=0, pady=10, columnspan=2)

# Botão Cadastrar dePara
botao_cadastrodePara = customtkinter.CTkButton(frame_cadastro, text="Cadastrar dePara", compound="left",command=abrir_janela_depara)
botao_cadastrodePara.grid(row=0, column=0, padx=10, pady=10)

# Botão Cadastrar Cliente
botao_cadastroCliente = customtkinter.CTkButton(frame_cadastro, text="Cadastrar Cliente", compound="left",command=abrir_janela_clientes)
botao_cadastroCliente.grid(row=0, column=1, padx=10, pady=10)

# Organizar o home_frame
home_frame.grid(row=0, column=1, sticky="nsew")



self.mainloop()