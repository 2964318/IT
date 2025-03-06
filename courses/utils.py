from .models import CustomUser, Notification

def notify_user(user, message, is_admin=False, is_global=False):
    Notification.objects.create(
        user=user,
        message=message,
        is_admin=is_admin,
        is_global=is_global
    )

def notify_admins(message):
    admins = CustomUser.objects.filter(is_staff=True)
    for admin in admins:
        notify_user(admin, message, is_admin=True)