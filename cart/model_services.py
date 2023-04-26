from django.db.models import Q

from discounts.models import Discount
from goods.models import GoodsInMarket, Category


def get_disc(disc: Discount, price: float) -> float:
    if disc.discount_mech_id == 1:
        # если скидка в процентах
        return round(price * disc.discount_value / 100)
    elif disc.discount_mech_id == 2:
        # если скидка в рублях
        return price - disc.discount_value
    else:
        # если скидка - фиксированная сумма
        return disc.discount_value


def price_with_discount(goods_in_market: GoodsInMarket, category: Category) -> float:
    price = goods_in_market.price
    goods = goods_in_market.goods
    disc = Discount.objects.filter(
        Q(discount_type=1),
        Q(goods_1=goods) | Q(category_1=category)
    ).order_by('-weight').first()
    if disc:
        discount = get_disc(disc, price)
    else:
        discount = 0
    return price - discount