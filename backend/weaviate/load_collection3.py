import weaviate
import json

client = weaviate.connect_to_custom(
    http_host="localhost",
    http_port=8082,
    http_secure=False,
    grpc_host="localhost",
    grpc_port=50051,
    grpc_secure=False
)

with open("proj_data3.json", "r", encoding="utf-8") as f:
    data = json.load(f)

projects = client.collections.get("ProjectSE")

with projects.batch.fixed_size(batch_size=200) as batch:
    for d in data:
        batch.add_object(
            {
                "string_project": d["string_project"],
                "ProjectDuration": d["ProjectDuration"],
                "Propietario": d["Propietario"],
                "ProjectPercentCompleted": d["ProjectPercentCompleted"],
                "ProjectStartDate": d["ProjectStartDate"],
                "ProjectFinishDate": d["ProjectFinishDate"],
                "ProjectCost": d["ProjectCost"],
            },
            uuid=d["ProjectId"],
        )
        if batch.number_errors > 10:
            print("Batch import stopped due to excessive errors.")
            break

failed_objects = projects.batch.failed_objects
if failed_objects:
    print(f"Number of failed imports: {len(failed_objects)}")
    print(f"First failed object: {failed_objects[0]}")

client.close()  # Free up resources