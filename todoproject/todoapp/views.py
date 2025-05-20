from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Todo
import json

def todo_list(request):
    todos = Todo.objects.all().order_by('-created_at')
    return render(request, 'todo_list.html', {'todos': todos})

def todo_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        
        if title:
            todo = Todo.objects.create(title=title)
            return JsonResponse({
                'id': todo.id,
                'title': todo.title,
                'completed': todo.completed,
                'created_at': todo.created_at.strftime('%b %d, %Y %I:%M %p')
            }, status=201)
        return JsonResponse({'error': 'Title is required'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def todo_update(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=pk)
        data = json.loads(request.body)
        
        if 'title' in data:
            todo.title = data['title']
        if 'completed' in data:
            todo.completed = data['completed']
        
        todo.save()
        return JsonResponse({
            'id': todo.id,
            'title': todo.title,
            'completed': todo.completed,
            'created_at': todo.created_at.strftime('%b %d, %Y %I:%M %p')
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

def todo_delete(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=pk)
        todo.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)