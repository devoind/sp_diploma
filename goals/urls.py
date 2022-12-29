from django.urls import path

from goals.views import GoalCategoryCreateAPIView, GoalCategoryListAPIView, GoalCategoryDetailUpdateDeleteAPIView, \
    GoalCreateAPIView, GoalListAPIView, GoalDetailUpdateDeleteAPIView, GoalCommentCreateAPIView, GoalCommentListAPIView, \
    GoalCommentDetailUpdateDeleteAPIView, BoardCreateAPIView, BoardListAPIView, BoardDetailUpdateDeleteAPIView

urlpatterns = [
    path('goal_category/create', GoalCategoryCreateAPIView.as_view(), name='category_goal_create'),
    path('goal_category/list', GoalCategoryListAPIView.as_view(), name='category_goal_list'),
    path('goal_category/<int:pk>', GoalCategoryDetailUpdateDeleteAPIView.as_view(),
         name='detail_update_delete_goal_category'),
    path('goal/create', GoalCreateAPIView.as_view(), name='create_goal'),
    path('goal/list', GoalListAPIView.as_view(), name='list_goal'),
    path('goal/<int:pk>', GoalDetailUpdateDeleteAPIView.as_view(), name='detail_update_delete_goal'),

    path('goal_comment/create', GoalCommentCreateAPIView.as_view(), name='comment_create_goal'),
    path('goal_comment/list', GoalCommentListAPIView.as_view(), name='comment_list_goal'),
    path('goal_comment/<int:pk>', GoalCommentDetailUpdateDeleteAPIView.as_view(), name='comment_pk_goal'),

    path('board/create', BoardCreateAPIView.as_view(), name='create_board'),
    path('board/list', BoardListAPIView.as_view(), name='list_board'),
    path('board/<int:pk>', BoardDetailUpdateDeleteAPIView.as_view(), name='detail_update_delete_board'),
]
