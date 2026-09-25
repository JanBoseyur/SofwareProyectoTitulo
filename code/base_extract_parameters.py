
import numpy as np
import parselmouth
from pathlib import Path

def normalized_band_energy(
    frequency_axis,
    energy_bin,
    lower_frequency,
    upper_frequency,
    total_frame_energy
):
    if (
        not np.isfinite(lower_frequency)
        or not np.isfinite(upper_frequency)
        or not np.isfinite(total_frame_energy)
        or total_frame_energy <= 0
    ):
        return np.nan

    # Limitar la banda al espectro disponible
    lower_frequency = max(
        lower_frequency,
        frequency_axis[0]
    )

    upper_frequency = min(
        upper_frequency,
        frequency_axis[-1]
    )

    if upper_frequency <= lower_frequency:
        return np.nan

    # Seleccionar bins dentro de la banda
    index_band = (
        (frequency_axis >= lower_frequency)
        & (frequency_axis <= upper_frequency)
    )

    if not np.any(index_band):
        return np.nan

    # Energía de la banda
    band_energy = np.sum(
        energy_bin[index_band]
    )

    # Normalización
    normalized_energy = (
        band_energy / total_frame_energy
    )

    return normalized_energy

def extraer_parametros_parselmouth(
    audio_path,
    sex_type="auto"
):
    # ============================================================
    # Inicializar salida
    # ============================================================

    feats = {

        # F0
        "mean_F_0": np.nan,
        "std_F_0": np.nan,
        "min_F_0": np.nan,
        "max_F_0": np.nan,

        # Jitter / Shimmer / HNR
        "jitter_Local": np.nan,
        "jitter_Abs": np.nan,
        "shimmer_Local": np.nan,
        "hnr": np.nan,

        # Formantes
        "F_1": np.nan,
        "F_2": np.nan,
        "F_3": np.nan,

        "std_F_1": np.nan,
        "std_F_2": np.nan,
        "std_F_3": np.nan,

        # Anchos de banda
        "mean_BW_F_1": np.nan,
        "mean_BW_F_2": np.nan,
        "mean_BW_F_3": np.nan,

        "std_BW_F_1": np.nan,
        "std_BW_F_2": np.nan,
        "std_BW_F_3": np.nan,

        # Energía normalizada
        "mean_E_F0_norm": np.nan,
        "mean_E_F1_norm": np.nan,
        "mean_E_F2_norm": np.nan,
        "mean_E_F3_norm": np.nan,

        "std_E_F0_norm": np.nan,
        "std_E_F1_norm": np.nan,
        "std_E_F2_norm": np.nan,
        "std_E_F3_norm": np.nan,

        # Energía en porcentaje
        "mean_E_F0_percent": np.nan,
        "mean_E_F1_percent": np.nan,
        "mean_E_F2_percent": np.nan,
        "mean_E_F3_percent": np.nan,

        # Frames
        "number_Formant_Frames": np.nan,
        "number_Valid_E_F0_Frames": np.nan,
        "number_Valid_E_F1_Frames": np.nan,
        "number_Valid_E_F2_Frames": np.nan,
        "number_Valid_E_F3_Frames": np.nan,
    }

    # ============================================================
    # Cargar audio
    # ============================================================

    audio_path = Path(audio_path)

    if not audio_path.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {audio_path}"
        )

    snd = parselmouth.Sound(str(audio_path))

    # Señal
    x = snd.values[0].astype(float)

    # Frecuencia de muestreo
    fs = snd.sampling_frequency

    # ============================================================
    # Preparar señal
    # ============================================================

    x = np.asarray(x).flatten()

    # Reemplazar valores no finitos
    x[~np.isfinite(x)] = 0

    if len(x) == 0 or np.max(np.abs(x)) == 0:
        raise ValueError(
            "La señal está vacía o contiene solamente ceros."
        )

    # Normalización global
    x = x / np.max(np.abs(x))

    duration = len(x) / fs

    # ============================================================
    # Parámetros según tipo de voz
    # ============================================================

    sex_type = sex_type.lower()

    if sex_type == "male":

        pitch_floor = 75
        pitch_ceiling = 300
        max_formant = 5000

    elif sex_type == "female":

        pitch_floor = 100
        pitch_ceiling = 500
        max_formant = 5500

    else:

        pitch_floor = 75
        pitch_ceiling = 500
        max_formant = 5500

    # ============================================================
    # Parámetros temporales
    # ============================================================

    time_step = 0.015
    window_duration = 0.030

    frame_length = round(
        window_duration * fs
    )

    frame_length = max(
        frame_length,
        2
    )

    # ============================================================
    # FFT
    # ============================================================

    nfft = max(
        4096,
        2 ** int(np.ceil(np.log2(frame_length)))
    )

    frequency_axis = (
        np.arange(nfft // 2 + 1)
        * fs
        / nfft
    )

    # Ventana Hann periódica
    sample_index = np.arange(frame_length)

    analysis_window = (
        0.5
        - 0.5
        * np.cos(
            2 * np.pi
            * sample_index
            / frame_length
        )
    )

    # ============================================================
    # PITCH
    # ============================================================

    pitch_obj = parselmouth.praat.call(
        snd,
        "To Pitch",
        0.0,
        pitch_floor,
        pitch_ceiling
    )

    feats["mean_F_0"] = parselmouth.praat.call(
        pitch_obj,
        "Get mean",
        0,
        0,
        "Hertz"
    )

    feats["std_F_0"] = parselmouth.praat.call(
        pitch_obj,
        "Get standard deviation",
        0,
        0,
        "Hertz"
    )

    feats["min_F_0"] = parselmouth.praat.call(
        pitch_obj,
        "Get minimum",
        0,
        0,
        "Hertz",
        "Parabolic"
    )

    feats["max_F_0"] = parselmouth.praat.call(
        pitch_obj,
        "Get maximum",
        0,
        0,
        "Hertz",
        "Parabolic"
    )

    # ============================================================
    # JITTER / SHIMMER
    # ============================================================

    pp = parselmouth.praat.call(
        snd,
        "To PointProcess (periodic, cc)",
        pitch_floor,
        pitch_ceiling
    )

    feats["jitter_Local"] = parselmouth.praat.call(
        pp,
        "Get jitter (local)",
        0,
        0,
        0.0001,
        0.02,
        1.3
    )

    feats["jitter_Abs"] = parselmouth.praat.call(
        pp,
        "Get jitter (local, absolute)",
        0,
        0,
        0.0001,
        0.02,
        1.3
    )

    feats["shimmer_Local"] = parselmouth.praat.call(
        [snd, pp],
        "Get shimmer (local)",
        0,
        0,
        0.0001,
        0.02,
        1.3,
        1.6
    )

    # ============================================================
    # HNR
    # ============================================================

    harmonicity_obj = parselmouth.praat.call(
        snd,
        "To Harmonicity (cc)",
        0.015,
        pitch_floor,
        0.03,
        1.0
    )

    feats["hnr"] = parselmouth.praat.call(
        harmonicity_obj,
        "Get mean",
        0,
        0
    )

    # ============================================================
    # FORMANTES
    # ============================================================

    formant_obj = parselmouth.praat.call(
        snd,
        "To Formant (burg)",
        time_step,
        5,
        max_formant,
        window_duration,
        50
    )

    # ============================================================
    # Obtener centros reales de los frames de Praat
    # ============================================================

    number_praat_frames = int(
        parselmouth.praat.call(
            formant_obj,
            "Get number of frames"
        )
    )

    all_frame_times = np.full(
        number_praat_frames,
        np.nan
    )

    for frame_index in range(
        number_praat_frames
    ):

        # Praat utiliza índices desde 1
        all_frame_times[frame_index] = (
            parselmouth.praat.call(
                formant_obj,
                "Get time from frame number",
                frame_index + 1
            )
        )

    # ============================================================
    # Seleccionar región central 20%-80%
    # ============================================================

    central_start_time = 0.2 * duration
    central_end_time = 0.8 * duration

    central_frame_index = (
        (all_frame_times >= central_start_time)
        &
        (all_frame_times <= central_end_time)
    )

    time_vector = all_frame_times[
        central_frame_index
    ]

    number_frames = len(time_vector)

    feats["number_Formant_Frames"] = number_frames

    # ============================================================
    # Variables frame a frame
    # ============================================================

    F0 = np.full(number_frames, np.nan)

    F1 = np.full(number_frames, np.nan)
    F2 = np.full(number_frames, np.nan)
    F3 = np.full(number_frames, np.nan)

    BW1 = np.full(number_frames, np.nan)
    BW2 = np.full(number_frames, np.nan)
    BW3 = np.full(number_frames, np.nan)

    E_F0_norm = np.full(number_frames, np.nan)
    E_F1_norm = np.full(number_frames, np.nan)
    E_F2_norm = np.full(number_frames, np.nan)
    E_F3_norm = np.full(number_frames, np.nan)

    # ============================================================
    # Procesamiento frame a frame
    # ============================================================

    for k, current_time in enumerate(time_vector):

        # --------------------------------------------------------
        # F0
        # --------------------------------------------------------

        F0[k] = parselmouth.praat.call(
            pitch_obj,
            "Get value at time",
            current_time,
            "Hertz",
            "Linear"
        )

        # --------------------------------------------------------
        # Formantes
        # --------------------------------------------------------

        F1[k] = parselmouth.praat.call(
            formant_obj,
            "Get value at time",
            1,
            current_time,
            "Hertz",
            "Linear"
        )

        F2[k] = parselmouth.praat.call(
            formant_obj,
            "Get value at time",
            2,
            current_time,
            "Hertz",
            "Linear"
        )

        F3[k] = parselmouth.praat.call(
            formant_obj,
            "Get value at time",
            3,
            current_time,
            "Hertz",
            "Linear"
        )

        # --------------------------------------------------------
        # Anchos de banda
        # --------------------------------------------------------

        BW1[k] = parselmouth.praat.call(
            formant_obj,
            "Get bandwidth at time",
            1,
            current_time,
            "Hertz",
            "Linear"
        )

        BW2[k] = parselmouth.praat.call(
            formant_obj,
            "Get bandwidth at time",
            2,
            current_time,
            "Hertz",
            "Linear"
        )

        BW3[k] = parselmouth.praat.call(
            formant_obj,
            "Get bandwidth at time",
            3,
            current_time,
            "Hertz",
            "Linear"
        )

        # --------------------------------------------------------
        # Validar F0
        # --------------------------------------------------------

        if (
            not np.isfinite(F0[k])
            or F0[k] < pitch_floor
            or F0[k] > pitch_ceiling
        ):
            F0[k] = np.nan

        # --------------------------------------------------------
        # Validar F1
        # --------------------------------------------------------

        if (
            not np.isfinite(F1[k])
            or F1[k] < 200
            or F1[k] > 1200
        ):
            F1[k] = np.nan
            BW1[k] = np.nan

        # --------------------------------------------------------
        # Validar F2
        # --------------------------------------------------------

        if (
            not np.isfinite(F2[k])
            or F2[k] < 600
            or F2[k] > 3000
        ):
            F2[k] = np.nan
            BW2[k] = np.nan

        # --------------------------------------------------------
        # Validar F3
        # --------------------------------------------------------

        if (
            not np.isfinite(F3[k])
            or F3[k] < 1500
            or F3[k] > 4200
        ):
            F3[k] = np.nan
            BW3[k] = np.nan

        # --------------------------------------------------------
        # Validar anchos de banda
        # --------------------------------------------------------

        if not np.isfinite(BW1[k]) or BW1[k] <= 0:
            BW1[k] = np.nan

        if not np.isfinite(BW2[k]) or BW2[k] <= 0:
            BW2[k] = np.nan

        if not np.isfinite(BW3[k]) or BW3[k] <= 0:
            BW3[k] = np.nan

        # ========================================================
        # Extraer frame de 30 ms
        # ========================================================

        center_sample = (
            round(current_time * fs)
        )

        first_sample = (
            center_sample
            - frame_length // 2
        )

        last_sample = (
            first_sample
            + frame_length
        )

        if (
            first_sample < 0
            or last_sample > len(x)
        ):
            continue

        current_frame = x[
            first_sample:last_sample
        ]

        # Eliminar componente DC
        current_frame = (
            current_frame
            - np.mean(current_frame)
        )

        # Ventana Hann
        windowed_frame = (
            current_frame
            * analysis_window
        )

        # ========================================================
        # FFT
        # ========================================================

        frame_fft = np.fft.fft(
            windowed_frame,
            n=nfft
        )

        # Energía unilateral
        energy_bin = (
            np.abs(
                frame_fft[:nfft // 2 + 1]
            ) ** 2
            / nfft
        )

        # Compensar frecuencias negativas
        if len(energy_bin) > 2:

            energy_bin[1:-1] *= 2

        # ========================================================
        # Energía total
        # ========================================================

        total_frame_energy = np.sum(
            energy_bin
        )

        if (
            not np.isfinite(total_frame_energy)
            or total_frame_energy <= 0
        ):
            continue

        # ========================================================
        # Energía alrededor de F0
        # ========================================================

        if np.isfinite(F0[k]):

            lower_F0 = 0.5 * F0[k]
            upper_F0 = 1.5 * F0[k]

            E_F0_norm[k] = normalized_band_energy(
                frequency_axis,
                energy_bin,
                lower_F0,
                upper_F0,
                total_frame_energy
            )

        # ========================================================
        # Energía alrededor de F1
        # ========================================================

        if (
            np.isfinite(F1[k])
            and np.isfinite(BW1[k])
        ):

            lower_F1 = (
                F1[k]
                - BW1[k] / 2
            )

            upper_F1 = (
                F1[k]
                + BW1[k] / 2
            )

            E_F1_norm[k] = normalized_band_energy(
                frequency_axis,
                energy_bin,
                lower_F1,
                upper_F1,
                total_frame_energy
            )

        # ========================================================
        # Energía alrededor de F2
        # ========================================================

        if (
            np.isfinite(F2[k])
            and np.isfinite(BW2[k])
        ):

            lower_F2 = (
                F2[k]
                - BW2[k] / 2
            )

            upper_F2 = (
                F2[k]
                + BW2[k] / 2
            )

            E_F2_norm[k] = normalized_band_energy(
                frequency_axis,
                energy_bin,
                lower_F2,
                upper_F2,
                total_frame_energy
            )

        # ========================================================
        # Energía alrededor de F3
        # ========================================================

        if (
            np.isfinite(F3[k])
            and np.isfinite(BW3[k])
        ):

            lower_F3 = (
                F3[k]
                - BW3[k] / 2
            )

            upper_F3 = (
                F3[k]
                + BW3[k] / 2
            )

            E_F3_norm[k] = normalized_band_energy(
                frequency_axis,
                energy_bin,
                lower_F3,
                upper_F3,
                total_frame_energy
            )

    # ============================================================
    # Estadísticas de formantes
    # ============================================================

    feats["F_1"] = np.nanmedian(F1)
    feats["F_2"] = np.nanmedian(F2)
    feats["F_3"] = np.nanmedian(F3)

    feats["std_F_1"] = np.nanstd(F1, ddof=1)
    feats["std_F_2"] = np.nanstd(F2, ddof=1)
    feats["std_F_3"] = np.nanstd(F3, ddof=1)

    # ============================================================
    # Estadísticas de anchos de banda
    # ============================================================

    feats["mean_BW_F_1"] = np.nanmean(BW1)
    feats["mean_BW_F_2"] = np.nanmean(BW2)
    feats["mean_BW_F_3"] = np.nanmean(BW3)

    feats["std_BW_F_1"] = np.nanstd(BW1, ddof=1)
    feats["std_BW_F_2"] = np.nanstd(BW2, ddof=1)
    feats["std_BW_F_3"] = np.nanstd(BW3, ddof=1)

    # ============================================================
    # Estadísticas de energía
    # ============================================================

    feats["mean_E_F0_norm"] = np.nanmean(E_F0_norm)
    feats["mean_E_F1_norm"] = np.nanmean(E_F1_norm)
    feats["mean_E_F2_norm"] = np.nanmean(E_F2_norm)
    feats["mean_E_F3_norm"] = np.nanmean(E_F3_norm)

    feats["std_E_F0_norm"] = np.nanstd(
        E_F0_norm,
        ddof=1
    )

    feats["std_E_F1_norm"] = np.nanstd(
        E_F1_norm,
        ddof=1
    )

    feats["std_E_F2_norm"] = np.nanstd(
        E_F2_norm,
        ddof=1
    )

    feats["std_E_F3_norm"] = np.nanstd(
        E_F3_norm,
        ddof=1
    )

    # ============================================================
    # Energía en porcentaje
    # ============================================================

    feats["mean_E_F0_percent"] = (
        100 * feats["mean_E_F0_norm"]
    )

    feats["mean_E_F1_percent"] = (
        100 * feats["mean_E_F1_norm"]
    )

    feats["mean_E_F2_percent"] = (
        100 * feats["mean_E_F2_norm"]
    )

    feats["mean_E_F3_percent"] = (
        100 * feats["mean_E_F3_norm"]
    )

    # ============================================================
    # Número de frames válidos
    # ============================================================

    feats["number_Valid_E_F0_Frames"] = np.sum(
        np.isfinite(E_F0_norm)
    )

    feats["number_Valid_E_F1_Frames"] = np.sum(
        np.isfinite(E_F1_norm)
    )

    feats["number_Valid_E_F2_Frames"] = np.sum(
        np.isfinite(E_F2_norm)
    )

    feats["number_Valid_E_F3_Frames"] = np.sum(
        np.isfinite(E_F3_norm)
    )

    return feats