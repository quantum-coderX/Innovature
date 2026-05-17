import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchPost, fetchComments, fetchUser } from "../api/posts";
import ErrorBanner from "../components/ErrorBanner";
import styles from "./PostPage.module.css";

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

function getGradient(id) {
  return GRADIENTS[(id - 1) % GRADIENTS.length];
}

export default function PostPage() {
  const { postId } = useParams();
  const navigate = useNavigate();
  const id = parseInt(postId, 10);

  const [post, setPost] = useState(null);
  const [user, setUser] = useState(null);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    setPost(null);
    setUser(null);
    setComments([]);

    async function load() {
      try {
        const [postData, commentsData] = await Promise.all([
          fetchPost(id),
          fetchComments(id),
        ]);
        if (cancelled) return;
        setPost(postData);
        setComments(commentsData);

        // Fetch author in parallel — non-blocking
        fetchUser(postData.userId)
          .then((u) => { if (!cancelled) setUser(u); })
          .catch(() => {}); // optional — ignore silently
      } catch (err) {
        if (!cancelled) setError(err.message || "Failed to load post.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => { cancelled = true; };
  }, [id]);

  /* ── Loading skeleton ─────────────────────── */
  if (loading) {
    return (
      <div className={styles.skeletonWrap}>
        <div className={`${styles.skHero} skeleton`} />
        <div className={styles.skBody}>
          <div className={`${styles.skTitle} skeleton`} />
          <div className={`${styles.skLine} skeleton`} />
          <div className={`${styles.skLine} skeleton`} />
          <div className={`${styles.skLineShort} skeleton`} />
        </div>
      </div>
    );
  }

  /* ── Error state ──────────────────────────── */
  if (error) {
    return (
      <div className={styles.centered}>
        <ErrorBanner message={error} onRetry={() => navigate(0)} />
      </div>
    );
  }

  /* ── Not found ────────────────────────────── */
  if (!post) return null;

  const gradient = getGradient(post.id);

  return (
    <article className={styles.article}>
      {/* Hero */}
      <div className={styles.hero} style={{ background: gradient }}>
        <div className={styles.heroOverlay} />
        <div className={styles.heroContent}>
          <button
            id="back-btn"
            className={styles.backBtn}
            onClick={() => navigate(-1)}
          >
            ← Back
          </button>
          <span className={styles.badge}>Post #{post.id}</span>
          <h1 className={styles.heroTitle}>{post.title}</h1>

          <div className={styles.heroMeta}>
            <div className={styles.avatar}>
              {user ? user.name.slice(0, 2).toUpperCase() : `U${post.userId}`}
            </div>
            <div className={styles.metaText}>
              <span className={styles.metaAuthor}>
                {user ? user.name : `User #${post.userId}`}
              </span>
              {user && (
                <>
                  <span className={styles.metaDot}>·</span>
                  <span className={styles.metaEmail}>{user.email}</span>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Body */}
      <div className={styles.body}>
        <div className={styles.content}>
          {post.body.split("\n").map((line, i) => (
            <p key={i} className={styles.para}>{line}</p>
          ))}
        </div>

        {/* User card */}
        {user && (
          <div className={styles.authorCard}>
            <h3 className={styles.authorCardTitle}>About the author</h3>
            <div className={styles.authorInfo}>
              <div className={styles.authorAvatar}>
                {user.name.slice(0, 2).toUpperCase()}
              </div>
              <div>
                <p className={styles.authorName}>{user.name}</p>
                <p className={styles.authorMeta}>@{user.username} · {user.email}</p>
                <p className={styles.authorMeta}>{user.company.name} · {user.address.city}</p>
              </div>
            </div>
          </div>
        )}

        {/* Comments */}
        {comments.length > 0 && (
          <section className={styles.comments}>
            <h2 className={styles.commentsTitle}>
              💬 {comments.length} Comments
            </h2>
            <div className={styles.commentList}>
              {comments.map((c) => (
                <div key={c.id} className={styles.comment}>
                  <div className={styles.commentHeader}>
                    <span className={styles.commentName}>{c.name}</span>
                    <span className={styles.commentEmail}>{c.email}</span>
                  </div>
                  <p className={styles.commentBody}>{c.body}</p>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </article>
  );
}
