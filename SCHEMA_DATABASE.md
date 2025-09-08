# Schéma du Modèle de Données - Consultator

## Vue d'ensemble du modèle relationnel avec cardinalités

```
┌─────────────────────┐
│      PRACTICE       │
│──────────────────── │
│ id (PK)             │
│ nom (UNIQUE)        │
│ description         │
│ responsable         │
│ date_creation       │
│ actif               │
└─────────────────────┘
          │
          │ 1:N
          ▼
┌─────────────────────┐
│     CONSULTANT      │
│──────────────────── │
│ id (PK)             │
│ nom                 │
│ prenom              │
│ email (UNIQUE)      │
│ telephone           │
│ salaire_actuel      │
│ date_creation       │
│ derniere_maj        │
│ disponibilite       │
│ notes               │
│ practice_id (FK)    │
└─────────────────────┘
     │        │        │        │
     │ 1:N    │ 1:N    │ 1:N    │ 1:N
     ▼        ▼        ▼        ▼
┌──────────┐ ┌────────┐ ┌────────────────┐ ┌─────────────────┐
│ MISSION  │ │   CV   │ │CONSULTANT_COMP │ │CONSULTANT_SAL   │
│──────────│ │────────│ │────────────────│ │─────────────────│
│ id (PK)  │ │id (PK) │ │ id (PK)        │ │ id (PK)         │
│ consul.. │ │consul..│ │ consultant_id  │ │ consultant_id   │
│ nom_mis..│ │fichier.│ │ competence_id  │ │ salaire         │
│ client   │ │fichier.│ │ annees_exp     │ │ date_debut      │
│ role     │ │contenu.│ │ niveau_mait    │ │ date_fin        │
│ date_deb │ │date_up │ │ certifications │ │ commentaire     │
│ date_fin │ │taille_ │ │ projets_real   │ └─────────────────┘
│ statut   │ └────────┘ │ date_ajout     │
│ taux_j.. │            └────────────────┘
│ revenus  │                      │
│ technos  │                      │ N:1
│ descript │                      ▼
└──────────┘            ┌─────────────────┐
                        │   COMPETENCE    │
                        │─────────────────│
                        │ id (PK)         │
                        │ nom (UNIQUE)    │
                        │ categorie       │
                        │ type_competence │
                        │ description     │
                        │ niveau_requis   │
                        └─────────────────┘

┌─────────────────────┐
│ CUSTOM_TECHNOLOGY   │  (Table autonome)
│─────────────────────│
│ id (PK)             │
│ nom (UNIQUE)        │
│ categorie           │
│ description         │
│ date_creation       │
└─────────────────────┘
```

## Cardinalités détaillées

### Relations principales :

1. **PRACTICE ↔ CONSULTANT**
   - **Cardinalité** : 1:N (Une practice peut avoir plusieurs consultants)
   - **Contrainte** : Un consultant peut être dans 0 ou 1 practice (practice_id nullable)

2. **CONSULTANT ↔ MISSION**
   - **Cardinalité** : 1:N (Un consultant peut avoir plusieurs missions)
   - **Contrainte** : Une mission appartient obligatoirement à un consultant

3. **CONSULTANT ↔ CV**
   - **Cardinalité** : 1:N (Un consultant peut avoir plusieurs CVs)
   - **Contrainte** : Un CV appartient obligatoirement à un consultant

4. **CONSULTANT ↔ CONSULTANT_SALAIRE**
   - **Cardinalité** : 1:N (Un consultant peut avoir plusieurs entrées de salaire)
   - **Contrainte** : Historique des évolutions de salaire

5. **CONSULTANT ↔ COMPETENCE** (via CONSULTANT_COMPETENCE)
   - **Cardinalité** : N:M (Plusieurs consultants peuvent avoir plusieurs compétences)
   - **Table de liaison** : CONSULTANT_COMPETENCE avec attributs supplémentaires

## Contraintes d'intégrité :

### Clés primaires :
- Toutes les tables ont un `id` auto-incrémenté comme clé primaire

### Clés uniques :
- `practice.nom` : Nom unique pour chaque practice
- `consultant.email` : Email unique pour chaque consultant
- `competence.nom` : Nom unique pour chaque compétence
- `custom_technology.nom` : Nom unique pour chaque technologie

### Clés étrangères :
- `consultant.practice_id` → `practice.id` (NULLABLE)
- `mission.consultant_id` → `consultant.id` (NOT NULL)
- `cv.consultant_id` → `consultant.id` (NOT NULL)
- `consultant_competence.consultant_id` → `consultant.id` (NOT NULL)
- `consultant_competence.competence_id` → `competence.id` (NOT NULL)
- `consultant_salaire.consultant_id` → `consultant.id` (NOT NULL)

### Suppressions en cascade :
- Suppression d'un consultant → supprime ses missions, CVs, compétences et salaires
- Suppression d'une practice → les consultants deviennent sans practice (practice_id = NULL)

## Champs calculés :

### CJM (Coût Journalier Moyen) :
- **Formule** : `salaire_actuel * 1.8 / 216`
- **Non stocké** : Calculé à la volée dans l'interface et le chatbot

### Propriétés calculées :
- `consultant.nom_complet` : Concaténation prénom + nom
- `mission.duree_jours` : Différence entre date_fin et date_debut
- `practice.nombre_consultants` : Nombre de consultants disponibles dans la practice

## Types de données utilisés :

- **Integer** : Clés primaires, IDs, tailles
- **String** : Textes courts (noms, emails, statuts)
- **Text** : Textes longs (descriptions, notes, contenus)
- **Float** : Montants (salaires, taux, revenus)
- **Date** : Dates sans heure (début/fin mission)
- **DateTime** : Timestamps complets (création, modification)
- **Boolean** : Drapeaux (disponibilité, actif)
