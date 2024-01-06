from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
import base64
from ..models import User
from ..utils.utils import saveHistory, getVectorWithHug
from ..utils.vector_database_client import VectorDatabaseClient
from secret import HF_TOKEN, ENDPOINT_URL

# initialize client
client = VectorDatabaseClient(
    collectionName="brand_collection",
    size=1024,
    alwaysRam=False,
)
# model = PreTrainedPipeline(path="blip_image_embeddings/")


@api_view(["POST"])
@parser_classes([MultiPartParser])
def search(request, id):
    try:
        image = request.data.get("image")
        if image:
            imageContent = image.read()

            # embed image and get vector
            b64Image = base64.b64encode(imageContent).decode("utf-8")
            vector = getVectorWithHug(b64Image)
            # search for image
            results = client.search(vector.json(), 5)

            if results[0] == True:
                # control if user is authenticated
                try:
                    user = User.objects.get(id=id)
                    saveHistory(user, imageContent, [data["id"] for data in results[1]])
                except User.DoesNotExist:
                    pass

                return Response({"results": results[1]}, status=status.HTTP_200_OK)
            else:
                return Response({"response": "search_error"})
        else:
            # if there is a problem about image
            return Response({"response": "image_error"})
    except:
        # unknown error
        return Response({"response": "error"})
