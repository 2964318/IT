from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
# 新加入包
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse

# class CustomLoginView(LoginView):
#     template_name = 'login.html'
#
#     def get_success_url(self):
#         if self.request.user.is_admin():
#             return reverse_lazy('admin_dashboard')
#         return reverse_lazy('dashboard')
@method_decorator(csrf_exempt, name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect_url = reverse_lazy('admin_dashboard') if user.is_superuser else reverse_lazy('dashboard')
            return JsonResponse({"message": "success", "redirect_url": str(redirect_url)}, status=200)
       
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)  # Login Failed

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({"message": "success"}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)
    else:
        return render(request, "register.html")  # Handling GET requests

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return JsonResponse({"message": "Password changed successfully"}, status=200)  #  JSON Response
        else:
            return JsonResponse({"error": form.errors}, status=400)  # JSON Response
    else:
        form = PasswordChangeForm(user=request.user)  # Define the form in the GET request

    return render(request, 'change_password.html', {'form': form})  #  Ensure that the form exists

@login_required
def account_settings(request):
    return render(request, 'account_settings.html')

def custom_logout(request):
    logout(request)
    return redirect('home')

@login_required
@user_passes_test(lambda u: u.is_admin())
def admin_account_settings(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully')
            return redirect('admin_dashboard')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'admin/account_settings.html', {'form': form})
