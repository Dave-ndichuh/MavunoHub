from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

class YourAppNameConfig(AppConfig):  # Replace "YourAppName" with your app's name
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'  # Replace with your app's name

    def ready(self):
        import accounts.signals