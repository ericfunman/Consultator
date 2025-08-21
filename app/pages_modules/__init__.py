"""
Module pages de Consultator
Contient toutes les pages de l'application Streamlit
"""

# Import des pages principales
from . import consultants
from . import home
from . import missions
from . import skills
from . import technologies

__all__ = ["home", "consultants", "skills", "missions", "technologies"]
