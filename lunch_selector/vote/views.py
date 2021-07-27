"""Voting related views"""
import datetime

from django.core.cache import cache
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from restaurant.models import Menu
from user.models import SelectorUser
from vote.serializers import MenuVoteSerializer


class MenuVoteViewSet(viewsets.ModelViewSet):
    """Vote create and update by employee"""
    serializer_class = MenuVoteSerializer
    RESULT_CACHE_KEY = "vote-result-key"

    @staticmethod
    def _calculate_vote_result():
        """Get menus with max vote today"""
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        day_before_yesterday = today - datetime.timedelta(days=2)

        today_menus = []
        yesterday_max, yesterday_id = -1, set()
        before_yesterday_max, before_yesterday_id = -1, set()

        menus = Menu.objects.filter(
            day__in=[today, yesterday, day_before_yesterday]
        )
        for menu in menus:
            if menu.day == today:
                today_menus.append(menu)
            elif menu.day == yesterday:
                if menu.vote_count > yesterday_max:
                    yesterday_max = menu.vote_count
                    yesterday_id = {menu.restaurant_id}
                elif menu.vote_count == yesterday_max:
                    yesterday_id.add(menu.restaurant_id)
            else:
                if menu.vote_count > before_yesterday_max:
                    before_yesterday_max = menu.vote_count
                    before_yesterday_id = {menu.restaurant_id}
                elif menu.vote_count == before_yesterday_max:
                    before_yesterday_id.add(menu.restaurant_id)

        intersect = yesterday_id.intersection(before_yesterday_id)
        today_max, today_max_menus = -1, set()
        for menu in today_menus:
            if menu.restaurant_id not in intersect:
                if menu.vote_count > today_max:
                    today_max = menu.vote_count
                    today_max_menus = {menu}
                elif menu.vote_count == today_max:
                    today_max_menus.add(menu)
        return today_max_menus

    @action(
        methods=["get"], detail=False,
        url_path="result"
    )
    def result(self, request):  # pylint: disable=unused-argument
        """Vote result get"""
        data = cache.get(self.RESULT_CACHE_KEY, None)
        if not data:
            data = [
                {
                    "restaurant": menu.restaurant.name,
                    "name": menu.name,
                    "details": menu.details
                }
                for menu in self._calculate_vote_result()
            ]
            cache.set(self.RESULT_CACHE_KEY, data)
        return Response(data)

    def create(self, request, *args, **kwargs):
        """Cache delete on vote create"""
        cache.delete(self.RESULT_CACHE_KEY)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Cache delete on vote update"""
        cache.delete(self.RESULT_CACHE_KEY)
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        """Get votes based on user"""
        objects = self.serializer_class.Meta.model.objects
        user_type = getattr(self.request.user, "user_type", None)
        if user_type is None:
            return objects.none()
        if user_type == SelectorUser.EMPLOYEE:
            return objects.filter(
                employee=self.request.user
            )
        return objects.all()

    def initial(self, request, *args, **kwargs):
        """Populate employee"""
        user_type = getattr(request.user, "user_type", None)
        if user_type == SelectorUser.EMPLOYEE:
            request.data["employee"] = request.user.id
        super().initial(request, *args, **kwargs)
