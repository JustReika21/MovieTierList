from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse
)

from api.serializers import (
    ItemSerializer,
    CollectionSerializer,
    ItemTagSerializer,
    ItemSearchSerializer
)
from item_collections.models import Collection
from items.models import Item, ItemTag
from api.permissions import IsOwner


@extend_schema(tags=['Items'])
class ItemCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=['Items'],
        request=ItemSerializer,
        responses={
            201: ItemSerializer,
            400: OpenApiResponse(description='Validation Error')
        },
    )
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Items'])
class ItemUpdateDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated, IsOwner,)

    @extend_schema(
        tags=['Items'],
        request=ItemSerializer,
        responses={
            204: None,
            403: OpenApiResponse(description='Forbidden'),
            404: OpenApiResponse(description='Item not found')
        },
    )
    def delete(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        self.check_object_permissions(request, item)
        item.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @extend_schema(
        request=ItemSerializer,
        responses={
            200: None,
            400: OpenApiResponse(description='Validation Error'),
            403: OpenApiResponse(description='Forbidden'),
            404: OpenApiResponse(description='Item not found')
        },
    )
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
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemSearchAPIView(APIView):
    @extend_schema(
        tags=['Items'],
        parameters=[
            OpenApiParameter(name='user_id', required=True, type=int),
            OpenApiParameter(name='query', required=True, type=str),
        ],
        responses={200: ItemSearchSerializer(many=True)}
    )
    def get(self, request):
        user_id = request.query_params.get('user_id', None)
        query = request.query_params.get('query', 'a')

        if user_id:
            item = Item.objects.filter(
                user=user_id,
                title__icontains=query
            )[:5]
            serializer = ItemSearchSerializer(item, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Item.objects.none()


class CollectionCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=['Collections'],
        request=CollectionSerializer,
        responses={
            201: CollectionSerializer,
            400: OpenApiResponse(description='Validation Error'),
        }
    )
    def post(self, request):
        serializer = CollectionSerializer(
            data=request.data,
            context={'request': request}
        )
        self.check_object_permissions(request, request.user)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectionDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated, IsOwner,)

    @extend_schema(
        tags=['Collections'],
        request=CollectionSerializer,
        responses={
            204: None,
            403: OpenApiResponse(description='Forbidden'),
            404: OpenApiResponse(description='Collection not found')
        },
    )
    def delete(self, request, collection_id):
        collection = get_object_or_404(Collection, id=collection_id)
        self.check_object_permissions(request, collection)
        collection.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class CollectionUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsOwner,)

    @extend_schema(
        tags=['Collections'],
        request=CollectionSerializer,
        responses={
            204: None,
            400: OpenApiResponse(description='Validation Error'),
            403: OpenApiResponse(description='Forbidden'),
            404: OpenApiResponse(description='Collection not found')
        },
    )
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
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemTagGetAPIView(APIView):
    @extend_schema(
        tags=['ItemTags'],
        parameters=[
            OpenApiParameter(name='query', required=True, type=str),
        ],
        responses={200: ItemTagSerializer(many=True)}
    )
    def get(self, request):
        query = request.query_params.get('query', 'a')

        tags = ItemTag.objects.filter(name__icontains=query)[:5]
        serializer = ItemTagSerializer(tags, many=True)
        return Response(serializer.data)
