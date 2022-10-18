from pathlib import Path
import zipfile
import os
import xmltodict
from time import sleep
from selenim import ChromeAuto
from zipfile import ZipFile
from zips import Zips


class TratXml:
    def __init__(self):
        self.cnpjs = list()
        self.resuldados = list()
        self.path_dowload = '/home/dannedeyble/Downloads'  # sem a / final
        self.path_xmls = f'{Path.home()}/DigitadorOrbi/XMLs/'
        self.path_ssw = f'{Path.home()}/DigitadorOrbi/xmlssw/'
        self.contador_xmls = 1
        self.notas = dict()
        self.transportadoras = list()
        self.ch = ChromeAuto()
        self.ch.acessar('http://www.ssw.inf.br/ssw')

    def shach_zip(self):
        Zips().unzip(path_in=f'{self.path_dowload}/', path_out=self.path_xmls)

    def _set_arquivos(self):
        # Buscar arquivos pasta padrao
        caminhos = [os.path.join(f'{self.path_xmls}', nome) for nome in
                    os.listdir(f'{self.path_xmls}')]
        arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
        xmls = [arq for arq in arquivos if arq.lower().endswith(".xml")]
        # print(len(xmls))
        return xmls

    def clean_foulder(self):
        # Buscar arquivos pasta padrao
        caminhos = [os.path.join(f'{self.path_xmls}', nome) for nome in
                    os.listdir(f'{self.path_xmls}')]
        arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
        for arq in arquivos:
            os.remove(arq)
        # print(len(xmls))


    def espera(self, tempo=3600):
        espera = 1
        while espera < tempo:
            print(f'{espera} de 3600 contador de email------', end='', flush=True)
            sleep(1)
            print('\r', end=' ')
            espera += 1

    def xml_ssw(self, xmls=None, patch_arqs=None):
        self.path_dowload = patch_arqs
        self._xml_Notas()

        if xmls is None:
            xmls = self._set_arquivos()

        try:
            os.remove(f'{self.path_ssw}ssw.zip')
        except:
            pass

        for arq in xmls:
            try:
                patch_xml = str(arq).split('/')[-1]
                with open(arq) as date:
                    dados = date.read()
                    dicionario = xmltodict.parse(dados)
                    dicionario['nfeProc']['NFe']['infNFe']['transp']['modFrete'] = '0'
                with open(f'{self.path_ssw}1.xml', '+w') as arq:
                    arq.write(xmltodict.unparse(dicionario))
                with ZipFile(f'{self.path_ssw}ssw.zip', 'a', 0) as zip:
                    zip.write(f'{self.path_ssw}1.xml', patch_xml)
            except:
                pass

    def _xml_Notas(self, xmls=None):
        self.shach_zip()
        # metodo de entrada de xmls refete a DOU
        if xmls is None:
            xmls = self._set_arquivos()
        self.total_xmls = len(xmls)
        self.cnpj_dest = list()
        self.cidade_dest = dict()
        red_proibidos = ['02072832000149', '07704914000182']
        for arq in xmls:
            try:
                with open(arq) as date:
                    dados = date.read()
                    dicionario = xmltodict.parse(dados)
                    NumeroNF = dicionario['nfeProc']['NFe']['infNFe']['ide']['nNF']
                    cif_fob = dicionario['nfeProc']['NFe']['infNFe']['transp']['modFrete']
                    redespacho = self.obsxml(str(dicionario['nfeProc']['NFe']['infNFe']['infAdic']))
                    # print(str(dicionario['nfeProc']['NFe']['infNFe']['infAdic']))
                    cnpj_dest = dicionario['nfeProc']['NFe']['infNFe']['dest']['CNPJ']

                    if cnpj_dest not in self.cnpj_dest:
                        self.cnpj_dest.append(cnpj_dest)

                    if redespacho and redespacho not in red_proibidos and str(redespacho) != str(cnpj_dest):
                        if redespacho == '11393773000100' and cif_fob == '0':
                            print(f'{NumeroNF} para rodo danny')
                            continue
                            pass
                        if NumeroNF in self.notas.keys():
                            continue
                        self.notas[NumeroNF] = redespacho
                        if redespacho not in self.transportadoras:
                            self.transportadoras.append(redespacho)

                # os.remove(arq)
            except:
                pass
        print(self.transportadoras)
        print(self.notas)

    def obsxml(self, obs):
        if 'Redespacho' in obs:
            obs = str(obs)
            cnpj = obs.split('CNPJ: ')
            cnpj = cnpj[1].split(' ')[0]
            cnpj = cnpj.replace('.', '')
            cnpj = cnpj.replace('/', '')
            cnpj = cnpj.replace('-', '')
            return cnpj
        else:
            return None

    def ler_notas(self):
        if len(self.cnpjs) == 0:
            self.xml_ssw()
            ch = ChromeAuto()
            ch.acessar('http://www.ssw.inf.br/ssw')
            sleep(2)
            # ch.login()
            # sleep(5)
            ch.opcao608()
            # sleep(2)
            # ch.opcao485(self.transportadoras)
            # ch.opcao389(s elf.cnpj_dest)
            # sleep(2)
            ch.opcao6(self.notas)
            # ch.opcao7()
        return self.resuldados
        # return [self.cnpjs,self.resuldados]


if __name__ == '__main__':
    cursor = TratXml()
    cnpj = cursor.clean_foulder()
    print(cnpj)
