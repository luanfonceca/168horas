from datetime import date, timedelta

from django.utils import timezone

from rest_framework import serializers

from activity.models import Activity


class ActivitySalesProgression(serializers.ModelSerializer):
    formatted_days = serializers.SerializerMethodField()
    sales_by_day = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ('formatted_days', 'sales_by_day')

    def get_formatted_days(self, instance):
        return [
            u'{:%d/%m}'.format(day)
            for day in self.get_days(instance)
        ]

    def get_days(self, instance):
        days = []
        delta = timezone.now() - instance.created_at

        for day in xrange(0, delta.days + 8, 7):
            days.append(
                instance.created_at + timedelta(days=day)
            )
        return days

    def get_sales_by_day(self, instance):
        sales = []
        days = self.get_days(instance)
        for day in days:
            sales.append(
                instance.attendee_set.filter(created_at__lte=day.date()).count()
            )
        return sales