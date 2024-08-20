
from rest_framework import generics, permissions

from .models import Article
from .serializers import ArticleSerializer


# Create your views here.

class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    http_method_names = ['get']
    permission_classes = [permissions.AllowAny]


class ArticleCreateView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    http_method_names = ['post']
    permission_classes = [permissions.AllowAny]
