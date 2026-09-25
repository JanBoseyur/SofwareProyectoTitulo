
from base_extract_parameters import extraer_parametros_parselmouth

# ================================================================
# MAIN EJECUTABLE
# ================================================================

if __name__ == "__main__":

    audio = "federer_speech.wav"

    resultados = extraer_parametros_parselmouth(
        audio,
        sex_type="auto"
    )
    
    print(f'\n------ Audio: "{audio}" ------\n')

    for nombre, valor in resultados.items():

        print(
            f"{nombre}: {valor}"
        )