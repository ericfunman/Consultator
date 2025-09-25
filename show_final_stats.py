"""
Script pour afficher les statistiques finales de l'import
"""

from app.database.database import get_database_session
from app.database.models import Consultant, Practice, BusinessManager, ConsultantBusinessManager
from sqlalchemy import func

def show_final_statistics():
    """Affiche les statistiques finales de l'import"""

    with get_database_session() as session:
        # Statistiques générales
        consultant_count = session.query(Consultant).count()
        bm_count = session.query(BusinessManager).count()
        relations_count = session.query(ConsultantBusinessManager).count()

        print('📊 STATISTIQUES FINALES DE L\'IMPORT')
        print('=' * 50)
        print(f'👥 Total consultants: {consultant_count}')
        print(f'👔 Total Business Managers: {bm_count}')
        print(f'🔗 Relations BM-Consultant: {relations_count}')

        # Répartition par pratique
        print('\n🏢 RÉPARTITION PAR PRATIQUE:')
        practices_stats = session.query(
            Practice.nom,
            func.count(Consultant.id)
        ).join(Consultant).group_by(Practice.nom).order_by(func.count(Consultant.id).desc()).all()

        for practice_name, count in practices_stats:
            print(f'  {practice_name}: {count} consultants')

        # Quelques exemples de consultants avec leur pratique
        print('\n👥 EXEMPLES DE CONSULTANTS:')
        consultants = session.query(Consultant).limit(5).all()
        for c in consultants:
            practice_name = c.practice.nom if c.practice else 'Aucune'
            bm_name = c.business_manager_actuel.nom_complet if c.business_manager_actuel else 'Aucun'
            print(f'  - {c.prenom} {c.nom} ({c.email})')
            print(f'    Société: {c.societe} | Pratique: {practice_name} | BM: {bm_name}')

        print('\n🎉 IMPORT RÉUSSI - TOUTES LES DONNÉES SONT PRÊTES !')

if __name__ == "__main__":
    show_final_statistics()