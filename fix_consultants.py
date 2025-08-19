#!/usr/bin/env python3
"""
Script pour corriger les problèmes dans consultants.py
"""

def fix_encoding_issues():
    """Corrige les problèmes d'encodage des emojis"""
    
    replacements = {
        'ðŸ'¥': '👥',
        'ðŸ'¤': '👤', 
        'ðŸ"‹': '📋',
        'âž•': '➕',
        'ðŸ"„': '📄',
        'ðŸ§ª': '🧪',
        'ðŸ'¡': '💡',
        'ðŸš€': '🚀',
        'â†': '←',
        'âœ…': '✅',
        'âŒ': '❌',
        'ðŸ'°': '💰',
        'ðŸ"Š': '📊',
        'ðŸ"…': '📅',
        'ðŸ'¼': '💼',
        'ðŸš€': '🚀',
        'ðŸ› ï¸': '🛠️',
        'ðŸ"': '📝',
        'ðŸ"ž': '📞',
        'ðŸ"§': '📧',
        'ðŸ—'ï¸': '🗑️',
        'âœï¸': '✏️',
        'ðŸ"¢': '🏢',
        'ðŸ"': '💾',
        'ðŸ"¥': '📥',
        'â„¹ï¸': 'ℹ️',
        'ðŸ"': '🔍',
        'â¸ï¸': '⏸️',
        'âš™ï¸': '⚙️',
        'GÃ©rez': 'Gérez',
        'VÃ©rifier': 'Vérifier', 
        'spÃ©cifique': 'spécifique',
        'fonctionnalitÃ©s': 'fonctionnalités',
        'organisÃ©': 'organisé',
        'terminÃ©e': 'terminée',
        'DerniÃ¨res': 'Dernières',
        'ajoutÃ©es': 'ajoutées',
        'dÃ©tectÃ©es': 'détectées',
        'modifiÃ©': 'modifié',
        'supprimÃ©e': 'supprimée',
        'supprimÃ©': 'supprimé',
        'ajoutÃ©e': 'ajoutée',
        'Ã©vitÃ©s': 'évités',
        'crÃ©ation': 'création',
        'dÃ©finitivement': 'définitivement',
        'associÃ©es': 'associées',
        'RÃ´le': 'Rôle',
        'spÃ©cifiÃ©': 'spécifié',
        'spÃ©cifiÃ©es': 'spécifiées',
        'DÃ©but': 'Début',
        'â‚¬': '€'
    }
    
    file_path = 'app/pages_modules/consultants.py'
    
    try:
        # Lire le fichier
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Appliquer les remplacements
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        # Réécrire le fichier
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Correction d'encodage appliquée avec succès")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")

if __name__ == "__main__":
    fix_encoding_issues()
