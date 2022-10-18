# import datetime

import os

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date

from selenium.webdriver.chrome.options import Options


###
# INICIO

class ChromeAuto:

    def __init__(self):
        self.u_path = os.getcwd()
        self.drive_path = os.path.join(os.getcwd(),'chromedriver')
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument(f'download.default_directory={self.u_path}/arquivos/')
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('user-data-dir=Perfil')
        self.ut_seq_escreve = ''
        self.chrome = webdriver.Chrome(
            self.drive_path,
            options=self.chrome_options

        )
        self.usuario = 'danne2'
        self.janelas = dict()

    def acessar(self, site):
        self.chrome.get(site)

    def sair(self):
        self.chrome.quit()

    def login(self, cpf, login,senha):
        self.janelas['principal'] = self.chrome.window_handles[0]
        self.chrome.find_element('id', '1').clear()
        self.chrome.find_element('id', '2').clear()
        self.chrome.find_element('id', '3').clear()
        self.chrome.find_element('id', '4').clear()
        sleep(1)
        self.chrome.find_element('id', '1').send_keys('ser')
        self.chrome.find_element('id', '2').send_keys(f'{cpf}')
        self.chrome.find_element('id', '3').send_keys(f'{login}')
        self.chrome.find_element('id', '4').send_keys(f'{senha}')
        self.chrome.find_element('id', '5').click()
        espera = self.chrome.find_element(By.ID, 'procimg').text
        self._espera_ssw_aguarde(espera)
        sleep(1)
        if len(self.chrome.find_elements(By.ID,'pnlatraso')) == 0:
            self.chrome.find_element(By.ID,'0').click()
            return False
        self.chrome.find_element('id', '2').clear()
        self.chrome.find_element('id', '2').send_keys("rao")
        return True

    def _espera_ssw_aguarde(self,espera):
        while espera == 'Aguarde ...':
            print('1')
            sleep(1)
            espera = self.chrome.find_element(By.ID, 'procimg').text

    def _espera_ssw(self, janela_in, janela_out, tipo, id):
        self.chrome.switch_to.window(self.janelas[janela_in])
        sleep(0.5)
        espera = self.chrome.find_element(By.ID, 'procimg').text
        self._espera_ssw_aguarde(espera)
        sleep(0.5)
        janelas_out = [x for x in self.chrome.window_handles if x not in self.janelas.values()]
        self.janelas[janela_out] = janelas_out[0]
        self.chrome.switch_to.window(self.janelas[janela_out])
        print(self.chrome.window_handles)
        print('____Entou na pagina______')
        while not len(self.chrome.find_elements(tipo, id)) > 0:
            print('esperar carregar')

        self.chrome.switch_to.window(self.janelas[janela_out])

    def opcao389(self, cnpj_dest):
        print(self.chrome.window_handles)
        '.srtr2: nth - child(3) >.srtd2: nth - child(9) >.srdvr'
        self.chrome.find_element('id', '3').send_keys('389')
        sleep(5)
        print(self.chrome.window_handles[1])
        self.chrome.switch_to.window(self.chrome.window_handles[1])
        print(self.chrome.window_handles)
        for x in cnpj_dest:
            try:

                sleep(0.5)

                self.chrome.find_element('id', '2').clear()
                self.chrome.find_element('id', '2').send_keys(str(x))
                print(x)
                sleep(0.8)
                print(self.chrome.window_handles)
                if len(self.chrome.window_handles) < 3:
                    while len(self.chrome.window_handles) < 3:
                        sleep(0.1)
                print(self.chrome.window_handles)
                self.chrome.switch_to.window(self.chrome.window_handles[2])
                sleep(0.5)
                item = self.chrome.find_element('id', '2').get_attribute("value")
                if self.chrome.find_element('id', '2').get_attribute("value") == "N":
                    self.chrome.find_element('id', '2').clear()
                    self.chrome.find_element('id', '2').send_keys('v')
                    sleep(0.5)
                    self.chrome.find_element('id', '5').click()
                    sleep(1)
                    self.chrome.switch_to.window(self.chrome.window_handles[1])
                else:
                    self.chrome.find_element('id', '6').click()
                    self.chrome.switch_to.window(self.chrome.window_handles[1])
            except:
                self.chrome.switch_to.window(self.chrome.window_handles[1])
        self.chrome.close()
        self.chrome.switch_to.window(self.janelas['principal'])

    def opcao608(self):
        self.chrome.find_element('id', '3').send_keys('608')
        self._espera_ssw(janela_in='principal', janela_out='608', tipo=By.ID, id='1')
        print(f'{os.getcwd()}/xmlssw/ssw.zip')
        self.chrome.find_element(By.ID, '1').send_keys(f'{os.getcwd()}/xmlssw/ssw.zip')
        self.chrome.find_element(By.ID, '2').click()
        self._espera_ssw_aguarde(self.chrome.find_element(By.ID, 'procimg').text)
        self.chrome.close()
        self.chrome.switch_to.window(self.janelas['principal'])
        return True

    def loop485(self, cnpj_transp):
        x = cnpj_transp
        try:
            self.chrome.switch_to.window(self.janelas['485'])
            sleep(0.5)
            self.chrome.find_element('id', 't_cgc').clear()
            self.chrome.find_element('id', 't_cgc').send_keys(str(x))
            self._espera_ssw(janela_in='485', janela_out='485_2', tipo=By.ID, id='tp_operacao')
            print(f'{x}x  aqio')
            sleep(0.5)
            valor = self.chrome.find_elements(By.CSS_SELECTOR, ".data:nth-child(69)")[0].text
            valor2 = self.chrome.find_element('id', 'tp_operacao').get_attribute('value')
            if valor == '' or valor2 != 'R':
                self.chrome.find_element('id', 'tp_operacao').clear()
                self.chrome.find_element('id', 'tp_operacao').send_keys('r')
                self.chrome.find_element('id', 'desc_icms').send_keys('n')
                self.chrome.find_element('id', 'desc_piscofins').send_keys('n')
                self.chrome.find_element('id', '3').click()
                while self.janelas['485_2'] in self.chrome.window_handles:
                    sleep(1)
                self.janelas['485_2'] = ''
                self.chrome.switch_to.window(self.janelas['485'])

                sleep(0.3)
                self.chrome.find_element(By.ID, "0").click()

            else:
                # self.chrome.switch_to.window(self.janelas['485_2'])
                self.chrome.find_element('id', '4').click()
                while self.janelas['485_2'] in self.chrome.window_handles:
                    sleep(1)
                    self.janelas['485_2'] = ''
        except:
            print(x)
            self.chrome.switch_to.window(self.janelas['485'])

    def opcao485(self, cnpjs_transp):
        """.srtr2: nth - child(3) >.srtd2: nth - child(9) >.srdvr"""
        self.chrome.find_element('id', '3').send_keys('485')
        self._espera_ssw(janela_in='principal', janela_out='485', tipo=By.ID, id='t_cgc')
        for x in cnpjs_transp:
            self.loop485(x)
        self.chrome.switch_to.window(self.janelas['485'])
        self.chrome.close()
        self.chrome.switch_to.window(self.janelas['principal'])

    def opcao6(self, list_nfs: dict):
        try:
            self.chrome.find_element('id', '3').send_keys('006')
            self._espera_ssw(janela_in='principal', janela_out='6', tipo=By.ID, id='id_tipo_doc')
            self.chrome.find_element('id', 'id_tipo_doc').clear()
            self.chrome.find_element('id', 'id_tipo_doc').send_keys('p')
            sleep(2)
            self.chrome.find_element('id', 'id_tipo_doc').clear()
            self.chrome.find_element('id', 'id_tipo_doc').send_keys('n')
            sleep(2)
            self.chrome.find_element('id', 'cgc_remetente').clear()
            self.chrome.find_element('id', 'tp_agrup').clear()
            self.chrome.find_element('id', 'placa_coleta').clear()
            self.chrome.find_element('id', 'cod_merc').clear()
            self.chrome.find_element('id', 'tab_gen').clear()
            self.chrome.find_element('id', 'cod_merc').clear()
            self.chrome.find_element('id', 'cgc_remetente').send_keys('07704914000182')
            self.chrome.find_element('id', 'tp_agrup').send_keys('d')
            self.chrome.find_element('id', 'placa_coleta').send_keys('jig8727')
            sleep(0.3)
            self.chrome.find_element('id', 'cod_merc').send_keys('1')
            sleep(0.5)
            self.chrome.find_element('id', 'tab_gen').send_keys('s')
            sleep(3)
            self.chrome.find_element('id', 'lnk_apontar').click()
            sleep(3)
            print(self.chrome.window_handles)
            self._espera_ssw(janela_in='6', janela_out='6_2', tipo=By.CSS_SELECTOR, id='.srtr2')

            # resolver pagina 1 e 2
            if self.chrome.find_elements(By.ID, '106'):
                self.loop_006(list_nfs)
                self.chrome.find_element(By.ID, '106').click()
                self.loop_006(list_nfs)
            else:
                self.loop_006(list_nfs)

            janelas = list(self.janelas.keys())
            janelas.remove('principal')
            for janela in janelas:
                print(janela)
                if self.janelas[janela] in self.chrome.window_handles:
                    print(self.janelas[janela])
                    self.chrome.switch_to.window(self.janelas[janela])
                    self.chrome.close()
            self.chrome.switch_to.window(self.janelas['principal'])
        except:
            janelas = list(self.janelas.keys())
            janelas.remove('principal')
            for janela in janelas:
                self.chrome.switch_to.window(self.janelas[janela])
                sleep(0.5)
                self.chrome.close()
            self.chrome.switch_to.window(self.janelas['principal'])
            return False

    def loop_006(self, list_nfs: dict):

        elem_status = '.srtr2:nth-child(%s) > .srtd2:nth-child(12) > .srdvl'
        recebedor = '.srtr2:nth-child(%s) > .srtd2:nth-child(4) > .srdvl'
        cidade = '.srtr2:nth-child(%s) > .srtd2:nth-child(6) > .srdvl'
        qtditens = len(self.chrome.find_elements(By.CSS_SELECTOR, '.srtr2')) - 1
        meus_itens = dict()

        for item in range(2, qtditens):
            # print(str(self.chrome.find_element(By.CSS_SELECTOR, str(recebedor)
            #                                    .replace('%s', f'{item}')).text))
            if str(self.chrome.find_element(By.CSS_SELECTOR, str(recebedor)
                    .replace('%s', f'{item}')).text) == ' ' and str(
                self.chrome.find_element(By.CSS_SELECTOR, str(cidade)
                        .replace('%s', f'{item}')).text) != ' ':
                meus_itens[str(self.chrome.find_element(By.CSS_SELECTOR, str(elem_status)
                                                        .replace('%s', f'{item}')).text)] = str(item)

                nota = self.chrome.find_element(By.CSS_SELECTOR, f'.srtr2:nth-child({str(item)}) u').text
                nota = nota[3:]
                # print(nota)
                try:
                    if not nota in list(list_nfs.keys()):
                        continue

                    self.chrome.find_element(By.CSS_SELECTOR, f'.srtr2:nth-child({str(item)}) u').click()

                    self._espera_ssw(janela_in='6_2', janela_out='6_3', tipo=By.ID, id='cnpj_red')

                    # print(f'NF {nota} Tran {list_nfs[nota]}')
                    sleep(1)
                    self.chrome.find_element('id', 'cnpj_red').clear()
                    self.chrome.find_element('id', 'cnpj_red').send_keys(list_nfs[nota])
                    while self.chrome.find_element('id', 'nome_red').get_attribute('value')=="":
                        sleep(0.3)
                    self.chrome.find_element('id', '89').click()

                    while self.janelas['6_3'] in self.chrome.window_handles:
                        sleep(1)
                        print("esperando intervençao")
                    if self.janelas['6_3'] in self.chrome.window_handles:
                        self.chrome.switch_to.window(self.janelas['6_3'])
                        self.chrome.close()
                        self.chrome.switch_to.window(self.janelas['6_2'])
                        print('fechou com erro')
                        print(f'NF {nota} Tran {list_nfs[nota]}')
                    else:
                        self.chrome.switch_to.window(self.janelas['6_2'])

                except:
                    janelas=list(self.janelas.keys())
                    janelas.remove('principal')
                    for janela in janelas:
                        self.chrome.switch_to.window(self.janelas[janela])
                        sleep(0.5)
                        self.chrome.close()
                    self.chrome.switch_to.window(self.janelas['principal'])
        print('proxima pagina')


if __name__ == '__main__':
    # # y = 1
    # # # while y == 1:
    data = date.today()
    hoje_h = date.strftime(data, '%d%m%y')
    hoje_ini = f'01{date.strftime(data, "%m%y")}'

    chrome = ChromeAuto()
    chrome.acessar('http://www.ssw.inf.br/ssw')
    print('acessar')
    sleep(5)
    chrome.login()
    print('login')
    sleep(5)
