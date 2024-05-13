"""
    Este programa tem como objetivo automatizar uma demanda relacionada ao DEPOL
    da Câmara dos Deputados. A demanda em questão envolve autorizações de acesso
    a Casa, fora do horário de expediente, onde cada autorização tem um prazo de
    validade, sendo que ao vencer, as autorizações em questão, devem ser arquivadas
    no software web tramitador de documentos (EDOC).
    Autoria: Erick Cezar Seabra da Silva
    A utilização (não comercial) deste software é unica e exclusiva à Câmara dos Deputados
    de Brasília - DF.
"""

# Imports necessários
# import configparser
import logging
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from tkinter import messagebox, Tk


# ------------------------------------- #
# Configs
# Determinando caminho de salvamento para logs
desktopPath = os.path.join(os.path.expanduser('~'), 'Desktop')
# Criando o arquivo log
logPath = os.path.join(desktopPath, 'arquivamento.log')
# Configurações básicas do arquivo log
logging.basicConfig(filename=logPath, level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s\n')
# ------------------------------------- #


# ------------------------------------- #
# Função para retornar o driver do navegador
def retornaDriver():
    # Guardando driver no navegador
    try:
        driver = webdriver.Chrome()
        logging.info(
            'Driver do navegador carregado com sucesso! Continuando execução...\n')
        return driver
    except Exception as e:
        logging.error(
            f'Erro ao carregar driver do navegador!\nMensagem de erro:{str(e)}\n')
# ------------------------------------- #


# ------------------------------------- #
# Função que abre a intranet onde ocorre a automação
def abreIntra(driver, url):
    wait = WebDriverWait(driver, 120)
    try:
        driver.get(url)
        driver.maximize_window()
        logging.info('Abertura da página concluída com sucesso!\n')
        try:
            """ Esperando o login manual do usuario"""
            tarefas = wait.until(
                EC.visibility_of_element_located((By.ID, 'tarefas_form')))
            if tarefas.is_displayed():
                logging.info(f'Login realizado com sucesso!\n')
        except Exception as e:
            logging.error(f'Falha no login. Erro retornado: {str(e)}')
    except Exception as e:
        logging.error(f'Erro ao abrir o EDOC\nMensagem de erro:{str(e)}\n')
# ------------------------------------- #


# ------------------------------------- #
# Função para abrir a lista de tarefas a serem arquivadas
def abreLista(wait):
    try:
        # Achando elemento referente a lista de tarefas de interesse
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/table[2]/tbody/tr/td[1]/div/div[1]/div[2]/form/div[4]/ul/li[2]/a'))).click()
        # Ordenando a lista pela coluna de prazo de conclusão, por ordem crescente
        ordenaLista(wait)
        logging.info('Lista de tarefas carregadas com sucesso!\n')
    except Exception as e:
        logging.error(
            f'Erro ao abrir lista de tarefas!\nMensagem de erro: {str(e)}')
# ------------------------------------- #


# ------------------------------------- #
# Função para ordenar a lista de tarefas, em ordem crescente, por prazo de vencimento
def ordenaLista(wait):
    try:
        # wait.until(EC.element_to_be_clickable(
        #     (By.ID, 'j_id421:j_id447header:sortDiv'))).click()
        wait.until(EC.element_to_be_clickable(
            (By.ID, 'j_id427:j_id453header:sortDiv'))).click()
        try:
            wait.until(EC.element_to_be_clickable(
                (By.ID, 'j_id427:j_id453header:sortDiv'))).click()
            # wait.until(EC.element_to_be_clickable(
            #     (By.ID, 'j_id421:j_id447header:sortDiv'))).click()
        except Exception as e:
            logging.error(
                f'Erro ao ordenar lista por prazo de conclusão!\nERRO:{str(e)}')
    except Exception as e:
        logging.error(
            f'Erro ao ordenar lista por prazo de conclusão!\nERRO:{str(e)}')
# ------------------------------------- #


# ------------------------------------- #
# Função que verifica se a data da tarefa ja esta vencida
def verificaData(wait):
    try:
        # wait.until(EC.presence_of_element_located((By.ID, 'j_id421:tb')))
        wait.until(EC.presence_of_element_located((By.ID, 'j_id427:tb')))
        # linha = wait.until(EC.presence_of_element_located(
        #     (By.ID, 'j_id421:0:j_id447')))
        linha = wait.until(EC.presence_of_element_located(
            (By.ID, 'j_id427:0:j_id453')))
        dataTexto = linha.text
        dataEncontrada = datetime.strptime(dataTexto, "%d/%m/%Y").date()
        dataAtual = datetime.now().date()
        if dataEncontrada < dataAtual:
            # tarefa = wait.until(EC.presence_of_element_located(
            #     (By.ID, 'j_id421:0:j_id465'))).text
            tarefa = wait.until(EC.presence_of_element_located(
                (By.ID, 'j_id427:0:j_id471'))).text
            palavras = tarefa.split()
            num = palavras[0]
            logging.info(
                f'Verificação de data concluída!\nNúmero de processo referente: {num}\n')
            return num
        else:
            return
    except Exception as e:
        logging.error(f'Erro ao verificar a data!\nMensagem de erro:{str(e)}')
# ------------------------------------- #

# ------------------------------------- #
# Função que busca pelo número do processo vencido, e arquiva o mesmo


def arquivaProc(numero, wait):
    try:
        dataAtualFormatada = datetime.now().date()
        msg = f'Tarefa vencida!\n(Arquivada automaticamente por automação no dia: {dataAtualFormatada})'
        input = wait.until(EC.presence_of_element_located(
            (By.ID, 'quick_search_input')))
        input.clear()
        input.send_keys(numero)
        wait.until(EC.element_to_be_clickable(
            (By.ID, 'quick_search_button'))).click()
        elemento = wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//a[@href='#' and contains(text(), '{numero}')]")))
        elemento.click()
        wait.until_not(EC.visibility_of_element_located(
            (By.ID, 'loading_mpContentDiv')))
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//input[@value="Arquivar"]'))).click()
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//textarea[@class="fieldColumn dataInputText"]'))).send_keys(msg)
        try:
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//a[@href="#" and @class="button" and contains(text(), "Arquivar")]'))).click()
            logging.info(
                f'Arquivamento concluído com sucesso!\nNúmero de processo referente: {numero}\n')
        except Exception as e:
            logging.error(
                f'Não foi possivel confirmar o arquivamento pela primeira estrutura!\nTentando pela segunda estrutura.')
            logging.error(f'Erro obtido: {str(e)}')
            try:
                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//input[@type="submit" and @value="Arquivar" and @class="buttonCD"]'))).click()
                logging.info(
                    f'Arquivamento confirmado pela segunda estrutura!\nNúmero de processo referente:{numero}\n')
            except Exception as e:
                logging.error(
                    f'Nem uma das estruturas pode confirmar o arquivamento!\nComeçando última tentativa de confirmar.\nErro: {str(e)}\n')
                try:
                    arquivar = wait.until(EC.visibility_of_element_located(
                        (By.XPATH, '//input[@type="submit" and @value="Arquivar" and @class="buttonCD"]')))
                    arquivar.click()
                    logging.info(
                        f'Arquivamento confirmado pela terceira estrutura!\nNúmero de processo referente:{numero}\n')
                except Exception as e:
                    logging.error(
                        f'Nem uma das estruturas pode confirmar o arquivamento!\nErro: {str(e)}\n')
    except Exception as e:
        logging.error(
            f'Erro ao arquivar processo:{numero}!\nMensagem de erro:{str(e)}\n')
        if "NewConnectionError" in str(e) or isinstance(e, WebDriverException):
            logging.critical(
                f'Erro de conexão detectado! Encerrando Programa.\nERRO RETORNADO: {str(e)}\n')
            sys.exit(1)


# ------------------------------------- #

# ------------------------------------- #
# Função principal do programa (Main)
def main():
    # Url utilizada
    url = 'https://edoc.camara.gov.br/nuxeo/login.jsp'
    dataAtual = datetime.now().date()
    dataAtualFormatada = datetime.strftime(dataAtual, '%d/%m/%Y')
    horaAtual = datetime.now().time()
    arquivados = []
    try:
        driver = retornaDriver()
        wait = WebDriverWait(driver, 10)

        abreIntra(driver, url)
        while True:
            abreLista(wait)
            processo = verificaData(wait)
            if processo:
                arquivaProc(processo, wait)
                logging.info(
                    f'Tarefa Arquivada!\nNumero de processo referente: {processo} Data: {dataAtualFormatada} Hora:{horaAtual}\n')
                arquivados.append(processo)
                abreLista(wait)
            else:
                logging.info('Automação concluída com sucesso!\n')
                break
    except Exception as e:
        logging.error(f'Erro na automação!\nMensagem de erro:{str(e)}')
    if len(arquivados) > 0:
        total = len(arquivados)
        logging.info(f'Total de processos arquivados: {total}\n')
        mensagem = f'Automação concluída com sucesso!\n\nTotal de autorizações arquivadas: {total}.\n'
    else:
        logging.info('Nem uma autorização vencida foi encontrada!\n')
        mensagem = f'Automação concluída com sucesso!\n\nNão foram encontradas autorizações vencidas!\n'

    driver.minimize_window()
    root = Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    messagebox.showinfo('Conclusão da automação', mensagem, parent=root)
    root.destroy()


if __name__ == "__main__":
    main()
# ------------------------------------- #
