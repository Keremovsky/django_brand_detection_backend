from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
import base64
from blip_image_embeddings.pipeline import PreTrainedPipeline
from ..models import User
from ..utils import saveHistory

# client = QdrantClient()
# model = PreTrainedPipeline(path="blip_image_embeddings/")


@api_view(["POST"])
@parser_classes([MultiPartParser])
def search(request, id):
    try:
        image = request.data.get("image")
        if image:
            imageContent = image.read()

            # embed image and get vector
            # b64Image = base64.b64encode(imageContent).decode("utf-8")
            # result = model.__call__(data={"inputs": b64Image})
            # vector = result["feature_vector"]
            # print(vector)
            # search for image
            # client.search(vector)

            # control if user is authenticated
            try:
                user = User.objects.get(id=id)
                saveHistory(user, imageContent, [1, 2, 3, 4, 5])
            except User.DoesNotExist:
                pass

            return Response({"response": "success"}, status=status.HTTP_200_OK)
        else:
            # if there is a problem about image
            return Response({"response": "image_error"})
    except:
        # unknown error
        return Response({"response": "error"})
