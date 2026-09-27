import unittest

from app.core.sql_guard import SQLValidationError, normalize_sql, validate_read_only_sql


class SqlGuardTests(unittest.TestCase):
    def test_accepts_select_with_trailing_semicolon(self):
        sql = validate_read_only_sql(" SELECT COUNT(*) AS total FROM enrollments; ")
        self.assertEqual(sql, "SELECT COUNT(*) AS total FROM enrollments")

    def test_rejects_write_statement(self):
        with self.assertRaises(SQLValidationError):
            validate_read_only_sql("DELETE FROM enrollments")

    def test_rejects_multiple_statements(self):
        with self.assertRaises(SQLValidationError):
            validate_read_only_sql("SELECT 1; SELECT 2")

    def test_normalize_sql_removes_markdown_fence(self):
        self.assertEqual(normalize_sql("```sql\nSELECT 1;\n```"), "SELECT 1")


if __name__ == "__main__":
    unittest.main()
