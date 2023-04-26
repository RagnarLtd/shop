from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.db import models

from cart.model_services import price_with_discount
from goods.models import GoodsInMarket, Category
from discounts.models import Discount
User = get_user_model()


class CartItems(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="user_for_cart")
    product_in_shop = models.ForeignKey(GoodsInMarket,
                                        null=True,
                                        on_delete=models.CASCADE,
                                        verbose_name="Товар в магазине",
                                        related_name="product_in_shop_for_cart")
    quantity = models.PositiveIntegerField(verbose_name='количество', default=1)
    category = models.ForeignKey(Category,
                                 verbose_name=_('category'),
                                 on_delete=models.CASCADE,
                                 related_name='category_in_cart', null=True)

    @property
    def discount_price(self):
        new_price = price_with_discount(self.product_in_shop, self.category)
        return new_price

    class Meta:
        verbose_name_plural = "Корзина"

    def __str__(self):
        return f"{self.product_in_shop} {self.user}"
