from celery.decorators import task
from django.shortcuts import get_object_or_404
from django.db.models import Max


@task()
def set_bidding_winner(product_id):
    from .models import Product, AuctionWinner, AuctionBidding
    product_object = get_object_or_404(Product, id=product_id)

    max_amount = AuctionBidding.objects.filter(
        product=product_object
    ).aggregate(max_amount=Max('amount'))['max_amount']
    winner = AuctionBidding.objects.filter(
        product=product_object, amount=max_amount).first()

    print(winner)

    if winner:
        AuctionWinner.objects.create(
            product=product_object, user=winner.user, amount=winner.amount, is_complted=True)
    else:
        AuctionWinner.objects.create(product=product_object)
