from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

CATEGORY_CHOICES = [
    ('Meds', 'Лекарства'),
    ('Home', 'Товары для дома'),
    ('Education', 'Образование'),
    ('Device', 'Техника'),
    ('Other', 'Прочее')
]


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Категория")
    description = models.TextField(max_length=2000, blank=True, null=True, verbose_name="Описание")
    picture = models.ImageField(null=True, blank=True, upload_to='product_pics', verbose_name="Картинка")

    def __str__(self):
        return f'{self.title}'

    def get_rate(self):
        reviews = self.review_product.all().exclude(is_moderated=False)
        rate = 0
        if reviews.count() > 0:
            for review in reviews:
                rate += review.rate
            rate = rate / reviews.count()
        return rate

    class Meta:
        db_table = 'Product'
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Review(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='review_author',
                               verbose_name='Автор')
    product = models.ForeignKey('webapp.Product', on_delete=models.CASCADE, related_name='review_product',
                                verbose_name='Товар')
    review_text = models.TextField(max_length=4000, verbose_name='Текст отзыва')
    rate = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Оценка')
    is_moderated = models.BooleanField(default=False, verbose_name='Промодерированно')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата редактировнаия')

    def __str__(self):
        return f'{self.author.username} | {self.product.title}'

    class Meta:
        db_table = 'Review'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        permissions = [
            ('can_moderate_reviews', 'Может модерировать отзывы')
        ]