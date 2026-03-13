from django import forms
from .models import Course, Lesson
from django.contrib.auth.models import User
from .models import Category, Resource, Feedback
from .models import Profile  # modèle à créer pour la photo et la bio


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['title', 'description', 'image']


class LessonForm(forms.ModelForm):

    class Meta:
        model = Lesson
        fields = ['course', 'title', 'content', 'video']


from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmer le mot de passe")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Les mots de passe ne correspondent pas")


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course', 'title', 'content', 'video']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'file']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Écrivez quelque chose sur vous...'}),
        }
