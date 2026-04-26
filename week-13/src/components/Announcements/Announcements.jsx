import styles from './Announcements.module.css'

/**
 * Announcements — Card-based feed of announcements
 * Props:
 *   announcements {Array} — array of announcement objects from mockData
 */
function Announcements({ announcements }) {
  /**
   * Get priority config — demonstrates inline style for dynamic coloring
   * based on the priority prop value
   */
  const getPriorityConfig = (priority) => {
    const configs = {
      high: {
        label: 'High',
        color: '#f43f5e',
        bg: 'rgba(244, 63, 94, 0.12)',
        border: '1px solid rgba(244, 63, 94, 0.25)',
      },
      medium: {
        label: 'Medium',
        color: '#f59e0b',
        bg: 'rgba(245, 158, 11, 0.12)',
        border: '1px solid rgba(245, 158, 11, 0.25)',
      },
      low: {
        label: 'Low',
        color: '#10b981',
        bg: 'rgba(16, 185, 129, 0.12)',
        border: '1px solid rgba(16, 185, 129, 0.25)',
      },
    }
    return configs[priority] || configs.low
  }

  return (
    <section className={styles.section} aria-labelledby="announcements-heading">
      <div className={styles.header}>
        <h2 id="announcements-heading" className={styles.title}>📢 Announcements</h2>
        <button id="announcements-view-all-btn" className={styles.viewAll} aria-label="View all announcements">
          View all →
        </button>
      </div>

      <div role="list" aria-label="Announcements feed">
        {announcements.map((ann) => {
          const config = getPriorityConfig(ann.priority)
          return (
            <article
              key={ann.id}
              className={styles.card}
              role="listitem"
              aria-label={`Announcement: ${ann.title}`}
              // Inline style: drives the ::before border color via CSS custom property
              style={{ '--priority-color': config.color }}
            >
              <div className={styles.cardHeader}>
                <h3 className={styles.cardTitle}>{ann.title}</h3>

                {/* Priority badge — background and color fully driven by inline style */}
                <span
                  className={styles.priorityBadge}
                  style={{
                    color: config.color,
                    background: config.bg,
                    border: config.border,
                  }}
                  aria-label={`Priority: ${config.label}`}
                >
                  {config.label}
                </span>
              </div>

              <div className={styles.meta}>📅 {ann.date}</div>
              <p className={styles.body}>{ann.body}</p>
            </article>
          )
        })}
      </div>
    </section>
  )
}

export default Announcements
