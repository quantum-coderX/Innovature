import { Outlet } from "react-router-dom";
import styles from "./BlogLayout.module.css";

export default function BlogLayout() {
  return (
    <div className={styles.layout}>
      <div className={styles.header}>
        <h1 className={styles.title}>The Blog</h1>
        <p className={styles.subtitle}>
          100 live posts fetched from JSONPlaceholder — scroll to load more.
        </p>
        <div className={styles.apiChip}>
          <span className={styles.live} />
          <span>Live API · jsonplaceholder.typicode.com</span>
        </div>
      </div>
      <Outlet />
    </div>
  );
}
