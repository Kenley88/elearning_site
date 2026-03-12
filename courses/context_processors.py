# courses/context_processors.py

def register_form(request):
    from .forms import RegisterForm  # import à l'intérieur de la fonction pour éviter les erreurs
    return {'register_form': RegisterForm()}