import React, { useEffect, useMemo, useState } from 'react'
import { createRoot } from 'react-dom/client'
import {
  Activity,
  ArrowUpRight,
  BarChart3,
  BookOpen,
  Check,
  ChevronRight,
  Clock3,
  Database,
  FileCode2,
  History,
  LoaderCircle,
  MessageSquareText,
  RefreshCw,
  Search,
  Send,
  ShieldCheck,
  Sparkles,
  Table2,
  X,
} from 'lucide-react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import './styles.css'

const examples = [
  '2026年1月至3月各校区的报名人数和收入是多少？',
  '2026年1月至3月完课率变化情况？',
  '各课程的报名人数排名如何？',
  '学生和成人学员的报名收入对比？',
]

const flowStages = ['提取关键字', '召回字段', '召回指标', '合并召回', '生成SQL', '校验SQL', '执行SQL']

function formatValue(value) {
  if (value === null || value === undefined) return '—'
  if (typeof value === 'number') return value.toLocaleString('zh-CN', { maximumFractionDigits: 2 })
  return String(value)
}

function getRows(data) {
  return Array.isArray(data) ? data : []
}

function inferChart(rows) {
  if (!rows.length) return { kind: 'empty', category: '', numeric: [] }
  const keys = Object.keys(rows[0])
  const numeric = keys.filter((key) => rows.some((row) => typeof row[key] === 'number'))
  const category = keys.find((key) => !numeric.includes(key)) || keys[0]
  const temporal = /日期|时间|月份|月|周|date|time|month/i.test(category)
  return { kind: temporal ? 'line' : 'bar', category, numeric: numeric.slice(0, 2) }
}

function ChartPanel({ rows }) {
  const chart = useMemo(() => inferChart(rows), [rows])
  if (chart.kind === 'empty' || !chart.numeric.length) {
    return <div className="chart-empty"><BarChart3 size={21} /><span>查询结果中的数值字段会自动生成图表</span></div>
  }
  const colors = ['#0f8b8d', '#ef8354']
  const Chart = chart.kind === 'line' ? LineChart : BarChart
  return (
    <div className="chart-wrap">
      <ResponsiveContainer width="100%" height={260}>
        <Chart data={rows} margin={{ top: 10, right: 12, left: -14, bottom: 0 }}>
          <CartesianGrid stroke="#e7edf0" vertical={false} />
          <XAxis dataKey={chart.category} tick={{ fill: '#71828b', fontSize: 12 }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fill: '#71828b', fontSize: 12 }} axisLine={false} tickLine={false} width={42} />
          <Tooltip contentStyle={{ border: '1px solid #dbe5e8', borderRadius: 10, boxShadow: '0 8px 24px rgba(13,39,54,.08)' }} formatter={(value) => formatValue(value)} />
          {chart.numeric.map((key, index) => chart.kind === 'line'
            ? <Line key={key} type="monotone" dataKey={key} stroke={colors[index]} strokeWidth={3} dot={{ r: 3, strokeWidth: 2, fill: '#fff' }} />
            : <Bar key={key} dataKey={key} fill={colors[index]} radius={[4, 4, 0, 0]} maxBarSize={38}>
              {rows.map((_, rowIndex) => <Cell key={rowIndex} fill={colors[index]} opacity={rowIndex % 2 ? 0.78 : 1} />)}
            </Bar>)}
        </Chart>
      </ResponsiveContainer>
    </div>
  )
}

