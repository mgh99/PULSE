import styles from './SidebarRight.module.css'

const ROMAN = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']

const HEATMAP_DATA = [
  2,3,4,3,5,2,1,
  3,4,5,4,6,3,2,
  4,5,7,6,8,4,2,
  5,6,8,9,10,5,3,
]

function Heatmap() {
  const days = ['M','T','W','T','F','S','S']
  const max  = Math.max(...HEATMAP_DATA)

  return (
    <div>
      <div className={styles.hmDays}>
        {days.map((d, i) => <span key={i}>{d}</span>)}
      </div>
      <div className={styles.heatmap}>
        {HEATMAP_DATA.map((v, i) => (
          <div
            key={i}
            className={styles.hmCell}
            style={{ opacity: 0.15 + (v / max) * 0.85 }}
          />
        ))}
      </div>
    </div>
  )
}

export default function SidebarRight({ brands = [], searchTerms = [] }) {
  const maxSearch = Math.max(...searchTerms.map(t => t.velocity || 0), 1)

  return (
    <aside className={styles.sidebar}>

      <div className={styles.section}>
        <div className={styles.sectionLabel}>Signal Velocity · 24h</div>
        <svg width="100%" height="52" viewBox="0 0 180 52" preserveAspectRatio="none">
          <defs>
            <linearGradient id="sg2" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%"   stopColor="#a87d3a" stopOpacity="0.2" />
              <stop offset="100%" stopColor="#a87d3a" stopOpacity="0"   />
            </linearGradient>
          </defs>
          <path
            d="M0,46 C15,44 30,42 50,38 C70,34 90,30 110,22 C130,14 150,10 170,6 L180,4 L180,52 L0,52Z"
            fill="url(#sg2)"
          />
          <path
            d="M0,46 C15,44 30,42 50,38 C70,34 90,30 110,22 C130,14 150,10 170,6 L180,4"
            fill="none" stroke="var(--gold)" strokeWidth="1"
          />
          <circle cx="180" cy="4" r="2" fill="var(--gold)" />
        </svg>
      </div>

      <div className={styles.section}>
        <div className={styles.sectionLabel}>Brand Momentum</div>
        {brands.slice(0, 7).map((b, i) => (
          <div key={i} className={styles.brandItem}>
            <span className={styles.bNum}>{ROMAN[i]}</span>
            <span className={styles.brandName}>{b.name}</span>
            <span className={`${styles.delta} ${styles[b.trend]}`}>
              {b.trend === 'up' ? '↑' : b.trend === 'down' ? '↓' : '—'} {Math.abs(b.delta_pct)}%
            </span>
          </div>
        ))}
      </div>

      <div className={styles.section}>
        <div className={styles.sectionLabel}>Top Searches</div>
        {searchTerms.slice(0, 6).map((t, i) => (
          <div key={i} className={styles.searchItem}>
            <span className={styles.sNum}>{ROMAN[i]}</span>
            <span className={styles.sTerm}>{t.term}</span>
            <div className={styles.sBarWrap}>
              <div
                className={styles.sBar}
                style={{ width: `${((t.velocity || 0) / maxSearch) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      <div className={styles.section}>
        <div className={styles.sectionLabel}>Activity Heatmap · 4w</div>
        <Heatmap />
      </div>

    </aside>
  )
}
