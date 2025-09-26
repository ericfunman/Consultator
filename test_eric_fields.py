#!/usr/bin/env python3
"""
Test direct des champs d'Eric LAPINA
"""

import sys

sys.path.append(".")

from app.database.database import get_session
from app.database.models import Consultant


def test_eric_fields():
    """Test des champs Eric"""

    with get_session() as session:
        eric = (
            session.query(Consultant)
            .filter(Consultant.email == "eric.lapina@quanteam.fr")
            .first()
        )

        print("=== TEST CHAMPS ERIC LAPINA ===")
        print(f"Nom: {eric.prenom} {eric.nom}")

        # Test getattr comme dans l'interface
        etat_pe = getattr(eric, "etat_periode_essai", None)
        print(f"getattr etat_periode_essai: {etat_pe}")

        fin_pe = getattr(eric, "fin_periode_essai", None)
        print(f"getattr fin_periode_essai: {fin_pe}")
        if fin_pe:
            print(f"  -> Formaté: {fin_pe.strftime('%d/%m/%Y')}")

        actif = getattr(eric, "actif", True)
        print(f"getattr actif: {actif}")
        statut_actif = "✅ Actif" if actif else "❌ Inactif"
        print(f"  -> Statut: {statut_actif}")

        # Test direct
        print(f"Direct etat_periode_essai: {eric.etat_periode_essai}")
        print(f"Direct fin_periode_essai: {eric.fin_periode_essai}")
        print(f"Direct actif: {eric.actif}")

        try:
            statut = eric.statut_societe
            print(f"Direct statut_societe: {statut}")
        except Exception as e:
            print(f"Erreur statut_societe: {e}")


if __name__ == "__main__":
    test_eric_fields()
