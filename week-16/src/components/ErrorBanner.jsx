import styles from "./ErrorBanner.module.css";

export default function ErrorBanner({ message, onRetry }) {
  return (
    <div className={styles.banner} role="alert">
      <div className={styles.icon}>⚠️</div>
      <div className={styles.text}>
        <p className={styles.title}>Something went wrong</p>
        <p className={styles.message}>{message}</p>
      </div>
      {onRetry && (
        <button id="retry-btn" className={styles.retry} onClick={onRetry}>
          Try again
        </button>
      )}
    </div>
  );
}
