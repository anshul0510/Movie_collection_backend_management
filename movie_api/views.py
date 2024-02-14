import requests
from requests.exceptions import HTTPError
from .utils import get_credentials
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken  
from rest_framework.decorators import api_view, permission_classes, authentication_classes  
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication  
from .serializers import CollectionSerializer
from .models import Collection, Movie
from django.core.cache import cache


'''api for listing movies created with the use of os and not hardcoded'''


def movie_list(request):
    url = 'https://demo.credy.in/api/v1/maya/movies/'
    username, password = get_credentials()

    try:
        response = requests.get(url, auth=(username, password), verify=False)  # Disable SSL verification
        response.raise_for_status()

        data = response.json().get('results', [])
        movies = []
        for movie_data in data:
            movies.append({
                'title': movie_data['title'],
                'description': movie_data['description'],
                'genres': movie_data.get('genres', ''),
                'uuid': movie_data['uuid'],
            })

        return JsonResponse(movies, safe=False)
    except HTTPError as e:
        return JsonResponse({'error': str(e)}, status=500)


'''api for user registration'''

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)

    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)


'''API for user login'''
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_collection(request):
    if request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            collection = serializer.save()
            return Response({'collection_uuid': collection.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_collections(request):
    if request.method == 'GET':
        collections = Collection.objects.all()
        serialized_collections = CollectionSerializer(collections, many=True).data
        
        all_movies = Movie.objects.all()
        genre_counts = {}
        for movie in all_movies:
            genres = movie.genres.split(',') if movie.genres else []
            for genre in genres:
                genre_counts[genre.strip()] = genre_counts.get(genre.strip(), 0) + 1
        
        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        top_3_genres = ', '.join([genre for genre, _ in sorted_genres])
        
        response_data = {
            'collections': serialized_collections,
            'favourite_genres': top_3_genres
        }
        return Response({'is_success': True, 'data': response_data}, status=status.HTTP_200_OK)
    
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_collection(request, collection_uuid):
    try:
        collection = Collection.objects.get(uuid=collection_uuid)
    except Collection.DoesNotExist:
        return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CollectionSerializer(collection, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def retrieve_collection(request, collection_uuid):
    try:
        collection = Collection.objects.get(uuid=collection_uuid)
    except Collection.DoesNotExist:
        return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CollectionSerializer(collection)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_collection(request, collection_uuid):
    try:
        collection = Collection.objects.get(uuid=collection_uuid)
    except Collection.DoesNotExist:
        return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

    collection.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def request_count(request):
    count = cache.get('request_count') or 0
    return Response({'requests': count})

@api_view(['POST'])
def reset_request_count(request):
    cache.set('request_count', 0)
    return Response({'message': 'request count reset successfully'})