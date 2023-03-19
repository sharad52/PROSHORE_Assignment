from django.db import models


class Content(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    blog_image_url = models.URLField()
    author_name = models.CharField(max_length=100)
    author_image_url = models.URLField()
    author_designation = models.CharField(max_length=100)
    reading_time = models.CharField(max_length=60)

    class Meta:
        db_table = 'content'
        verbose_name = 'Content'
        verbose_name_plural = "Contents"
