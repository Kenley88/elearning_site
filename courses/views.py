# ==============================
# IMPORTS
# ==============================

# Fonctions utiles Django
from django.shortcuts import render, redirect, get_object_or_404  # render page, redirection, récupérer objet
from django.contrib.auth.decorators import login_required, user_passes_test  # vérifier login et admin
from django.contrib.auth import login, logout, authenticate  # gérer authentification
from django.core.paginator import Paginator  # pagination
from django.contrib.auth.models import User  # modèle utilisateur
from django.core.mail import send_mail, BadHeaderError  # envoyer email
from django.contrib import messages  # messages de notification
from django.conf import settings  # accéder aux settings
from .forms import ProfileUpdateForm  # formulaire à créer
from .models import ForumPost  # ou ton modèle de posts
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .models import Challenge
# Import modèles
from .models import (
    Course, Enrollment, Lesson, Progress, Certificate,
    Comment, Activity, Notification, Category, Resource, Feedback
)

# Import formulaires
from .forms import (
    CourseForm, RegisterForm, LessonForm,
    CategoryForm, ResourceForm, FeedbackForm
)

# ==============================
# VERIFICATION ADMIN
# ==============================

def is_admin(user):
    # vérifie si l'utilisateur est superuser
    return user.is_superuser


# ==============================
# PAGE ACCUEIL
# ==============================

def home(request):

    # récupère 6 cours pour la page d'accueil
    courses = Course.objects.all()[:6]

    # affiche template
    return render(request, 'home.html', {'courses': courses})


def home_view(request):
    return render(request, 'home.html')

# ==============================
# CONTEXT PROCESSOR
# ==============================

def register_form(request):

    # rend formulaire d'inscription disponible globalement
    return {
        'register_form': RegisterForm()
    }




def discussion_forum(request):
    forum_posts = ForumPost.objects.all().order_by('-created_at')
    return render(request, 'discussion_forum.html', {'forum_posts': forum_posts})


def forum_post_detail(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    comments = post.comments.all().order_by('created_at')
    return render(request, 'forum_post_detail.html', {
        'post': post,
        'comments': comments
    })




# ==============================
# REGISTER
# ==============================

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Inscription réussie ! Vous pouvez maintenant vous connecter.")
            return redirect('login_view')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


# ==============================
# LOGIN
# ==============================

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Vérifier si l'utilisateur est superuser ou staff
            if user.is_staff or user.is_superuser:
                return redirect('dashboard_admin')  # <-- redirection vers dashboard admin
            else:
                return redirect('dashboard_user')   # <-- redirection vers dashboard user

        else:
            messages.error(request, "Nom d’utilisateur ou mot de passe incorrect")
            return redirect('login_view')
    else:
        return render(request, 'login.html')



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Met à jour la session pour ne pas déconnecter l'utilisateur
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été modifié avec succès !')
            return redirect('profile')  # Redirige vers la page de profil ou autre
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})



# ==============================
# LOGOUT
# ==============================

def logout_view(request):

    # déconnecte utilisateur
    logout(request)

    messages.success(request, "Vous êtes déconnecté.")

    return redirect('login_view')


# ==============================
# DASHBOARD
# ==============================

@login_required
def dashboard(request):

    # si admin
    if request.user.is_superuser:
        return render(request,'dashboard_user.html')

    # cours inscrits
    enrollments = Enrollment.objects.filter(user=request.user)

    # nombre total cours
    courses_count = Course.objects.count()

    # leçons complétées
    completed_lessons = Progress.objects.filter(
        user=request.user,
        completed=True
    ).count()

    # progression exemple
    progress_percent = 50

    # derniers cours
    latest_courses = Course.objects.order_by('-id')[:4]

    context = {
        'enrollments': enrollments,
        'courses_count': courses_count,
        'completed_lessons': completed_lessons,
        'progress_percent': progress_percent,
        'latest_courses': latest_courses
    }

    return render(request,'dashboard_user.html',context)


# ==============================
# AJOUTER UTILISATEUR
# ==============================


@login_required
@user_passes_test(is_admin)
def add_user(request):
    """
    Page pour ajouter un utilisateur.
    Pour l'instant elle affiche juste le template.
    Tu peux ajouter un formulaire plus tard.
    """

    return render(request, 'add_user.html')


# ==============================
# MODIFIER UTILISATEUR
# ==============================


