"""
Script pour chercher Eric Lapina dans le fichier Excel
"""

import pandas as pd

from import_vsa_personnes import classify_person_by_job_title


def search_eric_lapina():
    """Cherche Eric Lapina dans le fichier Excel et explique pourquoi il n'a pas été importé"""

    # Charger le fichier Excel
    df = pd.read_excel(r"C:\Users\b302gja\Documents\VSA Personnes.xlsx")

    # Chercher Eric Lapina (insensible à la casse)
    eric_lapina = df[
        (df["firstname"].str.lower() == "eric")
        & (df["lastname"].str.lower() == "lapina")
    ]

    if not eric_lapina.empty:
        print("✅ Eric Lapina trouvé dans le fichier Excel:")
        for _, row in eric_lapina.iterrows():
            print(f'  Prénom: {row["firstname"]}')
            print(f'  Nom: {row["lastname"]}')
            print(f'  Email: {row["email"]}')
            print(f'  Job Title: {row["job_title"]}')
            print(f'  Société: {row["EntiteCollab"]}')
            print(f'  Manager: {row["ManagerName"]}')
            print()

        # Vérifier la classification
        job_title = eric_lapina.iloc[0]["job_title"]
        classification = classify_person_by_job_title(job_title)
        print(f"📋 Classification selon job_title: {classification}")

        if classification == "bm":
            print(
                "⚠️ Ce consultant a été classé comme Business Manager et donc exclu de l'import des consultants"
            )
            print("   Il faut vérifier s'il a été créé comme Business Manager")
        else:
            print("✅ Ce consultant devrait avoir été importé comme consultant")
            print("   Vérifions s'il existe dans la base de données...")

            # Vérifier dans la base de données
            from app.database.database import get_database_session
            from app.database.models import Consultant

            with get_database_session() as session:
                email = str(row["email"]).strip().lower()
                existing = (
                    session.query(Consultant).filter(Consultant.email == email).first()
                )
                if existing:
                    print(
                        f"✅ Trouvé dans la base: {existing.prenom} {existing.nom} ({existing.email})"
                    )
                else:
                    print(f"❌ Non trouvé dans la base de données")

    else:
        print("❌ Eric Lapina n'existe pas dans le fichier Excel")

        # Chercher des variantes
        eric_rows = df[df["firstname"].str.lower() == "eric"]
        if not eric_rows.empty:
            print("\n🔍 Autres personnes nommées Eric:")
            for _, row in eric_rows.iterrows():
                print(
                    f'  {row["firstname"]} {row["lastname"]} - {row["email"]} - {row["job_title"]}'
                )


if __name__ == "__main__":
    search_eric_lapina()
