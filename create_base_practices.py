"""
Script pour créer des pratiques de base
"""

from datetime import datetime

from app.database.database import get_database_session
from app.database.models import Practice


def create_base_practices():
    """Crée des pratiques de base si elles n'existent pas"""

    # Créer quelques pratiques de base
    practices_data = [
        {
            "nom": "Data & Analytics",
            "description": "Expertise en data science, BI, analytics",
        },
        {
            "nom": "Digital & Innovation",
            "description": "Transformation digitale, innovation",
        },
        {
            "nom": "Finance & Risk",
            "description": "Finance, risk management, compliance",
        },
        {
            "nom": "IT & Infrastructure",
            "description": "Architecture IT, cloud, infrastructure",
        },
        {
            "nom": "Management & Strategy",
            "description": "Conseil en management, stratégie",
        },
        {
            "nom": "Operations & Supply Chain",
            "description": "Optimisation opérationnelle, supply chain",
        },
        {
            "nom": "RH & Organisation",
            "description": "Ressources humaines, organisation",
        },
        {"nom": "Sales & Marketing", "description": "Commercial, marketing, CRM"},
    ]

    with get_database_session() as session:
        for practice_data in practices_data:
            # Vérifier si la pratique existe déjà
            existing = (
                session.query(Practice)
                .filter(Practice.nom == practice_data["nom"])
                .first()
            )
            if not existing:
                practice = Practice(
                    nom=practice_data["nom"],
                    description=practice_data["description"],
                    actif=True,
                    date_creation=datetime.now(),
                )
                session.add(practice)
                print(f'✅ Créé: {practice_data["nom"]}')
            else:
                print(f'⏭️ Existe déjà: {practice_data["nom"]}')

        session.commit()

    print("\n🏢 Pratiques créées avec succès !")


if __name__ == "__main__":
    create_base_practices()
