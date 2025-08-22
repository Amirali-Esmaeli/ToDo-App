from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer
from todo.models import Task
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import PermissionDenied

# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework import generics
# from django.shortcuts import get_object_or_404
# from django.http import JsonResponse
# from rest_framework.decorators import api_view, permission_classes

User = get_user_model()

# FBV-DRF
'''
@api_view(["GET"])
def apiOverview(request):
    """Overview of the whole api urls"""
    api_urls = {
        "List": "/api/task-list/",
        "Detail": "/api/task-detail/<str:pk>/",
        "Create": "/api/task-create/",
        "Update": "/api/task-update/<str:pk>/",
        "Delete": "/api/task-delete/<str:pk>/",
    }

    return Response(api_urls)


@api_view(["GET", "POST"])
@permission_classes((IsAuthenticated,))
def taskList(request):
    """
    ---
    response_serializer: TaskSerializer
    parameters:
            - title: CharField

    """
    if request.method == "GET":
        tasks = Task.objects.filter(user=request.user.pk).order_by('-id')
        serializers = TaskSerializer(tasks, many=True)
        return Response(serializers.data)
    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["user"] = User.objects.get(
                pk=request.user.id
            )
            serializer.save()
            return JsonResponse(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return JsonResponse(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
@permission_classes((IsAuthenticated,))
@api_view(["GET", "POST", "DELETE"])
def taskDetail(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user.pk)
    if request.method == "GET":
        serializers = TaskSerializer(task, many=False)
        return Response(serializers.data)
    elif request.method == "POST":
        serializer = TaskSerializer(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    elif request.method == "DELETE":
        task.delete()
        return JsonResponse({"detail": "Task was deleted successfully!"})'''

# CBV-DRF-ApiView
'''
class TodoListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        List all the todo items for given requested user
        """
        todos = Task.objects.filter(user=request.user.id)
        serializer = TaskSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        """
        Create the Task with given todo data
        """
        serializer = TaskSerializer(data=request.data)
        serializer.validated_data["user"] = User.objects.get(
            pk=request.user.id
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, todo_id, user_id):
        """
        Helper method to get the object with given todo_id, and user_id
        """
        return get_object_or_404(Task, id=todo_id, user=user_id)
    def get(self, request, todo_id, *args, **kwargs):
        """
        Retrieves the Task with given todo_id
        """
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = TaskSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, todo_id, *args, **kwargs):
        """
        Updates the todo item with given todo_id if exists
        """
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            "title": request.data.get("title"),
            "completed": request.data.get("completed"),
            "user": request.user.id,
        }
        serializer = TaskSerializer(
            instance=todo_instance, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, todo_id, *args, **kwargs):
        """
        Deletes the todo item with given todo_id if exists
        """
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        todo_instance.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)
'''

# CBV-DRF-GenericView
"""
class TodoListApiView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    def list(self, request):
        queryset = self.get_queryset()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class TodoDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "todo_id"
    def get_object(self, queryset=None):
        obj = Task.objects.get(pk=self.kwargs["todo_id"])
        return obj
    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        object.delete()
        return Response({"detail": "successfully removed"})
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)"""


# CBV-DRF-ViewSet
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["complete"]
    search_fields = ["title"]
    ordering_fields = ["created_date"]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to view your tasks.")
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a task.")
        serializer.save(user=self.request.user)
