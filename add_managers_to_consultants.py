#!/usr/bin/env python3
"""
Script pour affecter des business managers aux consultants existants
"""

import os
import random
import sys
from datetime import date

# Ajouter le répertoire app au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

from app.database.database import get_database_session
from app.database.models import BusinessManager
from app.database.models import Consultant
from app.database.models import ConsultantBusinessManager


def assign_managers_to_consultants():
    """Affecter des business managers aux consultants qui n'en ont pas"""
    print("👔 Affectation des business managers aux consultants...")

    with get_database_session() as session:
        # Récupérer tous les consultants sans business manager
        consultants_sans_manager = (
            session.query(Consultant)
            .filter(
                ~Consultant.id.in_(
                    session.query(ConsultantBusinessManager.consultant_id).filter(
                        ConsultantBusinessManager.date_fin.is_(None)
                    )
                )
            )
            .all()
        )

        # Récupérer tous les business managers
        managers = session.query(BusinessManager).all()
        manager_ids = [m.id for m in managers]

        print(f"📊 {len(consultants_sans_manager)} consultants sans business manager")
        print(f"👔 {len(managers)} business managers disponibles")

        if not manager_ids:
            print("❌ Aucun business manager trouvé !")
            return

        # Affecter un business manager à chaque consultant
        assignments_created = 0

        for consultant in consultants_sans_manager:
            manager_id = random.choice(manager_ids)

            consultant_manager = ConsultantBusinessManager(
                consultant_id=consultant.id,
                business_manager_id=manager_id,
                date_debut=consultant.date_entree_societe or date.today(),
            )
            session.add(consultant_manager)
            assignments_created += 1

        session.commit()
        print(f"✅ {assignments_created} affectations créées")


def main():
    """Script principal"""
    print("🚀 Affectation des business managers")
    print("=" * 50)

    assign_managers_to_consultants()

    print("\n" + "=" * 50)
    print("🎉 Affectations terminées !")


if __name__ == "__main__":
    main()
