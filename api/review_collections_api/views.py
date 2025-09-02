from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse
)

from api.review_collections_api.serializers import (
    CollectionSerializer
)

from review_collections.models import Collection
from api.permissions import IsOwner


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


@extend_schema(tags=['Collections'])
class CollectionUpdateDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated, IsOwner,)

    @extend_schema(
        request=CollectionSerializer,
        responses={
            200: CollectionSerializer,
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
            if not request.data.get('reviews', None):
                serializer.save(user=request.user, reviews=[])
            else:
                serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
