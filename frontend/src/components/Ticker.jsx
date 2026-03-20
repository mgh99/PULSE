import styles from './Ticker.module.css'

export default function Ticker({ signals = [], searchTerms = [] }) {
  const items = [
    ...signals.map(s => ({
      tag: s.source?.split('·')[0]?.trim() || 'Signal',
      text: s.title,
      delta: s.status === 'rising' ? `↑ ${s.velocity}` : null,
      up: s.status === 'rising',
    })),
    ...searchTerms.map(t => ({
      tag: 'Search',
      text: `"${t.term}"`,
      delta: `↑ ${t.velocity}`,
      up: true,
    })),
  ]

  const doubled = [...items, ...items]

  return (
    <div className={styles.ticker}>
      <div className={styles.label}>Trending</div>
      <div className={styles.track}>
        <div className={styles.inner}>
          {doubled.map((item, i) => (
            <div key={i} className={styles.item}>
              <span className={styles.tag}>{item.tag}</span>
              <span>{item.text}</span>
              {item.delta && (
                <span className={item.up ? styles.up : styles.down}>
                  {item.delta}
                </span>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
