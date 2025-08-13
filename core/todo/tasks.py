from celery import shared_task
from .models import Task


@shared_task
def delete_completed_tasks():
    deleted_count, _ = Task.objects.filter(complete=True).delete()
    print(f"{deleted_count} completed tasks deleted")
    return f"{deleted_count} completed tasks deleted"
