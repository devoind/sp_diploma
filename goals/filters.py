import django_filters
from django.db import models

from goals.models import Goal, GoalComment, GoalCategory


class GoalFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Goal
        fields = {'category': ['exact', 'in'],
                  'priority': ['exact', 'in'],
                  'due_date': ['lte', 'gte'],
                  'status': ['exact', 'in']}
        filter_overrides = {
            models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter},
        }


class GoalCommentFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = GoalComment
        fields = {'goal': ['exact', 'in']}


class GoalCategoryFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = GoalCategory
        fields = {'board': ['exact', 'in']}
