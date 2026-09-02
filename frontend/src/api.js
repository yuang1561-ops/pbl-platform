const API = '/pbl-api'

export async function get(path, params = {}) {
  const qs = new URLSearchParams(params).toString()
  const res = await fetch(`${API}${path}${qs ? '?' + qs : ''}`)
  return res.json()
}

export async function post(path, body) {
  const res = await fetch(`${API}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  if (!res.ok) throw new Error('请求失败')
  const ct = res.headers.get('content-type') || ''
  if (ct.includes('json')) return res.json()
  return res
}

export function saveProgress(courseId, state) {
  const key = `pbl-progress-${courseId}`
  localStorage.setItem(key, JSON.stringify(state))
}

export function loadProgress(courseId) {
  try { return JSON.parse(localStorage.getItem(`pbl-progress-${courseId}`)) || {} } catch { return {} }
}

export function saveWorkshop(data) {
  localStorage.setItem('pbl-workshop', JSON.stringify(data))
}

export function loadWorkshop() {
  try { return JSON.parse(localStorage.getItem('pbl-workshop')) || null } catch { return null }
}
