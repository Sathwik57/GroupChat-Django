import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class CommonFields(models.Model):
    id = models.UUIDField(
        default= uuid.uuid4, 
        primary_key= True,
        editable= False,
        unique= True
    )
    created = models.DateField(auto_now_add=True)
    class Meta:
        abstract = True
        ordering = ['-created']


class User(AbstractUser,CommonFields):
    image = models.ImageField(null = True, blank = True, upload_to='images')


class Group(CommonFields):
    name = models.CharField(max_length= 50, unique= True)
    admin = models.ForeignKey(
        User, 
        on_delete= models.CASCADE,
        related_name= 'group_admin',
        blank = True
    )
    image = models.ImageField(null = True, blank = True, upload_to='images')
    slug = models.SlugField(unique= True)
    members = models.ManyToManyField(
        User, 
        blank= True,
        related_name= 'members')

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def load_message():
        return Message.objects.order_by('-timestamp').all()[:10] 



class Message(CommonFields):
    author = models.ForeignKey(
        User, 
        on_delete= models.CASCADE, 
        related_name= 'messages'
    )
    content = models.CharField(max_length= 100)
    group = models.ForeignKey(
        Group,
        on_delete= models.CASCADE,
        related_name ='group_messages'
    )

    def __str__(self) -> str:
        return self.content

    @classmethod
    def load_message(cls,grp):
        return cls.objects.filter(group = grp).order_by('-created').all()[:10]

    def likes_count(self):
        """
        Returns like count for current message
        """
        try:
            return self.msg_likes.count 
        except:
            return 0

    def like_message(self, liked_by):
        """
        Calls signal to increase like count and add user 
        into liked_by field
        """
        from .signals import change_likes
        change_likes.send(sender =self.__class__ , instance = self, user = liked_by)


class Likes(models.Model):
    message = models.OneToOneField(
        Message,
        on_delete=models.CASCADE,
        related_name= 'msg_likes'
    )
    liked_by = models.ManyToManyField( 
        User, 
        blank= True , 
        related_name= 'liked_users'
    )
    count = models.PositiveIntegerField(default= 0)

    def __str__(self) -> str:
        return self.message.content


# class Likes(models.Model):
#     message = models.ForeignKey(
#         Message,
#         on_delete=models.CASCADE,
#         related_name= 'msg_likes'
#     )
#     liked_by = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name= 'liked_messages'
#     )