from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import ItemSerializer
from items.models import Item


class ItemCreateAPIView(APIView):
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.user = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemDeleteAPIView(APIView):
    def delete(self, request, item_id):
        try:
            item = Item.objects.select_related('user').get(id=item_id)
            if item.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

