import { useState } from 'react'
import { useLang } from '../i18n/LangContext.jsx'
import ColourIntelligence from './lab/ColourIntelligence.jsx'
import styles from './LabView.module.css'

export default function LabView({ lang }) {
  const { t } = useLang()
  const [activeTab, setActiveTab] = useState('colour')

  const tabs = [
    { id: 'colour', dot: '#8B7355', label: 'Colour Intelligence', badge: 'NEW' },
    { id: 'outfit', dot: '#6a5f52', label: 'Outfit Generator', badge: 'Soon' },
    { id: 'brand',  dot: '#c9a05a', label: 'Brand DNA',        badge: 'Soon' },
    { id: 'crossover', dot: '#7B9E8C', label: 'Cultural Crossover', badge: 'Soon' },
  ]

  return (
    <div className={styles.lab}>

      <div className={styles.header}>
        <div className={styles.eyebrow}>Experimental · AI-Powered</div>
        <h1 className={styles.title}>Lab — <em>Fashion Intelligence Experiments</em></h1>
        <p className={styles.sub}>AI-powered tools for trend forecasting, styling and cultural analysis</p>
      </div>

      <div className={styles.subTabs}>
        {tabs.map(tab => (
          <div
            key={tab.id}
            className={`${styles.subTab} ${activeTab === tab.id ? styles.active : ''} ${tab.badge ? styles.disabled : ''}`}
            onClick={() => !tab.badge && setActiveTab(tab.id)}
          >
            <div className={styles.subTabDot} style={{ background: tab.dot }} />
            {tab.label}
            {tab.badge && <span className={styles.subTabBadge}>{tab.badge}</span>}
          </div>
        ))}
      </div>

      <div className={styles.content}>
        {activeTab === 'colour' && <ColourIntelligence lang={lang} />}
      </div>

    </div>
  )
}