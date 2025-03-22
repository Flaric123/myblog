from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст статьи")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    image = models.ImageField(upload_to="articles/", null=True, blank=True, verbose_name="Изображение")
    
    category = models.ForeignKey(
        "Category", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Категория"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_date"]

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="Авторизованный пользователь"
    )
    guest_name = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Гостевой никнейм"
    )
    content = models.TextField(verbose_name="Текст комментария")
    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def author_name(self):
        return self.user.username if self.user else self.guest_name

    def __str__(self):
        return f"Комментарий от {self.author_name}"

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    
    def __str__(self):
        return self.name