function App() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [events, setEvents] = useState([])
  const [result, setResult] = useState([])
  const [sql, setSql] = useState('')
  const [error, setError] = useState('')
  const [history, setHistory] = useState(() => JSON.parse(localStorage.getItem('data-agent-history') || '[]'))
  const [serviceOnline, setServiceOnline] = useState(false)
  const [activeView, setActiveView] = useState('workspace')

  useEffect(() => {
    fetch('/health').then((response) => setServiceOnline(response.ok)).catch(() => setServiceOnline(false))
  }, [])

  const currentStage = events.at(-1) || ''
  const rows = getRows(result)
  const columns = rows.length ? Object.keys(rows[0]) : []
  const hasCompletedQuery = Boolean(sql || error || events.length)

  async function ask(question = query) {
    const cleanQuestion = question.trim()
    if (!cleanQuestion || loading) return
    setQuery(cleanQuestion)
    setLoading(true)
    setError('')
    setResult([])
    setSql('')
    setEvents([])
    setActiveView('workspace')
    try {
      const response = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'text/event-stream' },
        body: JSON.stringify({ query: cleanQuestion }),
      })
      if (!response.ok || !response.body) throw new Error(`服务返回 ${response.status}`)
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      while (true) {
        const { value, done } = await reader.read()
        buffer += decoder.decode(value || new Uint8Array(), { stream: !done })
        const chunks = buffer.split('\n\n')
        buffer = chunks.pop() || ''
        for (const chunk of chunks) {
          const line = chunk.split('\n').find((item) => item.startsWith('data:'))
          if (!line) continue
          const event = JSON.parse(line.slice(5).trim())
          if (event.type === 'error') setError(event.message || '查询失败')
          if (event.type === 'progress' || event.stage || event.state) {
            const stage = event.stage || event.state
            if (stage) setEvents((previous) => previous.includes(stage) ? previous : [...previous, stage])
          }
          if (event.type === 'result') {
            setResult(event.result || [])
            setSql(event.sql || '')
          }
        }
        if (done) break
      }
      const record = { query: cleanQuestion, time: new Date().toISOString() }
      setHistory((previous) => {
        const next = [record, ...previous.filter((item) => item.query !== cleanQuestion)].slice(0, 6)
        localStorage.setItem('data-agent-history', JSON.stringify(next))
        return next
      })
    } catch (requestError) {
      setError(requestError.message || '网络请求失败')
    } finally {
      setLoading(false)
    }
  }

  function clearResult() {
    setQuery('')
    setEvents([])
    setResult([])
    setSql('')
    setError('')
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark"><Sparkles size={18} /></div>
          <div><strong>知数台</strong><span>EDU DATA AGENT</span></div>
        </div>
        <div className="side-label">工作空间</div>
        <nav className="side-nav">
          <button className={activeView === 'workspace' ? 'active' : ''} onClick={() => setActiveView('workspace')}><MessageSquareText size={17} /><span className="nav-text">问数工作台</span></button>
          <button className={activeView === 'history' ? 'active' : ''} onClick={() => setActiveView('history')}><History size={17} /><span className="nav-text">查询记录</span><span className="nav-count">{history.length}</span></button>
          <button className={activeView === 'guide' ? 'active' : ''} onClick={() => setActiveView('guide')}><BookOpen size={17} /><span className="nav-text">数据说明</span></button>
        </nav>
        <div className="sidebar-bottom">
          <div className="health-chip"><span className={serviceOnline ? 'status-dot online' : 'status-dot'}></span><span>{serviceOnline ? '服务已连接' : '等待服务连接'}</span></div>
          <div className="sidebar-note">只读查询 · LangGraph 编排<br />适用于教育经营分析</div>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumb"><span>教育数据平台</span><ChevronRight size={14} /><strong>{activeView === 'workspace' ? '问数工作台' : activeView === 'history' ? '查询记录' : '数据说明'}</strong></div>
          <div className="topbar-right"><div className="safe-badge"><ShieldCheck size={15} />只读安全模式</div><div className="avatar">廖</div></div>
        </header>

        {activeView === 'workspace' && <div className="workspace-content">
          <section className="welcome-row">
            <div><p className="eyebrow">EDUCATION ANALYTICS</p><h1>把问题交给数据，<em>答案马上出现。</em></h1><p className="welcome-copy">用自然语言探索报名、收入、课程与完课率，让每一次运营判断都有数据依据。</p></div>
            <div className="date-note"><Clock3 size={15} />今天 · 实时数仓</div>
          </section>

          <section className="ask-box">
            <div className="ask-icon"><Search size={20} /></div>
            <textarea value={query} onChange={(event) => setQuery(event.target.value)} onKeyDown={(event) => { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); ask() } }} placeholder="例如：最近三个月各课程的报名人数和收入是多少？" rows={2} />
            <div className="ask-actions"><span>Enter 发送 · Shift + Enter 换行</span><button className="send-button" onClick={() => ask()} disabled={loading || !query.trim()}>{loading ? <LoaderCircle size={17} className="spin" /> : <Send size={17} />}<span>{loading ? '分析中' : '开始分析'}</span></button></div>
          </section>

          <div className="suggestions">{examples.map((example) => <button key={example} onClick={() => ask(example)}><Sparkles size={13} />{example}<ArrowUpRight size={13} /></button>)}</div>

          {(loading || events.length > 0 || error) && <section className="process-panel panel"><div className="panel-heading"><div><span className="section-kicker">LIVE TRACE</span><h2>分析过程</h2></div><span className={loading ? 'live-state' : 'done-state'}>{loading ? <><Activity size={14} />正在处理</> : <><Check size={14} />已完成</>}</span></div><div className="stage-list">{flowStages.map((stage) => { const done = events.includes(stage); const current = currentStage === stage && loading; return <div className={`stage ${done ? 'done' : ''} ${current ? 'current' : ''}`} key={stage}><span className="stage-indicator">{done ? <Check size={12} /> : current ? <LoaderCircle size={12} className="spin" /> : ''}</span><span>{stage}</span>{current && <span className="stage-progress">处理中</span>}</div> })}</div>{error && <div className="error-box"><X size={16} /><span>{error}</span></div>}</section>}

          <section className="results-grid">
            <div className="result-main panel"><div className="panel-heading"><div><span className="section-kicker">QUERY RESULT</span><h2>查询结果 {rows.length > 0 && <small>{rows.length} 条记录</small>}</h2></div><div className="heading-actions">{rows.length > 0 && <button className="icon-button" title="清空结果" onClick={clearResult}><RefreshCw size={16} /></button>}<Table2 size={19} className="muted-icon" /></div></div>{rows.length > 0 ? <div className="table-scroll"><table><thead><tr>{columns.map((column) => <th key={column}>{column}</th>)}</tr></thead><tbody>{rows.map((row, index) => <tr key={index}>{columns.map((column) => <td key={column}>{formatValue(row[column])}</td>)}</tr>)}</tbody></table></div> : <div className="empty-result"><div className="empty-icon"><Database size={22} /></div><strong>{hasCompletedQuery ? '本次查询没有匹配到数据' : '你的数据答案会出现在这里'}</strong><span>{hasCompletedQuery ? '可以换一个时间范围，例如 2026 年 1 月至 3 月。' : '输入一个经营问题，系统会自动生成 SQL 并返回可视化结果。'}</span></div>}</div>
            <div className="result-chart panel"><div className="panel-heading"><div><span className="section-kicker">VISUAL SUMMARY</span><h2>趋势概览</h2></div><BarChart3 size={19} className="muted-icon" /></div><ChartPanel rows={rows} /></div>
          </section>

          <section className="detail-grid"><div className="sql-panel panel"><div className="panel-heading"><div><span className="section-kicker">GENERATED SQL</span><h2>生成的查询</h2></div><FileCode2 size={19} className="muted-icon" /></div><pre>{sql || '执行查询后，这里会展示经过只读校验的 SQL。'}</pre></div><div className="metric-panel panel"><div className="panel-heading"><div><span className="section-kicker">DATA CONTRACT</span><h2>指标口径</h2></div><ShieldCheck size={18} className="muted-icon" /></div><div className="contract-list"><div><span>数据范围</span><strong>教育经营数仓</strong></div><div><span>查询方式</span><strong>自然语言 → SQL</strong></div><div><span>安全策略</span><strong>单条只读查询</strong></div></div></div></section>
        </div>}

        {activeView === 'history' && <section className="secondary-view"><p className="eyebrow">QUERY HISTORY</p><h1>查询记录</h1><p className="welcome-copy">最近的问题会保存在当前浏览器中，点击即可重新分析。</p>{history.length ? <div className="history-list">{history.map((item) => <button key={item.time} onClick={() => ask(item.query)}><span className="history-icon"><History size={16} /></span><span><strong>{item.query}</strong><small>{new Date(item.time).toLocaleString('zh-CN')}</small></span><ArrowUpRight size={16} /></button>)}</div> : <div className="empty-secondary"><History size={24} /><span>还没有查询记录</span></div>}</section>}

        {activeView === 'guide' && <section className="secondary-view"><p className="eyebrow">DATA GUIDE</p><h1>数据说明</h1><p className="welcome-copy">知数台将教育业务问题拆解成可追溯的指标、字段和 SQL。</p><div className="guide-grid"><div><Database size={21} /><h3>教育经营数仓</h3><p>围绕学员、课程、校区与报名事实组织查询，支持报名人数、收入、完课率等核心分析。</p></div><div><Sparkles size={21} /><h3>智能问数流程</h3><p>关键词提取、字段与指标召回、SQL 生成、只读校验和执行全程可见。</p></div><div><ShieldCheck size={21} /><h3>安全执行</h3><p>系统只允许单条 SELECT / WITH 查询，生成 SQL 通过校验后才会访问数仓。</p></div></div></section>}
      </main>
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App />)
