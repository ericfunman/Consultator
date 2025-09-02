"""
Module pages de Consultator
Contient toutes les pages de l'application Streamlit
"""

# Import des pages principales
from . import home
from . import consultant_profile as consultants
from . import technologies
from . import practices
from . import business_managers
from . import chatbot

__all__ = ['home', 'consultants', 'technologies', 'practices', 'business_managers', 'chatbot']
