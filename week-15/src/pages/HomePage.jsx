import { Link } from "react-router-dom";
import styles from "./HomePage.module.css";

const FEATURED = [
  {
    title: "The Future of AI",
    cat: "Technology",
    id: 1,
    gradient: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
  },
  {
    title: "Design Systems That Scale",
    cat: "Design",
    id: 2,
    gradient: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
  },
  {
    title: "JWST: Year Three",
    cat: "Science",
    id: 3,
    gradient: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
  },
];

export default function HomePage() {
  return (
    <main className={styles.main}>
      {/* Hero */}
      <section className={styles.hero}>
        <div className={styles.heroGlow} />
        <p className={styles.heroLabel}>✦ The Modern Blog</p>
        <h1 className={styles.heroTitle}>
          Ideas Worth
          <br />
          <span className={styles.heroGradient}>Reading.</span>
        </h1>
        <p className={styles.heroSub}>
          Deep dives into technology, design, science, travel, lifestyle and
          business — curated for curious minds.
        </p>
        <Link to="/blog" id="explore-blog-btn" className={styles.heroCta}>
          Explore the Blog →
        </Link>
      </section>

      {/* Featured strip */}
      <section className={styles.featured}>
        <h2 className={styles.sectionTitle}>Featured Posts</h2>
        <div className={styles.featuredGrid}>
          {FEATURED.map((f) => (
            <Link
              key={f.id}
              to={`/blog/post/${f.id}`}
              id={`featured-post-${f.id}`}
              className={styles.featuredCard}
              style={{ background: f.gradient }}
            >
              <span className={styles.featuredCat}>{f.cat}</span>
              <h3 className={styles.featuredTitle}>{f.title}</h3>
              <span className={styles.featuredArrow}>→</span>
            </Link>
          ))}
        </div>
      </section>

      {/* Stats */}
      <section className={styles.stats}>
        {[
          { value: "12", label: "Articles" },
          { value: "6", label: "Categories" },
          { value: "8", label: "Authors" },
        ].map((s) => (
          <div key={s.label} className={styles.stat}>
            <span className={styles.statValue}>{s.value}</span>
            <span className={styles.statLabel}>{s.label}</span>
          </div>
        ))}
      </section>
    </main>
  );
}
