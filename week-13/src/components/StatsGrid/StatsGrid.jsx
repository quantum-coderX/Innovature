import styles from './StatsGrid.module.css'
import StatCard from '../StatCard/StatCard'

/**
 * StatsGrid — Responsive grid of StatCard components
 * Props:
 *   stats {Array} — array of stat objects from mockData.statsData
 */
function StatsGrid({ stats }) {
  return (
    <section className={styles.section} aria-labelledby="stats-heading">
      <div className={styles.sectionHeader}>
        <h2 id="stats-heading" className={styles.sectionTitle}>Overview</h2>
        <button id="stats-view-all-btn" className={styles.viewAll} aria-label="View all statistics">
          View all →
        </button>
      </div>

      <div className={styles.grid} role="list" aria-label="Statistics overview">
        {stats.map((stat) => (
          <div key={stat.id} role="listitem">
            <StatCard
              icon={stat.icon}
              label={stat.label}
              value={stat.value}
              trend={stat.trend}
              trendUp={stat.trendUp}
              color={stat.color}
            />
          </div>
        ))}
      </div>
    </section>
  )
}

export default StatsGrid
