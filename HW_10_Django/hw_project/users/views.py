from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import RegisterForm


# Create your views here.
class RegisterView(View):
    form_class = RegisterForm
    template_name = 'users/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='useful_quotes:root')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            print(username)
            messages.success(request, f'{username} , your account successfully created {username}')
            return redirect(to='users:signin')
        return render(request, self.template_name, {'form': form})
