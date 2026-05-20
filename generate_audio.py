"""
Generador de audios de prueba para Mic&Pose Evaluator
Genera 2 conversaciones (mal y buen vendedor) usando ElevenLabs Text to Dialogue API

Uso:
    pip install elevenlabs
    export ELEVENLABS_API_KEY=tu_key
    python generate_audio.py
"""

import os
from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

# Voces de la librería pública de ElevenLabs (español colombiano)
# Puedes cambiar estos IDs por cualquier voz de tu biblioteca
# Búscalas en: https://elevenlabs.io/app/voice-library
VENDEDOR_VOICE_ID = "pqHfZKP75CvOlQylNhV4"  # Bill - voz masculina neutra
CLIENTE_VOICE_ID  = "onwK4e9ZLuTAKqWW03F9"  # Daniel - voz masculina diferente

# ─── Libreto 1: MAL VENDEDOR ─────────────────────────────────────────────────

dialogo_mal_vendedor = [
    {"text": "[direct] Aló, buenas. Mire le llamo de Claro, tenemos un plan de 40 gigas por 45 mil. ¿Le interesa?", "voice_id": VENDEDOR_VOICE_ID},
    {"text": "[hesitant] Mmm, no sé, yo ya tengo plan.", "voice_id": CLIENTE_VOICE_ID},
    {"text": "Sí pero este es mejor. 40 gigas, llamadas ilimitadas, todo incluido.", "voice_id": VENDEDOR_VOICE_ID},
    {"text": "[curious] ¿Y cuánto vale exactamente?", "voice_id": CLIENTE_VOICE_ID},
    {"text": "45 mil pesos mensuales. Es una muy buena oferta, la verdad.", "voice_id": VENDEDOR_VOICE_ID},
    {"text": "[skeptical] Es que me parece caro, yo pago menos ahorita.", "voice_id": CLIENTE_VOICE_ID},
    {"text": "No, es que este plan incluye todo. Vale la pena.", "voice_id": VENDEDOR_VOICE_ID},
    {"text": "[doubtful] ¿Y si el servicio no me funciona bien?", "voice_id": CLIENTE_VOICE_ID},
    {"text": "No, Claro funciona bien en todas partes. No se preocupe por eso.", "voice_id": VENDEDOR_VOICE_ID},
    {"text": "Déjeme pensarlo mejor.", "voice_id": CLIENTE_VOICE_ID},
    {"text": "[urgent] Es que la oferta vence hoy. Si no se decide ahorita la perdemos.", "voice_id": VENDEDOR_VOICE_ID},
    {"text": "[firm] No, gracias, ahorita no.", "voice_id": CLIENTE_VOICE_ID},
    {"text": "[defeated] Bueno, ¿entonces le llamo mañana?", "voice_id": VENDEDOR_VOICE_ID},
    {"text": "No, no hace falta. Que esté bien.", "voice_id": CLIENTE_VOICE_ID},
    {"text": "[flat] Ah bueno. Chao.", "voice_id": VENDEDOR_VOICE_ID},
]

# ─── Libreto 2: BUEN VENDEDOR ─────────────────────────────────────────────────

