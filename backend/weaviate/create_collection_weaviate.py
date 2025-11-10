import weaviate
from weaviate.classes.config import Configure, Property, DataType

client = weaviate.connect_to_custom(
    http_host="localhost",
    http_port=8082,
    http_secure=False,
    grpc_host="localhost",
    grpc_port=50051,
    grpc_secure=False
)

projectDB = client.collections.create(
    name="Project",
    properties=[
        Property(name="string_project", data_type=DataType.TEXT),
        Property(name="Propietario", data_type=DataType.TEXT),
        Property(name="ProjectDuration", data_type=DataType.INT),
    ],
    vector_config=Configure.Vectors.text2vec_ollama(
        api_endpoint="http://host.docker.internal:11434",
        model="nomic-embed-text",
    ),
    generative_config=Configure.Generative.ollama(
        api_endpoint="http://host.docker.internal:11434",
        model="llama3.2",
    )
)

client.close()
