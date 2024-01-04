from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import User, HistoryModel, FeedbackModel
from ..serializers import FeedbackSerializer
from ..utils import saveFeedback


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
            saveFeedback(user, history, description)

            return Response({"response": "success"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # if there is no user with given id
            return Response({"response": "no_user"})
        except HistoryModel.DoesNotExist:
            # if there is no history item with given id
            return Response({"response": "no_history"})

    # unknown error
    return Response({"response": "error"})


@api_view(["GET"])
def getAllFeedback(request, id):
    try:
        # get user's feedbacks
        user = User.objects.get(id=id)
        feedbacks = FeedbackModel.objects.filter(user=user)

        if not feedbacks.exists():
            # if there is no feedback with given id
            return Response({"response": "no_feedback"})

        # get all histories that has feedback
        response = []
        for feedback in feedbacks:
            history = feedback.history
            description = feedback.description
            response.append(
                {
                    "id": history.id,
                    "date": history.date,
                    "image": history.image,
                    "resultIds": history.resultIds,
                    "isSaved": history.isSaved,
                    "description": description,
                }
            )

        return Response(response)
    except User.DoesNotExist:
        # if there is no user with given id
        return Response({"response": "no_user"})
    except:
        # unknown error
        return Response({"response": "error"})
