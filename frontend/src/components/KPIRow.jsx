import { useEffect, useRef } from 'react'
import { useLang } from '../i18n/LangContext.jsx'
import styles from './KPIRow.module.css'

function AnimatedNumber({ value }) {
  const ref = useRef(null)

  useEffect(() => {
    const target = parseInt(value) || 0
    if (isNaN(target)) return

    let start = 0
    const duration = 1200
    const step = (timestamp) => {
      if (!startTime) startTime = timestamp
      const progress = Math.min((timestamp - startTime) / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3) // ease out cubic
      ref.current.textContent = Math.floor(eased * target)
      if (progress < 1) requestAnimationFrame(step)
    }
    let startTime = null
    requestAnimationFrame(step)
  }, [value])

  return <span ref={ref}>{value}</span>
}

export default function KPIRow({ kpis = {} }) {
  const { t } = useLang()

  const cards = [
    { label: t.activeSignals, value: kpis.active_signals ?? '—', sub: t.updatedNow,     dir: 'up'   },
    { label: t.topVelocity,   value: kpis.top_velocity   ?? '—', sub: t.thisCycle,      dir: 'up'   },
    { label: t.markets,       value: kpis.markets        ?? '—', sub: t.regionsTracked, dir: 'flat' },
    { label: t.fading,        value: kpis.fading         ?? '—', sub: t.losingMomentum, dir: 'down' },
  ]

  return (
    <div className={styles.row}>
      {cards.map((c, i) => (
        <div key={i} className={styles.card}>
          <div className={styles.label}>{c.label}</div>
          <div className={styles.value}>
            <AnimatedNumber value={c.value} />
          </div>
          <div className={`${styles.sub} ${styles[c.dir]}`}>{c.sub}</div>
        </div>
      ))}
    </div>
  )
}