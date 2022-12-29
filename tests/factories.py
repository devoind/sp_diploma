import factory

from django.contrib.auth import get_user_model

from goals.models import GoalCategory, Board, BoardParticipant

USER_MODEL = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = USER_MODEL

    username = factory.Faker('name')
    email = factory.Faker('email')
    password = '007Weid007'


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.Faker('name')


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    user = factory.SubFactory(UserFactory)


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = factory.Faker('name')
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

# user = UserFactory.create()
# category = GoalCategoryFactory.create()
# board = BoardFactory.create()
