from pydantic import BaseModel

class QueryBase(BaseModel):
    Query: str
    GroupedTask: str

class QueryWithFilter(QueryBase):
    Filtro: str

class QueryNoFilter(QueryBase):
    pass

class NaturalQuery(BaseModel):
    question: str