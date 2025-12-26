"""
Elastic / OpenSearch abstraction layer
"""

from apps.news.models import Article
from .models import SearchIndex


class SearchService:
    @staticmethod
    def index_article(article: Article):
        """
        Create / update search index
        """
        SearchIndex.objects.update_or_create(
            article=article,
            defaults={
                "title": article.title,
                "summary": article.summary,
                "content": article.content,
                "category": article.category.name if article.category else "",
                "article_type": article.article_type,
                "published_at": article.published_at,
            }
        )

    @staticmethod
    def remove_article(article: Article):
        SearchIndex.objects.filter(article=article).delete()

    @staticmethod
    def search(query=None, *, category=None, article_type=None):
        """
        DB fallback search
        (Elastic/OpenSearch can replace this transparently)
        """
        qs = SearchIndex.objects.filter(is_deleted=False)

        if query:
            qs = qs.filter(
                title__icontains=query
            ) | qs.filter(
                summary__icontains=query
            ) | qs.filter(
                content__icontains=query
            )

        if category:
            qs = qs.filter(category__iexact=category)

        if article_type:
            qs = qs.filter(article_type=article_type)

        return qs.select_related("article")
