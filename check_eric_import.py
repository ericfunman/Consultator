"""
Script pour vérifier qu'Eric Lapina a été importé comme consultant
"""

from app.database.database import get_database_session
from app.database.models import Consultant


def check_eric_lapina_import():
    """Vérifie qu'Eric Lapina a bien été importé comme consultant"""

    with get_database_session() as session:
        # Chercher Eric Lapina comme consultant
        eric_consultant = (
            session.query(Consultant)
            .filter(Consultant.email == "eric.lapina@quanteam.fr")
            .first()
        )

        if eric_consultant:
            print("✅ Eric Lapina trouvé comme consultant:")
            print(f"  ID: {eric_consultant.id}")
            print(f"  Nom: {eric_consultant.nom_complet}")
            print(f"  Email: {eric_consultant.email}")
            print(f"  Société: {eric_consultant.societe}")
            print(
                f'  Pratique: {eric_consultant.practice.nom if eric_consultant.practice else "Aucune"}'
            )
            print(f"  Type contrat: {eric_consultant.type_contrat}")
            print(f"  Salaire: {eric_consultant.salaire_actuel}")
            print(
                f'  Business Manager: {eric_consultant.business_manager_actuel.nom_complet if eric_consultant.business_manager_actuel else "Aucun"}'
            )
        else:
            print("❌ Eric Lapina toujours pas trouvé comme consultant")


if __name__ == "__main__":
    check_eric_lapina_import()
