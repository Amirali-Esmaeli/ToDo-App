from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.views.generic import ListView,DeleteView,UpdateView,CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

# Create your views here.

# FUNCTION-BASED VIEWS (FBV)


'''
@login_required
def index(request):
    """
    Display all tasks for the current user and handle task creation.
    """
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
        return redirect("/")
    
    context = {"tasks": tasks, "form": form}
    return render(request, "tasks/list_task.html", context)'''

'''
@login_required
def updateTask(request, pk):
    """
    Update an existing task.
    """
    task = Task.objects.get(id=pk, user=request.user)
    form = TaskForm(instance=task)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect("/")
    context = {"form": form}

    return render(request, "tasks/update_task.html", context)
'''

'''
@login_required
def completeTask(request, pk):
    """
    Mark a task as complete for the current user.
    """
    item = get_object_or_404(Task, id=pk, user=request.user)
    item.complete = True
    item.save()
    return redirect("/")
'''

'''
@login_required
def deleteTask(request, pk):
    """
    Delete a task for the current user.
    """
    item = get_object_or_404(Task, id=pk, user=request.user)
    item.delete()
    return redirect("/")
'''

# CLASS-BASED VIEWS (CBV)


class TaskList(LoginRequiredMixin,ListView):
    """
    Display a list of tasks for the currently authenticated user.
    """
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/list_task.html"

    def get_queryset(self):
        # Only return tasks for the current user
        return self.model.objects.filter(user=self.request.user)
    
class TaskCreate(LoginRequiredMixin, CreateView):
    """
    Create a new task for the current user.
    """
    model = Task
    fields = ["title"]
    success_url = reverse_lazy("task_list") # Redirect after successful creation

    def form_valid(self, form):
        # Assign the current user to the new task before saving
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    """
    Update an existing task belonging to the current user.
    """
    model = Task
    success_url = reverse_lazy("task_list")
    form_class = TaskForm
    template_name = "tasks/update_task.html"

    def get_queryset(self):
        # Only allow updating user's own tasks
        return self.model.objects.filter(user=self.request.user)


class TaskComplete(LoginRequiredMixin, View):
    """
    Toggle the completion status of a task for the current user.
    """
    model = Task
    success_url = reverse_lazy("task_list")

    def get(self, request, *args, **kwargs):
        # Retrieve the task and toggle its completion status
        object = Task.objects.get(id=kwargs.get("pk"))
        object.complete = not object.complete
        object.save()
        return redirect(self.success_url)
    

class DeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a task belonging to the current user.
    """
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("task_list")

    def get(self, request, *args, **kwargs):
        # Only allow deleting user's own tasks
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        # For safety: handle GET request as POST for deletion
        return self.model.objects.filter(user=self.request.user)