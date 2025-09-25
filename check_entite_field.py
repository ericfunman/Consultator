"""
Script pour vérifier le champ entite après import
"""

from app.database.database import get_database_session
from app.database.models import Consultant

def check_entite_field():
    """Vérifie que le champ entite a été correctement importé"""

    with get_database_session() as session:
        # Chercher Eric Lapina
        eric = session.query(Consultant).filter(
            Consultant.email == 'eric.lapina@quanteam.fr'
        ).first()

        if eric:
            print('✅ Eric Lapina trouvé avec le nouveau champ entite:')
            print(f'  Nom: {eric.nom_complet}')
            print(f'  Email: {eric.email}')
            print(f'  Société: {eric.societe}')
            print(f'  Entité: {eric.entite}')
            print(f'  Pratique: {eric.practice.nom if eric.practice else "Aucune"}')
        else:
            print('❌ Eric Lapina non trouvé')

        # Vérifier quelques autres consultants avec leur entité
        print('\n📋 Exemples de consultants avec leur entité:')
        consultants = session.query(Consultant).limit(5).all()
        for c in consultants:
            print(f'  {c.prenom} {c.nom}: Société={c.societe}, Entité={c.entite}')

if __name__ == "__main__":
    check_entite_field()