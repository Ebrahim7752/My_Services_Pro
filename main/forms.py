from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def validate_complex_password(value):
    if len(value) < 8:
        raise ValidationError("كلمة المرور يجب أن تكون 8 أحرف على الأقل")
    if not re.search(r"[A-Z]", value):
        raise ValidationError("كلمة المرور يجب أن تحتوي على حرف كبير واحد على الأقل")
    if not re.search(r"[a-z]", value):
        raise ValidationError("كلمة المرور يجب أن تحتوي على حرف صغير واحد على الأقل")
    if not re.search(r"[0-9]", value):
        raise ValidationError("كلمة المرور يجب أن تحتوي على رقم واحد على الأقل")
from .models import App, Profile

# =============================
# فورم إدارة المستخدمين
# =============================
class AdminUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        required=False,
        label="كلمة المرور",
        help_text="اترك الحقل فارغاً إذا كنت لا تريد تغيير كلمة المرور."
    )
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            validate_complex_password(password)
        return password

    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'is_active', 'password']
        labels = {
            'username': 'اسم المستخدم',
            'email': 'البريد الإلكتروني',
            'is_staff': 'مدير',
            'is_active': 'نشط',
        }

# =============================
# فورم البروفايل
# =============================
class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone', 'country', 'city', 'country_code']
        labels = {
            'first_name': 'الاسم الأول',
            'last_name': 'الاسم الأخير',
            'phone': 'رقم الهاتف',
            'city': 'المدينة',
            'country': 'الدولة',
            'country_code': 'رمز الدولة',
        }
        widgets = {
             'country': forms.Select(attrs={'class': 'form-control', 'id': 'country'}),
             'city': forms.Select(attrs={'class': 'form-control', 'id': 'city'}),
             'country_code': forms.Select(attrs={'class': 'form-control', 'id': 'country_code'}),
             'first_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '30'}),
             'last_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '30'}),
             'phone': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '15'}),
        }

# =============================
# فورم إدارة التطبيقات
# =============================
class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['title', 'description', 'icon', 'apk_file', 'is_active']
        labels = {
            'title': 'عنوان التطبيق',
            'description': 'الوصف',
            'icon': 'أيقونة التطبيق',
            'apk_file': 'ملف APK',
            'is_active': 'نشط',
        }





# تعديل بيانات المستخدم
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'اسم المستخدم',
            'email': 'البريد الإلكتروني',
        }
        widgets = {
             'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
             'email': forms.EmailInput(attrs={'class': 'form-control', 'maxlength': '100'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'country', 'city', 'country_code', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'maxlength': '30'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'maxlength': '30'}),
            'country': forms.Select(attrs={'class':'form-control'}),
            'city': forms.Select(attrs={'class':'form-control'}),
            'country_code': forms.Select(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'maxlength': '15'}),
        }

# تغيير كلمة المرور
class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        label="كلمة المرور الحالية",
        required=False
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        label="كلمة المرور الجديدة",
        validators=[validate_complex_password],
        help_text="يجب أن تحتوي على 8 أحرف، حرف كبير، حرف صغير، ورقم.",
        required=False
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        label="تأكيد كلمة المرور الجديدة",
        required=False
    )



from .models import MainApp

class MainAppForm(forms.ModelForm):
    class Meta:
        model = MainApp
        fields = ['title', 'description', 'apk_file']
        labels = {
            'title': 'عنوان التطبيق',
            'description': 'الوصف',
            'apk_file': 'ملف APK',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':4}),
            'apk_file': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }
