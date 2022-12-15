from django.db import transaction
from rest_framework import serializers

from core.models import User
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user', 'board')
        fields = '__all__'


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError('not allowed in deleted category')
        else:
            return value


class GoalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'


class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    goal = serializers.IntegerField(source='goal.id', read_only=True)

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            board=board,
            user=user,
            role=BoardParticipant.Role.owner
        )
        return board


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.Role.choices)
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        read_only_fields = ('id', 'created', 'updated', 'board')
        fields = '__all__'


class BoardSerializers(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ('id', 'created', 'updated', 'board')
        fields = '__all__'

    def update(self, instance, validated_data):
        owner = validated_data.pop('user')
        new_participants = validated_data.pop('participants')
        new_by_id = {part['user'].id: part for part in new_participants}
        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_part in old_participants:
                if old_part.user_id not in new_by_id:
                    old_part.delete()
                elif old_part.role != new_by_id[old_part.user_id]['role']:
                    old_part.role = new_by_id[old_part.user_id]['role']
                    old_part.save()

                new_by_id.pop(old_part.user_id)

            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance,
                    user=new_part['user'],
                    role=new_part['role']
                )
            instance.title = validated_data.get('title')
            instance.save()

        return instance
