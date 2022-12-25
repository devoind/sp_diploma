from django.db import models


class DatesModelMixin(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')


class Board(DatesModelMixin):
    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'

    title = models.CharField(verbose_name='Название', max_length=255)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)


class GoalCategory(DatesModelMixin):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    user = models.ForeignKey('core.User', verbose_name='Автор', on_delete=models.PROTECT)
    board = models.ForeignKey(
        Board, verbose_name='Доска', on_delete=models.PROTECT, related_name='categories'
    )
    title = models.CharField(max_length=255, verbose_name='Название')
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)


class Goal(DatesModelMixin):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цель'

    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    due_date = models.DateField(verbose_name='Дата исполнения')
    user = models.ForeignKey('core.User', verbose_name='Пользователь', on_delete=models.PROTECT)
    category = models.ForeignKey(
        'goals.GoalCategory', related_name='goals', verbose_name='Категория', on_delete=models.CASCADE
    )
    priority = models.PositiveSmallIntegerField(
        choices=Priority.choices, default=Priority.low, verbose_name='Приоритет'
    )
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.to_do, verbose_name='Статус')


class GoalComment(DatesModelMixin):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    text = models.TextField(verbose_name='Текст')
    goal = models.ForeignKey('goals.Goal', on_delete=models.PROTECT)
    user = models.ForeignKey('core.User', verbose_name='Пользователь',
                             on_delete=models.PROTECT)


class BoardParticipant(DatesModelMixin):
    class Meta:
        unique_together = ('board', 'user')
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    class Role(models.IntegerChoices):
        owner = 1, 'Владелец'
        writer = 2, 'Редактор'
        reader = 3, 'Читатель'

    board = models.ForeignKey(Board, verbose_name='Доска', on_delete=models.PROTECT, related_name='participants')
    user = models.ForeignKey(
        'core.User', verbose_name='Пользователь', on_delete=models.PROTECT, related_name='participants'
    )
    role = models.PositiveSmallIntegerField(verbose_name='Роль', choices=Role.choices, default=Role.owner)
