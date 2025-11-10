from fastapi import APIRouter, Request
from weaviate.classes.query import Filter, Sort
from app.models.query_models import QueryWithFilter, QueryNoFilter

router = APIRouter()

@router.post("/queryFilter")
def query_filter(request: Request, body: QueryWithFilter):
    docs = request.app.state.docs
    try:
        gen = docs.generate.near_text(
            query=body.Query,
            limit=2,
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
            limit=2,
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