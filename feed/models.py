from django.db import models


class FeedUser(models.Model):
    name = models.CharField(max_length=25)
    password = models.CharField(max_length=25)

    def __str__(self):
        return f"User: {self.name}"


class Token(models.Model):
    token = models.CharField(max_length=36)
    expires_on = models.DateTimeField(null=False)
    user = models.ForeignKey(FeedUser, on_delete=models.CASCADE)


# Create your models here.
class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(FeedUser, on_delete=models.PROTECT)

    likes_count = models.IntegerField(default=0)

    liked_by = models.ManyToManyField(FeedUser, related_name='liked_posts')

    def __str__(self):
        return f"Post: {self.title} by {self.created_by.name}"

    def __repr__(self):
        return f"Post: {self.title} by {self.created_by.name}"


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()

    created_by = models.ForeignKey(FeedUser, on_delete=models.PROTECT)

    def __str__(self):
        return f"Comment: {self.message[0:40]} by {self.created_by.name}"

    def __repr__(self):
        return f"Comment: {self.message[0:40]} by {self.created_by.name}"
