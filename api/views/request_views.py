from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import User, RequestModel
from ..serializers import RequestSerializer
from ..utils import saveRequest


@api_view(["POST"])
def createRequest(request, id):
    serializer = RequestSerializer(data=request.data)

    # if taken data is valid
    if serializer.is_valid():
        try:
            user = User.objects.get(id=id)

            # create request and save it to the database
            saveRequest(user, serializer.validated_data)

            return Response({"response": "success"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"response": "no_user"})

    # unknown error
    return Response({"response": "error"})


@api_view(["GET"])
def getAllRequest(request, id):
    try:
        # get user's requests
        user = User.objects.get(id=id)
        requests = RequestModel.objects.filter(user=user)

        if not requests.exists():
            # if there is no request with given id
            return Response({"response": "no_request"})

        serializer = RequestSerializer(requests, many=True)

        return Response(serializer.data)
    except User.DoesNotExist:
        # if there is no user with given id
        return Response({"response": "no_user"})
    except:
        # unknown error
        return Response({"response": "error"})