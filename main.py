import os
import install
from time import sleep
from threading import Thread
from ssw import TratXml
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog

rtrhread = {'args': [], 'func': [], 'retorno': None}


def set_rtrhread(args, func):
    rtrhread['args'] = args
    rtrhread['func'] = func
    rtrhread['retorno'] = None


try:
    # ssw = ()
    ssw = TratXml()  # iniciar o chome
    erro_cromiun = False
except Exception as erro:
    erro_cromiun = str(erro)


class Trssw(Thread):
    def run(self):
        try:
            print('começar thread')
            if 'login' in rtrhread['func']:
                cpf, login, senha = rtrhread['args']
                rtrhread['retorno'] = ssw.ch.login(cpf, login, senha)
                return None

            if rtrhread['func']['bxctrc']:
                rtrhread['func']['bxctrc'] = False
                ssw.ch.opcao608()

            if rtrhread['func']['bxtransportadora']:
                rtrhread['func']['bxtransportadora'] = False
                ssw.ch.opcao485(cnpjs_transp=ssw.transportadoras)

            if rtrhread['func']['bxlancar']:
                rtrhread['func']['bxlancar'] = False
                ssw.ch.opcao6(list_nfs=ssw.notas)

            rtrhread['retorno'] = True
            return None
        except:
            rtrhread['retorno'] = True
            return None


class Smg(ScreenManager):
    pass


class Telaincio(MDScreen):
    def on_enter(self, *args):
        if not erro_cromiun:
            self.event = Clock.schedule_interval(self.nextscreen, 0.5)
        else:
            self.event = Clock.schedule_interval(self.screenerro, 0.2)

    def nextscreen(self, *args):
        self.manager.current = 'Tela_login'
        self.event.cancel()

    def screenerro(self, *args):
        self.ids.lberro.text = erro_cromiun


class Telalogin(MDScreen):

    def sendlogin(self, cpf, login, senha):
        """PAssa cpf, login, senha e inicia o SSw"""
        self.ids.btiniciarlogin.disabled = True
        self.dialog = None
        'Chamada no login'
        set_rtrhread(args=[cpf, login, senha], func=['login'])
        trd = Trssw()
        trd.start()
        self.event = Clock.schedule_interval(self.returnlogin, 0)
        # login = ssw.ch.login(cpf, login, senha)

    def returnlogin(self, *args):
        login = rtrhread['retorno']
        if login == None:
            return
        if login:
            self.event.cancel()
            self.manager.lx = []  # valiavel que recebe a lista de arquivos
            self.manager.current = 'Tela_uso'
        else:
            self.ids.btiniciarlogin.disabled = False
            self.event.cancel()
            print('erro')
            self.ids.txcpf.text = ''
            self.ids.txusuario.text = ''
            self.ids.txsenha.text = ''
            if not self.dialog:
                self.dialog = MDDialog(
                    text="Login Invalido",
                )

            self.dialog.open()


class Telauso(MDScreen):

    def iniciar(self):
        ''' Botao Inicia
        Verifica primeiro placa e arquivos
        '''
        self.dialog = None
        if self.ids.txplaca.text == '':
            if not self.dialog:
                self.dialog = MDDialog(
                    text="Placa invalida",
                )

            self.dialog.open()
            return
        if self.ids.lbcaminho.text == '':
            if not self.dialog:
                self.dialog = MDDialog(
                    text="POR FAVOR ESCOLHA A PASTA DOS ARQUIVOS",
                )

            self.dialog.open()

            return
        self.ids.btiniciar.disabled = True
        self.ids.btiniciar.text = 'AGUARDE:'
        self.ld = 1
        passos = {'bxctrc': self.ids.bxctrc.active,
                  'bxtransportadora': self.ids.bxtransportadora.active,
                  'bxlancar': self.ids.bxlancar.active
                  }
        trd = Trssw()
        set_rtrhread(args=[], func=passos)
        trd.start()

        self.event = Clock.schedule_interval(self.rt_bt_iniciar, 0.5)

    def rt_bt_iniciar(self, *args):

        if rtrhread['retorno'] == None:
            if self.ld < 10:
                self.ids.btiniciar.text = f'AGUARDE:{self.ld * "°"}'
                self.ids.bxtransportadora.active = rtrhread['func']['bxtransportadora']
                self.ids.bxctrc.active = rtrhread['func']['bxctrc']
                self.ids.bxlancar.active = rtrhread['func']['bxlancar']
                self.ld += 1
            else:
                self.ld = 1
            return
        else:
            self.event.cancel()

            self.ids.btiniciar.disabled = False
            self.ids.btiniciar.text = 'Iniciar'

    def file_manager_open(self):
        self.manager_open = True
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )
        self.file_manager.selector = 'folder'
        self.file_manager.ext = ['.7z']
        self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
        self.manager_open = True

    def select_path(self, path: str):
        """
        It will be called when you click on the file name
        or the catalog selection button.

        path :param path: path to the selected directory or file;
        """
        self.manager.lx = path
        self.exit_manager()

    def exit_manager(self, *args):
        """Called when the user reaches the root of the directory tree."""

        self.manager_open = False
        self.file_manager.close()
        self.ids.lbcaminho.text = f'Arquivos preparados {self.manager.lx}'
        ssw.xml_ssw(patch_arqs=self.manager.lx)
        self.manager.current = 'Tela_uso'


class MainApp(MDApp):
    def on_stop(self):
        ssw.clean_foulder()
        ssw.ch.sair()

    def build(self):
        # Window.bind(on_keyboard=self._reload_keypress)
        return Smg()


if __name__ == '__main__':
    MainApp().run()
