"""
Service de gestion des consultants
CRUD operations pour les consultants avec la base de données
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database.database import get_database_session
from app.database.models import Consultant


class ConsultantService:
    """Service pour la gestion des consultants"""
    
    @staticmethod
    def get_all_consultants(page: int = 1, per_page: int = 20) -> List[Consultant]:
        """Récupère tous les consultants avec pagination"""
        try:
            with get_database_session() as session:
                return session.query(Consultant)\
                    .offset((page - 1) * per_page)\
                    .limit(per_page)\
                    .all()
        except Exception as e:
            print(f"Erreur lors de la récupération des consultants: {e}")
            return []
    
    @staticmethod
    def get_consultant_by_id(consultant_id: int) -> Optional[Consultant]:
        """Récupère un consultant par son ID"""
        try:
            with get_database_session() as session:
                return session.query(Consultant).filter(Consultant.id == consultant_id).first()
        except Exception as e:
            print(f"Erreur lors de la récupération du consultant {consultant_id}: {e}")
            return None
    
    @staticmethod
    def create_consultant(data: dict) -> bool:
        """Crée un nouveau consultant"""
        try:
            with get_database_session() as session:
                consultant = Consultant(
                    prenom=data.get('prenom'),
                    nom=data.get('nom'),
                    email=data.get('email'),
                    telephone=data.get('telephone'),
                    salaire_actuel=data.get('salaire'),  # Corrigé: salaire_actuel au lieu de salaire
                    disponibilite=data.get('disponible', True),  # Corrigé: disponibilite au lieu de disponible
                    notes=data.get('notes'),
                    date_creation=datetime.now(),
                    derniere_maj=datetime.now()  # Corrigé: derniere_maj au lieu de date_mise_a_jour
                )
                
                session.add(consultant)
                session.commit()
                print(f"✅ Consultant {data.get('prenom')} {data.get('nom')} créé avec succès")
                return True
                
        except Exception as e:
            print(f"❌ Erreur lors de la création du consultant: {e}")
            return False
    
    @staticmethod
    def update_consultant(consultant_id: int, data: dict) -> bool:
        """Met à jour un consultant existant"""
        try:
            with get_database_session() as session:
                consultant = session.query(Consultant).filter(Consultant.id == consultant_id).first()
                
                if not consultant:
                    print(f"❌ Consultant avec l'ID {consultant_id} non trouvé")
                    return False
                
                # Mapping des attributs pour éviter les erreurs
                attribute_mapping = {
                    'salaire': 'salaire_actuel',
                    'disponible': 'disponibilite',
                    'date_mise_a_jour': 'derniere_maj'
                }
                
                # Mise à jour des champs
                for key, value in data.items():
                    # Utiliser le mapping si nécessaire
                    attr_name = attribute_mapping.get(key, key)
                    
                    if hasattr(consultant, attr_name):
                        setattr(consultant, attr_name, value)
                    else:
                        print(f"⚠️ Attribut {attr_name} non trouvé sur le modèle Consultant")
                
                consultant.derniere_maj = datetime.now()
                session.commit()
                print(f"✅ Consultant {consultant_id} mis à jour avec succès")
                return True
                
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour du consultant: {e}")
            return False
    
    @staticmethod
    def delete_consultant(consultant_id: int) -> bool:
        """Supprime un consultant"""
        try:
            with get_database_session() as session:
                consultant = session.query(Consultant).filter(Consultant.id == consultant_id).first()
                
                if not consultant:
                    print(f"❌ Consultant avec l'ID {consultant_id} non trouvé")
                    return False
                
                print(f"🔄 Suppression en cours du consultant {consultant.prenom} {consultant.nom} (ID: {consultant_id})")
                session.delete(consultant)
                session.commit()
                print(f"✅ Consultant {consultant_id} supprimé avec succès")
                return True
                
        except Exception as e:
            print(f"❌ Erreur lors de la suppression du consultant {consultant_id}: {e}")
            print(f"Type d'erreur: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return False
    
    @staticmethod
    def search_consultants(search_term: str) -> List[Consultant]:
        """Recherche des consultants par nom, prénom ou email"""
        try:
            with get_database_session() as session:
                return session.query(Consultant)\
                    .filter(
                        (Consultant.nom.ilike(f"%{search_term}%")) |
                        (Consultant.prenom.ilike(f"%{search_term}%")) |
                        (Consultant.email.ilike(f"%{search_term}%"))
                    )\
                    .all()
        except Exception as e:
            print(f"Erreur lors de la recherche: {e}")
            return []
    
    @staticmethod
    def get_consultants_count() -> int:
        """Retourne le nombre total de consultants"""
        try:
            with get_database_session() as session:
                return session.query(Consultant).count()
        except Exception as e:
            print(f"Erreur lors du comptage des consultants: {e}")
            return 0
    
    @staticmethod
    def get_available_consultants() -> List[Consultant]:
        """Retourne les consultants disponibles"""
        try:
            with get_database_session() as session:
                return session.query(Consultant)\
                    .filter(Consultant.disponibilite == True)\
                    .all()
        except Exception as e:
            print(f"Erreur lors de la récupération des consultants disponibles: {e}")
            return []
