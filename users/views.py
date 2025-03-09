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
@method_decorator(csrf_exempt, name='dispatch')  # 允许 AJAX 发送请求
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #return JsonResponse({"message": "success"}, status=200)  # 登录成功返回 JSON
            redirect_url = reverse_lazy('admin_dashboard') if user.is_superuser else reverse_lazy('dashboard')
            return JsonResponse({"message": "success", "redirect_url": str(redirect_url)}, status=200)
       
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)  # 登录失败
    

# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('dashboard')
#     else:
#         form = RegisterForm()
#     return render(request, 'register.html', {'form': form})
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({"message": "success"}, status=200)  # ✅ 返回 JSON
        else:
            return JsonResponse({"error": form.errors}, status=400)  # ✅ 返回 JSON
    else:
        return render(request, "register.html")  # ✅ 处理 GET 请求

# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(user=request.user, data=request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)
#             messages.success(request, 'Password updated successfully!')
#             if user.is_superuser:
#                 return redirect('admin_dashboard')
#             return redirect('dashboard')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = PasswordChangeForm(user=request.user)
#
#     return render(request, 'change_password.html', {'form': form})
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return JsonResponse({"message": "Password changed successfully"}, status=200)  # ✅ JSON 响应
        else:
            return JsonResponse({"error": form.errors}, status=400)  # ✅ JSON 响应
    else:
        form = PasswordChangeForm(user=request.user)  # ✅ 在 GET 请求时定义 form

    return render(request, 'change_password.html', {'form': form})  # ✅ 确保 form 存在

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
