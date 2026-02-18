from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import Orders, Revenue


@receiver(post_save, sender=Orders)
def update_total_revenue(sender, instance, **kwargs):

    if instance.payment_status == "SUCCESS":

        total = Orders.objects.filter(
            payment_status="SUCCESS"
        ).aggregate(
            total=Sum("total_amount")
        )["total"] or 0

        revenue, created = Revenue.objects.get_or_create(id=1)
        revenue.total_revenue = total
        revenue.save()
