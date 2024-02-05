from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import BlogPost, Comment
from .serializers import BlogPostSerializer, CommentSerializer
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from .serializers import BlogPostSerializer 
from rest_framework import status
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import *
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import json
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from signup.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist


# @method_decorator(csrf_exempt, name='dispatch')
class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            print("Received headers:", request.user)
            data = json.loads(request.body)

            # author_id = request.data.get('author') 
            author = CustomUser.objects.get(pk=request.user.id)
            print(author)
            data['author'] = author.id
            print(data)

            serializer = BlogPostSerializer(data=data, context={'user':author})  
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception:", str(e))
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RetrievePostsView(APIView):
    def get(self, request):
        try:
            posts = BlogPost.objects.all()
            serializer = BlogPostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception:", str(e))
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdatePostView(APIView):
    def put(self, request, post_id):
        try:
            post = BlogPost.objects.get(pk=post_id)
            data = request.data

            serializer = BlogPostSerializer(instance=post, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Exception:", str(e))
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeletePostView(APIView):
    def delete(self, request, post_id):
        try:
            post = BlogPost.objects.get(pk=post_id)
            post.delete()
            return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Exception:", str(e))
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['POST'])
# def add_comment(request, pk):
#     try:
#         post = get_object_or_404(BlogPost, pk=pk)
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(post=post, user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# def get_comments(request, pk):
#     post = get_object_or_404(BlogPost, pk=pk)
#     comments = Comment.objects.filter(post=post)
#     serializer = CommentSerializer(comments, many=True)
#     return Response(serializer.data)

class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = get_object_or_404(BlogPost, pk=post_id)
            print(post)
            print("Received headers:", request.headers)
            data = json.loads(request.body)
            user = request.user.id
            # print(data)
            custom_user = CustomUser.objects.get(id=user)
            print(user)
            
            data['post'] = post.id
            data['user'] = custom_user.id
            print(data)

            serializer = CommentSerializer(data=data, context={'user': user, 'post': post})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception:", str(e))
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
