import re
import PyPDF2
import BancoDeDados
from tkinter import filedialog, Entry, Button, Label, StringVar, CENTER, messagebox
from unidecode import unidecode
import os

def ler_pdf(arquivo_pdf):
    with open(arquivo_pdf, 'rb') as file:
        leitor_pdf = PyPDF2.PdfReader(file)
        num_paginas = len(leitor_pdf.pages)
        conteudo = ""
        for pagina in range(num_paginas):
            pagina_atual = leitor_pdf.pages[pagina]
            conteudo += pagina_atual.extract_text()
    return conteudo
def extrair_primeiras_palavras(dado, num_palavras=3):
    palavras = dado.split()  # Divide a string em uma lista de palavras
    return ' '.join(palavras[:num_palavras])  # Junta as primeiras num_palavras palavras
def corrigir_quebras(conteudo):
    linhas = conteudo.split('\n')
    linhas_corrigidas = []
    buffer = ""
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
        if linha[0].isdigit() and (len(linha) > 10 and linha[10] in "DC"):  # Verifica se a linha é um dado válido
            if buffer:
                linhas_corrigidas.append(buffer)  # Adiciona o buffer ao resultado
                buffer = ""
            linhas_corrigidas.append(linha)
        else:
            buffer += " " + linha  # Adiciona a linha ao buffer
    if buffer:
        linhas_corrigidas.append(buffer)  # Adiciona qualquer texto restante no buffer
    return "\n".join(linhas_corrigidas)
