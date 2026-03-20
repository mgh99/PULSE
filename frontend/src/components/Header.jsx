import { useLang } from '../i18n/LangContext.jsx'
import styles from './Header.module.css'

const NAV_ITEMS = ['Radar', 'Runway', 'Street', 'Archive', 'Brief']

export default function Header({ lastUpdate, onRefresh, activeTab, onTabChange }) {
  const { lang, toggle, t } = useLang()

  // Cambia el useState de active por el prop:
  // elimina: const [active, setActive] = useState('Radar')

  const timeStr = lastUpdate
    ? lastUpdate.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })
    : '--:--'

  const dateStr = new Date().toLocaleDateString(lang === 'es' ? 'es-ES' : 'en-GB', {
    weekday: 'short', day: 'numeric', month: 'short', year: 'numeric'
  })

  return (
    <header className={styles.header}>
      <div className={styles.wordmark}>Pulse</div>

      <nav className={styles.nav}>
        {(t?.nav || ['Radar','Runway','Street','Archive','Brief']).map((item, i) => (
          <span
            key={item}
            className={`${styles.navItem} ${activeTab === i ? styles.active : ''}`}
            onClick={() => onTabChange(i)}
          >
            {item}
          </span>
        ))}
      </nav>

      <div className={styles.right}>
        <span className={styles.date}>{dateStr} · {timeStr} CET</span>
        <button className={styles.langToggle} onClick={toggle}>
          {lang === 'en' ? 'ES' : 'EN'}
        </button>
        <button className={styles.livePill} onClick={onRefresh}>
          <span className={styles.liveDot} />
          {t?.live || 'Live'}
        </button>
      </div>
    </header>
  )
}
