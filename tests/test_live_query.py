import json
import os
import re
import unittest
from urllib.request import Request, urlopen


@unittest.skipUnless(os.getenv("DATA_AGENT_TEST_URL"), "需要运行中的服务及仓库附带的教育示例数据")
class LiveQueryTests(unittest.TestCase):
    def test_campus_student_counts_and_revenue(self):
        request = Request(
            os.environ["DATA_AGENT_TEST_URL"].rstrip("/") + "/api/query",
            data=json.dumps({"query": "2026年1月至3月各校区的报名人数和收入是多少？"}).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(request, timeout=120) as response:
            events = [json.loads(line[5:]) for line in response if line.startswith(b"data:")]
        self.assertFalse([event for event in events if event.get("type") == "error"])
        self.assertEqual(events[-1]["type"], "done")
        rows = next(event["result"] for event in events if event.get("type") == "result")
        expected = {"广州校区": [3, 7796], "深圳校区": [2, 6097], "线上学习中心": [3, 12296]}
        actual = {}
        for row in rows:
            # 模型可能使用中英文列别名，按校区值和数值比较业务结果。
            campus = next(value for value in row.values() if isinstance(value, str) and value in expected)
            actual[campus] = sorted(float(value) for value in row.values() if value != campus)
        self.assertEqual(len(rows), len(expected))
        self.assertEqual(actual, expected)

    def test_monthly_completion_rates_use_enrollment_dates(self):
        request = Request(
            os.environ["DATA_AGENT_TEST_URL"].rstrip("/") + "/api/query",
            data=json.dumps({"query": "2026年1月至3月完课率变化情况？"}).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urlopen(request, timeout=120) as response:
            events = [json.loads(line[5:]) for line in response if line.startswith(b"data:")]
        self.assertFalse([event for event in events if event.get("type") == "error"])
        self.assertEqual(events[-1]["type"], "done")
        rows = next(event["result"] for event in events if event.get("type") == "result")
        expected = {"202601": 78.8462, "202602": 70.5882, "202603": 53.5714}
        self.assertEqual(len(rows), 3, "月度趋势必须恰好包含三个月，不能按日分组")
        actual = {}
        for row in rows:
            date_value = next(value for value in row.values() if "2026" in str(value))
            parts = re.findall(r"\d+", str(date_value))
            month = parts[0] if len(parts) == 1 else parts[0] + parts[1].zfill(2)
            actual[month] = float(str(next(value for value in row.values() if value != date_value)).rstrip('%'))
        self.assertEqual(set(actual), set(expected))
        for month, rate in expected.items():
            self.assertAlmostEqual(actual[month], rate, delta=0.01)


if __name__ == "__main__":
    unittest.main()
