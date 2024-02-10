from decimal import Decimal

from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseModel):
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    rating_avg = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal(0.0))
    rating_count = models.PositiveIntegerField(blank=True, null=True, default=0,
                                               help_text="Cached count of rates of company to "
                                                         "avoid calculating rating every time"
                                               )

    def __str__(self):
        return self.title if self.title else 'Untitled Post'


class Rating(models.Model):
    STAR_CONVERSION = (
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
        (5, 'Five'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(choices=STAR_CONVERSION)
