import { useEffect, useState } from 'react'
import { useLang } from '../i18n/LangContext.jsx'
import styles from './ArchiveView.module.css'
import viewStyles from './TabViews.module.css'

export default function ArchiveView({ lang = 'en' }) {
  const { t } = useLang()
  const [snapshots, setSnapshots] = useState([])
  const [loading, setLoading]     = useState(true)
  const [selected, setSelected]   = useState(null)

  useEffect(() => {
    fetch(`/api/archive?lang=${lang}&limit=10`)
      .then(r => r.json())
      .then(data => { setSnapshots(data); setLoading(false) })
      .catch(() => setLoading(false))
  }, [lang])

  if (loading) return <div className={viewStyles.empty}>{t?.archiveLoading || 'Loading...'}</div>
  if (snapshots.length === 0) return <div className={viewStyles.empty}>{t?.archiveEmpty || 'No archive yet'}</div>

  return (
    <div className={viewStyles.view}>
      <div className={viewStyles.viewHeader}>
        <div className={viewStyles.viewEyebrow}>{t?.archiveTitle || 'Archive'}</div>
        <h2 className={viewStyles.viewTitle}>Signal History</h2>
        <p className={viewStyles.viewSub}>{snapshots.length} snapshots saved</p>
      </div>

      <div className={styles.archiveGrid}>
        {snapshots.map((snap, i) => (
          <div
            key={i}
            className={`${styles.archiveCard} ${selected === i ? styles.active : ''}`}
            onClick={() => setSelected(selected === i ? null : i)}
          >
            <div className={styles.archiveDate}>
              {new Date(snap.generated_at).toLocaleDateString('en-GB', {
                weekday: 'short', day: 'numeric', month: 'short',
                hour: '2-digit', minute: '2-digit'
              })}
            </div>
            <div className={styles.archiveHero}>{snap.hero?.title}</div>
            <div className={styles.archiveMeta}>{snap.signal_count} signals</div>

            {selected === i && (
              <div className={styles.archiveExpanded}>
                <div className={styles.archiveBrief}>{snap.editorial_brief}</div>
                <div className={styles.archiveSignals}>
                  {(snap.signals || []).slice(0, 3).map((s, j) => (
                    <div key={j} className={styles.archiveSignalItem}>
                      <span className={styles.archiveSignalSource}>{s.source}</span>
                      <span className={styles.archiveSignalTitle}>{s.title}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}