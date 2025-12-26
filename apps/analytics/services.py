from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from .models import ArticleView
from apps.news.models import Article

def record_article_view(article, user=None, ip_address=None):
    ArticleView.objects.create(
        article=article,
        user=user if user and user.is_authenticated else None,
        ip_address=ip_address,
    )
    # Increment count for faster retrieval
    article.view_count += 1
    article.save()

def get_popular_articles(limit=10):
    return Article.objects.filter(status="published").order_by("-view_count")[:limit]

def get_trending_articles(days=3, limit=10):
    since = timezone.now() - timedelta(days=days)
    return Article.objects.filter(
        status="published",
        views__created_at__gte=since
    ).annotate(recent_views=Count("views")).order_by("-recent_views")[:limit]