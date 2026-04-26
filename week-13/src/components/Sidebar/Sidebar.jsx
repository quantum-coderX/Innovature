import styles from './Sidebar.module.css'
import { navItems } from '../../data/mockData'

/**
 * Sidebar — Fixed left navigation panel
 * Props:
 *   activeItem {string} — currently active nav item id
 *   onNavClick {function} — callback when nav item is clicked
 *   user {object} — { name, role, avatar }
 */
function Sidebar({ activeItem, onNavClick, user }) {
  return (
    <aside className={styles.sidebar} aria-label="Main navigation">
      {/* Logo */}
      <div className={styles.logo}>
        <div className={styles.logoMark}>
          <div className={styles.logoIcon}>⚡</div>
          <div>
            <div className={styles.logoText}>AdminPulse</div>
            <div className={styles.logoSubtext}>Dashboard</div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className={styles.nav} aria-label="Sidebar navigation">
        {navItems.map((item) => (
          <button
            key={item.id}
            id={`nav-${item.id}`}
            className={`${styles.navItem} ${activeItem === item.id ? styles.active : ''}`}
            onClick={() => onNavClick(item.id)}
            aria-current={activeItem === item.id ? 'page' : undefined}
          >
            <span className={styles.navIcon} aria-hidden="true">{item.icon}</span>
            <span className={styles.navLabel}>{item.label}</span>
          </button>
        ))}
      </nav>

      {/* User Footer */}
      <div className={styles.sidebarFooter}>
        <div className={styles.userCard}>
          <div className={styles.userAvatar} aria-hidden="true">{user.avatar}</div>
          <div>
            <div className={styles.userName}>{user.name}</div>
            <div className={styles.userRole}>{user.role}</div>
          </div>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
