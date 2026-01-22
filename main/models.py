from django.db import models

from django.contrib.auth.models import User
import uuid  
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

class App(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.ImageField(upload_to='app_icons/', blank=True, null=True)
    apk_file = models.FileField(upload_to='downloads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_main_app = models.BooleanField(default=False)  
    def __str__(self):
        return self.title

class MainApp(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    apk_file = models.FileField(upload_to='downloads/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

        
class DownloadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE, null=True, blank=True)
    main_app = models.ForeignKey(MainApp, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.app:
            return f"{self.user.username} - {self.app.title}"
        elif self.main_app:
            return f"{self.user.username} - {self.main_app.title}"
        else:
            return f"{self.user.username} - Unknown App"




class ApiToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.token)