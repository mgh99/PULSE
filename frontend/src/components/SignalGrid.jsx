import { useLang } from '../i18n/LangContext.jsx'
import styles from './SignalGrid.module.css'

export default function SignalGrid({ signals = [], activeCategory = 'All' }) {
  const { t } = useLang()

  const STATUS_LABEL = {
    rising:   t?.rising   || '↑ Rising',
    watching: t?.watching || '◎ Watching',
    fading:   t?.fading2  || '↓ Fading',
  }

  return (
    <div className={styles.area}>
      <div className={styles.header}>
        <span className={styles.sectionLabel}>{t?.liveSignals || 'Live Signals'}</span>
        <span className={styles.count}>
          {signals.length} {t?.signals || 'signals'}
          {activeCategory !== 'All' && (
            <span style={{ color: 'var(--gold)', marginLeft: '6px' }}>
              · {activeCategory}
            </span>
          )}
        </span>
      </div>

      {signals.length === 0 ? (
        <div style={{
          padding: '32px 0',
          textAlign: 'center',
          fontFamily: 'var(--serif)',
          fontSize: '14px',
          fontStyle: 'italic',
          color: 'var(--ink4)'
        }}>
          No signals found for "{activeCategory}" — try another category
        </div>
      ) : (
        <div className={styles.grid}>
          {signals.map((s, i) => (
            <div key={i} className={styles.card}>
              <div className={styles.top}>
                <span className={styles.source}>{s.source}</span>
                <span className={`${styles.status} ${styles[s.status]}`}>
                  {STATUS_LABEL[s.status] || s.status}
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