
import pygame
import tkinter as tk
from tkinter import filedialog

from scipy.signal import hilbert
from scipy.ndimage import gaussian_filter1d

class AudioPlayer:

    def __init__(self, root):
        self.root = root
        self.root.title("Reproductor de audio")
        self.root.geometry("500x180")

        pygame.mixer.init()

        self.audio_path = None

        # Nombre del archivo
        self.label = tk.Label(
            root,
            text="Ningún audio seleccionado"
        )
        self.label.pack(pady=15)

        # Botones
        frame = tk.Frame(root)
        frame.pack()

        tk.Button(
            frame,
            text="Abrir",
            command=self.abrir_audio
        ).pack(side="left", padx=5)

        tk.Button(
            frame,
            text="▶ Reproducir",
            command=self.reproducir
        ).pack(side="left", padx=5)

        tk.Button(
            frame,
            text="⏸ Pausar",
            command=self.pausar
        ).pack(side="left", padx=5)

        tk.Button(
            frame,
            text="▶ Continuar",
            command=self.continuar
        ).pack(side="left", padx=5)

        tk.Button(
            frame,
            text="⏹ Detener",
            command=self.detener
        ).pack(side="left", padx=5)

    def abrir_audio(self):

        archivo = filedialog.askopenfilename(
            title="Seleccionar audio",
            filetypes=[
                ("Archivos de audio", "*.wav *.mp3 *.ogg"),
                ("Todos los archivos", "*.*")
            ]
        )

        if archivo:
            self.audio_path = archivo

            self.label.config(
                text=archivo.split("/")[-1]
            )

            pygame.mixer.music.load(archivo)

    def reproducir(self):
        if self.audio_path:
            pygame.mixer.music.play()

    def pausar(self):
        pygame.mixer.music.pause()

    def continuar(self):
        pygame.mixer.music.unpause()

    def detener(self):
        pygame.mixer.music.stop()


root = tk.Tk()

app = AudioPlayer(root)

root.mainloop()

pygame.mixer.quit()