
import unittest
from abc import ABC, abstractclassmethod


class TV:
    def ligar(self): print("tv ligada")
    def desligar(self): print("tv desligada")

class Projetor:
    def ligar(self): print("projetor ligado")
    def desligar(self): print("projetor desligado")
        
class Receiver:
    def ligar(self): print("receiver ligado")
    def modo_musica(self): print("receiver config. para modo cinema")
    def desligar(self): print("receiver desligado")
        
class MediaPlayer:
    def ligar(self): print("player ligado")
    def reproduzir(self, midia: str): print(f"Player de Mídia: Reproduzindo '{midia}'")
    def desligar(self): print("player desligado")
        
class Som:
    def ligar(self): print("Sistema de Som (Surround): Ligado")
    def ajustar_volume(self, nivel: int): print(f"Sistema de Som: Volume no nível {nivel}")
    def desligar(self): print("Sistema de Som: Desligado")
        
class LuzAmbiente:
    def ligar(self): print("Luzes: Acesas (100%)")
    def modo_cinema(self): print("Luzes: Escurecidas para modo cinema (10%)")
    def desligar(self): print("Luzes: Apagadas")
    
    
class HomeTheaterFacade:
    def __init__(self,tv:TV, projetor:Projetor,receiver: Receiver,player: MediaPlayer, som: Som, luz: LuzAmbiente):
        self.tv = tv
        self.projetor = projetor
        self.receiver = receiver
        self.player = player
        self.som = som
        self.luz = luz
    
    def assistirFilme(self, titulo: str):
        print(f"\nassitir: {titulo}")
        self.luz.modo_cinema()
        self.tv.ligar()
        self.projetor.ligar()
        self.som.ligar()
        self.som.ajustar_volume(8)
        self.player.ligar()
        self.player.reproduzir(titulo)
        
    def ouvirMusica(self, faixa: str):
        print(f"\nPreparando a sala para ouvir: {faixa}")
        self.luz.ligar()
        self.tv.desligar()
        self.projetor.desligar()
        self.receiver.ligar()
        self.receiver.modo_musica()
        self.som.ligar()
        self.som.ajustar_volume(5)
        self.player.ligar()
        self.player.reproduzir(faixa)
    
    def desligarTudo(self):
        print("\n Desligando todo o Home Theater")
        self.luz.ligar()
        self.tv.desligar()
        self.projetor.desligar()
        self.receiver.desligar()
        self.player.desligar()
        self.som.desligar()
        
if __name__ == "__main__":
    minha_tv = TV()
    meu_projetor = Projetor()
    meu_receiver = Receiver()
    meu_player = MediaPlayer()
    meu_som = Som()
    minhas_luzes = LuzAmbiente()
    
    home_theater = HomeTheaterFacade(
        tv=minha_tv, 
        projetor=meu_projetor, 
        receiver=meu_receiver, 
        player=meu_player, 
        som=meu_som, 
        luz=minhas_luzes
    )
    home_theater.assistirFilme("Totoro")
    home_theater.ouvirMusica("Birds of a feather de Billie")
    home_theater.desligarTudo()
    
