import django_filters
from django.db import transaction
from rest_framework import generics, permissions, filters

from goals.filters import GoalFilter, GoalCommentFilter, GoalCategoryFilter
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
from goals.permissions import GoalPermission, GoalCategoryPermission, GoalCommentPermission, BoardPermissions
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer, BoardCreateSerializer, BoardListSerializer, \
    BoardSerializers


class GoalCategoryCreateAPIView(generics.CreateAPIView):
    """Класс создания категорий для Целей"""
    model = GoalCategory
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = [permissions.IsAuthenticated, GoalCategoryPermission]


class GoalCategoryListAPIView(generics.ListAPIView):
    """Класс отображения списка Категорий"""
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

    def get_queryset(self) -> GoalCategory:
        """Переопределенное значение при использовании фильтров для поиска значений"""
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)


class GoalCategoryDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated, GoalCategoryPermission]

    def get_queryset(self) -> GoalCategory:
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: GoalCategory) -> GoalCategory:
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            goals = Goal.objects.filter(category=instance)
            for goal in goals:
                goal.status = Goal.Status.archived
                goal.save()
        return instance


class GoalCreateAPIView(generics.CreateAPIView):
    """Класс создания Целей, с использованием модели целей (model)"""
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [permissions.IsAuthenticated, GoalPermission]


class GoalListAPIView(generics.ListAPIView):
    """Класс отображения списка Целей, с использованием модели целей (model)"""
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

    def get_queryset(self) -> Goal:
        """Переопределенное значение при использовании фильтров для поиска значений"""
        return Goal.objects.filter(category__board__participants__user=self.request.user).exclude(
            status=Goal.Status.archived)


class GoalDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Класс отображения/изменения/удаления списка Категорий"""
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated, GoalPermission]

    def get_queryset(self) -> Goal:
        """Переопределенное значение при использовании фильтров для поиска значений"""
        return Goal.objects.filter(category__board__participants__user=self.request.user
                                   ).exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance: Goal) -> Goal:
        """Удаление экземпляра объекта - Категории"""
        instance.status = Goal.Status.archived
        instance.save()
        return instance


class GoalCommentCreateAPIView(generics.CreateAPIView):
    """Класс создания Комментариев к Целям"""
    model = GoalComment
    serializer_class = GoalCommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated, GoalCommentPermission]

    def perform_create(self, serializer: GoalCommentCreateSerializer):
        """Для сохранения нового экземпляра объекта (комментария)"""
        serializer.save(goal_id=self.request.data['goal'])


class GoalCommentListAPIView(generics.ListAPIView):
    """Класс отображения списка Комментариев к Целям"""
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

    def get_queryset(self) -> GoalComment:
        """Переопределенное значение при использовании фильтров для поиска значений"""
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class GoalCommentDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Класс отображения/изменения/удаления списка Комментариев к Целям"""
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated, GoalCommentPermission]

    def get_queryset(self) -> GoalComment:
        """Переопределенное значение при использовании фильтров для поиска значений"""
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


# Board's views
class BoardCreateAPIView(generics.CreateAPIView):
    """Класс создания Досок"""
    model = Board
    serializer_class = BoardCreateSerializer
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]


class BoardListAPIView(generics.ListAPIView):
    """Класс отображения списка Досок"""
    model = Board
    serializer_class = BoardListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> Board:
        """Переопределенное значение при использовании фильтров для поиска значений"""
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Класс отображения/изменения/удаления списка Досок"""
    model = Board
    serializer_class = BoardSerializers
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]

    def get_queryset(self) -> Board:
        """Переопределенное значение при использовании фильтров для поиска значений"""
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        """Класс отображения/изменения/удаления списка Досок"""
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)

        return instance
