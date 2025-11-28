from fastapi import FastAPI
from contextlib import asynccontextmanager
import weaviate
from weaviate.classes.init import AdditionalConfig, Timeout

#Define the lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    config = AdditionalConfig(
        timeout=Timeout(init=30, query=120, insert=120)
    )
    client = weaviate.connect_to_custom(
        http_host="localhost",
        http_port=8082,
        http_secure=False,
        grpc_host="localhost",
        grpc_port=50051,
        grpc_secure=False,
        additional_config=config
    )
    docs = client.collections.get("ProjectSE")
    app.state.weaviate_client = client
    app.state.docs = docs
    print("Weaviate client connected.")
    yield  #Control goes to the app here
    #Teardown phase
    client.close()
    print("Weaviate client closed.")

#Initialize the app with lifespan
app = FastAPI(lifespan=lifespan)
app.title = "Vector Database for Microsoft Project"

#routers
from app.api.query import router as query_router
app.include_router(query_router, prefix="/api")