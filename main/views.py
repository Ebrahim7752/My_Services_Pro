from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
import os
import re
from .models import App, Profile, MainApp, DownloadHistory, ApiToken
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from .forms import UserForm, ProfileForm, AdminUserForm, AdminProfileForm, AppForm , ChangePasswordForm, MainAppForm
from django.contrib.auth import update_session_auth_hash
import json
@login_required
def download_apk(request, app_id=None):
    # تحديد التطبيق
    if app_id:
        app = get_object_or_404(App, id=app_id)
        main_app = None
    else:
        main_app = get_object_or_404(MainApp, id=1)  # أول تطبيق رئيسي
        app = None

    # التحقق من وجود الملف
    file_path = app.apk_file.path if app else main_app.apk_file.path
    if not os.path.exists(file_path):
        return HttpResponseNotFound("الملف غير موجود")

    # تسجيل التحميل
    dh = DownloadHistory.objects.create(
        user=request.user,
        app=app,
        main_app=main_app,
        ip_address=request.META.get('REMOTE_ADDR', ''),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )

    # إرسال الملف
    f = app.apk_file.open('rb') if app else main_app.apk_file.open('rb')
    response = HttpResponse(f.read(), content_type='application/vnd.android.package-archive')
    f.close()
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    return response


def home(request):
    user = request.user

    # التحقق من إكمال بيانات البروفايل
    if user.is_authenticated and not hasattr(user, 'profile'):
        return redirect('complete_profile')

    apps = App.objects.all().order_by('-created_at')       
    main_app = MainApp.objects.first()                     

    return render(request, 'index.html', {
        'apps': apps,
        'main_app': main_app,
        'user': user
    })


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        if password != confirm:
            messages.error(request, "كلمتا المرور غير متطابقتين")
            return redirect('signup')

        if len(password) < 8:
            messages.error(request, "كلمة المرور يجب أن تكون 8 أحرف على الأقل")
            return redirect('signup')

        if not re.search(r"[A-Za-z]", password):
            messages.error(request, "كلمة المرور يجب أن تحتوي على أحرف")
            return redirect('signup')

        if not re.search(r"[0-9]", password):
            messages.error(request, "كلمة المرور يجب أن تحتوي على أرقام")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "البريد الإلكتروني مستخدم بالفعل")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "اسم المستخدم مستخدم بالفعل")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "تم إنشاء الحساب بنجاح، يمكنك تسجيل الدخول")
        return redirect('login')

    return render(request, "login.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.is_staff:
                return redirect('staff_dashboard')
            return redirect('home')

        messages.error(request, "خطأ في اسم المستخدم أو كلمة المرور")

    return render(request, "login.html")



@login_required
def logout_view(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass

    logout(request)
    messages.success(request, "تم تسجيل الخروج بنجاح")
    return redirect('login')


@login_required
def complete_profile(request):
    if request.method == "POST":
        first = request.POST['first_name']
        last = request.POST['last_name']
        code = request.POST['country_code']
        phone = request.POST['phone']
        country = request.POST['country']
        city = request.POST['city']

        profile, created = Profile.objects.get_or_create(user=request.user)

        profile.first_name = first
        profile.last_name = last
        profile.country_code = code
        profile.phone = phone
        profile.country = country
        profile.city = city
        profile.save()

        messages.success(request, "تم حفظ معلومات حسابك بنجاح")
        return redirect('home')

    return render(request, "profile_setup.html")




@staff_member_required
def staff_dashboard(request):
    total_users = User.objects.count()
    total_apps = App.objects.count()
    total_downloads = DownloadHistory.objects.count()
    
    # Recent activity
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_downloads = DownloadHistory.objects.order_by('-downloaded_at')[:5]

    # Data for charts
    # 1. Downloads per regular App
    apps = App.objects.annotate(d_count=Count('downloadhistory')).order_by('-d_count')[:5]
    app_labels = [app.title for app in apps]
    app_data = [app.d_count for app in apps]

    # 2. Downloads for MainApp
    main_app_downloads = DownloadHistory.objects.filter(main_app__isnull=False).count()
    if main_app_downloads > 0:
        # Get Main Name (Approximation, assuming one main app active or just generally "Main App")
        try:
             main_app_title = MainApp.objects.first().title
        except:
             main_app_title = "التطبيق الرئيسي"
        
        app_labels.append(main_app_title)
        app_data.append(main_app_downloads)

    context = {
        'total_users': total_users,
        'total_apps': total_apps,
        'total_downloads': total_downloads,
        'recent_users': recent_users,
        'recent_downloads': recent_downloads,
        'app_labels': json.dumps(app_labels),
        'app_data': json.dumps(app_data),
    }
    return render(request, 'staff/dashboard.html', context)


@staff_member_required
def create_user(request):
    if request.method == "POST":
        user_form = AdminUserForm(request.POST)
        profile_form = AdminProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            if user_form.cleaned_data.get("password"):
                user.set_password(user_form.cleaned_data["password"])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, f"✅ تم إنشاء المستخدم {user.username} بنجاح")
            return redirect("staff_users")  

        else:
            messages.error(request, "❌ يوجد خطأ في البيانات، يرجى التحقق")
    else:
        user_form = AdminUserForm()
        profile_form = AdminProfileForm()

    return render(request, "staff/create_user.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        user_form = AdminUserForm(request.POST, instance=user)
        profile_form = AdminProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            
            # التحقق من وجود كلمة مرور جديدة
            new_password = user_form.cleaned_data.get('password')
            if new_password:
                user.set_password(new_password)
                messages.success(request, f"✅ تم تعديل بيانات المستخدم {user.username} وتغيير كلمة المرور")
            else:
                messages.success(request, f"✅ تم تعديل بيانات المستخدم {user.username} بنجاح")
            
            user.save()
            profile_form.save()
            return redirect("staff_users")
        else:
            messages.error(request, "❌ يوجد خطأ في البيانات")
    else:
        user_form = AdminUserForm(instance=user)
        profile_form = AdminProfileForm(instance=profile)

    return render(request, "staff/edit_user.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "user": user
    })



@staff_member_required
def staff_apps(request):
    apps = App.objects.all().order_by('-created_at')
    return render(request, 'staff/apps.html', {'apps': apps})




@staff_member_required
def create_app(request):
    if request.method == "POST":
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إنشاء التطبيق بنجاح")
            return redirect('staff_apps')
    else:
        form = AppForm()
    return render(request, 'staff/create_app.html', {'form': form})

@staff_member_required
def edit_app(request, app_id):
    app = get_object_or_404(App, id=app_id)
    if request.method == "POST":
        form = AppForm(request.POST, request.FILES, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث التطبيق بنجاح")
            return redirect('staff_apps')
    else:
        form = AppForm(instance=app)
    return render(request, 'staff/edit_app.html', {'form': form})






def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    username = user.username  
    user.delete()
    messages.success(request, f"✅ تم حذف المستخدم {username} بنجاح")
    return redirect("staff_users") 


@staff_member_required
def delete_app(request, app_id):
    app = get_object_or_404(App, id=app_id)
    app.delete()
    messages.success(request, "تم حذف التطبيق بنجاح")
    return redirect('staff_apps')



@staff_member_required
def staff_users(request):
    users = User.objects.all()
    return render(request, 'staff/users.html', {'users': users})


@login_required
def user_dashboard(request):
    apps = App.objects.all().order_by('-created_at')
    total_downloads = DownloadHistory.objects.filter(user=request.user).count()
    return render(request, 'user/dashboard.html', {
        'apps': apps,
        'total_downloads': total_downloads
    })

@login_required
def app_detail(request, app_id):
    app = get_object_or_404(App, id=app_id)
    return render(request, 'user/app_detail.html', {'app': app})

















@login_required
def profile_view(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        password_form = ChangePasswordForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            # حفظ بيانات المستخدم الأساسية (بدون كلمة المرور حالياً)
            user_form.save()
            profile_form.save()

            # منطق تغيير كلمة المرور (فقط إذا تم إدخال بيانات)
            if request.POST.get('current_password') or request.POST.get('new_password'):
                 if not user.check_password(password_form.data['current_password']):
                     messages.error(request, "❌ كلمة المرور الحالية غير صحيحة")
                     # لا نوقف التنفيذ، بل نعيد التوجيه مع رسالة خطأ، لكن تم حفظ البيانات الأخرى
                     return redirect('profile_view')

                 if password_form.data['new_password'] != password_form.data['confirm_password']:
                     messages.error(request, "❌ كلمتا المرور غير متطابقتين")
                     return redirect('profile_view')
                
                 # التحقق من شروط كلمة المرور يدوياً أو عبر الفورم
                 if len(password_form.data['new_password']) < 8:
                      messages.error(request, "❌ كلمة المرور قصيرة جداً")
                      return redirect('profile_view')

                 user.set_password(password_form.data['new_password'])
                 user.save()
                 messages.success(request, "✅ تم حفظ البيانات وتغيير كلمة المرور بنجاح")
            else:
                messages.success(request, "✅ تم حفظ التعديلات بنجاح")
            
            return redirect('profile_view')

        else:
            messages.error(request, "❌ يوجد خطأ في البيانات")

    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)
        password_form = ChangePasswordForm()

    return render(request, 'user/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
        'profile': profile,
    })


def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def staff_mainapp(request):
    main_app = MainApp.objects.first() 

    if request.method == 'POST':
        form = MainAppForm(request.POST, request.FILES, instance=main_app)
        if form.is_valid():
            form.save()
            return redirect('staff_mainapp')
    else:
        form = MainAppForm(instance=main_app)

    return render(request, 'staff/mainapp.html', {'form': form})














@csrf_exempt
def api_download_app(request, app_id):
    token = request.headers.get('Authorization')

    if not token:
        return JsonResponse({'error': 'Token missing'}, status=401)

    try:
        api_token = ApiToken.objects.get(token=token)
    except ApiToken.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=403)

    app = get_object_or_404(App, id=app_id)

    if not app.apk_file:
        return JsonResponse({'error': 'File not found'}, status=404)

    # ✅ تسجيل التحميل
    DownloadHistory.objects.create(
        user=api_token.user,
        app=app,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )

    response = HttpResponse(
        app.apk_file.open('rb'),
        content_type='application/vnd.android.package-archive'
    )
    response['Content-Disposition'] = (
        f'attachment; filename="{os.path.basename(app.apk_file.name)}"'
    )
    return response




@staff_member_required
def staff_download_stats(request):

    users_stats = (
        DownloadHistory.objects
        .values('user__username')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    apps_stats = (
        DownloadHistory.objects
        .values('app__title')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    downloads = DownloadHistory.objects.all().order_by('-downloaded_at')
    total_downloads = downloads.count()

    return render(request, 'staff/download_stats.html', {
        'users_stats': users_stats,
        'apps_stats': apps_stats,
        'downloads': downloads,
        'total_downloads': total_downloads,
    })




@login_required
def user_downloads(request):

    downloads = (
        DownloadHistory.objects
        .filter(user=request.user)
        .select_related('app')
        .order_by('-downloaded_at')
    )

    total_downloads = downloads.count()

    return render(request, 'user/downloads.html', {
        'downloads': downloads,
        'total_downloads': total_downloads,
    })
