#!/usr/bin/env python3
"""
Script pour initialiser les Business Managers et les affecter aux consultants
"""

import os
import sys
from datetime import date
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from database.database import get_database_session
from database.models import BusinessManager
from database.models import Consultant
from database.models import ConsultantBusinessManager


def init_business_managers():
    """Initialise les Business Managers de base"""
    session = get_database_session()

    # Business Managers de base
    bms_base = [
        {
            "nom": "Leroy",
            "prenom": "Laurent",
            "email": "laurent.leroy@consultator.com",
            "telephone": "01.45.67.89.12",
            "notes": "BM senior, spÃ©cialisÃ© secteur bancaire",
        },
        {
            "nom": "Moreau",
            "prenom": "Sophie",
            "email": "sophie.moreau@consultator.com",
            "telephone": "01.45.67.89.13",
            "notes": "BM experte, focus assurance et finance",
        },
        {
            "nom": "Dubois",
            "prenom": "Marc",
            "email": "marc.dubois@consultator.com",
            "telephone": "01.45.67.89.14",
            "notes": "BM junior, secteur technologie",
        },
        {
            "nom": "Rousseau",
            "prenom": "Julie",
            "email": "julie.rousseau@consultator.com",
            "telephone": "01.45.67.89.15",
            "notes": "BM senior, transformation digitale",
        },
    ]

    print("ð¥ Initialisation des Business Managers...")

    for bm_data in bms_base:
        # VÃ©rifier si le BM existe dÃ©jÃ
        existing = (
            session.query(BusinessManager)
            .filter(BusinessManager.email == bm_data["email"])
            .first()
        )

        if not existing:
            bm = BusinessManager(
                nom=bm_data["nom"],
                prenom=bm_data["prenom"],
                email=bm_data["email"],
                telephone=bm_data["telephone"],
                notes=bm_data["notes"],
            )
            session.add(bm)
            print(f"  â {bm_data['prenom']} {bm_data['nom']} ajoutÃ©(e)")
        else:
            print(f"  â ï¸  {bm_data['prenom']} {bm_data['nom']} existe dÃ©jÃ ")

    try:
        session.commit()
        print(f"\nâ {len(bms_base)} Business Managers initialisÃ©s avec succÃ¨s!")

        # Afficher le rÃ©sumÃ©
        total_bms = session.query(BusinessManager).count()
        print(f"ð Total des BMs en base : {total_bms}")

    except (SQLAlchemyError, ValueError, AttributeError) as e:
        session.rollback()
        print(f"â Erreur lors de l'initialisation : {e}")
    finally:
        session.close()


def assign_consultants_to_bms():
    """Affecte les consultants existants aux Business Managers"""
    session = get_database_session()

    try:
        # RÃ©cupÃ©rer les BMs et consultants
        bms = session.query(BusinessManager).all()
        consultants = session.query(Consultant).all()

        if not bms:
            print("â Aucun Business Manager trouvÃ©")
            return

        if not consultants:
            print("â Aucun consultant trouvÃ©")
            return

        print(
            f"\nð¨âð¼ Affectation de {len(consultants)} consultants Ã  {len(bms)} BMs..."
        )

        # RÃ©partir les consultants entre les BMs
        for i, consultant in enumerate(consultants):
            # VÃ©rifier si le consultant n'a pas dÃ©jÃ  un BM actuel
            bm_actuel = consultant.business_manager_actuel
            if bm_actuel:
                print(
                    f"  â ï¸  {consultant.nom_complet} dÃ©jÃ  gÃ©rÃ© par {bm_actuel.nom_complet}"
                )
                continue

            # Affecter de maniÃ¨re cyclique
            bm = bms[i % len(bms)]

            # CrÃ©er l'affectation
            affectation = ConsultantBusinessManager(
                consultant_id=consultant.id,
                business_manager_id=bm.id,
                date_debut=date.today(),
                commentaire="Affectation initiale",
            )
            session.add(affectation)
            print(f"  â {consultant.nom_complet} â {bm.nom_complet}")

        session.commit()
        print("\nâ Affectations crÃ©Ã©es avec succÃ¨s!")

        # Statistiques finales
        print("\nð RÃ©partition des consultants :")
        for bm in session.query(BusinessManager).all():
            nb_consultants = bm.nombre_consultants_actuels
            print(f"  â¢ {bm.nom_complet}: {nb_consultants} consultant(s)")

    except (SQLAlchemyError, ValueError, AttributeError) as e:
        session.rollback()
        print(f"â Erreur lors des affectations : {e}")
    finally:
        session.close()


if __name__ == "__main__":
    init_business_managers()
    assign_consultants_to_bms()
