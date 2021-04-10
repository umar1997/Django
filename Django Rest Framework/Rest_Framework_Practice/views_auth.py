################################################## Settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
################################################ Generic with Permissions Views.py

from .models import Article
from .serializers import ArticleSerializer
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication,TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated



class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id = None):

        if id:
            return self.retrieve(request)

        else:
           return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)

######################################################### Viewset and Routers (Views.py)
# Viewsets And Routers
# A ViewSet class is simply a type of class-based View, that does not provide any method handlers 
# such as .get() or .post(), and instead provides actions such as .list() and .create(). the method 
# handlers for a ViewSet are only bound to the corresponding actions at the point of finalizing the 
# view, using the .as_view() method.
# There are different ways that you can implement viewsets, first way is that you can write your own 
# viewsets. Now we are going to change our views.py.

# Custom viewset
from .models import Article
from .serializers import ArticleSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404




class ArticleViewSet(viewsets.ViewSet):

    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


    def create(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

# urls.py
from django.urls import path, include
from .views import ArticleViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article')


urlpatterns = [

    path('viewset/', include(router.urls))
]

######################################################### ModelViewset and Routers (Views.py)
# Rather than writing your own you'll often have to use existing base classes

class ArticleViewSet(viewsets.ModelViewSet):
    """
        A viewset for viewing and editing article instances.
        """

    serializer_class = ArticleSerializer
    queryset = Article.objects.all()