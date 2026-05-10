import { Link } from "react-router-dom";
import styles from "./PostCard.module.css";

export default function PostCard({ post }) {
  return (
    <article className={styles.card}>
      <div className={styles.cover} style={{ background: post.coverGradient }}>
        <span className={styles.category}>{post.category}</span>
      </div>

      <div className={styles.body}>
        <div className={styles.meta}>
          <div className={styles.avatar}>{post.authorAvatar}</div>
          <div className={styles.metaInfo}>
            <span className={styles.author}>{post.author}</span>
            <span className={styles.dot}>·</span>
            <span className={styles.date}>
              {new Date(post.date).toLocaleDateString("en-US", {
                month: "short",
                day: "numeric",
                year: "numeric",
              })}
            </span>
          </div>
        </div>

        <h2 className={styles.title}>{post.title}</h2>
        <p className={styles.excerpt}>{post.excerpt}</p>

        <div className={styles.footer}>
          <div className={styles.tags}>
            {post.tags.slice(0, 2).map((tag) => (
              <span key={tag} className={styles.tag}>
                {tag}
              </span>
            ))}
          </div>
          <Link
            to={`/blog/post/${post.id}`}
            className={styles.readMore}
            id={`read-post-${post.id}`}
          >
            Read →
          </Link>
        </div>

        <div className={styles.readTime}>⏱ {post.readTime}</div>
      </div>
    </article>
  );
}
