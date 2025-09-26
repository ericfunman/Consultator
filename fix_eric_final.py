#!/usr/bin/env python3
"""
Script pour corriger définitivement Eric LAPINA et ses missions
"""

import logging
from datetime import datetime

from app.database.database import get_session
from app.database.models import Consultant
from app.database.models import Mission
from app.database.models import VSA_Mission

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


def fix_eric_lapina():
    """Correction définitive d'Eric LAPINA"""

    try:
        with get_session() as session:
            # Recherche Eric LAPINA par email
            eric = (
                session.query(Consultant)
                .filter(Consultant.email == "eric.lapina@quanteam.fr")
                .first()
            )

            if not eric:
                logger.error("Eric LAPINA non trouvé dans la base")
                return False

            logger.info(f"✅ Eric trouvé: {eric.prenom} {eric.nom} (ID: {eric.id})")

            # 1. Vérifier les nouveaux champs
            logger.info(f"📋 État période essai: {eric.etat_periode_essai}")
            logger.info(f"📋 Fin période essai: {eric.fin_periode_essai}")
            logger.info(f"📋 Actif: {eric.actif}")

            # 2. Supprimer toutes les missions existantes d'Eric
            missions_eric = (
                session.query(Mission).filter(Mission.consultant_id == eric.id).all()
            )
            logger.info(f"🗑️ Suppression de {len(missions_eric)} missions existantes")

            for mission in missions_eric:
                session.delete(mission)

            vsa_missions_eric = (
                session.query(VSA_Mission).filter(VSA_Mission.user_id == eric.id).all()
            )
            logger.info(
                f"🗑️ Suppression de {len(vsa_missions_eric)} missions VSA existantes"
            )

            for vsa_mission in vsa_missions_eric:
                session.delete(vsa_mission)

            session.commit()

            # 3. Créer la mission VSA manquante (2023)
            vsa_mission = VSA_Mission(
                user_id=eric.id,
                code="AFFAS263",
                orderid="AFFAS263-2023",
                client_name="GENERALI VIE",
                date_debut=datetime(2023, 8, 21).date(),
                date_fin=datetime(2023, 12, 31).date(),
                tjm=0,
            )
            session.add(vsa_mission)
            logger.info("✅ Mission VSA 2023 créée: AFFAS263 (21/08/2023 - 31/12/2023)")

            # 4. Créer la mission classique complète (2023-2025)
            mission_classique = Mission(
                consultant_id=eric.id,
                nom_mission="AFFAS263",
                client="GENERALI VIE",
                date_debut=datetime(2023, 8, 21).date(),
                date_fin=datetime(2025, 12, 31).date(),
                taux_journalier=0,
                description="Mission longue durée chez Generali Vie",
            )
            session.add(mission_classique)
            logger.info(
                "✅ Mission classique créée: AFFAS263 (21/08/2023 - 31/12/2025)"
            )

            session.commit()
            logger.info("💾 Toutes les modifications sauvegardées")

            # 5. Vérification finale
            missions_finales = (
                session.query(Mission).filter(Mission.consultant_id == eric.id).all()
            )
            vsa_missions_finales = (
                session.query(VSA_Mission).filter(VSA_Mission.user_id == eric.id).all()
            )

            logger.info(f"✅ Vérification finale:")
            logger.info(f"   - Missions classiques: {len(missions_finales)}")
            logger.info(f"   - Missions VSA: {len(vsa_missions_finales)}")

            for mission in missions_finales:
                logger.info(
                    f"   - Mission classique: {mission.nom_mission} ({mission.date_debut} -> {mission.date_fin})"
                )

            for vsa in vsa_missions_finales:
                logger.info(
                    f"   - Mission VSA: {vsa.code} ({vsa.date_debut} -> {vsa.date_fin})"
                )

            return True

    except Exception as e:
        logger.error(f"❌ Erreur lors de la correction: {e}")
        return False


if __name__ == "__main__":
    print("🔧 Correction finale d'Eric LAPINA...")
    success = fix_eric_lapina()
    if success:
        print("✅ Correction terminée avec succès!")
    else:
        print("❌ Échec de la correction")
