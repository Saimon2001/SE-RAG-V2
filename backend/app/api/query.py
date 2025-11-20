from fastapi import APIRouter, Request
from weaviate.classes.query import Filter, Sort
from app.models.query_models import QueryWithFilter, QueryNoFilter, NaturalQuery
from app.api.llm_utils import query_ollama_llm

router = APIRouter()

@router.post("/queryFilter")
def query_filter(request: Request, body: QueryWithFilter):
    docs = request.app.state.docs
    try:
        gen = docs.generate.near_text(
            query=body.Query,
            limit=5,
            grouped_task=body.GroupedTask,
            filters=Filter.by_property("string_project").equal(body.Filtro)
        )
        return {"response": gen.generative.text}
    except Exception as e:
        return {"error": str(e)}

@router.post("/query")
def query_no_filter(request: Request, body: QueryNoFilter):
    docs = request.app.state.docs
    try:
        gen = docs.generate.near_text(
            query=body.Query,
            limit=5,
            grouped_task=body.GroupedTask
        )
        return {"response": gen.generative.text}
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/projectDuration")
def query_no_filter(request: Request):
    docs = request.app.state.docs
    try:
        response = docs.query.fetch_objects(
            sort=Sort.by_property(name="projectDuration", ascending=False),
            limit=5
        )
        lista = []
        for i, o in enumerate(response.objects, start=1):
            duration = o.properties["projectDuration"]
            lista.append(f"{i}. {duration}")
            
        return {"top_project_durations": lista}
    except Exception as e:
        return {"error": str(e)}

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


@router.post("/queryNatural")
def query_from_natural(request: Request, body: NaturalQuery):
    prompt = PROMPT_TEMPLATE.format(user_input=body.question)

    try:
        parsed = query_ollama_llm(prompt=prompt, model="llama32")
        docs = request.app.state.docs

        gen = docs.generate.near_text(
            query=parsed["query"],
            limit=5,
            grouped_task=parsed["grouped_task"],
            filters=Filter.by_property("string_project").equal(parsed["filter"])
        )

        return {"response": gen.generative.text}

    except Exception as e:
        return {"error": str(e)}
