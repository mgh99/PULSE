import { useLang } from '../i18n/LangContext.jsx'
import styles from './BriefView.module.css'
import viewStyles from './TabViews.module.css'

export default function BriefView({ data }) {
  const { t } = useLang()

  if (!data) return null

  return (
    <div className={viewStyles.view}>
      <div className={viewStyles.viewHeader}>
        <div className={viewStyles.viewEyebrow}>{t?.briefSubtitle || 'AI-generated fashion intelligence'}</div>
        <h2 className={viewStyles.viewTitle}>{t?.briefTitle || 'Editorial Brief'}</h2>
      </div>

      <div className={styles.briefBody}>
        <div className={styles.briefHero}>
          <div className={styles.briefHeroTitle}>{data.hero?.title}</div>
          <div className={styles.briefHeroSub}>{data.hero?.subtitle}</div>
        </div>

        <div className={styles.briefText}>{data.editorial_brief}</div>

        <div className={styles.briefDivider}>
          <div className={styles.briefDividerLine} />
          <div className={styles.briefDividerDiamond} />
          <div className={styles.briefDividerLine} />
        </div>

        <div className={styles.briefSignals}>
          {(data.signals || []).map((s, i) => (
            <div key={i} className={styles.briefSignalItem}>
              <div className={styles.briefSignalNum}>{['I','II','III','IV','V','VI'][i]}</div>
              <div className={styles.briefSignalContent}>
                <div className={styles.briefSignalSource}>{s.source}</div>
                <div className={styles.briefSignalTitle}>{s.title}</div>
                <div className={styles.briefSignalExcerpt}>{s.excerpt}</div>
              </div>
              <div className={`${styles.briefSignalStatus} ${styles[s.status]}`}>
                {s.status}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}