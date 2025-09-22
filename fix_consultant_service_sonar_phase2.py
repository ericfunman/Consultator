#!/usr/bin/env python3
"""
Script pour corriger get_all_consultants_with_stats et autres anomalies SonarQube
"""

import re


def add_stats_helpers():
    """Ajoute les helpers spécifiques pour get_all_consultants_with_stats"""
    
    helpers_code = '''
    @staticmethod
    def _build_consultants_stats_base_query(session):
        """Construit la requête de base pour les consultants avec stats"""
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
                Consultant.derniere_maj,
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
    def _apply_consultants_stats_filters(query, practice_filter, grade_filter, availability_filter):
        """Applique les filtres à la requête consultants avec stats"""
        if practice_filter:
            query = query.filter(Practice.nom == practice_filter)

        if grade_filter:
            query = query.filter(Consultant.grade == grade_filter)

        if availability_filter is not None:
            query = query.filter(Consultant.disponibilite == availability_filter)

        return query

    @staticmethod
    def _finalize_consultants_stats_query(query, page, per_page):
        """Finalise la requête consultants avec stats avec grouping et pagination"""
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
                Consultant.derniere_maj,
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
    def _format_consultants_stats_results(results):
        """Formate les résultats des consultants avec stats"""
        consultant_list = []
        for row in results:
            consultant_dict = ConsultantService._build_consultant_stats_dict(row)
            consultant_list.append(consultant_dict)
        return consultant_list

    @staticmethod
    def _build_consultant_stats_dict(row):
        """Construit le dictionnaire consultant avec stats détaillées"""
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
            "practice_name": row.practice_name or "Non affecté",
            "date_creation": row.date_creation,
            "derniere_maj": row.derniere_maj,
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
            "grade": row.grade or "Junior",
            "type_contrat": row.type_contrat or "CDI",
        }
'''
    
    return helpers_code


def fix_get_all_consultants_with_stats():
    """Refactorise get_all_consultants_with_stats pour réduire la complexité"""
    
    new_function = '''    @staticmethod
    def get_all_consultants_with_stats(
        page: int = 1,
        per_page: int = 50,
        practice_filter: Optional[str] = None,
        grade_filter: Optional[str] = None,
        availability_filter: Optional[bool] = None,
    ) -> List[Dict]:
        """
        Récupère tous les consultants avec leurs statistiques en une seule requête optimisée
        Résout le problème N+1 des requêtes pour compter les missions
        """
        try:
            with get_database_session() as session:
                query = ConsultantService._build_consultants_stats_base_query(session)
                query = ConsultantService._apply_consultants_stats_filters(
                    query, practice_filter, grade_filter, availability_filter
                )
                query = ConsultantService._finalize_consultants_stats_query(query, page, per_page)

                results = query.all()
                return ConsultantService._format_consultants_stats_results(results)
        except (SQLAlchemyError, ValueError, TypeError, AttributeError) as e:
            print(f"Erreur lors de la récupération optimisée des consultants: {e}")
            return []'''
    
    return new_function


def fix_session_parameter():
    """Corrige le paramètre 'session' qui devrait être 'self'"""
    
    # Pattern pour trouver la ligne problématique
    old_pattern = r'(\s+session: Session, consultant_id: int, competence_name: str, type_competence: str)'
    new_pattern = r'\1'.replace('session: Session,', 'self, session: Session,')
    
    return old_pattern, new_pattern


def main():
    """Fonction principale pour appliquer les corrections"""
    file_path = "app/services/consultant_service.py"
    
    # Lire le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Application des corrections SonarQube (Phase 2)...")
    
    # 1. Ajouter les helpers pour stats avant get_consultant_summary_stats
    helpers = add_stats_helpers()
    
    # Trouver la position pour insérer les helpers
    summary_stats_pos = content.find("    @staticmethod\n    def get_consultant_summary_stats() -> Dict[str, int]:")
    if summary_stats_pos != -1:
        content = content[:summary_stats_pos] + helpers + "\n" + content[summary_stats_pos:]
        print("✅ Helpers stats ajoutés")
    
    # 2. Refactoriser get_all_consultants_with_stats
    start_marker = "    def get_all_consultants_with_stats("
    end_marker = "            return []"
    
    start_pos = content.find(start_marker)
    if start_pos != -1:
        # Trouver la fin de la fonction en cherchant le bon end_marker après le start
        temp_content = content[start_pos:]
        
        # Chercher la séquence exacte de fin de cette fonction
        lines = temp_content.split('\n')
        end_line_idx = -1
        
        for i, line in enumerate(lines):
            if 'print(f"Erreur lors de la récupération optimisée des consultants: {e}")' in line:
                # La ligne suivante devrait être return []
                if i + 1 < len(lines) and 'return []' in lines[i + 1]:
                    end_line_idx = i + 1
                    break
        
        if end_line_idx != -1:
            # Calculer la position de fin
            end_content = '\n'.join(lines[:end_line_idx + 1])
            full_end_pos = start_pos + len(end_content)
            
            new_func = fix_get_all_consultants_with_stats()
            content = content[:start_pos] + new_func + "\n\n" + content[full_end_pos:]
            print("✅ get_all_consultants_with_stats refactorisée")
    
    # 3. Corriger le paramètre session
    content = re.sub(
        r'(\s+)session: Session, consultant_id: int, competence_name: str, type_competence: str',
        r'\1self, session: Session, consultant_id: int, competence_name: str, type_competence: str',
        content
    )
    print("✅ Paramètre session corrigé")
    
    # Sauvegarder le fichier modifié
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("🎉 Corrections SonarQube Phase 2 appliquées avec succès !")


if __name__ == "__main__":
    main()