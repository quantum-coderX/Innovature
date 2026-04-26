import styles from './RecentItems.module.css'

/**
 * RecentItems — Styled activity table
 * Props:
 *   items {Array}  — array of recent activity items from mockData
 *   title {string} — section title
 */
function RecentItems({ items, title }) {
  // Map statusType to CSS module class
  const getBadgeClass = (statusType) => {
    const map = {
      success: styles.badgeSuccess,
      warning: styles.badgeWarning,
      info: styles.badgeInfo,
      error: styles.badgeError,
    }
    return map[statusType] || styles.badgeInfo
  }

  return (
    <section className={styles.section} aria-labelledby="recent-items-heading">
      <div className={styles.header}>
        <h2 id="recent-items-heading" className={styles.title}>{title}</h2>
        <div className={styles.controls}>
          <button id="recent-filter-btn" className={styles.filterBtn} aria-label="Filter recent items">
            ⚡ Filter
          </button>
          <button id="recent-export-btn" className={styles.filterBtn} aria-label="Export recent items">
            ↓ Export
          </button>
        </div>
      </div>

      <div className={styles.tableWrapper}>
        <table className={styles.table} aria-label="Recent activity table">
          <thead>
            <tr>
              <th scope="col">User</th>
              <th scope="col">Action</th>
              <th scope="col">Amount</th>
              <th scope="col">Date</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                {/* User cell */}
                <td>
                  <div className={styles.userCell}>
                    <div className={styles.avatar} aria-hidden="true">{item.avatar}</div>
                    <span className={styles.userName}>{item.name}</span>
                  </div>
                </td>

                {/* Action */}
                <td className={styles.action}>{item.action}</td>

                {/* Amount */}
                <td className={styles.amount}>{item.amount}</td>

                {/* Date */}
                <td>{item.date}</td>

                {/* Status badge */}
                <td>
                  <span className={`${styles.badge} ${getBadgeClass(item.statusType)}`}>
                    {item.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className={styles.footer}>
        <button id="recent-load-more-btn" className={styles.loadMore}>
          Load more activity →
        </button>
      </div>
    </section>
  )
}

export default RecentItems
