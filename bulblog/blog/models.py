from django.db import models
from django.urls import reverse

class Blog(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название поста")
    slug = models.SlugField(unique=True, max_length=255, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Содержание поста")
    creat_time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания поста")
    update_time = models.DateTimeField(auto_now=True, verbose_name="Время изменения поста")
    cat = models.ForeignKey("Categories", on_delete=models.PROTECT, verbose_name="Категория")
    last_accessed = models.DateTimeField("Последний просмотр", null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug":self.slug})

    class Meta:
        verbose_name = "пост"
        verbose_name_plural = "посты"



class Categories(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(unique=True, max_length=255, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("show_posts_by_cat", kwargs={"cat_slug":self.slug})

    class Meta:
        verbose_name = "Выбрать все категории"
        verbose_name_plural = "Категории"
        ordering = ['name']