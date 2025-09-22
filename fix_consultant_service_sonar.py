#!/usr/bin/env python3
"""
Script pour corriger automatiquement les anomalies SonarQube dans consultant_service.py
Réduit la complexité cognitive des fonctions complexes
"""

import re


def add_helper_methods():
    """Ajoute les méthodes helpers pour réduire la complexité"""
    
    helpers_code = '''
    @staticmethod
    def _build_search_base_query(session):
        """Construit la requête de base pour la recherche"""
        return (
            session.query(
                Consultant.id,
                Consultant.prenom,
                Consultant.nom,
                Consultant.email,
                Consultant.telephone,
                Consultant.salaire_actuel,
                Consultant.disponibilite,
                Consultant.date_creation,
                Consultant.societe,
                Consultant.date_entree_societe,
                Consultant.date_sortie_societe,
                Consultant.date_premiere_mission,
                Consultant.grade,
                Consultant.type_contrat,
                Practice.nom.label("practice_name"),
                func.count(Mission.id).label("nb_missions"),
            )
            .outerjoin(Practice, Consultant.practice_id == Practice.id)
            .outerjoin(Mission, Consultant.id == Mission.consultant_id)
        )

    @staticmethod
    def _apply_search_filters(query, search_term, practice_filter, grade_filter, availability_filter):
        """Applique tous les filtres à la requête"""
        if practice_filter:
            query = query.filter(Practice.nom == practice_filter)

        if grade_filter:
            query = query.filter(Consultant.grade == grade_filter)

        if availability_filter is not None:
            query = query.filter(Consultant.disponibilite == availability_filter)

        if search_term:
            search_filter = f"%{search_term}%"
            query = query.filter(
                (Consultant.nom.ilike(search_filter))
                | (Consultant.prenom.ilike(search_filter))
                | (Consultant.email.ilike(search_filter))
                | (Consultant.societe.ilike(search_filter))
            )

        return query

    @staticmethod
    def _finalize_search_query(query, page, per_page):
        """Finalise la requête avec grouping et pagination"""
        return (
            query.group_by(
                Consultant.id,
                Consultant.prenom,
                Consultant.nom,
                Consultant.email,
                Consultant.telephone,
                Consultant.salaire_actuel,
                Consultant.disponibilite,
                Consultant.date_creation,
                Consultant.societe,
                Consultant.date_entree_societe,
                Consultant.date_sortie_societe,
                Consultant.date_premiere_mission,
                Consultant.grade,
                Consultant.type_contrat,
                Practice.nom,
            )
            .offset((page - 1) * per_page)
            .limit(per_page)
        )

    @staticmethod
    def _format_search_results(results):
        """Formate les résultats de recherche en dictionnaires"""
        consultant_list = []
        for row in results:
            consultant_dict = ConsultantService._build_consultant_dict(row)
            consultant_list.append(consultant_dict)
        return consultant_list

    @staticmethod
    def _build_consultant_dict(row):
        """Construit le dictionnaire consultant avec calculs"""
        salaire = row.salaire_actuel or 0
        cjm = ConsultantService._calculate_cjm(salaire)
        experience_annees = ConsultantService._calculate_experience(row.date_premiere_mission)

        return {
            "id": row.id,
            "prenom": row.prenom,
            "nom": row.nom,
            "email": row.email,
            "telephone": row.telephone,
            "salaire_actuel": salaire,
            "disponibilite": row.disponibilite,
            "grade": row.grade or "Junior",
            "type_contrat": row.type_contrat or "CDI",
            "practice_name": row.practice_name or "Non affecté",
            "date_creation": row.date_creation,
            "nb_missions": row.nb_missions,
            "cjm": cjm,
            "salaire_formatted": f"{salaire:,}€",
            "cjm_formatted": f"{cjm:,.0f}€",
            "statut": (
                ConsultantService.STATUS_AVAILABLE
                if row.disponibilite
                else ConsultantService.STATUS_BUSY
            ),
            "societe": row.societe or "Quanteam",
            "experience_annees": experience_annees,
            "experience_formatted": (
                f"{experience_annees} ans" if experience_annees > 0 else "N/A"
            ),
        }

    @staticmethod
    def _calculate_cjm(salaire):
        """Calcule le coût journalier moyen"""
        return (salaire * 1.8 / 216) if salaire else 0

    @staticmethod
    def _calculate_experience(date_premiere_mission):
        """Calcule l'expérience en années"""
        if not date_premiere_mission:
            return 0
        
        from datetime import date
        today = date.today()
        delta = today - date_premiere_mission
        return round(delta.days / 365.25, 1)
'''
    
    return helpers_code


def fix_search_consultants_optimized():
    """Refactorise search_consultants_optimized pour réduire la complexité"""
    
    new_function = '''    @staticmethod
    def search_consultants_optimized(
        search_term: str,
        page: int = 1,
        per_page: int = 50,
        practice_filter: Optional[str] = None,
        grade_filter: Optional[str] = None,
        availability_filter: Optional[bool] = None,
    ) -> List[Dict]:
        """Recherche optimisée avec cache pour de gros volumes - avec statistiques intégrées"""
        try:
            with get_database_session() as session:
                query = ConsultantService._build_search_base_query(session)
                query = ConsultantService._apply_search_filters(
                    query, search_term, practice_filter, grade_filter, availability_filter
                )
                query = ConsultantService._finalize_search_query(query, page, per_page)

                results = query.all()
                return ConsultantService._format_search_results(results)
        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"Erreur lors de la recherche optimisée: {e}")
            return []'''
    
    return new_function


def main():
    """Fonction principale pour appliquer les corrections"""
    file_path = "app/services/consultant_service.py"
    
    # Lire le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Application des corrections SonarQube...")
    
    # 1. Ajouter les helpers avant get_consultants_count
    helpers = add_helper_methods()
    
    # Trouver la position pour insérer les helpers
    get_consultants_count_pos = content.find("    @staticmethod\n    def get_consultants_count() -> int:")
    if get_consultants_count_pos != -1:
        content = content[:get_consultants_count_pos] + helpers + "\n" + content[get_consultants_count_pos:]
        print("✅ Helpers ajoutés")
    
    # 2. Refactoriser search_consultants_optimized
    # Trouver et remplacer la fonction complexe
    pattern = r'(    @staticmethod\s+def search_consultants_optimized\(.*?\n.*?".*?".*?\n.*?try:.*?return \[\])'
    new_func = fix_search_consultants_optimized()
    
    # Utiliser une approche plus simple : trouver le début et la fin de la fonction
    start_marker = "    def search_consultants_optimized("
    end_marker = '            return []'
    
    start_pos = content.find(start_marker)
    if start_pos != -1:
        # Trouver la fin de la fonction
        temp_content = content[start_pos:]
        end_pos = temp_content.find(end_marker) + len(end_marker)
        
        if end_pos > len(end_marker):
            full_end_pos = start_pos + end_pos
            content = content[:start_pos] + new_func + "\n\n" + content[full_end_pos:]
            print("✅ search_consultants_optimized refactorisée")
    
    # Sauvegarder le fichier modifié
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("🎉 Corrections SonarQube appliquées avec succès !")


if __name__ == "__main__":
    main()