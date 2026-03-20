import { useLang } from '../i18n/LangContext.jsx'
import styles from './SignalGrid.module.css'
import viewStyles from './TabViews.module.css'

const STREET_SOURCES = ['Reddit', 'Refinery29', 'Street']

export default function StreetView({ signals = [] }) {
  const { t } = useLang()

  const streetSignals = signals.filter(s =>
    STREET_SOURCES.some(src => s.source?.includes(src))
  )

  return (
    <div className={viewStyles.view}>
      <div className={viewStyles.viewHeader}>
        <div className={viewStyles.viewEyebrow}>Street & Community</div>
        <h2 className={viewStyles.viewTitle}>
          {t?.tabStreet || 'Street'} — What people are actually wearing
        </h2>
        <p className={viewStyles.viewSub}>
          {streetSignals.length} signals from community and street sources
        </p>
      </div>

      {streetSignals.length === 0 ? (
        <div className={viewStyles.empty}>{t?.noSignals || 'No signals found for this source'}</div>
      ) : (
        <div className={styles.grid}>
          {streetSignals.map((s, i) => (
            <div key={i} className={styles.card}>
              <div className={styles.top}>
                <span className={styles.source}>{s.source}</span>
                <span className={`${styles.status} ${styles[s.status]}`}>
                  {s.status}
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