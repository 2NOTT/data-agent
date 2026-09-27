import json
import unittest
from unittest.mock import AsyncMock, patch

from app.services.query_service import QueryService


class QueryServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_search_emits_graph_events_and_done(self):
        service = QueryService(None, None, None, None, None, None)

        async def fake_astream(**_kwargs):
            yield {"stage": "提取关键字"}
            yield {"result": [{"报名人数": 12}]}

        with patch("app.services.query_service.graph.astream", fake_astream):
            events = [event async for event in service.search("本月报名人数")]

        payloads = [json.loads(event.removeprefix("data: ").strip()) for event in events]
        self.assertEqual(payloads[0], {"stage": "提取关键字", "type": "progress"})
        self.assertEqual(payloads[1], {"result": [{"报名人数": 12}], "type": "progress"})
        self.assertEqual(payloads[-1]["type"], "done")

    async def test_search_turns_graph_errors_into_sse_error(self):
        service = QueryService(None, None, None, None, None, None)

        async def failing_astream(**_kwargs):
            raise RuntimeError("database unavailable")
            yield  # pragma: no cover

        with patch("app.services.query_service.graph.astream", failing_astream):
            events = [event async for event in service.search("查询收入")]

        payload = json.loads(events[-1].removeprefix("data: ").strip())
        self.assertEqual(payload["type"], "error")
        self.assertIn("database unavailable", payload["message"])


if __name__ == "__main__":
    unittest.main()
