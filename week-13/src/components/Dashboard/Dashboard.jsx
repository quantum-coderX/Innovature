import styles from './Dashboard.module.css'
import StatsGrid from '../StatsGrid/StatsGrid'
import RecentItems from '../RecentItems/RecentItems'
import Announcements from '../Announcements/Announcements'
import { statsData, recentItems, announcements } from '../../data/mockData'

/**
 * Dashboard — Main page compositing all sections
 * Props: none (pulls data from mockData directly)
 */
function Dashboard() {
  const heroStats = statsData.slice(0, 3)

  return (
    <main id="dashboard-main" className={styles.dashboard}>
      <section className={styles.hero} aria-labelledby="dashboard-hero-title">
        <div className={styles.heroCopy}>
          <span className={styles.heroEyebrow}>Welcome back, Arjun</span>
          <h2 id="dashboard-hero-title" className={styles.heroTitle}>
            Dashboard overview
          </h2>
          <p className={styles.heroText}>
            A polished dashboard shell with strong hierarchy, summary cards, and content blocks you can extend into orders, users, analytics, or inventory pages.
          </p>

          <div className={styles.heroActions}>
            <button className={styles.primaryAction}>Create report</button>
            <button className={styles.secondaryAction}>View analytics</button>
          </div>
        </div>

        <div className={styles.heroPanel} aria-label="Quick metrics">
          {heroStats.map((stat) => (
            <article key={stat.id} className={styles.heroMetric}>
              <span className={styles.heroMetricLabel}>{stat.label}</span>
              <strong className={styles.heroMetricValue}>{stat.value}</strong>
              <span className={stat.trendUp ? styles.heroTrendUp : styles.heroTrendDown}>{stat.trend}</span>
            </article>
          ))}
        </div>
      </section>

      {/* Stats Overview */}
      <StatsGrid stats={statsData} />

      {/* Two-column: Recent Activity + Announcements */}
      <div className={styles.mainGrid}>
        <RecentItems items={recentItems} title="Recent Transactions" />
        <Announcements announcements={announcements} />
      </div>
    </main>
  )
}

export default Dashboard
