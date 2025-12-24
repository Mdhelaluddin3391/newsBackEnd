from datetime import timedelta
from django.utils import timezone
from django.db.models import Count

from .models import ArticleView
from apps.news.models import Article


def record_article_view(article, user=None, ip_address=None):
    """
    Call this whenever an article detail is opened
    """
    ArticleView.objects.create(
        article=article,
        user=user if user and user.is_authenticated else None,
        ip_address=ip_address,
    )


def get_popular_articles(limit=10):
    """
    All-time popular articles
    """
    return (
        Article.objects.filter(status="published")
        .annotate(view_count=Count("views"))
        .order_by("-view_count")[:limit]
    )


def get_trending_articles(days=3, limit=10):
    """
    Trending = most views in last N days
    """
    since = timezone.now() - timedelta(days=days)

    return (
        Article.objects.filter(
            status="published",
            views__created_at__gte=since,
        )
        .annotate(view_count=Count("views"))
        .order_by("-view_count")[:limit]
    )