dialogo_buen_vendedor = [
    {"text": "[warm, professional] Buenas tardes, con mucho gusto, habla Sofía, asesora comercial de Claro. ¿Me comunico con don Carlos?", "voice_id": VENDEDOR_VOICE_ID},
    {"text": "Sí, con él.", "voice_id": CLIENTE_VOICE_ID},
    {"text": "[friendly] Don Carlos, qué gusto. Mire, le llamo porque tenemos una oferta especial esta semana. Pero antes de contarle, ¿me permite preguntarle con qué operador está actualmente y cómo le ha ido con el servicio?", "voice_id": VENDEDOR_VOICE_ID},
    {"text": "[neutral] Estoy con Movistar, más o menos, a veces el internet se pone lento.", "voice_id": CLIENTE_VOICE_ID},
    {"text": "[interested] Entiendo. ¿Y cuántos gigas tiene en su plan actual?", "voice_id": VENDEDOR_VOICE_ID},
    {"text": "[uncertain] Creo que 15, pero se me acaban antes de que termine el mes.", "voice_id": CLIENTE_VOICE_ID},
    {"text": "[empathetic] Eso es muy común, don Carlos. Lo que tenemos para usted es un plan de 40 gigas mensuales, con llamadas ilimitadas a cualquier operador, y si se le acaban los gigas la velocidad baja pero no le cobramos nada adicional. Todo por 45 mil pesos al mes.", "voice_id": VENDEDOR_VOICE_ID},
    {"text": "[skeptical] Uy, eso me parece caro. Yo pago menos ahorita.", "voice_id": CLIENTE_VOICE_ID},
    {"text": "Entiendo que parece más al principio. Cuénteme, cuando se le acaban los 15 gigas, ¿recarga datos adicionales?", "voice_id": VENDEDOR_VOICE_ID},
    {"text": "[reluctant] Sí, a veces recargo como 10 mil pesos.", "voice_id": CLIENTE_VOICE_ID},
    {"text": "[confident] Ahí está — su plan actual más las recargas ya lo tienen cerca de los 45 mil, pero sin la tranquilidad de tener gigas todo el mes. Con nosotros eso no pasa.", "voice_id": VENDEDOR_VOICE_ID},
    {"text": "[resistant] Sí pero cambiar de operador es complicado, lo del número y eso.", "voice_id": CLIENTE_VOICE_ID},
    {"text": "Para eso estamos nosotros, don Carlos. La portación la gestionamos completamente, usted conserva su mismo número y en menos de 24 horas está activo, sin costo de activación.", "voice_id": VENDEDOR_VOICE_ID},
    {"text": "[still doubtful] ¿Y si la señal no me funciona bien en mi zona?", "voice_id": CLIENTE_VOICE_ID},
    {"text": "[calm] Válida pregunta. ¿En qué sector está ubicado?", "voice_id": VENDEDOR_VOICE_ID},
    {"text": "En Chapinero, Bogotá.", "voice_id": CLIENTE_VOICE_ID},
    {"text": "[reassuring] Perfecto, Chapinero tiene cobertura 4G y 5G con Claro. Y le doy 15 días de prueba — si en ese tiempo no está satisfecho, cancelamos sin ningún cobro y vuelve a su operador actual sin problema.", "voice_id": VENDEDOR_VOICE_ID},
    {"text": "[warming up] Bueno... eso suena razonable.", "voice_id": CLIENTE_VOICE_ID},
    {"text": "[closing, confident] Entonces le propongo esto: le envío el link de activación ahora a su WhatsApp, lo revisa tranquilo, y si tiene alguna duda me escribe directamente. ¿Le parece bien?", "voice_id": VENDEDOR_VOICE_ID},
    {"text": "[agreeing] Listo, mándelo.", "voice_id": CLIENTE_VOICE_ID},
    {"text": "[warm] Perfecto don Carlos, ya le llega. Que tenga muy buena tarde.", "voice_id": VENDEDOR_VOICE_ID},
]


def generar_audio(dialogo: list[dict], nombre_archivo: str):
    print(f"⏳ Generando {nombre_archivo}...")

    audio = client.text_to_dialogue.convert(
        model_id="eleven_v3",
        inputs=dialogo,          # 👈 era "dialogue", es "inputs"
    )

    with open(nombre_archivo, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    print(f"✅ Guardado: {nombre_archivo}")


if __name__ == "__main__":
    generar_audio(dialogo_mal_vendedor,  "audio_mal_vendedor.mp3")
    generar_audio(dialogo_buen_vendedor, "audio_buen_vendedor.mp3")
    print("\n🎙️ Listo — sube los dos .mp3 al evaluador para probar.")