@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    """
    Page pour modifier un utilisateur.
    Pour l'instant elle charge juste la page.
    Tu peux ajouter un formulaire plus tard.
    """

    from django.contrib.auth.models import User
    user = User.objects.get(id=user_id)

    context = {
        'user_obj': user
    }

    return render(request, 'edit_user.html', context)


def users_list(request):
    from django.contrib.auth.models import User
    users = User.objects.all()
    return render(request, 'users_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    from django.contrib.auth.models import User
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('users_list')


# ==============================
# DASHBOARD USER
# ==============================

def dashboard_user(request):

    # si utilisateur pas connecté
    if not request.user.is_authenticated:
        return redirect('login_view')

    # récupère tous les cours
    courses = Course.objects.all()

    return render(request, 'dashboard_user.html', {'courses': courses})


# ==============================
# LISTE DES COURS
# ==============================

@login_required
def course_list(request):

    # recherche
    query = request.GET.get('q')

    if query:
        courses = Course.objects.filter(title__icontains=query)
    else:
        courses = Course.objects.all()

    # pagination
    paginator = Paginator(courses,6)

    page = request.GET.get('page')

    courses = paginator.get_page(page)

    return render(request,'course_list.html',{'courses':courses})


# ==============================
# SEARCH COURSES
# ==============================

def search_courses(request):

    query = request.GET.get('q', '')

    courses = Course.objects.filter(title__icontains=query)

    return render(request, 'courses.html', {'courses': courses, 'query': query})


# ==============================
# AJOUTER COURS
# ==============================

@login_required
@user_passes_test(is_admin)
def add_course(request):

    if request.method == "POST":

        form = CourseForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            messages.success(request,"Cours ajouté avec succès")

            return redirect('courses')

    else:

        form = CourseForm()

    return render(request, 'add_course_form.html', {'form': form})


# ==============================
# MODIFIER COURS
# ==============================

@login_required
@user_passes_test(is_admin)
def update_course(request, id):

    course = get_object_or_404(Course, id=id)

    form = CourseForm(request.POST or None, request.FILES or None, instance=course)

    if form.is_valid():

        form.save()

        return redirect('courses')

    return render(request, 'course_form.html', {'form': form})


# ==============================
# SUPPRIMER COURS
# ==============================

@login_required
@user_passes_test(is_admin)
def delete_course(request, id):

    course = get_object_or_404(Course, id=id)

    course.delete()

    return redirect('courses')


# ==============================
# INSCRIPTION COURS
# ==============================

@login_required
def enroll_course(request, id):

    course = get_object_or_404(Course, id=id)

    Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )

    return redirect('courses')


# ==============================
# COMPLETER LESSON
# ==============================

@login_required
def complete_lesson(request, id):

    lesson = get_object_or_404(Lesson, id=id)

    Progress.objects.update_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'completed': True}
    )

    return redirect('dashboard')


# ==============================
# AJOUTER LESSON
# ==============================


@login_required
@user_passes_test(is_admin)
def add_lesson(request):

    if request.method == "POST":

        form = LessonForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('courses')

    else:

        form = LessonForm()

    return render(request, 'add_lesson.html', {'form': form})



