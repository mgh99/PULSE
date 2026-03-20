import { useCallback, useEffect, useState } from 'react'

const POLL_INTERVAL = 15000
const API_BASE = import.meta.env.VITE_API_URL || ''

export function useDashboard(lang = 'en') {
  const [data, setData]             = useState(null)
  const [loading, setLoading]       = useState(true)
  const [error, setError]           = useState(null)
  const [lastUpdate, setLastUpdate] = useState(null)

  const fetchDashboard = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/api/dashboard?lang=${lang}`)
      if (!res.ok) throw new Error(`API error: ${res.status}`)
      const json = await res.json()
      setData(json)
      setLastUpdate(new Date())
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [lang])

  // Cuando cambia el idioma, resetea datos y vuelve a cargar
  useEffect(() => {
    setData(null)
    setLoading(true)
    fetchDashboard()
  }, [lang])

  // Polling cada 15s
  useEffect(() => {
    const interval = setInterval(fetchDashboard, POLL_INTERVAL)
    return () => clearInterval(interval)
  }, [fetchDashboard])

  const triggerRefresh = useCallback(async () => {
    await fetch(`${API_BASE}/api/refresh?lang=${lang}`, { method: 'POST' })
    setTimeout(fetchDashboard, 3000)
  }, [lang, fetchDashboard])

  return { data, loading, error, lastUpdate, triggerRefresh }
}