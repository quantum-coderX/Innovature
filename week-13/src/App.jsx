import { useState } from 'react'
import styles from './App.module.css'
import Sidebar from './components/Sidebar/Sidebar'
import Header from './components/Header/Header'
import Dashboard from './components/Dashboard/Dashboard'
import { currentUser, navItems } from './data/mockData'

/**
 * App — Root component, layout shell
 * Manages:
 *   - activeNav: which sidebar item is currently active
 */
function App() {
  const [activeNav, setActiveNav] = useState('dashboard')

  // Get the page title from the active nav item
  const activeNavItem = navItems.find((item) => item.id === activeNav)
  const pageTitle = activeNavItem ? activeNavItem.label : 'Dashboard'

  return (
    <div className={styles.appShell}>
      {/* Background decorative gradients */}
      <div className={styles.bgDecoration} aria-hidden="true" />
      <div className={styles.bgDecoration2} aria-hidden="true" />

      {/* Sidebar */}
      <Sidebar
        activeItem={activeNav}
        onNavClick={setActiveNav}
        user={currentUser}
      />

      {/* Main area: header + content */}
      <div className={styles.mainArea}>
        <Header
          user={currentUser}
          title={pageTitle}
        />

        <div className={styles.content}>
          {/* Only render Dashboard for now; other nav items show placeholder */}
          {activeNav === 'dashboard' ? (
            <Dashboard />
          ) : (
            <PlaceholderPage title={pageTitle} />
          )}
        </div>
      </div>
    </div>
  )
}

/**
 * PlaceholderPage — Simple placeholder for non-dashboard routes
 * Props:
 *   title {string} — page title
 */
function PlaceholderPage({ title }) {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        flex: 1,
        gap: '16px',
        color: 'var(--text-muted)',
        minHeight: '60vh',
      }}
    >
      <div style={{ fontSize: '3rem' }}>🚧</div>
      <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-secondary)' }}>
        {title} — Coming Soon
      </h2>
      <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', maxWidth: '300px', textAlign: 'center' }}>
        This section is under construction. Navigate back to the Dashboard to explore the UI.
      </p>
    </div>
  )
}

export default App
