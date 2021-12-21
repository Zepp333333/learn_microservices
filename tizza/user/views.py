from django.shortcuts import render

from django.contrib.auth import  login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse


class SignupView(View):
    template_name = 'signup.html'

    def post(self, request: HttpRequest):
        # if request.method == 'GET':
        #     form = UserCreationForm()
        #     return render(request, self.template_name, {'form': form})

        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse({'Something wend wrong in user.views'})

    def get(self, request):
        return render(request, self.template_name,
                      {'form': UserCreationForm})
