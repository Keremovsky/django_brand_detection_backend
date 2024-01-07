from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    PointStruct,
    ScalarQuantization,
    ScalarQuantizationConfig,
    ScalarType,
    ScoredPoint,
    Record,
)


def formatScoredPoint(points: List[ScoredPoint]):
    formattedData = []
    for point in points:
        data = {
            "id": point.id,
            "name": point.payload["name"],
            "location": point.payload["location"],
            "description": point.payload["description"],
            "web": point.payload["url"],
            "twitter": point.payload["twitter_url"],
            "image": f"/media/logo/{point.payload['file_name']}",
            "similarity": ((point.score + 1) * 50),
        }
        formattedData.append(data)
    return formattedData


def formatRecord(records: List[Record]):
    formattedData = []
    for record in records:
        data = {
            "id": record.id,
            "name": record.payload["name"],
            "location": record.payload["location"],
            "description": record.payload["description"],
            "web": record.payload["url"],
            "twitter": record.payload["twitter_url"],
            "image": f"/media/logo/{record.payload['file_name']}",
        }

        formattedData.append(data)
    return formattedData


class VectorDatabaseClient:
    def __init__(self, collectionName: str, size: int, alwaysRam: bool):
        self.collection_name = collectionName
        self.client = QdrantClient("localhost", port=6333)

        # get all collections
        createdCollections = self.client.get_collections().collections

        # control if client has a collection with given name
        for collection in createdCollections:
            if collection.name == collectionName:
                return

        # if it doesn't have the collection create one
        self.client.create_collection(
            collection_name=collectionName,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE),
            quantization_config=ScalarQuantization(
                scalar=ScalarQuantizationConfig(
                    type=ScalarType.INT8,
                    quantile=0.99,
                    always_ram=alwaysRam,
                )
            ),
        )

    # add vector to the database
    def addVector(self, id: int, vector: List[float], payload: dict):
        try:
            result = self.client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                limit=1,
            )
            if(result[0].score > 0.96):
                return False

            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=id,
                        vector=vector,
                        payload=payload,
                    )
                ],
            )
            return True
        except:
            return False

    # get all payload data of given ids
    def getVectorsWithId(self, ids: List[int]):
        try:
            result = []
            for i in range(len(ids)):
                vectorData = self.client.retrieve(
                    collection_name=self.collection_name,
                    ids=[ids[i]],
                )
                result.append(vectorData[0])

            data = formatRecord(result)
            return True, data
        except Exception as e:
            return False, str(e)

    # search one vector
    def search(self, vector: List[float], limit: int):
        try:
            result = self.client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                limit=limit,
            )
            data = formatScoredPoint(result)
            return True, data
        except Exception as e:
            print(e)
            return False, str(e)
