import { useEffect, useRef, useState } from 'react'
import { useLang } from '../i18n/LangContext.jsx'
import styles from './SidebarLeft.module.css'

function DonutChart({ mix = {} }) {
  const { t } = useLang()
  const circumference = 163
  const labels = t?.donutLabels || ['Silhouette', 'Fabric', 'Colour', 'Other']
  const segments = [
    { key: 'silhouette', color: 'var(--gold)',   label: labels[0] },
    { key: 'fabric',     color: 'var(--gold2)',  label: labels[1] },
    { key: 'colour',     color: 'var(--gold3)',  label: labels[2] },
    { key: 'other',      color: 'var(--cream3)', label: labels[3] },
  ]

  let offset = 0
  const slices = segments.map(seg => {
    const pct  = mix[seg.key] || 0
    const dash = (pct / 100) * circumference
    const slice = { ...seg, pct, dash, offset }
    offset += dash
    return slice
  })

  return (
    <div className={styles.donutWrap}>
      <svg width="72" height="72" viewBox="0 0 72 72">
        <circle cx="36" cy="36" r="26" fill="none" stroke="var(--cream3)" strokeWidth="10" />
        {slices.map((s, i) => (
          <circle
            key={i}
            cx="36" cy="36" r="26"
            fill="none"
            stroke={s.color}
            strokeWidth="10"
            strokeDasharray={`${s.dash} ${circumference - s.dash}`}
            strokeDashoffset={-s.offset}
            transform="rotate(-90 36 36)"
            style={{ animation: `donutFill 1s ease ${i * 0.15}s both` }}
          />
        ))}
        <text x="36" y="39" textAnchor="middle" fontFamily="'Playfair Display',serif" fontSize="11" fill="var(--ink)">SS26</text>
      </svg>
      <div className={styles.legend}>
        {slices.map((s, i) => (
          <div key={i} className={styles.legendItem}>
            <div className={styles.legendDot} style={{ background: s.color, border: s.key === 'other' ? '0.5px solid var(--gold2)' : 'none' }} />
            <span className={styles.legendName}>{s.label}</span>
            <span className={styles.legendPct}>{s.pct}%</span>
          </div>
        ))}
      </div>
    </div>
  )
}

function Typewriter({ text = '', lang }) {
  const [displayed, setDisplayed] = useState('')
  const prevText = useRef('')

  useEffect(() => {
    if (text === prevText.current) return
    prevText.current = text
    setDisplayed('')
    let i = 0
    const interval = setInterval(() => {
      setDisplayed(text.slice(0, i + 1))
      i++
      if (i >= text.length) clearInterval(interval)
    }, 18)
    return () => clearInterval(interval)
  }, [text, lang])

  return <span>{displayed}<span className={styles.cursor}>|</span></span>
}

export default function SidebarLeft({ categoryMix, editorialBrief, generatedAt, onCategoryChange, activeCategory, lang, regionalScores }) {
  const { t } = useLang()

  const REGIONS = [
    { flag: '🇮🇹', name: 'Milan',    key: 'milan',    scoreFallback: 88 },
    { flag: '🇫🇷', name: 'Paris',    key: 'paris',    scoreFallback: 81 },
    { flag: '🇯🇵', name: 'Tokyo',    key: 'tokyo',    scoreFallback: 74 },
    { flag: '🇺🇸', name: 'New York', key: 'new_york', scoreFallback: 69 },
    { flag: '🇰🇷', name: 'Seoul',    key: 'seoul',    scoreFallback: 62 },
    { flag: '🇬🇧', name: 'London',   key: 'london',   scoreFallback: 55 },
  ]

  const CATEGORIES = t?.pills || ['All', 'Silhouette', 'Colour', 'Fabric', 'Footwear', 'Accessories', 'Streetwear', 'Couture']

  const handleCategory = (c) => {
    onCategoryChange(c)
  }

  const timeStr = generatedAt
    ? new Date(generatedAt).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })
    : '--:--'

  return (
    <aside className={styles.sidebar}>

      <div className={styles.section}>
        <div className={styles.sectionLabel}>{t?.regionalPulse || 'Regional Pulse'}</div>
        {REGIONS.map(r => {
          const score = regionalScores?.[r.key] ?? r.scoreFallback
          return (
            <div key={r.name} className={styles.regionItem}>
              <span className={styles.flag}>{r.flag}</span>
              <span className={styles.regionName}>{r.name}</span>
              <div className={styles.barWrap}>
                <div className={styles.bar} style={{ width: `${score}%` }} />
              </div>
              <span className={styles.score}>{score}</span>
            </div>
          )
        })}
      </div>

      <div className={styles.section}>
        <div className={styles.sectionLabel}>{t?.categories || 'Categories'}</div>
        <div className={styles.pills}>
          {CATEGORIES.map(c => (
            <div
              key={c}
              className={`${styles.pill} ${activeCategory === c ? styles.active : ''}`}
              onClick={() => handleCategory(c)}
            >
              {c}
            </div>
          ))}
        </div>
      </div>

      <div className={styles.section}>
        <div className={styles.sectionLabel}>{t?.categoryMix || 'Category Mix · SS26'}</div>
        <DonutChart mix={categoryMix} />
      </div>

      <div className={styles.section} style={{ flex: 1 }}>
        <div className={styles.sectionLabel}>{t?.aiEditorial || 'AI Editorial Brief'}</div>
        <div className={styles.aiBrief}>
          <div className={styles.aiLabel}>{t?.generated || 'Generated'} · {timeStr} UTC</div>
          <div className={styles.aiText}>
            <Typewriter text={editorialBrief || ''} lang={lang} />
          </div>
        </div>
      </div>

    </aside>
  )
}