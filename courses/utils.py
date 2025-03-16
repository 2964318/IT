from .models import Users, Notification

def notify_user(user,title, message, is_admin=False, is_global=False):
    Notification.objects.create(
        user=user,
        message=message,
        is_admin=is_admin,
        is_global=is_global,
        title=title
    )

def notify_admins(title, message, is_admin=False, is_global=False):
    admins = Users.objects.filter(is_superuser=True)
    for admin in admins:
        Notification.objects.create(
            user=admin,
            message=message,
            is_admin=is_admin,
            is_global=is_global,
            title=title
    )

