from django.urls import path
from .views import HomeView, ArticleDetailView, CommentCreateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("article/<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("comment/new/<int:article_id>/", CommentCreateView.as_view(), name="add_comment"),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
