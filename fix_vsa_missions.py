import re
import random

file_path = 'tests/problematic_tests/regression/test_import_regression.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern pour trouver VSA_Mission sans orderid
pattern = r'(VSA_Mission\([^)]*?user_id=[^,]+,\s*code=[^,]+,)(\s*client_name=)'

# Fonction de remplacement qui ajoute orderid
def add_orderid(match):
    orderid_value = f'"ORD-{random.randint(1000, 9999)}-{random.randint(100, 999)}"'
    return match.group(1) + f'\n                orderid={orderid_value},' + match.group(2)

# Appliquer le remplacement
new_content = re.sub(pattern, add_orderid, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Correction des VSA_Mission terminée')