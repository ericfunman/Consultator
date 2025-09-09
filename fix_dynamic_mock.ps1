with open('tests/test_consultants_simple.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the DynamicMock to be iterable
old_mock = '''        # Create a mock that supports dynamic attributes
        class DynamicMock:
            def __init__(self):
                self._dynamic_attrs = {}

            def __setattr__(self, name, value):
                if name.startswith('_'):
                    object.__setattr__(self, name, value)
                else:
                    self._dynamic_attrs[name] = value

            def __getattr__(self, name):
                if name in self._dynamic_attrs:
                    return self._dynamic_attrs[name]
                raise AttributeError(f\"'{self.__class__.__name__}' object has no attribute '{name}'\")'''

new_mock = '''        # Create a mock that supports dynamic attributes and iteration
        class DynamicMock:
            def __init__(self):
                self._dynamic_attrs = {}

            def __setattr__(self, name, value):
                if name.startswith('_'):
                    object.__setattr__(self, name, value)
                else:
                    self._dynamic_attrs[name] = value

            def __getattr__(self, name):
                if name in self._dynamic_attrs:
                    return self._dynamic_attrs[name]
                raise AttributeError(f\"'{self.__class__.__name__}' object has no attribute '{name}'\")

            def __contains__(self, key):
                return key in self._dynamic_attrs

            def __iter__(self):
                return iter(self._dynamic_attrs)'''

content = content.replace(old_mock, new_mock)

with open('tests/test_consultants_simple.py', 'w', encoding='utf-8') as f:
    f.write(content)
