import { useState } from 'react'
import styles from './Header.module.css'

/**
 * Header — Top bar with page title, search, notifications, and user menu
 * Props:
 *   user {object} — { name, role, avatar }
 *   title {string} — current page title
 */
function Header({ user, title }) {
  const [searchValue, setSearchValue] = useState('')

  // Get time-based greeting
  const getGreeting = () => {
    const hour = new Date().getHours()
    if (hour < 12) return 'Good morning'
    if (hour < 18) return 'Good afternoon'
    return 'Good evening'
  }

  return (
    <header className={styles.header} role="banner">
      {/* Left: greeting + page title */}
      <div className={styles.left}>
        <span className={styles.greeting}>
          {getGreeting()}, {user.name.split(' ')[0]} 👋
        </span>
        <h1 className={styles.pageTitle}>{title}</h1>
      </div>

      {/* Right: search + actions + user */}
      <div className={styles.right}>
        {/* Search */}
        <div className={styles.searchWrapper}>
          <span className={styles.searchIcon} aria-hidden="true">🔍</span>
          <input
            id="header-search"
            type="search"
            className={styles.searchInput}
            placeholder="Search..."
            value={searchValue}
            onChange={(e) => setSearchValue(e.target.value)}
            aria-label="Search dashboard"
          />
        </div>

        {/* Notifications */}
        <button id="notifications-btn" className={styles.iconBtn} aria-label="Notifications (4 unread)">
          🔔
          <span className={styles.badge} aria-hidden="true">4</span>
        </button>

        {/* Messages */}
        <button id="messages-btn" className={styles.iconBtn} aria-label="Messages">
          💬
        </button>

        <div className={styles.divider} aria-hidden="true" />

        {/* User avatar */}
        <button id="user-menu-btn" className={styles.userBtn} aria-label={`User menu: ${user.name}`}>
          <div className={styles.userAvatarSmall} aria-hidden="true">{user.avatar}</div>
          <span className={styles.userNameSmall}>{user.name}</span>
          <span className={styles.chevron} aria-hidden="true">▼</span>
        </button>
      </div>
    </header>
  )
}

export default Header