def lesson_detail(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    return render(request, 'lesson_detail.html', {'lesson': lesson})



# ==============================
# CERTIFICAT
# ==============================

@login_required

def certificates(request):
    # Exemple : récupérer tous les certificats de l'utilisateur
    user_certificates = Certificate.objects.filter(user=request.user)
    return render(request, 'certificates.html', {'certificates': user_certificates})


# def certificates(request, course_id):

#     course = get_object_or_404(Course, id=course_id)

#     Certificate.objects.get_or_create(
#         user=request.user,
#         course=course
#     )

#     return render(request, 'certificates.html', {
#         'course': course
#     })


# ==============================
# COMMENTAIRE
# ==============================

@login_required
def add_comment(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":

        text = request.POST.get('text')

        if text:

            Comment.objects.create(
                user=request.user,
                course=course,
                text=text
            )

    return redirect('courses')


# ==============================
# LESSONS
# ==============================

def all_lessons(request):

    lessons = Lesson.objects.all()

    return render(request, 'lessons_list.html', {'lessons': lessons})


@login_required
@user_passes_test(is_admin)
def update_lesson(request, id):

    lesson = get_object_or_404(Lesson, id=id)

    form = LessonForm(request.POST or None, request.FILES or None, instance=lesson)

    if form.is_valid():

        form.save()

        return redirect('courses')

    return render(request,'lesson_form.html',{'form':form})


@login_required
@user_passes_test(is_admin)
def delete_lesson(request, id):

    lesson = get_object_or_404(Lesson, id=id)

    lesson.delete()

    return redirect('courses')


@login_required
def lesson_list(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    lessons = Lesson.objects.filter(course=course)

    return render(request, 'lesson_list.html', {'course': course, 'lessons': lessons})


def lesson_detail(request, id):

    lesson = get_object_or_404(Lesson, id=id)

    lessons = Lesson.objects.filter(course=lesson.course)

    next_lesson = Lesson.objects.filter(
        course=lesson.course,
        id__gt=lesson.id
    ).order_by('id').first()

    context = {
        'lesson': lesson,
        'lessons': lessons,
        'next_lesson': next_lesson
    }

    return render(request, 'lesson_detail.html', context)


# ==============================
# ADMIN DASHBOARD
# ==============================

@login_required
@user_passes_test(is_admin)
def dashboard_admin(request):

    courses_count = Course.objects.count()
    users_count = User.objects.count()
    lessons_count = Lesson.objects.count()

    context = {
        'courses_count': courses_count,
        'users_count': users_count,
        'lessons_count': lessons_count
    }

    return render(request, 'dashboard_admin.html', context)


def manage_users(request):

    users = User.objects.all()

    return render(request, 'users.html', {'users': users})


# ==============================
# ABOUT
# ==============================

def about(request):

    return render(request, 'about.html')


# ==============================
# CONTACT
# ==============================

def contact(request):

    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:

            subject = f"Message de contact de {name}"

            full_message = f"Nom:{name}\nEmail:{email}\n\nMessage:{message}"

            recipient_list = [settings.DEFAULT_FROM_EMAIL]

            try:

                send_mail(subject, full_message, settings.DEFAULT_FROM_EMAIL, recipient_list)

                messages.success(request,"Message envoyé")

            except BadHeaderError:

                messages.error(request,"Erreur email")

            return redirect('contact')

    return render(request,'contact.html')


# ==============================
# PROGRESS
# ==============================

def progress(request):
    return render(request, 'progress.html')



# ==============================
# RECENT ACTIVITY
# ==============================

def recent_activity(request):
    """
    Page qui affiche les activités récentes de l'utilisateur.
    """

    return render(request, 'recent_activity.html')


# ==============================
# NOTIFICATIONS
# ==============================

def notifications(request):
    """
    Page qui affiche les notifications de l'utilisateur.
    """
    return render(request, 'notifications.html')


# ==============================
# MANAGE CATEGORIES
# ==============================
def manage_categories(request):
    """Gérer les catégories du site"""
    return render(request, 'manage_categories.html')



# ==============================
# UPLOAD RESOURCES
# ==============================
def upload_resources(request):
    """Page pou telechaje resous pou kou yo"""
    return render(request, 'upload_resources.html')


def review_feedback(request):
    return render(request, 'review_feedback.html')

def system_settings(request):
    return render(request, 'system_settings.html')


# ---------------- SEARCH ----------------
def search_courses(request):
    return render(request, 'search_courses.html')




from django.shortcuts import render

def continue_learning(request):
    return render(request, 'continue_learning.html')

def my_certificates(request):
    return render(request, 'my_certificates.html')

def my_progress(request):
    return render(request, 'my_progress.html')

def browse_courses(request):
    return render(request, 'browse_courses.html')

def download_pdfs(request):
    return render(request, 'download_pdfs.html')

def watch_tutorials(request):
    return render(request, 'watch_tutorials.html')

def practice_exercises(request):
    return render(request, 'practice_exercises.html')

def study_guides(request):
    return render(request, 'study_guides.html')

def discussion_forum(request):
    return render(request, 'discussion_forum.html')

def study_groups(request):
    return render(request, 'study_groups.html')

def learning_challenges(request):
    return render(request, 'learning_challenges.html')

def help_center(request):
    return render(request, 'help_center.html')

def report_issue(request):
    return render(request, 'report_issue.html')

def contact_support(request):
    return render(request, 'contact_support.html')

def faq(request):
    return render(request, 'faq.html')

def edit_profile(request):
    return render(request, 'edit_profile.html')

def change_password(request):
    return render(request, 'change_password.html')





def active_challenge(request):
    # Récupère tous les défis actifs
    challenges = Challenge.objects.filter(is_active=True)
    return render(request, 'active_challenges.html', {'challenges': challenges})



@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès !")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user.profile)

    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'profile.html', context)
