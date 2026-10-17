export function createReplayResponse(question, recordings) {
  const recording = recordings.find((item) => item.query === question)
  if (!recording) throw new Error('在线演示支持下方四个示例问题，完整自由问数请运行 GitHub 中的后端。')
  const encoder = new TextEncoder()
  const stream = new ReadableStream({
    async start(controller) {
      for (const event of recording.events) {
        controller.enqueue(encoder.encode(`data: ${JSON.stringify(event)}\n\n`))
        if (event.stage || event.state) await new Promise((resolve) => setTimeout(resolve, 140))
      }
      controller.close()
    },
  })
  return new Response(stream, { headers: { 'Content-Type': 'text/event-stream' } })
}
