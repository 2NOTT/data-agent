import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import test from 'node:test'
import { toChartRows, inferChart } from '../frontend/src/chart-data.js'
import { createReplayResponse } from '../frontend/src/replay.js'

test('database decimal strings become chart values while dates and IDs remain categories', () => {
  const rows = [{ month: '202601', student_id: '001', monthly_revenue: '7796.00', revenue: '7796.00', rate: '78.8462', campus: '广州校区', missing: null }]
  assert.deepEqual(toChartRows(rows), [{ month: '202601', student_id: '001', monthly_revenue: 7796, revenue: 7796, rate: 78.8462, campus: '广州校区', missing: null }])
  assert.equal(rows[0].revenue, '7796.00')
})

test('percentages chart as numbers and readable course names label categories', () => {
  const rows = toChartRows([{ month: '2026-01', completion_rate: '78.85%' }])
  assert.equal(rows[0].completion_rate, 78.85)
  assert.equal(inferChart(rows).kind, 'line')
  const course = inferChart([{ course_id: 1, course_name: 'Python数据分析', count: 3 }])
  assert.equal(course.category, 'course_name')
  assert.deepEqual(course.numeric, ['count'])
})

test('every public example replays its recorded SQL and rows through SSE', async () => {
  const data = JSON.parse(await readFile(new URL('../frontend/src/demo-queries.json', import.meta.url), 'utf8'))
  assert.equal(data.queries.length, 4)
  for (const recording of data.queries) {
    const response = createReplayResponse(recording.query, data.queries)
    assert.equal(response.headers.get('Content-Type'), 'text/event-stream')
    const events = (await response.text()).trim().split('\n\n').map((chunk) => JSON.parse(chunk.slice(6)))
    assert.deepEqual(events, recording.events)
    assert.equal(events.at(-1).type, 'done')
    const result = events.find((event) => event.type === 'result')
    assert.ok(result.sql && result.result.length)
  }
  assert.throws(() => createReplayResponse('unsupported question', data.queries), /四个示例/)
})
