#!/usr/bin/env python3
"""
Script pour migrer Laurence Oziel de Consultant vers Business Manager
"""

from datetime import datetime

from app.database.database import get_database_session
from app.database.models import BusinessManager, Consultant, ConsultantBusinessManager


def migrate_laurence_to_business_manager():
    """
    Migre Laurence Oziel de la table Consultant vers BusinessManager
    """
    print("🔄 Migration de Laurence Oziel vers Business Manager...")
    
    with get_database_session() as session:
        # Trouver Laurence dans la table Consultant
        laurence_consultant = session.query(Consultant).filter(
            Consultant.prenom.ilike('%laurence%'),
            Consultant.nom.ilike('%oziel%')
        ).first()
        
        if not laurence_consultant:
            print("❌ Laurence Oziel non trouvée dans la table Consultant")
            return False
        
        print(f"✅ Laurence trouvée: {laurence_consultant.prenom} {laurence_consultant.nom}")
        
        # Vérifier si elle n'existe pas déjà comme BM
        existing_bm = session.query(BusinessManager).filter(
            BusinessManager.email == laurence_consultant.email
        ).first()
        
        if existing_bm:
            print("⚠️ Laurence existe déjà comme Business Manager")
            return True
        
        # Créer l'entrée Business Manager
        laurence_bm = BusinessManager(
            nom=laurence_consultant.nom,
            prenom=laurence_consultant.prenom,
            email=laurence_consultant.email,
            telephone=laurence_consultant.telephone,
            actif=True,
            date_creation=datetime.now()
        )
        
        session.add(laurence_bm)
        session.flush()  # Pour obtenir l'ID
        
        print(f"✅ Business Manager créé avec ID: {laurence_bm.id}")
        
        # Vérifier s'il y a des consultants qui ont Laurence comme manager dans Excel
        # On va chercher dans la table Consultant si quelqu'un a "Laurence OZIEL" comme manager
        
        # Note: Cette information n'est pas directement stockée, 
        # mais on peut vérifier les relations ConsultantBusinessManager existantes
        
        session.commit()
        
        print("✅ Migration réussie !")
        print(f"📊 Laurence OZIEL est maintenant Business Manager (ID: {laurence_bm.id})")
        
        return True


def check_consultants_managed_by_laurence():
    """
    Vérifie si des consultants sont gérés par Laurence en analysant les données source
    """
    print("\n🔍 Recherche des consultants gérés par Laurence...")
    
    with get_database_session() as session:
        # Chercher les consultants qui pourraient être gérés par Laurence
        # Cela nécessiterait d'analyser le fichier Excel original
        # Pour l'instant, on peut vérifier manuellement
        
        # Compter les BM actuels
        total_bm = session.query(BusinessManager).count()
        print(f"📊 Total Business Managers après migration: {total_bm}")
        
        # Vérifier Laurence BM
        laurence_bm = session.query(BusinessManager).filter(
            BusinessManager.email == 'laurence.oziel@quanteam.fr'
        ).first()
        
        if laurence_bm:
            print(f"✅ Laurence OZIEL est bien dans BusinessManager (ID: {laurence_bm.id})")
        else:
            print("❌ Laurence non trouvée dans BusinessManager")


if __name__ == "__main__":
    print("🚀 Script de migration Laurence Oziel")
    print("=" * 50)
    
    try:
        success = migrate_laurence_to_business_manager()
        if success:
            check_consultants_managed_by_laurence()
            
            print("\n💡 Étapes suivantes:")
            print("1. Vérifier dans l'interface VSA si Laurence apparaît maintenant")
            print("2. Si des consultants sont sous sa responsabilité, les associer manuellement")
            print("3. Vérifier le fichier Excel source pour identifier ses consultants")
            
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        raise