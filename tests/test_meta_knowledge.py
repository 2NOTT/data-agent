import unittest
from datetime import date
from decimal import Decimal

from app.services.meta_knowledge_service import _json_safe


class MetaKnowledgeTests(unittest.TestCase):
    def test_json_safe_converts_database_scalar_values(self):
        value = _json_safe([date(2026, 1, 3), Decimal("1999.00"), 2])
        self.assertEqual(value, ["2026-01-03", 1999.0, 2])


if __name__ == "__main__":
    unittest.main()
