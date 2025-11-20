from llm_utils import query_ollama_llm
PROMPT_TEMPLATE = """
Eres un asistente que transforma preguntas en lenguaje natural en instrucciones estructuradas para un sistema de búsqueda semántica (vectorial).

Dada la siguiente pregunta del usuario, devuelve únicamente un objeto JSON con las siguientes claves:
- "query": una frase breve que se utilizará para la búsqueda semántica por similitud.
- "grouped_task": una tarea que el sistema debe realizar sobre los resultados encontrados (por ejemplo: resumir, listar nombres, etc.).
- "filter": el nombre exacto del proyecto mencionado, propietario o director del proyecto, si se hace referencia a alguno.

No incluyas explicaciones ni comentarios adicionales. Devuelve solo el JSON, correctamente formateado.

Ejemplo de entrada:
"¿Qué proyectos relacionados con salud pública ya fueron completados al 100%?"

Ejemplo de salida:
{{
  "query": "proyectos de salud pública porcentaje completado",
  "grouped_task": "Muestra una lista de los nombres de los proyectos completados relacionados con salud pública",
  "filter": "Salud Pública"
}}

Ahora procesa esta pregunta: "{user_input}"
"""

query = 'resumen ejecutivo del proyecto GatesMRI_Implementación'

prompt = PROMPT_TEMPLATE.format(user_input=query)

parsed = query_ollama_llm(prompt=prompt, model="llama32")

print(parsed)