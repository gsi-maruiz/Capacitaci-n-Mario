import io

from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.decorators import api_view, action
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from snippets.permissions import IsOwnerOrReadOnly
from snippets.models import Snippet, Person, Author, Book, Track, Album
from snippets.serializers import SnippetSerializer, UserSerializer, PersonaSerializer, AuthorSerializer, BookSerializer, \
    TrackSerializer, AlbumSerializer
from rest_framework import generics, renderers, viewsets, status
from rest_framework import permissions
from django.http import HttpResponse, JsonResponse, Http404
from rest_framework import filters


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


# using ViewSet
class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonaSerializer

    # overwrite the method List of the ModelViewSet
    '''
    def list(self, request, *args, **kwargs):
        personas = self.get_queryset()
        serializer = PersonaSerializer(personas, many=True)
        return Response(serializer.data)
    '''


# working with Class based views
class PersonaWithApiWeb(APIView):

    def get(self, request):
        personas = Person.objects.all()
        serializer = PersonaSerializer(personas, many=True)
        return Response(serializer.data)


class PersonaDetailsWithApiWeb(APIView):

    def get_object(self, pk):
        try:
            return Person.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        person = self.get_object(pk)
        serializer = PersonaSerializer(person)
        return Response(serializer.data)


# working with function based views
@api_view(['GET', 'POST'])
def persona_list(request):
    if request.method == 'GET':
        persons = Person.objects.all()
        serializer = PersonaSerializer(persons, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PersonaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# working with Generic View
class PersonaGenericView(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonaSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]  # this setting is only in this view
    filterset_fields = ['name', 'age', 'sex']  # fields to filter
    search_fields = ['name']
    ordering = ['name']

    '''
    #make my own filters    
    def get_queryset(self):
        query_set = Persona.objects.all()
        id = self.request.query_params.get('id')
        name = self.request.query_params.get('name')
        age = self.request.query_params.get('age')
        if name is not None:
            query_set = query_set.filter(name=name)
        if age is not None:
            query_set = query_set.filter(age=age)
        return query_set
    '''


class AuthorView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['name']

    '''
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            for book in request.data["books"]:
                nameBook = book["name"]
                book = Book(name=nameBook, author_id=serializer.data["id"])
                book.save()

            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
'''


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['name']

    def perform_create(self, serializer):
        authors = Author.objects.filter(id=self.request.data["author_id"])
        if authors:
            serializer.save(author=authors[0])


class AlbumView(generics.ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['name']


class TrackView(generics.ListAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['name']
