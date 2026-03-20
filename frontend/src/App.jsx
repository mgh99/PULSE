import { useEffect, useState } from 'react'
import styles from './App.module.css'
import ArchiveView from './components/ArchiveView.jsx'
import BriefView from './components/BriefView.jsx'
import ChartRow from './components/ChartRow.jsx'
import Header from './components/Header.jsx'
import Hero from './components/Hero.jsx'
import KPIRow from './components/KPIRow.jsx'
import RunwayView from './components/RunwayView.jsx'
import SidebarLeft from './components/SidebarLeft.jsx'
import SidebarRight from './components/SidebarRight.jsx'
import SignalGrid from './components/SignalGrid.jsx'
import StreetView from './components/StreetView.jsx'
import Ticker from './components/Ticker.jsx'
import { useDashboard } from './hooks/useDashboard.js'
import { useLang } from './i18n/LangContext.jsx'

function Ornament() {
  return (
    <div className={styles.ornament}>
      <div className={styles.ornLine} />
      <div className={styles.ornCenter}>
        <div className={styles.diamond} />
        Global Fashion Intelligence
        <div className={styles.diamond} />
      </div>
      <div className={styles.ornLine} />
    </div>
  )
}

function LoadingScreen() {
  return (
    <div className={styles.loading}>
      <div className={styles.loadingWordmark}>Pulse</div>
      <div className={styles.loadingText}>Collecting signals from global sources...</div>
    </div>
  )
}

function ErrorScreen({ message }) {
  return (
    <div className={styles.loading}>
      <div className={styles.loadingWordmark}>Pulse</div>
      <div className={styles.loadingText}>Could not connect to backend — {message}</div>
      <div className={styles.loadingHint}>Make sure the FastAPI server is running on port 8000</div>
    </div>
  )
}

export default function App() {
  const { lang, toggle, t } = useLang()
  const { data, loading, error, lastUpdate, triggerRefresh } = useDashboard(lang)
  const [activeCategory, setActiveCategory] = useState('All')
  const [activeTab, setActiveTab] = useState(0)

  useEffect(() => {
    setActiveCategory(lang === 'en' ? 'All' : 'Todo')
  }, [lang])

  if (loading) return <LoadingScreen />
  if (error)   return <ErrorScreen message={error} />

  // Filtrar signals por categoría activa
  const CATEGORY_MAP = {
    'Silhouette':  ['silhouette', 'shape', 'form'],
    'Colour':      ['colour', 'color', 'hue', 'tone', 'yellow', 'green', 'blue', 'red', 'pink', 'beige', 'butter'],
    'Fabric':      ['fabric', 'textile', 'linen', 'silk', 'cotton', 'knit', 'knitwear'],
    'Footwear':    ['footwear', 'shoe', 'shoes', 'boot', 'heel', 'flat', 'sneaker'],
    'Accessories': ['accessories', 'accessory', 'bag', 'belt', 'scarf', 'hat', 'jewelry'],
    'Streetwear':  ['streetwear', 'street', 'urban', 'casual', 'workwear', 'cargo'],
    'Couture':     ['couture', 'luxury', 'haute', 'designer', 'runway', 'editorial'],
  }

  const CATEGORY_MAP_ES = {
    'Silueta':    ['silhouette', 'shape', 'silueta'],
    'Color':      ['colour', 'color', 'hue', 'yellow', 'green', 'blue', 'red', 'pink', 'beige'],
    'Tejido':     ['fabric', 'textile', 'linen', 'silk', 'cotton', 'knit', 'tejido'],
    'Calzado':    ['footwear', 'shoe', 'boot', 'heel', 'flat', 'sneaker', 'calzado'],
    'Accesorios': ['accessories', 'accessory', 'bag', 'belt', 'scarf', 'hat', 'accesorios'],
    'Streetwear': ['streetwear', 'street', 'urban', 'casual', 'workwear'],
    'Costura':    ['couture', 'luxury', 'haute', 'designer', 'runway'],
  }

  const isAll = activeCategory === 'All' || activeCategory === 'Todo' || activeCategory === ''

  const filteredSignals = isAll
    ? (data?.signals || [])
    : (data?.signals || []).filter(s => {
        const keywords = CATEGORY_MAP[activeCategory] || CATEGORY_MAP_ES[activeCategory] || [activeCategory.toLowerCase()]
        return s.tags?.some(tag =>
          keywords.some(kw => tag.toLowerCase().includes(kw))
        ) || keywords.some(kw =>
          s.title?.toLowerCase().includes(kw) ||
          s.excerpt?.toLowerCase().includes(kw)
        )
      })

  return (
    <div className={styles.app}>
      <Header
        lastUpdate={lastUpdate}
        onRefresh={triggerRefresh}
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />

      <Ticker
        signals={data?.signals || []}
        searchTerms={data?.search_terms || []}
      />

      <Ornament />

      <div className={styles.layout}>
        <SidebarLeft
          categoryMix={data?.category_mix}
          editorialBrief={data?.editorial_brief}
          generatedAt={data?.generated_at}
          onCategoryChange={setActiveCategory}
          activeCategory={activeCategory}
          lang={lang}
          regionalScores={data?.regional_scores}
        />

        <main className={styles.center}>
          {activeTab === 0 && (
            <>
              <Hero hero={data?.hero} />
              <KPIRow kpis={data?.kpis} />
              <ChartRow categoryMix={data?.category_mix} />
              <SignalGrid signals={filteredSignals} activeCategory={activeCategory} />
            </>
          )}
          {activeTab === 1 && <RunwayView signals={data?.signals || []} />}
          {activeTab === 2 && <StreetView signals={data?.signals || []} />}
          {activeTab === 3 && <ArchiveView lang={lang} />}
          {activeTab === 4 && <BriefView data={data} />}
        </main>

        <SidebarRight
          brands={data?.brands || []}
          searchTerms={data?.search_terms || []}
        />
      </div>

      <footer className={styles.footer}>
        <span className={styles.footerLeft}>
          Pulse · Global Fashion Intelligence · Refreshed every 15 min
        </span>
        <div className={styles.footerSources}>
          {['Vogue Runway', 'Business of Fashion', 'Google Trends', 'Reddit'].map(s => (
            <span key={s} className={styles.footerSrc}>{s}</span>
          ))}
        </div>
      </footer>
    </div>
  )
}
