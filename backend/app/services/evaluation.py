import json

import openai

from app.config import settings

# gpt-4o-mini: ~$0.00015/1K tokens input. Para ~300 palabras de transcript = <$0.001/evaluación
# vs gpt-4o: 33x más caro sin mejora significativa para análisis de conversación corta
_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

CRITERIA = [
    {
        "id": 1,
        "name": "Apertura y rapport",
        "description": "¿El vendedor saluda correctamente, se presenta y genera confianza inicial con el cliente?",
    },
    {
        "id": 2,
        "name": "Identificación de necesidad",
        "description": "¿El vendedor hace preguntas abiertas y escucha activamente para entender qué necesita el cliente?",
    },
    {
        "id": 3,
        "name": "Presentación del producto",
        "description": "¿El vendedor menciona beneficios relevantes y alineados con la necesidad identificada del cliente?",
    },
    {
        "id": 4,
        "name": "Manejo de objeciones",
        "description": "¿El vendedor responde las dudas o rechazos del cliente con empatía y argumentos concretos?",
    },
    {
        "id": 5,
        "name": "Cierre",
        "description": "¿El vendedor propone un siguiente paso claro (reunión, demo, compra) antes de terminar la llamada?",
    },
]

# El prompt pide JSON estricto para evitar parsing frágil de texto libre
_SYSTEM_PROMPT = """Eres un evaluador experto en conversaciones de venta en español latinoamericano.
La transcripción está en formato dialogado con etiquetas VENDEDOR y CLIENTE.
Evalúa ÚNICAMENTE las intervenciones del VENDEDOR contra la rúbrica comercial.
El CLIENTE puede poner objeciones — evalúa cómo el VENDEDOR las maneja en el criterio de Manejo de Objeciones.
Responde ÚNICAMENTE con un JSON válido, sin texto adicional."""

_USER_PROMPT_TEMPLATE = """Transcripción de la llamada de venta (formato dialogado):
---
{transcript}
---

Analiza SOLO las intervenciones del VENDEDOR y evalúa según estos 5 criterios.
Para cada uno, asigna un puntaje entero de 0 a 10 y escribe un feedback conciso (máximo 2 oraciones) en español.
Usa las respuestas del CLIENTE únicamente como contexto para evaluar al VENDEDOR.

Criterios:
{criteria_list}

Responde con este JSON exacto:
{{
  "results": [
    {{"criterion_id": 1, "score": <0-10>, "feedback": "<texto>"}},
    {{"criterion_id": 2, "score": <0-10>, "feedback": "<texto>"}},
    {{"criterion_id": 3, "score": <0-10>, "feedback": "<texto>"}},
    {{"criterion_id": 4, "score": <0-10>, "feedback": "<texto>"}},
    {{"criterion_id": 5, "score": <0-10>, "feedback": "<texto>"}}
  ]
}}"""


async def evaluate_transcript(transcript: str) -> list[dict]:
    criteria_list = "\n".join(
        f"{c['id']}. {c['name']}: {c['description']}" for c in CRITERIA
    )
    user_prompt = _USER_PROMPT_TEMPLATE.format(
        transcript=transcript,
        criteria_list=criteria_list,
    )

    response = await _client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    data = json.loads(raw)

    results = data.get("results", [])
    if len(results) != 5:
        raise ValueError(f"El LLM devolvió {len(results)} resultados en lugar de 5")

    # Enriquecer cada resultado con los datos del criterio para guardar en DB
    criterion_map = {c["id"]: c for c in CRITERIA}
    for r in results:
        cid = r["criterion_id"]
        r["criterion_name"] = criterion_map[cid]["name"]
        r["criterion_description"] = criterion_map[cid]["description"]
        r["score"] = float(r["score"])

    return results
