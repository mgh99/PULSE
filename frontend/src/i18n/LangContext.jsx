import { createContext, useContext, useState } from 'react'
import { t } from './translations.js'

const LangContext = createContext()

export function LangProvider({ children }) {
  const [lang, setLang] = useState('en')
  const toggle = () => setLang(l => l === 'en' ? 'es' : 'en')
  return (
    <LangContext.Provider value={{ lang, toggle, t: t[lang] }}>
      {children}
    </LangContext.Provider>
  )
}

export function useLang() {
  return useContext(LangContext)
}