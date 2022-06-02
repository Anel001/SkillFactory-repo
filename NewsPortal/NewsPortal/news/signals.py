from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post, Category, UserCategory, PostCategory
from django.shortcuts import render, reverse, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.models import User


@receiver(m2m_changed, sender=Post)
def post(sender, instance, *args, **kwargs):
    for cat_id in instance.PostCategory.all():
        users = Category.objects.filter(pk=cat_id).values("subscribers")
        for i in users:
            send_mail(
                subject=f"{instance.caption}",
                message=f"Здравствуй, {User.objects.get(pk=i['subscribers']).username}."
                        f" Новая статья в твоём любимом разделе! \n Заголовок статьи: {instance.caption} \n"
                        f" Текст статьи: {instance.text[:50]}",
                from_email='anel031@yandex.ru',
                recipient_list=['anel04tileulieva05@gmail.com']#User.objects.get(pk=i['subscribers']).email
            )
            return redirect('/posts/')

