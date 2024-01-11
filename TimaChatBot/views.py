from django.shortcuts import render
from django.http import JsonResponse
from TimaChatBot.main import generate_response

# Create your views here.

def simple_page(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        bot_response = generate_response(user_input)
        return render(request, 'chat.html')



