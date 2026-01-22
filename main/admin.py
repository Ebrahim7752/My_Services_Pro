from django.contrib import admin
from .models import App, MainApp, Profile, DownloadHistory, ApiToken
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone', 'country')
    search_fields = ('user__username', 'first_name', 'last_name', 'phone', 'country')

# جدول التطبيقات الأخرى
@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'apk_file', 'created_at')
    search_fields = ('title',)

# جدول التطبيق الرئيسي فقط
@admin.register(MainApp)
class MainAppAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'apk_file')



@admin.register(DownloadHistory)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ('user', 'app', 'downloaded_at')
    list_filter = ('user', 'app')

@admin.register(ApiToken)
class ApiTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')

