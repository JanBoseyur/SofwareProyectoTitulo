
import numpy as np
import librosa
import pandas as pd
import matplotlib.pyplot as plt

import pygame
import tkinter as tk
from tkinter import filedialog

from scipy.signal import hilbert
from scipy.ndimage import gaussian_filter1d

def detectar_segmentos(mask, sr):

    segmentos_voz = []
    segmentos_pausa = []

    if len(mask) == 0:
        return segmentos_voz, segmentos_pausa

    inicio = 0
    estado_actual = mask[0]

    for i in range(1, len(mask)):

        if mask[i] != estado_actual:

            fin = i

            duracion = (fin - inicio) / sr

            if estado_actual:
                segmentos_voz.append(
                    (inicio / sr, fin / sr, duracion)
                )
            else:
                segmentos_pausa.append(
                    (inicio / sr, fin / sr, duracion)
                )

            inicio = i
            estado_actual = mask[i]

    # Último segmento
    fin = len(mask)

    duracion = (fin - inicio) / sr

    if estado_actual:
        segmentos_voz.append(
            (inicio / sr, fin / sr, duracion)
        )
    else:
        segmentos_pausa.append(
            (inicio / sr, fin / sr, duracion)
        )

    return segmentos_voz, segmentos_pausa

def unir_pausas_cortas(mask, sr, min_pausa):

    mask = mask.copy()
    segmentos_voz, segmentos_pausa = detectar_segmentos(mask, sr)

    for inicio, fin, duracion in segmentos_pausa:

        if duracion < min_pausa:

            inicio_sample = int(inicio * sr)
            fin_sample = int(fin * sr)

            mask[inicio_sample:fin_sample] = True

    return mask

def eliminar_segmentos_voz_cortos(mask, sr, min_voz):

    mask = mask.copy()
    segmentos_voz, _ = detectar_segmentos(mask, sr)

    for inicio, fin, duracion in segmentos_voz:

        if duracion < min_voz:

            inicio_sample = int(inicio * sr)
            fin_sample = int(fin * sr)

            mask[inicio_sample:fin_sample] = False

    return mask

