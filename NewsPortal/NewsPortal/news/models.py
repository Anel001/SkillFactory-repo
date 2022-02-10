from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.category_name}'


class Post(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    caption = models.CharField(max_length=64)
    text = models.TextField()
    category = models.ForeignKey(to='Category',
                                 on_delete=models.CASCADE,
                                 related_name='posts', )

    def __str__(self):
        return f'{self.caption}: {self.text}...'
