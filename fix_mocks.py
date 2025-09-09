import re

# Read the file
with open('tests/test_pages_modules.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all occurrences of the mock_columns_func
old_pattern = '''        # Dynamic mock for columns that returns the correct number of mocks
        def mock_columns_func(arg):
            if isinstance(arg, list):
                return [MagicMock() for _ in range(len(arg))]
            else:
                return [MagicMock() for _ in range(arg)]
        mock_st.columns = MagicMock(side_effect=mock_columns_func)'''

new_pattern = '''        # Dynamic mock for columns that returns the correct number of mocks
        def mock_columns_func(arg):
            if isinstance(arg, list):
                return [MagicMock() for _ in range(len(arg))]
            else:
                # Return at least 3 columns by default to handle most cases
                return [MagicMock() for _ in range(max(arg, 3))]
        mock_st.columns = MagicMock(side_effect=mock_columns_func)'''

# Replace all occurrences
new_content = re.sub(re.escape(old_pattern), new_pattern, content, flags=re.MULTILINE | re.DOTALL)

# Write back to file
with open('tests/test_pages_modules.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Updated all mock_columns_func definitions')