def extrair_dados(conteudo):

    global relatorio_separado, resultados
    conteudo = re.sub(r'.*Saldo anterior.*?(\d{2}/\d{2}/\d{4})', r'\1', conteudo, flags=re.DOTALL)
    conteudo = corrigir_quebras(conteudo)
    # Regex para extrair os dados
    padrao = re.compile(r'(\d{2}/\d{2}/\d{4})\s+(.*?)\s+(D|C)\s+([-]?[\d,.]+)\s+([-]?[\d,.]+)', re.MULTILINE | re.DOTALL)
    resultados = []
    linha = 1

    for match in padrao.finditer(conteudo):
        data = match.group(1).strip()
        descricao = match.group(2).strip()
        descricaoCliente = descricao[12:]
        tipo = match.group(3).strip()
        valor = match.group(4).strip().replace(".","").replace(",",".")
        saldo = match.group(5).strip()
        contaD = contaDebito(tipo,descricao)
        contaC = contaCredito(tipo,descricao)
        Historico = historicoComp(tipo)

        if float(valor) == 0:
            continue

        if descricao[:6] == "Boleto":
            consultarCliente = BancoDeDados.consultarCliente(descricaoCliente)
            consultarDistribuicao = BancoDeDados.consultarDistribuicao(descricaoCliente)
            consultarTarifa = BancoDeDados.consultarTarifa(descricaoCliente)
            if consultarTarifa == 1:
                valordaTaxa = 6.00
            elif consultarTarifa == 0:
                valordaTaxa = 0.00
            if consultarDistribuicao == "1":
                if consultarTarifa == 1:
                    valorConvertido = float(valor)
                    valorSemTaxa = (valorConvertido - valordaTaxa)
                    strvalorConvertido = "{:.2f}".format(valorConvertido).replace(".",",")
                    strvalorSemTaxa = "{:.2f}".format(valorSemTaxa).replace(".",",")
                    strvalorDaTaxa = "{:.2f}".format(valordaTaxa).replace(".",",")
                    resultados.append(f"{data};{contaD};;{strvalorConvertido};;{Historico}{descricao};1;;;")
                    resultados.append(f"{data};;{consultarCliente};{strvalorSemTaxa};;{Historico}{descricao};;;;")
                    resultados.append(f"{data};;535;{strvalorDaTaxa};;TARIFA BANCARIA REF. {descricao};;;;")
                    contaC = consultarCliente
                    strvalor = strvalorConvertido

                elif consultarTarifa == 0:
                    valorConvertido = float(valor)
                    strvalorConvertido = "{:.2f}".format(valorConvertido).replace(".", ",")
                    resultados.append(f"{data};{contaD};{consultarCliente};{strvalorConvertido};;{Historico}{descricao};1;;;")
                    contaC = consultarCliente
                    strvalor = strvalorConvertido

            elif consultarDistribuicao == "2":
                if consultarTarifa == 1:
                    valorConvertido = float(valor)
                    valorSemTaxa = valorConvertido - valordaTaxa
                    strvalorConvertido = "{:.2f}".format(valorConvertido).replace(".", ",")
                    strvalorDaTaxa = "{:.2f}".format(valordaTaxa).replace(".", ",")
                    parteMaldonado = round(valorSemTaxa * 0.3333,2)
                    parteLaks = round(valorSemTaxa * 0.3333,2)
                    partePili = round(valorConvertido-valordaTaxa-parteMaldonado-parteLaks,2)

                    strparteMaldonado = "{:.2f}".format(parteMaldonado).replace(".",",")
                    strparteLaks = "{:.2f}".format(parteLaks).replace(".",",")
                    strpartePili = "{:.2f}".format(partePili).replace(".",",")

                    resultados.append(f"{data};{contaD};;{strvalorConvertido};;{Historico}{descricao};1;;;")
                    resultados.append(f"{data};;{consultarCliente};{strparteMaldonado};;{Historico}{descricao};;;;")
                    resultados.append(f"{data};;10006;{strparteLaks};;{Historico}{descricao};;;;")
                    resultados.append(f"{data};;10002;{strpartePili};;{Historico}{descricao};;;;")
                    resultados.append(f"{data};;535;{strvalorDaTaxa};;TARIFA BANCARIA REF. {descricao};;;;")
                    contaC = consultarCliente
                    strvalor = valorConvertido
                elif consultarTarifa == 0:
                    valorConvertido = float(valor)
                    parteMaldonado = round(valorConvertido * 0.3333,2)
                    parteLaks = round(valorConvertido * 0.3333,2)
                    partePili = round(valorConvertido-parteMaldonado-parteLaks,2)
                    strvalorConvertido = "{:.2f}".format(valorConvertido).replace(".", ",")
                    strparteMaldonado = "{:.2f}".format(parteMaldonado).replace(".", ",")
                    strparteLaks = "{:.2f}".format(parteLaks).replace(".", ",")
                    strpartePili = "{:.2f}".format(partePili).replace(".", ",")
                    resultados.append(f"{data};{contaD};;{strvalorConvertido};;{Historico}{descricao};1;;;")
                    resultados.append(f"{data};;{consultarCliente};{strparteMaldonado};;{Historico}{descricao};;;;")
                    resultados.append(f"{data};;10006;{strparteLaks};;{Historico}{descricao};;;;")
                    resultados.append(f"{data};;10002;{strpartePili};;{Historico}{descricao};;;;")
                    contaC = consultarCliente
                    strvalor = valorConvertido
            else:
                strvalor = str(valor).replace(".", ",")
                resultados.append(f"{data};{contaD};{contaC};{strvalor};;{Historico}{descricao};1;;;")
        else:
            strvalor = str(valor).replace(".", ",")
            resultados.append(f"{data};{contaD};{contaC};{strvalor};;{Historico}{descricao};1;;;")
            linhas_erros = unidecode(f"Aviso: No Dia {data} o lançamento com o historico: - ({Historico}) O lançamento irá para acerto!")
        if contaD == "6" or contaC == "6":
            relatorio_separado.append(f"{data};{contaD};{contaC};{strvalor};;{Historico}{descricao};1;;;")
        linha = linha + 1
    return resultados, relatorio_separado, dados_laks, dados_pili