def extraer_caracteristicas_envolvente(
    audio_path,
    threshold_ratio=0.10,
    smoothing_ms=30,
    min_voice_ms=80,
    min_pause_ms=200,
    mostrar_grafico=True
):
    # =========================================================
    # 1. CARGAR AUDIO
    # =========================================================

    y, sr = librosa.load(
        audio_path,
        sr=None,
        mono=True
    )

    if len(y) == 0:
        raise ValueError("El archivo de audio está vacío.")

    duracion_audio = len(y) / sr

    # Normalización
    max_audio = np.max(np.abs(y))

    if max_audio > 0:
        y = y / max_audio

    # =========================================================
    # 2. ENVOLVENTE DE AMPLITUD
    # =========================================================

    # Transformada de Hilbert
    analytic_signal = hilbert(y)

    # Magnitud de la señal analítica
    envelope = np.abs(analytic_signal)

    # =========================================================
    # 3. SUAVIZAR ENVOLVENTE
    # =========================================================

    smoothing_samples = int(
        (smoothing_ms / 1000) * sr
    )

    # Evitar sigma = 0
    if smoothing_samples < 1:
        smoothing_samples = 1

    envelope = gaussian_filter1d(
        envelope,
        sigma=smoothing_samples
    )

    # Normalización de la envolvente
    max_envelope = np.max(envelope)

    if max_envelope > 0:
        envelope_normalized = (
            envelope / max_envelope
        )
    else:
        envelope_normalized = envelope

    # =========================================================
    # 4. ENERGÍA
    # =========================================================

    # Energía instantánea
    energia = envelope_normalized ** 2

    energia_media = np.mean(energia)
    energia_maxima = np.max(energia)
    variabilidad_energia = np.std(energia)

    # =========================================================
    # 5. DETECCIÓN INICIAL DE ACTIVIDAD
    # =========================================================

    threshold = (
        np.max(envelope_normalized)
        * threshold_ratio
    )

    actividad = (
        envelope_normalized > threshold
    )

    # =========================================================
    # 6. ELIMINAR MICRO-PAUSAS
    # =========================================================

    min_pause = min_pause_ms / 1000

    actividad = unir_pausas_cortas(
        actividad,
        sr,
        min_pause
    )

    # =========================================================
    # 7. ELIMINAR MICRO-SEGMENTOS DE VOZ
    # =========================================================

    min_voice = min_voice_ms / 1000

    actividad = eliminar_segmentos_voz_cortos(
        actividad,
        sr,
        min_voice
    )

    # =========================================================
    # 8. VOLVER A UNIR PAUSAS CORTAS
    # =========================================================

    # Después de eliminar segmentos de voz pequeños
    # pueden aparecer nuevas pausas pequeñas.

    actividad = unir_pausas_cortas(
        actividad,
        sr,
        min_pause
    )

    # =========================================================
    # 9. DETECTAR SEGMENTOS FINALES
    # =========================================================

    segmentos_voz, segmentos_pausa = detectar_segmentos(
        actividad,
        sr
    )

    # =========================================================
    # 10. DURACIONES
    # =========================================================

    duraciones_voz = [
        segmento[2]
        for segmento in segmentos_voz
    ]

    duraciones_pausas = [
        segmento[2]
        for segmento in segmentos_pausa
    ]

    # Duración total de voz
    duracion_total_voz = sum(
        duraciones_voz
    )

    # Duración total de pausas
    duracion_total_pausas = sum(
        duraciones_pausas
    )

    # =========================================================
    # 11. DURACIONES PROMEDIO
    # =========================================================

    if len(duraciones_voz) > 0:

        duracion_promedio_voz = np.mean(
            duraciones_voz
        )

    else:

        duracion_promedio_voz = 0.0

    if len(duraciones_pausas) > 0:

        duracion_promedio_pausas = np.mean(
            duraciones_pausas
        )

    else:

        duracion_promedio_pausas = 0.0

    # =========================================================
    # 12. CANTIDAD DE PAUSAS
    # =========================================================

    cantidad_pausas = len(
        duraciones_pausas
    )

    # =========================================================
    # 13. PROPORCIONES
    # =========================================================

    # Estas dos cantidades deberían sumar exactamente
    # la duración del audio.

    duracion_total_clasificada = (
        duracion_total_voz +
        duracion_total_pausas
    )

    if duracion_total_clasificada > 0:

        proporcion_voz = (
            duracion_total_voz /
            duracion_total_clasificada
        )

        proporcion_silencio = (
            duracion_total_pausas /
            duracion_total_clasificada
        )

    else:
        proporcion_voz = 0.0
        proporcion_silencio = 0.0

    # Voz / silencio
    if duracion_total_pausas > 0:

        proporcion_voz_silencio = (
            duracion_total_voz /
            duracion_total_pausas
        )

    else:
        proporcion_voz_silencio = np.inf

    # =========================================================
    # 14. VARIACIONES TEMPORALES DE AMPLITUD
    # =========================================================

    # Diferencia entre muestras consecutivas
    variaciones_amplitud = np.diff(
        envelope_normalized
    )

    # Magnitud media del cambio
    variacion_amplitud_media = np.mean(
        np.abs(variaciones_amplitud)
    )

    # Variabilidad de los cambios
    variabilidad_amplitud = np.std(
        variaciones_amplitud
    )

    # Mayor cambio de amplitud
    variacion_amplitud_maxima = np.max(
        np.abs(variaciones_amplitud)
    )

    # =========================================================
    # 15. VECTOR FINAL DE CARACTERÍSTICAS
    # =========================================================

    features = {

        # -----------------------------
        # Energía
        # -----------------------------

        "energia_media":
            energia_media,

        "energia_maxima":
            energia_maxima,

        "variabilidad_energia":
            variabilidad_energia,

        # -----------------------------
        # Segmentos de voz
        # -----------------------------

        "duracion_total_voz":
            duracion_total_voz,

        "duracion_promedio_segmentos_voz":
            duracion_promedio_voz,

        # -----------------------------
        # Pausas
        # -----------------------------

        "duracion_total_pausas":
            duracion_total_pausas,

        "duracion_promedio_pausas":
            duracion_promedio_pausas,

        "cantidad_pausas":
            cantidad_pausas,

        # -----------------------------
        # Voz / silencio
        # -----------------------------

        "proporcion_voz":
            proporcion_voz,

        "proporcion_silencio":
            proporcion_silencio,

        "proporcion_voz_silencio":
            proporcion_voz_silencio,

        # -----------------------------
        # Amplitud
        # -----------------------------

        "variacion_amplitud_media":
            variacion_amplitud_media,

        "variabilidad_amplitud":
            variabilidad_amplitud,

        "variacion_amplitud_maxima":
            variacion_amplitud_maxima
    }

    # =========================================================
    # 16. MOSTRAR INFORMACIÓN
    # =========================================================

    print("\n======================================")
    print("ANÁLISIS DE ENVOLVENTE")
    print("======================================")

    print(f"Archivo: {audio_path}")
    print(f"Frecuencia de muestreo: {sr} Hz")
    print(f"Duración audio: {duracion_audio:.3f} s")

    print("\n--- Parámetros ---")

    print(
        f"Umbral: {threshold:.4f}"
    )

    print(
        f"Suavizado: {smoothing_ms} ms"
    )

    print(
        f"Mínimo voz: {min_voice_ms} ms"
    )

    print(
        f"Mínimo pausa: {min_pause_ms} ms"
    )

    print("\n--- Segmentación ---")

    print(
        f"Segmentos de voz: "
        f"{len(segmentos_voz)}"
    )

    print(
        f"Pausas: "
        f"{cantidad_pausas}"
    )

    print(
        f"Voz total: "
        f"{duracion_total_voz:.3f} s"
    )

    print(
        f"Pausas total: "
        f"{duracion_total_pausas:.3f} s"
    )

    print(
        f"Voz + pausas: "
        f"{duracion_total_clasificada:.3f} s"
    )

    print("\n--- Características ---")

    for nombre, valor in features.items():

        if np.isinf(valor):

            print(
                f"{nombre}: infinito"
            )

        else:

            print(
                f"{nombre}: {valor}"
            )

    # =========================================================
    # 17. GRÁFICO
    # =========================================================

    if mostrar_grafico:

        times = np.arange(
            len(y)
        ) / sr

        plt.figure(
            figsize=(15, 6)
        )

        # Señal original
        plt.plot(
            times,
            y,
            alpha=0.35,
            label="Señal"
        )

        # Envolvente
        plt.plot(
            times,
            envelope_normalized,
            linewidth=2,
            label="Envolvente"
        )

        # Umbral
        plt.axhline(
            threshold,
            linestyle="--",
            label="Umbral"
        )

        # Pintar segmentos de voz
        for inicio, fin, duracion in segmentos_voz:

            plt.axvspan(
                inicio,
                fin,
                alpha=0.15
            )

        plt.xlabel(
            "Tiempo (s)"
        )

        plt.ylabel(
            "Amplitud normalizada"
        )

        plt.title(
            "Análisis de la envolvente de la señal"
        )

        plt.legend()

        plt.tight_layout()

        plt.show()

    return (
        features,
        envelope_normalized,
        np.arange(len(y)) / sr
    )

# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    audio = "federer_speech.wav"

    features, envelope, times = (
        extraer_caracteristicas_envolvente(
            audio_path=audio,

            # 10% del máximo
            threshold_ratio=0.10,

            # Suavizado de 30 ms
            smoothing_ms=30,

            # Voz debe durar al menos 80 ms
            min_voice_ms=80,

            # Pausas menores a 200 ms
            # se consideran parte de la voz
            min_pause_ms=200,

            mostrar_grafico=True
        )
    )