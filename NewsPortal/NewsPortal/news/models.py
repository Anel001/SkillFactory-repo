from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authUser = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('post_rating'))
        prat = 0
        prat += postRat.get('postRating')

        commentRat = self.authUser.comment_set.aggregate(commentRating=Sum('com_rating'))
        crat = 0
        crat += commentRat.get('commentRating')

        self.user_rating = prat * 3 + crat
        self.save()

    def __str__(self):
        return f' {self.authUser}'


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, through='UserCategory', related_name='subscribers')

    def __str__(self):
        return f' {self.category_name}'


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    Author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article = 'AR'
    news = 'NW'
    GENRE = [(article, 'Статья'),
             (news, 'Новости')]
    choice = models.CharField(max_length=2, choices=GENRE, default=article)
    date_create = models.DateTimeField(auto_now_add=True)
    caption = models.CharField(max_length=100)
    text = models.TextField()
    post_rating = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')

    def get_absolute_url(self):
        return f'/posts/{self.id}'

    def __str__(self):
        return f' {self.caption}: {self.text}...'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()


class PostCategory(models.Model):
    Post = models.ForeignKey('Post', on_delete=models.CASCADE)
    Category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    com_text = models.TextField()
    com_date = models.DateTimeField(auto_now_add=True)
    com_rating = models.IntegerField(default=0)

    def like(self):
        self.com_rating += 1
        self.save()

    def dislike(self):
        self.com_rating += 1
        self.save()

