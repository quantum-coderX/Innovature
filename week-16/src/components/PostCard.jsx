import { Link } from "react-router-dom";
import styles from "./PostCard.module.css";

/* Deterministic gradient based on post id */
const GRADIENTS = [
  "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
  "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
  "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
  "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
  "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
  "linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)",
  "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)",
  "linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)",
  "linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%)",
  "linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)",
];

/* Deterministic user avatar colour */
const AVATAR_COLORS = [
  "#a78bfa", "#60a5fa", "#34d399", "#f472b6",
  "#fb923c", "#a3e635", "#38bdf8", "#e879f9",
];

function getGradient(id) {
  return GRADIENTS[(id - 1) % GRADIENTS.length];
}

function getAvatarColor(userId) {
  return AVATAR_COLORS[(userId - 1) % AVATAR_COLORS.length];
}

function initials(name = "") {
  return name
    .split(" ")
    .slice(0, 2)
    .map((w) => w[0])
    .join("")
    .toUpperCase();
}

export default function PostCard({ post }) {
  const gradient = getGradient(post.id);
  const avatarColor = getAvatarColor(post.userId);
  // JSONPlaceholder body is one long string — use first 120 chars as excerpt
  const excerpt = post.body.slice(0, 120).replace(/\n/g, " ") + "…";

  return (
    <article className={styles.card}>
      {/* Cover */}
      <div className={styles.cover} style={{ background: gradient }}>
        <span className={styles.userId}>User #{post.userId}</span>
      </div>

      <div className={styles.body}>
        {/* Meta */}
        <div className={styles.meta}>
          <div
            className={styles.avatar}
            style={{ background: avatarColor }}
          >
            {initials(`U${post.userId}`)}
          </div>
          <div className={styles.metaInfo}>
            <span className={styles.author}>User #{post.userId}</span>
            <span className={styles.dot}>·</span>
            <span className={styles.postId}>Post #{post.id}</span>
          </div>
        </div>

        {/* Title */}
        <h2 className={styles.title}>{post.title}</h2>

        {/* Excerpt */}
        <p className={styles.excerpt}>{excerpt}</p>

        {/* Footer */}
        <div className={styles.footer}>
          <div className={styles.tags}>
            <span className={styles.tag}>API Live</span>
            <span className={styles.tag}>JSONPlaceholder</span>
          </div>
          <Link
            to={`/blog/post/${post.id}`}
            className={styles.readMore}
            id={`read-post-${post.id}`}
          >
            Read →
          </Link>
        </div>
      </div>
    </article>
  );
}
