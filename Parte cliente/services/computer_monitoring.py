import pynput as pyt
import pyautogui as pag
import pywinctl as pyw
import time
from pynput import keyboard
import requests as rq

EVENTOS = {"copiar": "copió algo",
           "cambio de ventana": "cambió la ventana actual",
           "cambio de pestañas": "cambió la pestaña actual",
           "pegar": "pegó algo"}

EVENT_URL = "http://127.0.0.1:8000/events/add"
PING_URL = "http://127.0.0.1:8000/events/ping"
OPEN_URL = "http://127.0.0.1:8000/events/start"
CLOSE_URL = "http://127.0.0.1:8000/events/close"

class Watchdog:
    """Clase encargada de vigilar los eventos locales de la computadora"""

    def __init__(self, user:str):

        self.running = False
        self.escucha = None
        self.teclas_presionadas = set()
        self.user = user
    
    def on_press(self, key:keyboard.Key):
        """Capturan cuando una tecla es presionada"""

        if key not in self.teclas_presionadas:
            self.teclas_presionadas.add(key)
        
        if keyboard.Key.tab in self.teclas_presionadas:
            if keyboard.Key.alt in self.teclas_presionadas:
                enviar_evento("cambio de ventana")
            elif keyboard.Key.ctrl in self.teclas_presionadas:
                enviar_evento("cambio de pestaña")
        
        if keyboard.Key.ctrl in self.teclas_presionadas:
            if keyboard.KeyCode.from_char("c") in self.teclas_presionadas:
                enviar_evento("copiar")
            
            if keyboard.KeyCode.from_char("v") in self.teclas_presionadas:
                enviar_evento("pegar")
        
    
    def on_release(self, key:keyboard.Key):
        """Capturan cuando una tecla es soltada"""

        if key in self.teclas_presionadas:
            self.teclas_presionadas.remove(key)

    def enviar_ventana(self):
        """Captura y envía la ventana en la que se encuentra actualmente el estudiante"""

        ventana = pyw.getActiveWindowTitle()
        mensaje = f"{self.user} está en la ventana: {ventana}"
        fecha = time.time()

        envio = {"user": self.user,
                 "message": mensaje,
                 "date": fecha}
        
        try:
            rq.post(EVENT_URL, json=envio)
        except rq.exceptions.RequestException as re:
            pass
    
    def enviar_evento(self, issue:str):
        """Envía los eventos en dependencia de ciertas combinaciones del teclado"""

        mensaje = f"{self.user} {EVENTOS[issue]}"
        fecha = time.time()

        envio = {}