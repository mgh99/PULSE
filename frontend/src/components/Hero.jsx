import { useLang } from '../i18n/LangContext.jsx'
import styles from './Hero.module.css'

export default function Hero({ hero = {} }) {
  const { t } = useLang()
  const words = hero.title?.split(' ') || []
  const half  = Math.ceil(words.length / 2)

  return (
    <div className={styles.hero}>
      <div className={styles.eyebrow}>{t.signalOfHour}</div>
      <h1 className={styles.title}>
        {words.slice(0, half).join(' ')} <em>{words.slice(half).join(' ')}</em>
      </h1>
      <div className={styles.meta}>
        {(hero.sources || []).map((src, i) => (
          <span key={i} className={styles.src}>{src}</span>
        ))}
        <span className={styles.velocity}>↑ {hero.velocity} {t.velocity}</span>
      </div>
    </div>
  )
}