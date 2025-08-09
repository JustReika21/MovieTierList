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
    ReviewSerializer,
    CollectionSerializer,
    ReviewTagSerializer,
    ReviewSearchSerializer
)
from review_collections.models import Collection
from reviews.models import Review, ReviewTag
from api.permissions import IsOwner


@extend_schema(tags=['Reviews'])
class ReviewCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=ReviewSerializer,
        responses={
            201: ReviewSerializer,
            400: OpenApiResponse(description='Validation Error')
        },
    )
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Reviews'])
class ReviewUpdateDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated, IsOwner,)

    @extend_schema(
        request=ReviewSerializer,
        responses={
            204: None,
            403: OpenApiResponse(description='Forbidden'),
            404: OpenApiResponse(description='Review not found')
        },
    )
    def delete(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        self.check_object_permissions(request, review)
        review.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @extend_schema(
        request=ReviewSerializer,
        responses={
            200: None,
            400: OpenApiResponse(description='Validation Error'),
            403: OpenApiResponse(description='Forbidden'),
            404: OpenApiResponse(description='Review not found')
        },
    )
    def patch(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        self.check_object_permissions(request, review)
        serializer = ReviewSerializer(
            instance=review,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewSearchAPIView(APIView):
    @extend_schema(
        tags=['Reviews'],
        parameters=[
            OpenApiParameter(name='user_id', required=True, type=int),
            OpenApiParameter(name='query', required=True, type=str),
        ],
        responses={200: ReviewSearchSerializer(many=True)}
    )
    def get(self, request):
        user_id = request.query_params.get('user_id', None)
        query = request.query_params.get('query', 'a')

        if user_id:
            review = Review.objects.filter(
                user=user_id,
                title__icontains=query
            )[:5]
            serializer = ReviewSearchSerializer(review, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Review.objects.none()


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


class ReviewTagGetAPIView(APIView):
    @extend_schema(
        tags=['ReviewTags'],
        parameters=[
            OpenApiParameter(name='query', required=True, type=str),
        ],
        responses={200: ReviewTagSerializer(many=True)}
    )
    def get(self, request):
        query = request.query_params.get('query', 'a')

        tags = ReviewTag.objects.filter(name__icontains=query)[:5]
        serializer = ReviewTagSerializer(tags, many=True)
        return Response(serializer.data)
