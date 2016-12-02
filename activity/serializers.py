from datetime import date, timedelta

from django.utils import timezone

from rest_framework import serializers

from activity.models import Activity


class ActivitySalesProgression(serializers.ModelSerializer):
    formatted_days = serializers.SerializerMethodField()
    sales_by_day = serializers.SerializerMethodField()
    last_days = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ('formatted_days', 'sales_by_day', 'last_days')

    def get_formatted_days(self, instance):
        return [
            u'{:%d/%m}'.format(day)
            for day in self.get_days(instance)
        ]

    def def_get_delta(self, instance):
        ending_on = timezone.now()
        # tzinfo = timezone.pytz.timezone(
        #     timezone.get_default_timezone_name()
        # )
        # import ipdb; ipdb.set_trace()
        # if instance.end_scheduled_date > timezone.now().date():
        #     ending_on = timezone.datetime.combine(
        #         instance.end_scheduled_date,
        #         timezone.datetime.min.time()
        #     ).replace(tzinfo=tzinfo)
        return ending_on - instance.created_at
        
    def get_last_days(self, instance):
        delta = self.def_get_delta(instance)
        last_days = delta.days - 14
        if not last_days > 0:
            last_days = delta.days - 7
        if not last_days > 0:
            last_days = 0
        return last_days

    def get_days(self, instance):
        days = []
        delta = self.def_get_delta(instance)
        last_days = self.get_last_days(instance)
        end_date = timezone.now() + timedelta(1)
        start_date = end_date - timedelta(last_days)

        def date_range(start_date, end_date):
            for n in range(int ((end_date - start_date).days)):
                yield start_date + timedelta(n)

        return date_range(start_date, end_date)

    def get_sales_by_day(self, instance):
        sales = []
        for day in self.get_days(instance):
            sales.append(
                instance.attendee_set.filter(created_at__contains=day.date()).count()
            )
        return sales