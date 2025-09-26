"""
Package fixtures pour les tests Consultator
Contient les classes de base et configurations partagées
"""

from .base_test import BaseDatabaseTest
from .base_test import BaseIntegrationTest
from .base_test import BaseServiceTest
from .base_test import BaseTest
from .base_test import BaseUITest
from .base_test import BaseUnitTest
from .base_test import TestDataFactory
from .base_test import assert_contains_text
from .base_test import assert_positive_number
from .base_test import assert_valid_email

__all__ = [
    "BaseTest",
    "BaseUnitTest",
    "BaseIntegrationTest",
    "BaseUITest",
    "BaseDatabaseTest",
    "BaseServiceTest",
    "TestDataFactory",
    "assert_contains_text",
    "assert_valid_email",
    "assert_positive_number",
]
