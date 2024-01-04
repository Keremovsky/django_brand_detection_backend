from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import User, HistoryModel
from ..serializers import FeedbackSerializer


@api_view(["POST"])
def createFeedback(request, id):
    serializer = FeedbackSerializer(data=request.data)

    # if taken data is valid
    if serializer.is_valid():
        historyId = serializer.validated_data["historyId"]
        description = serializer.validated_data["description"]

        try:
            user = User.objects.get(id=id)
            history = HistoryModel.objects.get(id=historyId)

            # create feedback and save it to the database
            createFeedback(user, history, description)

            return Response({"response": "success"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # if there is no user with given id
            return Response({"response": "no_user"})
        except HistoryModel.DoesNotExist:
            # if there is no history item with given id
            return Response({"response": "no_history"})

    # unknown error
    return Response({"response": "error"})
