import { useEffect, useState } from 'react'
import styles from './ColourIntelligence.module.css'

function FeatureDesc() {
  return (
    <div className={styles.featureDesc}>
      <div className={styles.featureIcon}>◈</div>
      <div>
        <div className={styles.featureTitle}>AI Colour Forecasting</div>
        <div className={styles.featureSub}>Mistral analyses live signals from runways, street and search to predict the dominant colours of the coming season. Palettes regenerated every refresh cycle.</div>
        <span className={styles.featureTag}>
          <span className={styles.liveDot} />
          Generated from live signals · Updated every 15 min
        </span>
      </div>
    </div>
  )
}

function ColourCard({ colour, isHero = false }) {
  return (
    <div className={`${styles.card} ${isHero ? styles.hero : ''}`}>
      <div className={styles.swatch} style={{ background: colour.hex }}>
        <div className={styles.confPill}>{colour.confidence}%</div>
      </div>
      <div className={styles.cardInfo}>
        <div className={styles.colourName}>{colour.name}</div>
        <div className={styles.colourStatus}>{colour.status} · SS26</div>
        <div className={styles.colourDesc}>{colour.description}</div>
        <div className={styles.palette}>
          {(colour.combinations || []).map((hex, i) => (
            <div key={i} className={styles.pdot} style={{ background: hex }} title={hex} />
          ))}
        </div>
        <div className={styles.sources}>
          {(colour.sources || []).map((src, i) => (
            <span key={i} className={styles.sourceTag}>{src}</span>
          ))}
        </div>
      </div>
    </div>
  )
}

