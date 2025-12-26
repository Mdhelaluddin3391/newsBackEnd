from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from apps.news.models import Article

def search_articles(query: str):
    # Weightage: Title (A) sabse important, phir Summary (B), phir Content (C)
    vector = (
        SearchVector("title", weight="A") +
        SearchVector("summary", weight="B") +
        SearchVector("content", weight="C")
    )

    search_query = SearchQuery(query)

    return (
        Article.objects.filter(status="published")
        .annotate(rank=SearchRank(vector, search_query))
        .filter(rank__gte=0.1)
        .order_by("-rank")
    )