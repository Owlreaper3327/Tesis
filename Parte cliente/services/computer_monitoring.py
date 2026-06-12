import pynput as pyt
import pyautogui as pag
import pywinctl as pyw
import time
from pynput import keyboard
import requests as rq
import threading

EVENTOS = {"copiar": "copió algo",
           "cambio de ventana": "cambió la ventana actual",
           "cambio de pestaña": "cambió la pestaña actual",
           "pegar": "pegó algo"}

EVENT_URL = "http://127.0.0.1:8000/events/add"
PING_URL = "http://127.0.0.1:8000/events/ping"
OPEN_URL = "http://127.0.0.1:8000/events/start"
CLOSE_URL = "http://127.0.0.1:8000/events/close"

class Watchdog:
    """Clase encargada de vigilar los eventos locales de la computadora"""
    _instancia = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):

        with cls._lock:

            if cls._instancia is None:
                cls._instancia = super().__new__(cls)
        
        return cls._instancia

    def __init__(self, user:str):

        if not hasattr(self, "_iniciado"):
            self.running = False
            self.escucha = None
            self.teclas_presionadas = set()
            self.user = user
            self._iniciado = True
    
    def _on_press(self, key:keyboard.KeyCode):
        """Capturan cuando una tecla es presionada"""

        if key not in self.teclas_presionadas:
            self.teclas_presionadas.add(key)
        
        if keyboard.Key.tab in self.teclas_presionadas:
            if keyboard.Key.alt in self.teclas_presionadas:
                self.enviar_evento("cambio de ventana")
            elif keyboard.Key.ctrl in self.teclas_presionadas:
                self.enviar_evento("cambio de pestaña")
        
        if keyboard.Key.ctrl in self.teclas_presionadas:
            if keyboard.KeyCode.from_char("c") in self.teclas_presionadas:
                self.enviar_evento("copiar")
            
            if keyboard.KeyCode.from_char("v") in self.teclas_presionadas:
                self.enviar_evento("pegar")
        
    
    def _on_release(self, key:keyboard.KeyCode):
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

        envio = {"user": self.user,
                 "message": mensaje,
                 "date": fecha}

        try:
            rq.post(EVENT_URL, json=envio)
        except rq.exceptions.RequestException as re:
            pass
    
    def ping(self):
        """Notifica a la API que está activo"""

        while True:

            try:
                envio = {"user": self.user}

                rq.get(PING_URL, json=envio)
                break
            except rq.exceptions.RequestException as re:
                pass
    
    def start(self):
        """Inicia el vigilante"""

        if self.running:
            return

        self.escucha = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        self.escucha.start()
        self.running = True
    
    def stop(self):
        """Detiene el vigilante"""

        if self.running and self.escucha:
            self.escucha.stop()
            self.running = False