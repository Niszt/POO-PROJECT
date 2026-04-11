import unittest
from abc import ABC, abstractmethod

class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance.app_name = "NotifySys"
            cls._instance.server = "smtp.servidor.com"
            cls._instance.tentativas_max = 3
            cls._instance.Tem_Permissao = True
        return cls._instance

class Notificacao(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        pass

class EmailNotificacao(Notificacao):
    def send(self, message: str) -> str:
        return f"EMAIL enviado via {AppConfig().server}: {message}"

class PushNotificacao(Notificacao):
    def send(self, message: str) -> str:
        return f"PUSH via {AppConfig().server}: {message}"

class ExternalSmsApi:
    def despachar_sms_p_provador(self, text: str) -> str:
        return f"[API EXTERNA SMS]: Mensagem '{text}' processada."

class SmsAdaptador(Notificacao):
    def __init__(self):
        self.external_api = ExternalSmsApi()

    def send(self, message: str) -> str:
        return self.external_api.despachar_sms_p_provador(message)

class NotificacaoProxy(Notificacao):
    def __init__(self, real_Notificacao: Notificacao):
        self.real_Notificacao = real_Notificacao

    def send(self, message: str) -> str:
        config = AppConfig()
   
        if not config.Tem_Permissao:
            return "[PROXY LOG]: Bloqueado. Sistema sem permissão de envio."

        tentativas = 0
        sucesso = False
        resultado = ""

        print("\nPROXY LOG: Iniciando processo de envio...")
        while tentativas < config.tentativas_max and not sucesso:
            tentativas += 1
            print(f"PROXY LOG: Tentativa {tentativas} de {config.tentativas_max}...")
           
            try:
                resultado = self.real_Notificacao.send(message)
                sucesso = True
                print("PROXY LOG: Envio bem sucedido.")
            except Exception as e:
                print(f"PROXY LOG: Falha na tentativa {tentativas} - Erro: {e}")

        if not sucesso:
            return f"PROXY LOG: Cancelado após {config.tentativas_max} tentativas falhas."
           
        return resultado

class NotificacaoFactory:
    @staticmethod
    def create(Tipo_Notificacao: str) -> Notificacao:
        t = Tipo_Notificacao.lower()
       
        if t == "email":
            real_notif = EmailNotificacao()
        elif t == "sms":
            real_notif = SmsAdaptador()
        elif t == "push":
            real_notif = PushNotificacao()
        else:
            raise ValueError(f"Tipo '{Tipo_Notificacao}' inválido.")
           
        return NotificacaoProxy(real_notif)

class TestNotificacaoSystemV2(unittest.TestCase):
    def test_sms_adapter(self):
        notificacao = NotificacaoFactory.create("sms")
        resultadoado = notificacao.send("Seu código é 123")
        self.assertIn("[API EXTERNA SMS]", resultadoado)
       
    def test_proxy_permissions(self):
        AppConfig().Tem_Permissao = False
        notificacao = NotificacaoFactory.create("email")
        resultadoado = notificacao.send("Aviso")
        self.assertEqual(resultadoado, "[PROXY LOG]: Bloqueado. Sistema sem permissão de envio.")
        AppConfig().Tem_Permissao = True

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNotificacaoSystemV2)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
