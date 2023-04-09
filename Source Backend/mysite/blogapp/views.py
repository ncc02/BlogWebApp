from rest_framework import viewsets
from .models import User, Article, Comments
from .serializers import UserPasswordUpdateSerializer, UserSerializer, ArticleSerializer
from .serializers import CommentsSerializer, SearchUserSerializer, SearchArticleSerializer, UserUpdateSerializer

from rest_framework.response import Response

from rest_framework.views import APIView, status
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password

from rest_framework import generics, permissions

# Viewsets for User model
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Viewsets for Article model
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# Viewsets for Comments model
class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            user = serializer.save()
            
            return JsonResponse({
                'message': 'Register successful!'
            }, status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({
                'error_message': 'error',
                'errors_code': 400,
            }, status=status.HTTP_400_BAD_REQUEST)


class SearchView(APIView):
    def get(self, request):
        text_search = request.GET.get('text_search', '').strip()
        users = User.objects.filter(fullname__icontains=text_search)[:10]
        articles = Article.objects.filter(title__icontains=text_search)[:10-len(users)]
        user_serializer = SearchUserSerializer(users, many=True)
        article_serializer = SearchArticleSerializer(articles, many=True)
        data = user_serializer.data + article_serializer.data
        return Response({'data': data})


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class UserPasswordUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPasswordUpdateSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        oldpassword = request.data.get('oldpassword')
        newpassword = make_password(request.data.get('password'))
        if check_password(oldpassword, instance.password):
            instance.password = newpassword
            instance.save(update_fields=['password'])
            serializer = self.get_serializer(instance)
            return Response({'message': 'Password Changed'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Incorrect Old Password'}, status=status.HTTP_400_BAD_REQUEST)