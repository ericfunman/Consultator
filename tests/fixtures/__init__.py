"""
Package fixtures pour les tests Consultator
Contient les classes de base et configurations partagées
"""

from .base_test import (
    BaseTest,
    BaseUnitTest,
    BaseIntegrationTest,
    BaseUITest,
    BaseDatabaseTest,
    BaseServiceTest,
    TestDataFactory,
    assert_contains_text,
    assert_valid_email,
    assert_positive_number
)

__all__ = [
    'BaseTest',
    'BaseUnitTest',
    'BaseIntegrationTest',
    'BaseUITest',
    'BaseDatabaseTest',
    'BaseServiceTest',
    'TestDataFactory',
    'assert_contains_text',
    'assert_valid_email',
    'assert_positive_number'
]
