from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(TestCase):
    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_login(self):
        User.objects.create_user(username='testuser', password='testpass123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_password_change(self):
        # 创建测试用户
        user = User.objects.create_user(
            username='testuser',
            password='oldpassword123'  # 确保旧密码符合验证规则
        )
        
        # 登录用户
        self.client.login(username='testuser', password='oldpassword123')
        
        # 提交密码修改请求
        response = self.client.post(
            reverse('change_password'),
            {
                'old_password': 'oldpassword123',
                'new_password1': 'newcomplexpass123',  # 新密码
                'new_password2': 'newcomplexpass123',
            },
            follow=True  # 跟随重定向
        )
        
        # 刷新用户实例
        user.refresh_from_db()
        
        # 验证密码修改
        self.assertTrue(user.check_password('newcomplexpass123'))
        self.assertRedirects(response, reverse('dashboard'))