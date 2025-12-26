from django.db.models import Count
from django.utils import timezone

from .models import ArticleViewEvent, ArticleAnalytics
from apps.news.models import Article


def record_view(*, article, user, session_id, ip, user_agent):
    ArticleViewEvent.objects.create(
        article=article,
        user=user,
        session_id=session_id,
        ip_address=ip,
        user_agent=user_agent,
    )


def recalculate_article_analytics(article_id):
    article = Article.objects.get(id=article_id)

    events = ArticleViewEvent.objects.filter(article=article)

    total_views = events.count()
    unique_users = events.exclude(user=None).values("user").distinct().count()

    analytics, _ = ArticleAnalytics.objects.get_or_create(article=article)

    analytics.total_views = total_views
    analytics.unique_users = unique_users
    analytics.last_calculated_at = timezone.now()
    analytics.save(
        update_fields=[
            "total_views",
            "unique_users",
            "last_calculated_at",
            "updated_at",
        ]
    )