def extrair_repasse(conteudo):
    # Listas para armazenar múltiplas ocorrências de repasses
    conteudo = corrigir_quebras(conteudo)  # Corrigir quebras de linha no conteúdo do PDF

    # Regex para encontrar múltiplas ocorrências das informações desejadas
    nome_empresa = r'Extrato de\s+(.+?)\s+Posição'
    taxa_admin_pattern = r'Taxa de administração\s*[-]?\s*([\d,.]+)'
    total_repasse_pattern = r'Total para repasse\s*[-]?\s*([\d,.]+)'
    vencimento_pattern = r'Vencimento\s*(\d{2}/\d{2}/\d{4})\s*Pagamento\s*(\d{2}/\d{2}/\d{4})'
    locatario_pattern = r'Locatário\s+(.+?)(?:CPF|CNPJ)'  # Pega apenas até antes do CPF ou CNPJ

    empresa = re.findall(nome_empresa, conteudo)
    taxas_admin = re.findall(taxa_admin_pattern, conteudo)
    total_repasses = re.findall(total_repasse_pattern, conteudo)
    vencimentos = re.findall(vencimento_pattern, conteudo)
    locatarios = [locatario.strip() for locatario in re.findall(locatario_pattern, conteudo)]

    # Remover o ponto como separador de milhar e garantir o formato de vírgula para os valores
    taxas_admin = [taxa.replace(".", "").replace(",", ".") for taxa in taxas_admin]
    taxas_admin = [taxa.replace(".", ",") for taxa in taxas_admin]

    total_repasses = [repasse.replace(".", "").replace(",", ".") for repasse in total_repasses]
    total_repasses = [repasse.replace(".", ",") for repasse in total_repasses]

    contaMaldonado = ''
    contraPartida = ''
    bancoRepasse = ''

    # Verifique se 'empresa' contém o nome da empresa
    if empresa and empresa[0] == "PILIPILI ADMINISTRADORA PATRIMONIAL EIRELI":
        contaMaldonado = "10003"
        bancoRepasse = '537'
    elif empresa and empresa[0] == "LAKSHMI ADMINISTRAÇÃO DE IMÓVEIS EIRELI":
        contaMaldonado = "10002"
        bancoRepasse = '536'
    else:
        contaMaldonado = "Sem cadastro de empresa"

    # Inicializar uma lista para armazenar cada linha de repasse
    repasses = []

    # Verificar se há locatários, taxas administrativas e totais suficientes
    num_repasses = min(len(locatarios), len(taxas_admin), len(total_repasses), len(vencimentos))

    for i in range(num_repasses):
        # Consultar o locatário da linha atual
        if empresa and empresa[0] == "LAKSHMI ADMINISTRAÇÃO DE IMÓVEIS EIRELI":
            contraPartida = BancoDeDados.consultarClienteLaks(locatarios[i])
        elif empresa and empresa[0] == "PILIPILI ADMINISTRADORA PATRIMONIAL EIRELI":
            contraPartida = BancoDeDados.consultarClientePili(locatarios[i])
        else:
            contraPartida = "61"

        # Adicionar as informações formatadas
        repasses.append(f"{vencimentos[i][1]};{contaMaldonado};{contraPartida};{taxas_admin[i]};;VALOR REF. TAXA DE ADM - {locatarios[i]};1;;;")
        repasses.append(f"{vencimentos[i][1]};{bancoRepasse};{contraPartida};{total_repasses[i]};;RECEBIMENTO REF. REPASSE - {locatarios[i]};1;;;")

    return repasses
def contaDebito(origem,descricao):
    if origem == "C":
        retorno = "536"
    else:
        retorno = BancoDeDados.TrazerConta(descricao)
    return retorno
def contaCredito(origem,descricao):
    if origem == "C":
        retorno = BancoDeDados.TrazerConta(descricao)
    else:
        retorno = "536"
    return retorno
def historicoComp(origem):
    if origem == "C":
        retorno = "RECEBIMENTO REF. "
    else:
        retorno = "PGTO REF. "
    return retorno

