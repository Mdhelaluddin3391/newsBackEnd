def submit_for_review(article):
    article.status = "review"
    article.save()

def publish(article):
    article.status = "published"
    article.save()
