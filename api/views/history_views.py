from qdrant_client import QdrantClient
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import HistoryIdSerializer, HistorySerializer
from ..models import User, HistoryModel
from ..utils.vector_database_client import VectorDatabaseClient
from ..utils.utils import formatHistory

# initialize client
client = VectorDatabaseClient(
    collectionName="brand_collection",
    size=1024,
    alwaysRam=False,
)


@api_view(["GET"])
def getAllHistory(request, id):
    try:
        user = User.objects.get(id=id)
        allHistory = HistoryModel.objects.filter(user=user)

        histories = []
        # iterate all histories
        for history in allHistory:
            # get result ids and get company data from qdrant
            resultIds = history.getResultIds()
            results = client.getVectorsWithId(ids=resultIds)
            # if process was success
            if results[0] == True:
                finalResult = formatHistory(history, results[1])

                histories.append(finalResult)
            else:
                return Response({"response": "history_error"})

        return Response({"histories": histories})
    except User.DoesNotExist:
        # if there is no user with given id
        return Response({"response": "no_user"})
    except HistoryModel.DoesNotExist:
        # if there is no history item with given id
        return Response({"response": "no_history"})
    except Exception as e:
        # unknown error
        return Response({"response": "error"})


@api_view(["DELETE"])
def deleteHistory(request, id):
    serializer = HistoryIdSerializer(request.data)

    if serializer.is_valid():
        try:
            user = User.objects.get(id=id)

            historyId = serializer.validated_data["id"]
            history = HistoryModel.objects.get(id=historyId)

            # control if user that request delete is the user that owns history item
            if history.user != user:
                return Response({"response": "no_access"})

            history.delete()

            return Response({"response": "success"})
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


@api_view(["PUT"])
def handleSaveHistory(request, id):
    serializer = HistoryIdSerializer(request.data)

    if serializer.is_valid():
        try:
            user = User.objects.get(id=id)

            historyId = serializer.validated_data["id"]
            history = HistoryModel.objects.get(id=historyId)

            # control if user that request delete is the user that owns history item
            if history.user != user:
                return Response({"response": "no_access"})

            history.isSaved = not history.isSaved
            history.save()

            return Response({"response": "success"})
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
