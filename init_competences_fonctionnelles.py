"""
Script pour initialiser les compÃ©tences fonctionnelles bancaire/assurance
Lance ce script pour peupler la base avec le rÃ©fÃ©rentiel compÃ©tences fonctionnelles
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import SessionLocal
from app.database.models import Competence
from app.utils.skill_categories import COMPETENCES_FONCTIONNELLES


def init_competences_fonctionnelles():
    """Initialise les compÃ©tences fonctionnelles dans la base de donnÃ©es"""

    session = SessionLocal()

    try:
        print("ð¦ Initialisation des compÃ©tences fonctionnelles bancaire/assurance...")

        # Compter les compÃ©tences fonctionnelles existantes
        existing_func = (
            session.query(Competence)
            .filter(Competence.type_competence == "fonctionnelle")
            .count()
        )

        print(f"ð CompÃ©tences fonctionnelles existantes: {existing_func}")

        competences_ajoutees = 0
        competences_existantes = 0

        # Parcourir toutes les catÃ©gories fonctionnelles
        for categorie, competences_list in COMPETENCES_FONCTIONNELLES.items():
            print(f"\nð CatÃ©gorie: {categorie}")

            for competence_nom in competences_list:
                # VÃ©rifier si la compÃ©tence existe dÃ©jÃ
                existing = (
                    session.query(Competence)
                    .filter(
                        Competence.nom == competence_nom,
                        Competence.type_competence == "fonctionnelle",
                    )
                    .first()
                )

                if not existing:
                    # CrÃ©er la nouvelle compÃ©tence fonctionnelle
                    nouvelle_competence = Competence(
                        nom=competence_nom,
                        categorie=categorie,
                        type_competence="fonctionnelle",
                        description=f"CompÃ©tence fonctionnelle en {competence_nom.lower()}",
                        niveau_requis="junior",
                    )

                    session.add(nouvelle_competence)
                    competences_ajoutees += 1
                    print(f"   â AjoutÃ©: {competence_nom}")
                else:
                    competences_existantes += 1
                    print(f"   â ï¸ Existe dÃ©jÃ : {competence_nom}")

        # Sauvegarder les changements
        session.commit()

        print("\nð¯ RÃ©sumÃ© de l'initialisation:")
        print(f"   â CompÃ©tences ajoutÃ©es: {competences_ajoutees}")
        print(f"   â ï¸ CompÃ©tences existantes: {competences_existantes}")
        print(f"   ð Total traitÃ©: {competences_ajoutees + competences_existantes}")

        # VÃ©rification finale
        total_fonctionnelles = (
            session.query(Competence)
            .filter(Competence.type_competence == "fonctionnelle")
            .count()
        )

        print(f"\nð Total compÃ©tences fonctionnelles en base: {total_fonctionnelles}")

        # Afficher quelques exemples par catÃ©gorie
        print("\nð AperÃ§u des catÃ©gories crÃ©Ã©es:")
        for categorie in COMPETENCES_FONCTIONNELLES.keys():
            count = (
                session.query(Competence)
                .filter(
                    Competence.categorie == categorie,
                    Competence.type_competence == "fonctionnelle",
                )
                .count()
            )
            print(f"   â¢ {categorie}: {count} compÃ©tences")

        print("\nð Initialisation terminÃ©e avec succÃ¨s!")

    except Exception as e:
        print(f"â Erreur lors de l'initialisation: {e}")
        session.rollback()
        raise
    finally:
        session.close()


def show_competences_summary():
    """Affiche un rÃ©sumÃ© des compÃ©tences en base"""
    session = SessionLocal()

    try:
        print("\nð RÃSUMÃ DES COMPÃTENCES EN BASE:")
        print("=" * 50)

        # CompÃ©tences techniques
        tech_count = (
            session.query(Competence)
            .filter(Competence.type_competence == "technique")
            .count()
        )
        print(f"ð§ CompÃ©tences techniques: {tech_count}")

        # CompÃ©tences fonctionnelles
        func_count = (
            session.query(Competence)
            .filter(Competence.type_competence == "fonctionnelle")
            .count()
        )
        print(f"ð¦ CompÃ©tences fonctionnelles: {func_count}")

        # Total
        total = session.query(Competence).count()
        print(f"ð Total compÃ©tences: {total}")

        # DÃ©tail des catÃ©gories fonctionnelles
        print("\nð¦ DÃTAIL COMPÃTENCES FONCTIONNELLES:")
        print("-" * 40)

        categories_func = (
            session.query(Competence.categorie)
            .filter(Competence.type_competence == "fonctionnelle")
            .distinct()
            .all()
        )

        for (categorie,) in categories_func:
            count = (
                session.query(Competence)
                .filter(
                    Competence.categorie == categorie,
                    Competence.type_competence == "fonctionnelle",
                )
                .count()
            )
            print(f"   â¢ {categorie}: {count}")

            # Afficher quelques exemples
            exemples = (
                session.query(Competence.nom)
                .filter(
                    Competence.categorie == categorie,
                    Competence.type_competence == "fonctionnelle",
                )
                .limit(3)
                .all()
            )

            for (nom,) in exemples:
                print(f"     - {nom}")

            if count > 3:
                print(f"     ... et {count - 3} autres")
            print()

    finally:
        session.close()


if __name__ == "__main__":
    print("ð INITIALISATION COMPÃTENCES FONCTIONNELLES")
    print("=" * 60)

    # Initialiser les compÃ©tences
    init_competences_fonctionnelles()

    # Afficher le rÃ©sumÃ©
    show_competences_summary()

    print("\nâ¨ Script terminÃ©!")
