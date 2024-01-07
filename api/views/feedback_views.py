from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from ..models import User, HistoryModel, FeedbackModel
from ..serializers import FeedbackSerializer
from ..utils.utils import saveFeedback


@api_view(["POST"])
def createFeedback(request, id):
    serializer = FeedbackSerializer(data=request.data)

    # if taken data is valid
    if serializer.is_valid():
        historyId = int(serializer.validated_data["historyId"])
        description = serializer.validated_data["description"]

        try:
            user = User.objects.get(id=id)
            history = HistoryModel.objects.get(id=historyId)

            # create feedback and save it to the database
            saveFeedback(user, history, description)

            # send mail to user email to notify user
            title = "Geri Bildirim"
            message = "Geri bildiriminiz tarafımıza ulaştırıldı, en yakın zamanda incelenerek işleme alınacaktır."
            from_email = settings.EMAIL_HOST_USER
            sent_to = [user.email]
            send_mail(
                title,
                message,
                from_email,
                sent_to,
                fail_silently=False,
            )
            return Response({"response": "success"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # if there is no user with given id
            return Response({"response": "no_user"})
        except HistoryModel.DoesNotExist:
            # if there is no history item with given id
            return Response({"response": "no_history"})
        except:
            # unknown error
            return Response({"response": "error"})

    # unknown error
    return Response({"response": "error"})


@api_view(["GET"])
def getAllFeedback(request, id):
    try:
        # get user's feedbacks
        user = User.objects.get(id=id)
        feedbackModels = FeedbackModel.objects.filter(user=user)

        if not feedbackModels.exists():
            # if there is no feedback with given id
            return Response({"response": "no_feedback"})

        print(feedbackModels)
        # get all histories that has feedback
        feedbacks = []
        for feedback in feedbackModels:
            history = feedback.history
            description = feedback.description
            feedbacks.append(
                {
                    "id": feedback.id,
                    "historyId": history.id,
                    "image": history.image.url,
                    "date": feedback.date.strftime("%d/%m/%Y"),
                    "description": description,
                }
            )
        return JsonResponse({"feedbacks": feedbacks})
    except User.DoesNotExist:
        # if there is no user with given id
        return Response({"response": "no_user"})
    except:
        # unknown error
        return Response({"response": "error"})
