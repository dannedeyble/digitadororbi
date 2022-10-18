import os
from py7zr import SevenZipFile


class Zips:
    def __init__(self):
        self.path_dowload = None
        self.arquivos = None
        self.contador = 1

    def seach_arquivos(self,ext):
        caminhos = [os.path.join(self.path_dowload, nome) for nome in

                    os.listdir(self.path_dowload[:-1])]
        arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
        self.arquivos = [arq for arq in arquivos if arq.lower().endswith(f"{ext}")]
        return self.arquivos

    def unzip(self,path_in, path_out):
        self.path_dowload=path_in
        self.arquivos = self.seach_arquivos('.7z')
        total=len(self.arquivos)
        if not total>0:
            print('nenhum zip')
            return
        for arquivo in self.arquivos:
            try:
                print(f'Unzip {round((total/self.contador)*100,2)}%', end='', flush=True)
                with SevenZipFile(arquivo, 'r') as z:
                    z.extractall(path=path_out)
                print('\r', end=' ')
                self.contador+=1
                os.remove(arquivo)
                retorno=True
            except Exception as erro:
                print(erro)
                retorno = False
                os.remove(arquivo)
        return retorno

if __name__=='__main__':
    z=Zips()
    z.path_dowload='/home/dannedeyble/Área de Trabalho/digitadororbi/XMLs/'
    print(z.path_dowload[:-1])
    z.unzip('.7z')