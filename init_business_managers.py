#!/usr/bin/env python3
"""
Script pour initialiser les Business Managers et les affecter aux consultants
"""

import os
import sys
from datetime import date
from datetime import datetime

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
            "notes": "BM senior, spécialisé secteur bancaire",
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

    print("👥 Initialisation des Business Managers...")

    for bm_data in bms_base:
        # Vérifier si le BM existe déjà
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
            print(f"  ✅ {bm_data['prenom']} {bm_data['nom']} ajouté(e)")
        else:
            print(f"  ⚠️  {bm_data['prenom']} {bm_data['nom']} existe déjà")

    try:
        session.commit()
        print(f"\n✅ {len(bms_base)} Business Managers initialisés avec succès!")

        # Afficher le résumé
        total_bms = session.query(BusinessManager).count()
        print(f"📊 Total des BMs en base : {total_bms}")

    except Exception as e:
        session.rollback()
        print(f"❌ Erreur lors de l'initialisation : {e}")
    finally:
        session.close()


def assign_consultants_to_bms():
    """Affecte les consultants existants aux Business Managers"""
    session = get_database_session()

    try:
        # Récupérer les BMs et consultants
        bms = session.query(BusinessManager).all()
        consultants = session.query(Consultant).all()

        if not bms:
            print("❌ Aucun Business Manager trouvé")
            return

        if not consultants:
            print("❌ Aucun consultant trouvé")
            return

        print(
            f"\n👨‍💼 Affectation de {len(consultants)} consultants à {len(bms)} BMs..."
        )

        # Répartir les consultants entre les BMs
        for i, consultant in enumerate(consultants):
            # Vérifier si le consultant n'a pas déjà un BM actuel
            bm_actuel = consultant.business_manager_actuel
            if bm_actuel:
                print(
                    f"  ⚠️  {consultant.nom_complet} déjà géré par {bm_actuel.nom_complet}"
                )
                continue

            # Affecter de manière cyclique
            bm = bms[i % len(bms)]

            # Créer l'affectation
            affectation = ConsultantBusinessManager(
                consultant_id=consultant.id,
                business_manager_id=bm.id,
                date_debut=date.today(),
                commentaire="Affectation initiale",
            )
            session.add(affectation)
            print(f"  ✅ {consultant.nom_complet} → {bm.nom_complet}")

        session.commit()
        print(f"\n✅ Affectations créées avec succès!")

        # Statistiques finales
        print(f"\n📊 Répartition des consultants :")
        for bm in session.query(BusinessManager).all():
            nb_consultants = bm.nombre_consultants_actuels
            print(f"  • {bm.nom_complet}: {nb_consultants} consultant(s)")

    except Exception as e:
        session.rollback()
        print(f"❌ Erreur lors des affectations : {e}")
    finally:
        session.close()


if __name__ == "__main__":
    init_business_managers()
    assign_consultants_to_bms()