function HeroPanel({ hero, colours }) {
  if (!hero) return null

  return (
    <div className={styles.panel}>
      <div className={styles.sectionLabel}>Colour of the Season</div>
      <div className={styles.heroSwatch} style={{ background: `linear-gradient(135deg, ${hero.hex}, ${hero.hex}dd)` }}>
        <div className={styles.heroLabel}>
          <div className={styles.heroName}>{hero.name}</div>
          <div className={styles.heroHex}>{hero.hex}</div>
          <div className={styles.heroSub}>{hero.subtitle}</div>
        </div>
      </div>

      {hero.signal_strength && Object.entries(hero.signal_strength).map(([key, val]) => (
        <div key={key} className={styles.strengthRow}>
          <span className={styles.sLabel}>{key.charAt(0).toUpperCase() + key.slice(1)}</span>
          <div className={styles.sBarWrap}><div className={styles.sBar} style={{ width: `${val}%` }} /></div>
          <span className={styles.sVal}>{val}</span>
        </div>
      ))}

      <div style={{ marginTop: '14px' }}>
        <div className={styles.sectionLabel}>Season Palette Overview</div>
        <div className={styles.miniSwatches}>
          {(colours || []).map((c, i) => (
            <div key={i}>
              <div className={styles.miniSw} style={{ background: c.hex }} title={c.name} />
              <div className={styles.miniSwName}>{c.name.split(' ')[0]}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function ForecastPanel({ forecast, analysis }) {
  return (
    <div className={styles.panel} style={{ borderTop: '0.5px solid var(--border)' }}>
      <div className={styles.sectionLabel}>Colour Forecast · FW26</div>
      {(forecast || []).map((c, i) => (
        <div key={i} className={styles.forecastItem}>
          <div className={styles.fdot} style={{ background: c.hex }} />
          <span className={styles.fname}>{c.name}</span>
          <span className={styles.fpct}>↑ {c.confidence}%</span>
        </div>
      ))}
      {analysis && (
        <div className={styles.aiPanel}>
          <div className={styles.aiPanelLabel}>AI Colour Analysis · Mistral</div>
          <div className={styles.aiPanelText}>{analysis}</div>
        </div>
      )}
    </div>
  )
}

function ConsensusSidebar({ consensus, loading, expandedItem, setExpandedItem }) {
  const ROMAN = ['i','ii','iii','iv','v','vi','vii','viii']
  const BADGE_LABEL = { dominant: 'Dominant', strong: 'Strong', emerging: 'Emerging' }

  if (loading) return (
    <div className={styles.sidebarLeft}>
      <div className={styles.sidebarLoading}>Calculating consensus...</div>
    </div>
  )

  return (
    <div className={styles.sidebarLeft}>
      <div className={styles.sbSection}>
        <div className={styles.sectionLabel}>Season</div>
        <div className={styles.seasonTabs}>
          <div className={`${styles.seasonTab} ${styles.active}`}>
            SS26 — Current
            <span className={styles.seasonCount}>{consensus[0]?.total_cycles || 0} cycles</span>
          </div>
          <div className={styles.seasonTab}>
            FW26 — Forecast
            <span className={styles.seasonCount}>preview</span>
          </div>
        </div>
      </div>

      <div className={`${styles.sbSection} ${styles.sbSectionFlex}`}>
        <div className={styles.sectionLabel}>Dominant Colours · SS26</div>
        {consensus.length === 0 ? (
          <div className={styles.sidebarLoading}>Not enough data yet — check back after a few cycles.</div>
        ) : (
          <div className={styles.consensusList}>
            {consensus.map((c, i) => (
              <div
                key={i}
                className={styles.consensusItem}
                onClick={() => setExpandedItem(expandedItem === i ? null : i)}
              >
                <div className={styles.consensusTop}>
                  <span className={styles.consensusRank}>{ROMAN[i]}</span>
                  <div className={styles.consensusSwatch} style={{ background: c.hex }} />
                  <span className={styles.consensusName}>{c.name}</span>
                  <span className={`${styles.consensusBadge} ${styles[c.badge]}`}>
                    {BADGE_LABEL[c.badge] || c.badge}
                  </span>
                </div>

                <div className={styles.consensusStats}>
                  <div className={styles.consensusBarWrap}>
                    <div className={styles.consensusBar} style={{ width: `${c.freq_pct}%` }} />
                  </div>
                  <span className={styles.consensusStatText}>
                    {c.appearances} / {Math.round(c.total_cycles / 6)} cycles · avg {c.avg_confidence}%
                  </span>
                </div>

                <div className={styles.stabilityWrap}>
                  {Array.from({ length: 10 }).map((_, j) => (
                    <div
                      key={j}
                      className={`${styles.stabilityDot} ${j < Math.round(c.freq_pct / 10) ? styles.filled : ''}`}
                    />
                  ))}
                  <span className={styles.stabilityLabel}>7d stability</span>
                </div>

                {expandedItem === i && (
                  <div className={styles.consensusDetail}>
                    <div className={styles.detailRow}>
                      <span className={styles.detailLabel}>Appearances</span>
                      <span className={styles.detailVal}>{c.appearances} cycles</span>
                    </div>
                    <div className={styles.detailRow}>
                      <span className={styles.detailLabel}>Avg confidence</span>
                      <span className={styles.detailVal}>{c.avg_confidence}%</span>
                    </div>
                    {c.aliases?.length > 0 && (
                      <div className={styles.consensusAliases}>
                        Also as: "{c.aliases.join('", "')}"
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default function ColourIntelligence({ lang }) {
  const [data, setData]                   = useState(null)
  const [loading, setLoading]             = useState(true)
  const [error, setError]                 = useState(null)
  const [consensus, setConsensus]         = useState([])
  const [consensusLoading, setConsensusLoading] = useState(true)
  const [expandedItem, setExpandedItem]   = useState(null)

  useEffect(() => {
    setLoading(true)
    fetch(`/api/colours?lang=${lang}`)
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json() })
      .then(d => { setData(d); setLoading(false) })
      .catch(e => { setError(e.message); setLoading(false) })
  }, [lang])

  useEffect(() => {
    fetch(`/api/colours/consensus?lang=${lang}&days=7`)
      .then(r => r.json())
      .then(d => { setConsensus(d); setConsensusLoading(false) })
      .catch(() => setConsensusLoading(false))
  }, [lang])

  if (loading) return (
    <div className={styles.loadingWrap}>
      <div className={styles.loadingText}>Analysing colour signals...</div>
    </div>
  )

  if (error) return (
    <div className={styles.loadingWrap}>
      <div className={styles.loadingText}>Could not load colour forecast — {error}</div>
    </div>
  )

  return (
    <div className={styles.layoutFull}>
      <ConsensusSidebar
        consensus={consensus}
        loading={consensusLoading}
        expandedItem={expandedItem}
        setExpandedItem={setExpandedItem}
      />

      <div className={styles.layout}>
        <div className={styles.main}>
          <FeatureDesc />
          <div className={styles.gridWrap}>
            <div className={styles.sectionLabel}>Current Cycle · Predicted Colours</div>
            <div className={styles.grid}>
              {(data?.colours || []).map((c, i) => (
                <ColourCard key={i} colour={c} isHero={c.status === 'hero'} />
              ))}
            </div>
          </div>
        </div>

        <div className={styles.sidebar}>
          <HeroPanel hero={data?.hero_colour} colours={data?.colours} />
          <ForecastPanel forecast={data?.forecast_next} analysis={data?.editorial_analysis} />
        </div>
      </div>
    </div>
  )
}