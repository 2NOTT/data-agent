export function toChartRows(rows) {
  return rows.map((row) => Object.fromEntries(Object.entries(row).map(([key, value]) => {
    const categorical = /(?:^|_)(?:date|time|month|week|year|day|id)$|(?:日期|时间|月份|年月|年|月|周|编号)$/i.test(key)
    const numeric = typeof value === 'string' && value.trim() !== '' ? Number(value.replace(/%$/, '')) : value
    return [key, !categorical && typeof numeric === 'number' && Number.isFinite(numeric) ? numeric : value]
  })))
}

export function inferChart(rows) {
  if (!rows.length) return { kind: 'empty', category: '', numeric: [] }
  const keys = Object.keys(rows[0])
  const numeric = keys.filter((key) => !/(?:^|_)id$|编号/i.test(key) && rows.some((row) => typeof row[key] === 'number'))
  const categories = keys.filter((key) => !numeric.includes(key))
  const category = categories.find((key) => !/(?:^|_)id$|编号/i.test(key)) || keys[0]
  const temporal = /日期|时间|月份|月|周|date|time|month/i.test(category)
  return { kind: temporal ? 'line' : 'bar', category, numeric: numeric.slice(0, 2) }
}
