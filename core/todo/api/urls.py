from django.urls import path
from .views import TodoViewSet
from rest_framework.routers import DefaultRouter

app_name = "api"

router = DefaultRouter()
router.register("task", TodoViewSet, basename="task")


urlpatterns = router.urls

# urlpatterns = [
#     # path('', views.apiOverview, name='api-overview'),
#     # path("task-list/", views.taskList, name="task-list"),
#     # path("task-create/", views.taskList, name="task-create"),
#     # path("task-detail/<str:pk>/", views.taskDetail, name="task-detail"),
#     # path("task-update/<str:pk>/", views.taskDetail, name="task-update"),
#     # path("task-delete/<str:pk>/", views.taskDetail, name="task-delete"),
#     # path("task-list/", TodoListApiView.as_view(), name="task_list"),
#     # path("task-detail/<int:todo_id>/", TodoDetailApiView.as_view(), name="task_detail")
# ]
