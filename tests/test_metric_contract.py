import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from langchain_core.runnables import RunnableLambda

from app.agent.nodes.filter_table import filter_table
from app.conf.meta_config import meta_config


class MetricContractTests(unittest.IsolatedAsyncioTestCase):
    def test_metric_dependencies_match_formulas(self):
        metrics = {metric.name: metric for metric in meta_config.metrics}
        self.assertIn("fact_enrollment.student_id", metrics["ENROLLMENT_COUNT"].relevant_columns)
        for metric in metrics.values():
            self.assertIn("fact_enrollment.status_code", metric.relevant_columns)
            self.assertIn("fact_enrollment.enrollment_date", metric.relevant_columns)

    async def test_table_filter_preserves_metric_dependencies(self):
        state = {
            "query": "报名人数",
            "metric_infos": [{"relevant_columns": ["fact_enrollment.student_id", "fact_enrollment.status_code"]}],
            "table_infos": [
                {"name": "fact_enrollment", "columns": [
                    {"name": "student_id"}, {"name": "status_code"}, {"name": "amount"},
                ]},
                {"name": "dim_course", "columns": [{"name": "course_name"}]},
            ],
        }
        runtime = SimpleNamespace(stream_writer=Mock())
        with patch("app.agent.nodes.filter_table.llm", RunnableLambda(lambda _: "{}")):
            result = await filter_table(state, runtime)
        self.assertEqual(len(result["table_infos"]), 1)
        self.assertEqual(
            [column["name"] for column in result["table_infos"][0]["columns"]],
            ["student_id", "status_code"],
        )


if __name__ == "__main__":
    unittest.main()
