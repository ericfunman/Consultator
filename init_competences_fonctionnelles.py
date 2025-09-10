"""
Script pour initialiser les compétences fonctionnelles bancaire/assurance
Lance ce script pour peupler la base avec le référentiel compétences fonctionnelles
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import SessionLocal
from app.database.models import Competence
from app.utils.skill_categories import COMPETENCES_FONCTIONNELLES


def init_competences_fonctionnelles():
    """Initialise les compétences fonctionnelles dans la base de données"""

    session = SessionLocal()

    try:
        print("🏦 Initialisation des compétences fonctionnelles bancaire/assurance...")

        # Compter les compétences fonctionnelles existantes
        existing_func = (
            session.query(Competence)
            .filter(Competence.type_competence == "fonctionnelle")
            .count()
        )

        print(f"📊 Compétences fonctionnelles existantes: {existing_func}")

        competences_ajoutees = 0
        competences_existantes = 0

        # Parcourir toutes les catégories fonctionnelles
        for categorie, competences_list in COMPETENCES_FONCTIONNELLES.items():
            print(f"\n📂 Catégorie: {categorie}")

            for competence_nom in competences_list:
                # Vérifier si la compétence existe déjà
                existing = (
                    session.query(Competence)
                    .filter(
                        Competence.nom == competence_nom,
                        Competence.type_competence == "fonctionnelle",
                    )
                    .first()
                )

                if not existing:
                    # Créer la nouvelle compétence fonctionnelle
                    nouvelle_competence = Competence(
                        nom=competence_nom,
                        categorie=categorie,
                        type_competence="fonctionnelle",
                        description=f"Compétence fonctionnelle en {competence_nom.lower()}",
                        niveau_requis="junior",
                    )

                    session.add(nouvelle_competence)
                    competences_ajoutees += 1
                    print(f"   ✅ Ajouté: {competence_nom}")
                else:
                    competences_existantes += 1
                    print(f"   ⚠️ Existe déjà: {competence_nom}")

        # Sauvegarder les changements
        session.commit()

        print("\n🎯 Résumé de l'initialisation:")
        print(f"   ✅ Compétences ajoutées: {competences_ajoutees}")
        print(f"   ⚠️ Compétences existantes: {competences_existantes}")
        print(f"   📊 Total traité: {competences_ajoutees + competences_existantes}")

        # Vérification finale
        total_fonctionnelles = (
            session.query(Competence)
            .filter(Competence.type_competence == "fonctionnelle")
            .count()
        )

        print(f"\n📈 Total compétences fonctionnelles en base: {total_fonctionnelles}")

        # Afficher quelques exemples par catégorie
        print("\n📋 Aperçu des catégories créées:")
        for categorie in COMPETENCES_FONCTIONNELLES.keys():
            count = (
                session.query(Competence)
                .filter(
                    Competence.categorie == categorie,
                    Competence.type_competence == "fonctionnelle",
                )
                .count()
            )
            print(f"   • {categorie}: {count} compétences")

        print("\n🎉 Initialisation terminée avec succès!")

    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        session.rollback()
        raise
    finally:
        session.close()


def show_competences_summary():
    """Affiche un résumé des compétences en base"""
    session = SessionLocal()

    try:
        print("\n📊 RÉSUMÉ DES COMPÉTENCES EN BASE:")
        print("=" * 50)

        # Compétences techniques
        tech_count = (
            session.query(Competence)
            .filter(Competence.type_competence == "technique")
            .count()
        )
        print(f"🔧 Compétences techniques: {tech_count}")

        # Compétences fonctionnelles
        func_count = (
            session.query(Competence)
            .filter(Competence.type_competence == "fonctionnelle")
            .count()
        )
        print(f"🏦 Compétences fonctionnelles: {func_count}")

        # Total
        total = session.query(Competence).count()
        print(f"📈 Total compétences: {total}")

        # Détail des catégories fonctionnelles
        print("\n🏦 DÉTAIL COMPÉTENCES FONCTIONNELLES:")
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
            print(f"   • {categorie}: {count}")

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
    print("🚀 INITIALISATION COMPÉTENCES FONCTIONNELLES")
    print("=" * 60)

    # Initialiser les compétences
    init_competences_fonctionnelles()

    # Afficher le résumé
    show_competences_summary()

    print("\n✨ Script terminé!")
