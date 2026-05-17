import styles from "./SkeletonCard.module.css";

export default function SkeletonCard() {
  return (
    <div className={styles.card}>
      <div className={`${styles.cover} skeleton`} />
      <div className={styles.body}>
        <div className={styles.metaRow}>
          <div className={`${styles.avatar} skeleton`} />
          <div className={`${styles.metaLine} skeleton`} />
        </div>
        <div className={`${styles.title} skeleton`} />
        <div className={`${styles.titleShort} skeleton`} />
        <div className={`${styles.excerpt} skeleton`} />
        <div className={`${styles.excerptShort} skeleton`} />
        <div className={styles.footer}>
          <div className={`${styles.tag} skeleton`} />
          <div className={`${styles.btn} skeleton`} />
        </div>
      </div>
    </div>
  );
}
