from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from ..models import User, RequestModel
from ..serializers import OutputRequestSerializer, InputRequestSerializer
from ..utils.utils import saveRequest


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def createRequest(request, id):
    serializer = InputRequestSerializer(data=request.data)

    # if taken data is valid
    if serializer.is_valid():
        try:
            user = User.objects.get(id=id)

            # create request and save it to the database
            saveRequest(user, serializer.validated_data)

            # send mail to user email to notify user
            title = "İstek Oluşturuldu"
            message = "İsteğiniz başarıyla oluşturuldu, en yakın zamanda incelenerek işleme alınacaktır."
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
            return Response({"response": "no_user"})
        except:
            # unknown error
            return Response({"response": "error"})

    # unknown error
    return Response({"response": "error"})


@api_view(["GET"])
def getAllRequest(request, id):
    try:
        # get user's requests
        user = User.objects.get(id=id)
        requests = RequestModel.objects.filter(user=user)

        if not requests.exists():
            # if there is no request for given user
            return Response({"response": "no_request"})

        serializer = OutputRequestSerializer(requests, many=True)

        return JsonResponse({"requests": serializer.data})
    except User.DoesNotExist:
        # if there is no user with given id
        return Response({"response": "no_user"})
    except:
        # unknown error
        return Response({"response": "error"})
