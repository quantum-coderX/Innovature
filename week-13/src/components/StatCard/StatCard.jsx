import styles from './StatCard.module.css'

/**
 * StatCard — Reusable metric tile
 * Props:
 *   icon    {string}  — emoji or character for the icon
 *   label   {string}  — metric label
 *   value   {string}  — metric value (e.g. "$48,295")
 *   trend   {string}  — trend string (e.g. "+12.5%")
 *   trendUp {boolean} — true = positive (green), false = negative (red)
 *   color   {string}  — accent hex color for icon background & glow (inline style)
 */
function StatCard({ icon, label, value, trend, trendUp, color }) {
  return (
    <article
      className={styles.card}
      // Inline style: dynamic accent color via CSS custom property
      style={{ '--accent-color': color }}
      aria-label={`${label}: ${value}, trend ${trend}`}
    >
      <div className={styles.top}>
        {/* Icon — background tinted with inline style */}
        <div
          className={styles.iconWrapper}
          style={{ background: `${color}18`, border: `1px solid ${color}30` }}
          aria-hidden="true"
        >
          {icon}
        </div>

        {/* Trend badge */}
        <span className={`${styles.trend} ${trendUp ? styles.trendUp : styles.trendDown}`}>
          <span aria-hidden="true">{trendUp ? '↑' : '↓'}</span>
          {trend}
        </span>
      </div>

      <div className={styles.bottom}>
        {/* Value — inline style color tint for visual pop */}
        <div className={styles.value} style={{ color: '#f1f5f9' }}>
          {value}
        </div>
        <div className={styles.label}>{label}</div>
      </div>
    </article>
  )
}

export default StatCard
