from blog.models import Post
from .serializers import PostSerializer

from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser, DjangoModelPermissions
from rest_framework import viewsets, filters, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404


############ TYPE GENERIC
# Display All Posts
# ListCreateAPIView: List Items and Create Items
class PostList(generics.ListAPIView): # viewsets.ModelViewSet.PostUserWritePermission
    permission_classes = [permissions.IsAuthenticated]
    # DjangoModelPermissions (Since the view is ListAPIView it can only view)
    #   if for e.g its ListCreateAPIView because of DjangoModelPermisssions we will only be allowed to add or view
    # DjangoModelPermissionOrAnonReadOnly (Anons read only)
    # IsAdminUser is for where Is_Staff= True
    serializer_class = PostSerializer
    queryset = Post.objects.all() # Want to list this data  
    # Here we can display all  the posts which are published if use the query below because of how we defined our blog/models
    # queryset = Post.postobjects.all()

    # Serializers are used because we want that the data is returned from the
    # database in the correct format
# Display One Post
# RetrieveDestroyAPIView: Retrieve and Destroy Items
class PostDetail(generics.RetrieveAPIView): # viewsets.ModelViewSet.PostUserWritePermission

    # If type 127.0.0.1:8000/api/<title name> it will get that
    serializer_class = PostSerializer
    # pk is coming from the url
    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Post, slug=item)



# ############ TYPE VIEWSETS FOR ROUTES
# To speed up development
# # INSTEAD OF MULTIPLE VIEWS WE USE FUNCTIONS IN VIEWS
# # ----------------------------------------------------
# class Posts(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Post.postobjects.all()

#     def list(self, request):
#         serializer_class = PostSerializer(self.queryset, many=True)
#         return Response(serializer_class.data)
#     def create(self, request):
#         pass
#     def retrieve(self, request, pk=None):
#         post = get_object_or_404(self.queryset, pk=pk)
#         serializer_class = PostSerializer(post)
#         return Response(serializer_class.data)
#     def update(self, request, pk=None):
#         pass
#     def partial_update(self, request, pk=None): 
#         pass
#     def destroy(self, request, pk=None):
#         pass


############ MODEL VIEWSET
# Need Routes for Model Viewset as well or dont (Not sure)
# MOdel Viewset already has create(), list() type apis etc.

# class PostList(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = Post.postobjects.all()
#     serializer_class = PostSerializer

# class PostDetail(viewsets.ModelViewSet, PostUserWritePermission):
    #     permission_classes = [PostUserWritePermission]
    #     queryset = Post.objects.all()
    #     serializer_class = PostSerializer

################# Customizing the Viewset

# class PostList(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer

# If type 127.0.0.1:8000/api/<title name> it will get that
#     def get_object(self, queryset=None, **kwargs):
#         item = self.kwargs.get('pk')
#         return get_object_or_404(Post, slug=item)

#     # Define Custom Queryset
#     def get_queryset(self):
#         return Post.objects.all()



# Post Search
class PostListDetailfilter(generics.ListAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    # '^' Starts-with search.
    # '=' Exact matches.
    search_fields = ['^slug']

# class CreateAnyPost(generics.CreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


class CreatePost(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        print(request.data)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminPostDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class EditPost(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class DeletePost(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


""" Concrete View Classes
# CreateAPIView
Used for create-only endpoints.
# ListAPIView
Used for read-only endpoints to represent a collection of model instances.
# RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
# DestroyAPIView
Used for delete-only endpoints for a single model instance.
# UpdateAPIView
Used for update-only endpoints for a single model instance.
# ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
# RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
# RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""
# CUSTOM PERMISSIONS
# For custom permissions we need to override the BasePermissions
# - has_permission or - has_object_permission

class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # All other requests methods are true if the person is the user
        return obj.author == request.user

# With generics.RetrieveAPIView you still could only just view because its retreive only 
# But if it was RetrieveUpdateDestroyAPIView it will give special permission to author of the post
class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):

    permission_classes = [PostUserWritePermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


############### Filters and Search
class PostList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    # queryset = Post.objects.all()
    # for custom queryset use
    def get_queryset(self):