resultados = []
repasse_extraido = []
relatorio_separado = []
dados_laks = []
dados_pili = []
def buscarArquivo():

  global dados_extraidos, resultados
  arquivo = filedialog.askopenfilename(
    title="Selecione um arquivo PDF",
    filetypes=(("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*"))
  )
  if arquivo:
    print(f"Arquivo Seleciona {arquivo}")
    conteudo_pdf = ler_pdf(arquivo)
    dadosGerais = extrair_dados(conteudo_pdf)
    print(dadosGerais)
    return
  else:
    return None
def buscarRepasse():
    global repasse_extraido

    # Abre a caixa de diálogo para selecionar o arquivo PDF
    arquivo = filedialog.askopenfilename(
        title="Seleciona o Repasse desejado",
        filetypes=(("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*"))
    )

    if arquivo:
        conteudo_pdf = ler_pdf(arquivo)
        repasse_extraido = extrair_repasse(conteudo_pdf)
        # Extração do nome da empresa usando a regex
        nome_empresa_pattern = r'Extrato de\s+(.+?)\s+Posição'
        nome_empresa_match = re.search(nome_empresa_pattern, conteudo_pdf)
        nome_empresa = nome_empresa_match.group(1) if nome_empresa_match else "Repasse"

        # Sugestão de nome para o arquivo com base no nome da empresa e no nome do arquivo original
        arquivo_original_nome = arquivo.split("/")[-1].replace(".pdf", "")
        nome_sugerido = f"REPASSES - {nome_empresa.strip()}.txt"

        # Abre a caixa de diálogo para selecionar onde salvar o arquivo, com nome sugerido
        caminho_salvar = filedialog.asksaveasfilename(
            title="Salvar arquivo de repasse",
            defaultextension=".txt",
            initialfile=nome_sugerido,
            filetypes=(("Text files", "*.txt"), ("Todos os arquivos", "*.*"))
        )

        # Se o usuário escolher um caminho para salvar
        if caminho_salvar:
            with open(caminho_salvar, 'w', encoding='utf-8') as file:
                for repasse in repasse_extraido:
                    file.write(repasse + '\n')
            print(f"Arquivo salvo em: {caminho_salvar}")
        else:
            print("Nenhum caminho de arquivo foi selecionado para salvar.")
        repasse_extraido = []

        return
    else:

        return None
def gerarArquivos():
    global resultados, relatorio_separado
    # Solicita ao usuário uma pasta para salvar os arquivos
    caminho_pasta = filedialog.askdirectory(
        title="Selecione uma pasta para salvar os arquivos"
    )
    if caminho_pasta:
        # Definir os nomes dos arquivos e os dados correspondentes
        arquivos = [
            ("ArquivoMaldonado.txt", resultados),
            ("ContasEmAcerto.txt", relatorio_separado),
        ]
        try:
            # Salva cada arquivo na pasta selecionada
            for nome_arquivo, dados in arquivos:
                caminho_arquivo_txt = os.path.join(caminho_pasta, nome_arquivo)

                # Certifique-se de que 'dados' seja uma lista ou iterável de strings
                if isinstance(dados, str):
                    dados = [dados]  # Converte uma única string em uma lista de uma linha

                with open(caminho_arquivo_txt, "w") as arquivo:
                    for dado in dados:
                        # Certifique-se de que cada item é uma string antes de aplicar upper()
                        arquivo.write(str(dado).upper() + "\n")
                print(f"Arquivo '{nome_arquivo}' salvo com sucesso em {caminho_pasta}")

            messagebox.showinfo("Sucesso", f"Arquivos salvos com sucesso em: {caminho_pasta}")
        except Exception as e:
            print(f"Erro ao salvar arquivos: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar os arquivos: {e}")

        resultados = []
        relatorio_separado = []

    else:
        print("Pasta de salvamento não selecionada")



