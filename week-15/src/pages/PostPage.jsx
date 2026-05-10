import { useParams, Link, useNavigate } from "react-router-dom";
import { posts } from "../data/posts";
import styles from "./PostPage.module.css";

export default function PostPage() {
  const { postId } = useParams();
  const navigate = useNavigate();
  const post = posts.find((p) => p.id === parseInt(postId, 10));

  if (!post) {
    return (
      <div className={styles.notFound}>
        <h2>Post not found</h2>
        <p>The post you're looking for doesn't exist.</p>
        <Link to="/blog" className={styles.backBtn}>
          ← Back to Blog
        </Link>
      </div>
    );
  }

  // Related posts (same category, excluding current)
  const related = posts
    .filter((p) => p.category === post.category && p.id !== post.id)
    .slice(0, 3);

  // Parse simple markdown-ish content (## headings, paragraphs)
  function renderContent(text) {
    return text.split("\n\n").map((block, i) => {
      if (block.startsWith("## ")) {
        return (
          <h2 key={i} className={styles.contentH2}>
            {block.slice(3)}
          </h2>
        );
      }
      return (
        <p key={i} className={styles.contentP}>
          {block}
        </p>
      );
    });
  }

  return (
    <article className={styles.article}>
      {/* Hero */}
      <div
        className={styles.hero}
        style={{ background: post.coverGradient }}
      >
        <div className={styles.heroOverlay} />
        <div className={styles.heroContent}>
          <button
            id="back-to-blog-btn"
            className={styles.backLink}
            onClick={() => navigate(-1)}
          >
            ← Back
          </button>
          <span className={styles.heroCat}>{post.category}</span>
          <h1 className={styles.heroTitle}>{post.title}</h1>

          <div className={styles.heroMeta}>
            <div className={styles.avatar}>{post.authorAvatar}</div>
            <div className={styles.metaText}>
              <span className={styles.metaAuthor}>{post.author}</span>
              <span className={styles.metaDot}>·</span>
              <span className={styles.metaDate}>
                {new Date(post.date).toLocaleDateString("en-US", {
                  month: "long",
                  day: "numeric",
                  year: "numeric",
                })}
              </span>
              <span className={styles.metaDot}>·</span>
              <span className={styles.metaRead}>{post.readTime}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Body */}
      <div className={styles.body}>
        <div className={styles.content}>{renderContent(post.content)}</div>

        {/* Tags */}
        <div className={styles.tags}>
          {post.tags.map((tag) => (
            <span key={tag} className={styles.tag}>
              # {tag}
            </span>
          ))}
        </div>

        {/* Related Posts */}
        {related.length > 0 && (
          <aside className={styles.related}>
            <h3 className={styles.relatedTitle}>More in {post.category}</h3>
            <div className={styles.relatedGrid}>
              {related.map((r) => (
                <Link
                  key={r.id}
                  to={`/blog/post/${r.id}`}
                  id={`related-post-${r.id}`}
                  className={styles.relatedCard}
                >
                  <div
                    className={styles.relatedCover}
                    style={{ background: r.coverGradient }}
                  />
                  <div className={styles.relatedBody}>
                    <span className={styles.relatedCat}>{r.category}</span>
                    <h4 className={styles.relatedCardTitle}>{r.title}</h4>
                    <span className={styles.relatedRead}>{r.readTime}</span>
                  </div>
                </Link>
              ))}
            </div>
          </aside>
        )}
      </div>
    </article>
  );
}
