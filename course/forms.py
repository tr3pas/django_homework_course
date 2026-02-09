from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import StudentCourses, StudentProfile
from django.forms import modelformset_factory

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Електронна пошта",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваш Email: example@email.com'
        })
        )  
    
    first_name = forms.CharField(
        required=False,
        label="Ім'я",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Ваше ім'я"
        })
    )

    last_name = forms.CharField(
        required=False,
        label="Прізвище",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Ваше прізвище"
        })
    )

    age = forms.IntegerField(
        required=False,
        label="Вік",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': "Ваш вік"
        })
        
    )
    
    phone = forms.CharField(
        required=False,
        label="Номер телефону",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Ваш номер телефону"
        })
    )

    remember_me = forms.BooleanField(
        required=False,
        label="Запам'ятати мене")
    


    class Meta:
        model = StudentProfile
        fields = ("username", "first_name", "last_name",'age','phone', "email", "password1", "password2")
        
        widgets = {
            "username": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш логін'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["remember_me"].widget.attrs.update({'class': 'form-check-input'})
        self.fields["password1"].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ваш пароль'
        })
        self.fields["age"].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ваш вік'
        })
        self.fields["phone"].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ваш номер телефону'
        })
        self.fields["password2"].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Підтвердження пароля'
        })  

    def clean_email(self):
        """Валідація email"""
        
        email = self.cleaned_data.get('email')
        if not email:
            return email
            
        # Перевіряємо унікальність
        if StudentProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("Користувач з таким email вже існує!")
        
        # Заборонені тестові домени
        if email.lower().endswith('@test.com'):
            raise forms.ValidationError("Тестові email адреси заборонені")
        return email

    def clean_phone(self):
        
        phone = self.cleaned_data.get('phone')

        if not phone.startswith("+380"):
            raise forms.ValidationError("Телефон має бути у форматі +380XXXXXXXXX")
        return phone
    
    def clean_age(self):
        
        age = self.cleaned_data.get('age')

        if age >= 18 or age <= 12:
            raise forms.ValidationError("Для реєстрації на сайті потрібен вік від 12 до 18 років")
        return age
    
    def save(self, commit=True):
        """Зберігаємо користувача з додатковими полями"""

        # Спочатку зберігаємо стандартні поля
        user: StudentProfile = super().save(commit=False)
                
        # Додаємо наші кастомні поля
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.age = self.cleaned_data['age']
        user.phone = self.cleaned_data['phone']

        # Зберігаємо в базу даних якщо commit=True
        if commit:
            user.save()

        return user


class CourseForm(forms.ModelForm):
    course = forms.MultipleChoiceField(
        required=True,
        label="Курси",
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-control',
            'placeholder': f""
        })
        )
    priority = forms.IntegerField(
        required=True,
        label="Курси",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': "Введіть пріорітет від 1 до 3"
        }))
    
    class Meta:
        model = StudentCourses
        fields = ("course","priority")

    def clean_priority(self):
        priority = self.cleaned_data.get('priority')

        if priority <= 0 or priority > 3:
            raise forms.ValidationError("Пріорітет повинен бути від 1 до 3")
        return priority



class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = StudentProfile
        fields = ("username",
                    "first_name",
                    "last_name",
                    'age',
                    'phone',
                    "email",
                    )


class CustomUserChangeForm(UserCreationForm):
    class Meta:
        model = StudentProfile
        fields = ("username",
                    "first_name",
                    "last_name",
                    'age',
                    'phone',
                    "email",
                    'is_active',
                    'is_staff',
                    'is_superuser')
        



CourseFormSet = modelformset_factory(
    StudentCourses,
    fields=("course", "priority"),
    extra=3,
    max_num=3,
    validate_max=True
)