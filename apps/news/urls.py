from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import ArticleViewSet

router = DefaultRouter()
router.register("articles", ArticleViewSet, basename="articles")

urlpatterns = [
    path("", include(router.urls)),
]


from django.urls import path
from .views import home, article_detail, category_page

urlpatterns = [
    path("", home, name="home"),
    path("news/<slug:slug>/", article_detail, name="article_detail"),
    path("category/<slug:slug>/", category_page, name="category_page"),
]
