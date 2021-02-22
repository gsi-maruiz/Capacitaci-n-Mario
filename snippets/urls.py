from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'persona', views.PersonaViewSet)
router.register(r'author', views.AuthorView)
router.register(r'book', views.BookView)
#router.register(r'album', views.AlbumView)
#router.register(r'track', views.TrackView)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('personasApiView', views.PersonaWithApiWeb.as_view()),
    path('personasApiViewClass/<int:pk>', views.PersonaDetailsWithApiWeb.as_view()),
    path('personasApiViewFunc', views.persona_list),
    path('personasGenericView', views.PersonaGenericView.as_view()),
    path('album', views.AlbumView.as_view()),

]
