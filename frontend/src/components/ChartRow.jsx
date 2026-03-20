import styles from './ChartRow.module.css'

function VelocityChart() {
  return (
    <svg width="100%" height="70" viewBox="0 0 260 70" preserveAspectRatio="none">
      <defs>
        <linearGradient id="vg" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%"   stopColor="#a87d3a" stopOpacity="0.18" />
          <stop offset="100%" stopColor="#a87d3a" stopOpacity="0"    />
        </linearGradient>
      </defs>
      <path
        d="M0,58 C20,56 40,54 60,50 C80,46 100,44 120,38 C140,32 160,28 180,20 C200,12 220,10 240,7 L260,5 L260,70 L0,70Z"
        fill="url(#vg)"
      />
      <path
        d="M0,58 C20,56 40,54 60,50 C80,46 100,44 120,38 C140,32 160,28 180,20 C200,12 220,10 240,7 L260,5"
        fill="none" stroke="var(--gold)" strokeWidth="1.2"
      />
      <circle cx="260" cy="5" r="2.5" fill="var(--gold)" />
      <line x1="0" y1="70" x2="260" y2="70" stroke="var(--border)" strokeWidth="0.5" />
    </svg>
  )
}

function CategoryBars({ mix = {} }) {
  const cats = [
    { key: 'silhouette', label: 'Sil.' },
    { key: 'fabric',     label: 'Fab.' },
    { key: 'colour',     label: 'Col.' },
    { key: 'footwear',   label: 'Foot.' },
    { key: 'other',      label: 'Other' },
  ]
  const max = Math.max(...cats.map(c => mix[c.key] || 0), 1)

  return (
    <div className={styles.bars}>
      {cats.map(c => (
        <div key={c.key} className={styles.barCol}>
          <div
            className={`${styles.bar} ${(mix[c.key] || 0) >= 30 ? styles.hot : ''}`}
            style={{ height: `${((mix[c.key] || 0) / max) * 100}%` }}
          />
          <span className={styles.barLabel}>{c.label}</span>
        </div>
      ))}
    </div>
  )
}

export default function ChartRow({ categoryMix }) {
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Today']

  return (
    <div className={styles.row}>
      <div className={styles.card}>
        <div className={styles.title}>Signal Velocity · Past 7 days</div>
        <VelocityChart />
        <div className={styles.dayLabels}>
          {days.map(d => <span key={d}>{d}</span>)}
        </div>
      </div>

      <div className={styles.card}>
        <div className={styles.title}>Top Categories · Rising Signals</div>
        <CategoryBars mix={categoryMix} />
      </div>
    </div>
  )
}
