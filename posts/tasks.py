from celery import shared_task

from posts.models import Post


@shared_task()
def schedule_post():
    posts = Post.objects.filter(is_publish=False)
    for post in posts:
        post.is_publish = True
        post.save()
