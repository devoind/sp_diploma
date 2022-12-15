import django_filters
from django.db import transaction
from rest_framework import generics, permissions, filters

from goals.filters import GoalFilter, GoalCommentFilter, GoalCategoryFilter
from goals.models import GoalCategory, Goal, GoalComment, Board
from goals.permissions import GoalPermission, GoalCategoryPermission, GoalCommentPermission, BoardPermissions
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer, BoardCreateSerializer, BoardListSerializer, \
    BoardSerializers


class GoalCategoryCreateAPIView(generics.CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = [permissions.IsAuthenticated, GoalCategoryPermission]


class GoalCategoryListAPIView(generics.ListAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    search_fields = ['title']
    ordering_fields = ['title', 'created']
    ordering = ['title']
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = GoalCategoryFilter

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)


class GoalCategoryDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated, GoalCategoryPermission]

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            goals = Goal.objects.filter(category=instance)
            for goal in goals:
                goal.status = Goal.Status.archived
                goal.save()
        return instance


class GoalCreateAPIView(generics.CreateAPIView):
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [permissions.IsAuthenticated, GoalPermission]


class GoalListAPIView(generics.ListAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    search_fields = ['title']
    ordering_fields = ['priority', 'due_date']
    ordering = ['-priority', 'due_date']

    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = GoalFilter

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user).exclude(
            status=Goal.Status.archived)


class GoalDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated, GoalPermission]

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user
                                   ).exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived
        instance.save()
        return instance


class GoalCommentCreateAPIView(generics.CreateAPIView):
    model = GoalComment
    serializer_class = GoalCommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated, GoalCommentPermission]


class GoalCommentListAPIView(generics.ListAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    ordering_fields = ['goal', 'created', 'updated']
    ordering = ['-created']

    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = GoalCommentFilter

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class GoalCommentDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated, GoalCommentPermission]

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class BoardCreateAPIView(generics.CreateAPIView):
    model = Board
    serializer_class = BoardCreateSerializer
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]


class BoardListAPIView(generics.ListAPIView):
    model = Board
    serializer_class = BoardListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    model = Board
    serializer_class = BoardSerializers
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)

        return instance
