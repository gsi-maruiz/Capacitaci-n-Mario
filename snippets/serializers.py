from django.contrib.auth.models import User
from rest_framework import serializers

from snippets.models import Snippet, Person, Author, Book, Track, Album


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']


class PersonaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'url', 'name', 'lastName', 'age', 'sex']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    # books = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # retorna una lista de id (llave foranea)
    # books = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='book-detail')  # retorna una lista de links, para la vista de detalle del book
    books = BookSerializer(many=True, read_only=True)  # retorna el objeto book serializado

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

    '''
    def create(self, validated_data):
        print(validated_data)
        books_data = validated_data.pop('books')
        author = Author.objects.create(**validated_data)
        for book_data in books_data:
            Book.objects.create(author=author, **book_data)
        return author
    '''


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['order', 'title', 'duration']


class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']

    def create(self, validated_data):
        tracks_data = validated_data.pop('tracks')
        album = Album.objects.create(**validated_data)
        for track_data in tracks_data:
            Track.objects.create(album=album, **track_data)
        return album
