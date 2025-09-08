"""
Module pages de Consultator
Contient toutes les pages de l'application Streamlit
"""

# Import des pages principales avec gestion d'erreurs
home = None
consultants = None
technologies = None
practices = None
business_managers = None
chatbot = None

try:
    from . import home
except Exception as e:
    print(f"Erreur import home: {e}")

try:
    from . import consultants
except Exception:
    try:
        from . import consultant_profile as consultants
    except Exception as e:
        print(f"Erreur import consultants: {e}")

try:
    from . import technologies
except Exception as e:
    print(f"Erreur import technologies: {e}")

try:
    from . import practices
except Exception as e:
    print(f"Erreur import practices: {e}")

try:
    from . import business_managers
except Exception as e:
    print(f"Erreur import business_managers: {e}")

try:
    from . import chatbot
except Exception as e:
    print(f"Erreur import chatbot: {e}")

__all__ = [
    "home",
    "consultants",
    "technologies",
    "practices",
    "business_managers",
    "chatbot",
]
