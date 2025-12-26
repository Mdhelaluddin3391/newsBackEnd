from django.shortcuts import render, get_object_or_404
from .models import Article, Category

def home(request):
    articles = Article.objects.filter(status="published", is_deleted=False)[:10]
    return render(request, "pages/home.html", {"articles": articles})


def article_detail(request, slug):
    article = get_object_or_404(
        Article,
        slug=slug,
        status="published",
        is_deleted=False
    )
    article.views += 1
    article.save(update_fields=["views"])

    related = Article.objects.filter(
        category=article.category,
        status="published"
    ).exclude(id=article.id)[:4]

    return render(request, "pages/article_detail.html", {
        "article": article,
        "related_articles": related
    })


def category_page(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    articles = Article.objects.filter(
        category=category,
        status="published",
        is_deleted=False
    )

    return render(request, "pages/category.html", {
        "category": category,
        "articles": articles
    })
