import os
import glob
files = glob.glob('tests/test_*.py')
total = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        total += content.count('def test_')
print(f'{len(files)} fichiers de test, {total} tests trouvés')
