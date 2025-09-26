"""
Script pour mapper les sociétés aux pratiques
"""

from sqlalchemy import func

from app.database.database import get_database_session
from app.database.models import Consultant
from app.database.models import Practice


def get_societe_practice_mapping():
    """
    Retourne un mapping suggéré société -> practice basé sur les noms
    """
    # Mapping suggéré basé sur les noms des sociétés
    mapping = {
        # QUANTEAM et ses filiales
        "QUANTEAM": "Management & Strategy",
        "QUANTEAM PORTUGAL": "Management & Strategy",
        "QUANTEAM US": "Management & Strategy",
        "QUANTEAM CANADA": "Management & Strategy",
        "QUANTEAM LUXEMBOURG": "Management & Strategy",
        "QUANTEAM SINGAPORE": "Management & Strategy",
        "QUANTEAM SPRL": "Management & Strategy",
        "QUANTEAM SWITZERLAND": "Management & Strategy",
        # Sociétés spécialisées Data/Analytics
        "QUANT FACTORY": "Data & Analytics",
        "QUANTLABS": "Data & Analytics",
        "GRADIANT": "Data & Analytics",
        # Sociétés IT/Infrastructure
        "ASIGMA": "IT & Infrastructure",
        "ASIGMA CANADA": "IT & Infrastructure",
        # Sociétés Digital/Innovation
        "AYBO": "Digital & Innovation",
        "RAINBOW PARTNERS": "Digital & Innovation",
        "RAINBOW LYON": "Digital & Innovation",
        # Sociétés Finance/Risk
        "CERES ADVISORY": "Finance & Risk",
        # Sociétés Operations/Supply Chain
        "NEOBUY": "Operations & Supply Chain",
        "NEOBUY LYON": "Operations & Supply Chain",
        "OHANA CONSEIL": "Operations & Supply Chain",
        # Business Units (BU)
        "BU DIRECTION QUANTEAM": "Management & Strategy",
        "BU LOZ": "Management & Strategy",
        "BU SAW": "Management & Strategy",
        "BU TGI": "Management & Strategy",
        "BU TVI": "Management & Strategy",
        # Business Managers (les classer comme Management)
        "BUSINESS MANAGERS ARCHINOV": "Management & Strategy",
        "BUSINESS MANAGERS ASIGMA": "Management & Strategy",
        "BUSINESS MANAGERS AYBO": "Management & Strategy",
        "BUSINESS MANAGERS GRADIANT": "Management & Strategy",
        "BUSINESS MANAGERS NEOBUY": "Management & Strategy",
        "BUSINESS MANAGERS NEOBUY LYON": "Management & Strategy",
        "BUSINESS MANAGERS OHANA": "Management & Strategy",
        "BUSINESS MANAGERS QUANTEAM CANADA": "Management & Strategy",
        "BUSINESS MANAGERS QUANTEAM LUXEMBOURG": "Management & Strategy",
        "BUSINESS MANAGERS QUANTEAM PORTUGAL": "Management & Strategy",
        "BUSINESS MANAGERS RAINBOW LYON": "Management & Strategy",
        # Autres
        "KEEP CONSULTING": "Management & Strategy",
    }

    return mapping


def apply_practice_mapping():
    """
    Applique le mapping société -> practice aux consultants
    """
    print("🚀 Début du mapping sociétés -> pratiques")

    # Obtenir le mapping
    mapping = get_societe_practice_mapping()

    with get_database_session() as session:
        # Lister toutes les sociétés dans la base
        societes = (
            session.query(Consultant.societe, func.count(Consultant.id))
            .group_by(Consultant.societe)
            .all()
        )

        print("🏢 Mapping des sociétés aux pratiques:")
        mapped_count = 0
        total_consultants = 0

        for societe, count in societes:
            total_consultants += count

            # Trouver la pratique correspondante
            practice_name = mapping.get(societe.strip())

            if practice_name:
                # Trouver l'ID de la pratique
                practice = (
                    session.query(Practice)
                    .filter(Practice.nom == practice_name)
                    .first()
                )

                if practice:
                    # Mettre à jour tous les consultants de cette société
                    updated = (
                        session.query(Consultant)
                        .filter(Consultant.societe == societe)
                        .update({"practice_id": practice.id})
                    )
                    mapped_count += updated
                    print(f"  ✅ {societe}: {count} consultants -> {practice_name}")
                else:
                    print(f"  ❌ {societe}: Pratique '{practice_name}' introuvable")
            else:
                print(f"  ⚠️ {societe}: {count} consultants - Aucune pratique mappée")

        session.commit()

        print(f"\n📊 Résultats du mapping:")
        print(f"  👥 Total consultants: {total_consultants}")
        print(f"  ✅ Consultants mappés: {mapped_count}")
        print(f"  ⚠️ Consultants non mappés: {total_consultants - mapped_count}")

        print("\n🎉 Mapping terminé !")


def show_unmapped_societes():
    """
    Affiche les sociétés qui n'ont pas été mappées
    """
    print("📋 Sociétés non mappées:")

    mapping = get_societe_practice_mapping()

    with get_database_session() as session:
        societes = (
            session.query(Consultant.societe, func.count(Consultant.id))
            .group_by(Consultant.societe)
            .all()
        )

        unmapped = []
        for societe, count in societes:
            if societe.strip() not in mapping:
                unmapped.append((societe, count))

        if unmapped:
            for societe, count in unmapped:
                print(f"  {societe}: {count} consultants")
        else:
            print("  ✅ Toutes les sociétés sont mappées !")


if __name__ == "__main__":
    # Afficher d'abord les sociétés non mappées
    show_unmapped_societes()
    print()

    # Appliquer le mapping
    apply_practice_mapping()
