# -*- coding: utf-8 -*-
from rest_framework import generics, permissions
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Article
from .serializers import ArticleSerializer
from webauthn.utils import is_authenticated

class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    http_method_names = ['get']
    permission_classes = [permissions.AllowAny]


class ArticleCreateView(LoginRequiredMixin, generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    http_method_names = ['post']
    permission_classes = [permissions.AllowAny]

@is_authenticated
def createarticle(request):
    pass