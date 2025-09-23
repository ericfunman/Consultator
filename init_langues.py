#!/usr/bin/env python3
"""
Script pour initialiser les langues de base dans la base de donnÃ©es
"""

import os
import sys

from sqlalchemy.exc import SQLAlchemyError

# Ajouter le chemin vers le module app
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from database.database import get_database_session  # noqa: E402
from database.models import Langue  # noqa: E402


def init_langues():
    """Initialise les langues de base"""
    session = get_database_session()

    # Langues principales avec codes ISO
    langues_base = [
        {"nom": "FranÃ§ais", "code_iso": "FR", "description": "Langue franÃ§aise"},
        {"nom": "Anglais", "code_iso": "EN", "description": "Langue anglaise"},
        {"nom": "Espagnol", "code_iso": "ES", "description": "Langue espagnole"},
        {"nom": "Allemand", "code_iso": "DE", "description": "Langue allemande"},
        {"nom": "Italien", "code_iso": "IT", "description": "Langue italienne"},
        {"nom": "Portugais", "code_iso": "PT", "description": "Langue portugaise"},
        {
            "nom": "NÃ©erlandais",
            "code_iso": "NL",
            "description": "Langue nÃ©erlandaise",
        },
        {"nom": "Russe", "code_iso": "RU", "description": "Langue russe"},
        {
            "nom": "Chinois Mandarin",
            "code_iso": "ZH",
            "description": "Chinois mandarin",
        },
        {"nom": "Japonais", "code_iso": "JA", "description": "Langue japonaise"},
        {"nom": "Arabe", "code_iso": "AR", "description": "Langue arabe"},
        {"nom": "Hindi", "code_iso": "HI", "description": "Langue hindi"},
    ]

    print("ð Initialisation des langues...")

    for langue_data in langues_base:
        # VÃ©rifier si la langue existe dÃ©jÃ
        existing = (
            session.query(Langue).filter(Langue.nom == langue_data["nom"]).first()
        )

        if not existing:
            langue = Langue(
                nom=langue_data["nom"],
                code_iso=langue_data["code_iso"],
                description=langue_data["description"],
            )
            session.add(langue)
            print(f"  â {langue_data['nom']} ({langue_data['code_iso']}) ajoutÃ©e")
        else:
            print(f"  â ï¸  {langue_data['nom']} existe dÃ©jÃ ")

    try:
        session.commit()
        print(f"\nâ {len(langues_base)} langues initialisÃ©es avec succÃ¨s!")

        # Afficher le rÃ©sumÃ©
        total_langues = session.query(Langue).count()
        print(f"ð Total des langues en base : {total_langues}")

    except (SQLAlchemyError, ValueError, AttributeError) as e:
        session.rollback()
        print(f"â Erreur lors de l'initialisation : {e}")
    finally:
        session.close()


def add_sample_consultant_languages():
    """Ajoute des langues d'exemple aux consultants existants"""
    session = get_database_session()

    try:
        from database.models import Consultant
        from database.models import ConsultantLangue

        # RÃ©cupÃ©rer quelques consultants et langues
        consultants = session.query(Consultant).limit(5).all()
        francais = session.query(Langue).filter(Langue.nom == "FranÃ§ais").first()
        anglais = session.query(Langue).filter(Langue.nom == "Anglais").first()
        espagnol = session.query(Langue).filter(Langue.nom == "Espagnol").first()

        if not (francais and anglais):
            print("â Langues de base non trouvÃ©es")
            return

        print("\nð£ï¸  Ajout de langues d'exemple aux consultants...")

        for i, consultant in enumerate(consultants):
            # Tous les consultants parlent franÃ§ais (niveau natif)
            existing_fr = (
                session.query(ConsultantLangue)
                .filter(
                    ConsultantLangue.consultant_id == consultant.id,
                    ConsultantLangue.langue_id == francais.id,
                )
                .first()
            )

            if not existing_fr:
                langue_fr = ConsultantLangue(
                    consultant_id=consultant.id,
                    langue_id=francais.id,
                    niveau=5,  # Natif
                    commentaire="Langue maternelle",
                )
                session.add(langue_fr)

            # Anglais avec niveaux variables
            existing_en = (
                session.query(ConsultantLangue)
                .filter(
                    ConsultantLangue.consultant_id == consultant.id,
                    ConsultantLangue.langue_id == anglais.id,
                )
                .first()
            )

            if not existing_en:
                niveau_anglais = 3 + (i % 3)  # Niveaux 3, 4, 5
                commentaires = {
                    3: "TOEIC 750 - Bon niveau professionnel",
                    4: "TOEIC 900 - TrÃ¨s bon niveau",
                    5: "Bilingue - Travail en environnement anglophone",
                }

                langue_en = ConsultantLangue(
                    consultant_id=consultant.id,
                    langue_id=anglais.id,
                    niveau=niveau_anglais,
                    commentaire=commentaires[niveau_anglais],
                )
                session.add(langue_en)

            # Espagnol pour certains consultants
            if espagnol and i % 2 == 0:  # 1 consultant sur 2
                existing_es = (
                    session.query(ConsultantLangue)
                    .filter(
                        ConsultantLangue.consultant_id == consultant.id,
                        ConsultantLangue.langue_id == espagnol.id,
                    )
                    .first()
                )

                if not existing_es:
                    langue_es = ConsultantLangue(
                        consultant_id=consultant.id,
                        langue_id=espagnol.id,
                        niveau=2,  # ÃlÃ©mentaire
                        commentaire="Notions scolaires",
                    )
                    session.add(langue_es)

            print(f"  â Langues ajoutÃ©es pour {consultant.prenom} {consultant.nom}")

        session.commit()
        print("\nâ Langues d'exemple ajoutÃ©es avec succÃ¨s!")

    except (SQLAlchemyError, ValueError, AttributeError) as e:
        session.rollback()
        print(f"â Erreur lors de l'ajout des langues d'exemple : {e}")
    finally:
        session.close()


if __name__ == "__main__":
    init_langues()
    add_sample_consultant_languages()
