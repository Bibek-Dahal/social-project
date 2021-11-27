from django.db import models
from myapp.models import Profile

class Post(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="posts",default='')
    title = models.CharField(max_length=300,blank=True)
    description = models.TextField(default='')
    pic = models.ImageField( upload_to = 'Post/Images',blank = True)
    liked_by = models.ManyToManyField(Profile,related_name = 'post_liked_by',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.user} {self.title}"

    def return_desc(self):
        return self.description[:50]

    def likedby(self):
        return  ",".join([str(p) for p in self.liked_by.all()])

    def show_comments(self):
        return self.comments.all()
    


class Comment(models.Model):
    text = models.TextField(max_length=300)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} {self.text}"

    class Meta:
        ordering = ('-created_at',)
# choice_set = (
#     ('Liked','Liked'),
#     ('Unliked','Unliked')
# )

class Like(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likes")
    # status = models.CharField(choices=choice_set,max_length='20')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
