from django.db.models import Avg

from app.models import Post, Rating


def rate(user, post: Post, rate_num: int):
    """
    Rate a post and update its rating average and count.

    Args:
        user (User): The user who is rating the post.
        post (Post): The post to be rated.
        rate_num (int): The rating value (0-5).

    Returns:
        Tuple[bool, Rating]: A tuple containing a boolean indicating if the rating was successful and the rating object.
    """

    if 0 <= int(rate_num) <= 5:
        rating_obj, created = Rating.objects.update_or_create(owner=user, post=post, defaults={'rate': rate_num})
        aggregates = Rating.objects.filter(post__id=post.id).aggregate(average=Avg('rate'))
        post.rating_avg = aggregates.get('average') or 0.0
        rating_count = Rating.objects.filter(post__id=post.id).count()
        post.rating_count = rating_count
        post.save()
        return True, rating_obj
