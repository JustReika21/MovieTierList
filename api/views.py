from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import (
    ItemSerializer,
    CollectionSerializer,
    ItemTagSerializer,
    ItemSearchSerializer
)
from item_collections.models import Collection
from items.models import Item, ItemTag
from api.permissions import IsOwner


class ItemCreateAPIView(APIView):
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemDeleteAPIView(APIView):
    permission_classes = (IsOwner,)

    def delete(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        self.check_object_permissions(request, item)
        item.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class ItemUpdateAPIView(APIView):
    permission_classes = (IsOwner,)

    def patch(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        self.check_object_permissions(request, item)
        serializer = ItemSerializer(
            instance=item,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemSearchAPIView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id', None)
        query = request.query_params.get('query', 'a')

        if user_id:
            item = Item.objects.filter(
                user=user_id,
                title__icontains=query
            )[:5]
            serializer = ItemSearchSerializer(item, many=True)
            return Response(serializer.data)
        return Item.objects.none()


class CollectionCreateAPIView(APIView):
    def post(self, request):
        serializer = CollectionSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectionDeleteAPIView(APIView):
    permission_classes = (IsOwner,)

    def delete(self, request, collection_id):
        collection = get_object_or_404(Collection, id=collection_id)
        self.check_object_permissions(request, collection)
        collection.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class CollectionUpdateAPIView(APIView):
    permission_classes = (IsOwner,)

    def patch(self, request, collection_id):
        collection = get_object_or_404(Collection, id=collection_id)
        self.check_object_permissions(request, collection)
        serializer = CollectionSerializer(
            instance=collection,
            data=request.data,
            context={'request': request},
            partial=True
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemTagGetAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('query', 'a')

        tags = ItemTag.objects.filter(name__icontains=query)[:5]
        serializer = ItemTagSerializer(tags, many=True)
        return Response(serializer.data)
