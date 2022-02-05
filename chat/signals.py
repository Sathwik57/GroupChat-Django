from django.dispatch import receiver,Signal

from .models import Message,Likes

change_likes = Signal()


@receiver(change_likes, sender = Message)
def likes_change(sender, instance ,user ,*args, **kwargs):
    try:
        likes = instance.msg_likes
    except:
        likes = Likes.objects.create( message = instance)
    if user not in likes.liked_by.all(): 
        likes.liked_by.add(user)
        likes.count += 1
        likes.save()