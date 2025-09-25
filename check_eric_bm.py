"""
Script pour vérifier si Eric Lapina existe comme Business Manager
"""

from app.database.database import get_database_session
from app.database.models import BusinessManager

def check_eric_lapina_bm():
    """Vérifie si Eric Lapina existe comme Business Manager"""

    with get_database_session() as session:
        # Chercher Eric Lapina comme Business Manager
        eric_bm = session.query(BusinessManager).filter(
            BusinessManager.email == 'eric.lapina@quanteam.fr'
        ).first()

        if eric_bm:
            print('✅ Eric Lapina existe comme Business Manager:')
            print(f'  ID: {eric_bm.id}')
            print(f'  Nom: {eric_bm.nom_complet}')
            print(f'  Email: {eric_bm.email}')
            print(f'  Actif: {eric_bm.actif}')

            # Vérifier s'il a des consultants
            consultants_count = len(eric_bm.consultants_actuels)
            print(f'  Nombre de consultants: {consultants_count}')

            if consultants_count > 0:
                print('  Liste des consultants:')
                for c in eric_bm.consultants_actuels:
                    print(f'    - {c.prenom} {c.nom} ({c.email})')
        else:
            print('❌ Eric Lapina n\'existe pas comme Business Manager dans la base de données')

            # Lister tous les BM pour voir
            print('\n📋 Liste de tous les Business Managers:')
            all_bms = session.query(BusinessManager).all()
            for bm in all_bms:
                print(f'  {bm.nom_complet} ({bm.email})')

if __name__ == "__main__":
    check_eric_lapina_bm()