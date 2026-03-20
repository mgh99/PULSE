import { useLang } from '../i18n/LangContext.jsx'
import styles from './SignalGrid.module.css'
import viewStyles from './TabViews.module.css'

const RUNWAY_SOURCES = ['Vogue', 'WWD', "Harper's Bazaar", 'Business of Fashion', 'BoF']

const STATUS_LABEL_EN = { rising: '↑ Rising', watching: '◎ Watching', fading: '↓ Fading' }

export default function RunwayView({ signals = [] }) {
  const { t } = useLang()

  const runwaySignals = signals.filter(s =>
    RUNWAY_SOURCES.some(src => s.source?.includes(src))
  )

  return (
    <div className={viewStyles.view}>
      <div className={viewStyles.viewHeader}>
        <div className={viewStyles.viewEyebrow}>Runway & Editorial</div>
        <h2 className={viewStyles.viewTitle}>
          {t?.tabRunway || 'Runway'} — {new Date().toLocaleDateString('en-GB', { month: 'long', year: 'numeric' })}
        </h2>
        <p className={viewStyles.viewSub}>
          {runwaySignals.length} signals from runway and editorial sources
        </p>
      </div>

      {runwaySignals.length === 0 ? (
        <div className={viewStyles.empty}>{t?.noSignals || 'No signals found for this source'}</div>
      ) : (
        <div className={styles.grid}>
          {runwaySignals.map((s, i) => (
            <div key={i} className={styles.card}>
              <div className={styles.top}>
                <span className={styles.source}>{s.source}</span>
                <span className={`${styles.status} ${styles[s.status]}`}>
                  {STATUS_LABEL_EN[s.status] || s.status}
                </span>
              </div>
              <div className={styles.title}>{s.title}</div>
              <div className={styles.excerpt}>{s.excerpt}</div>
              <div className={styles.tags}>
                {(s.tags || []).map((tag, j) => (
                  <span key={j} className={styles.tag}>{tag}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}