import { Link } from "react-router-dom";
import styles from "./HomePage.module.css";

export default function HomePage() {
  return (
    <main className={styles.main}>
      <div className={styles.glow} aria-hidden="true" />

      <section className={styles.hero}>
        <div className={styles.badge}>
          <span className={styles.dot} />
          Live from JSONPlaceholder API
        </div>

        <h1 className={styles.heading}>
          Stories that{" "}
          <span className={styles.gradient}>move</span>{" "}
          you.
        </h1>

        <p className={styles.sub}>
          Inkwell pulls real posts from a live public API — explore
          100 dynamically loaded articles with infinite scroll, loading
          skeletons, and graceful error handling.
        </p>

        <div className={styles.actions}>
          <Link to="/blog" id="hero-cta-blog" className={styles.cta}>
            Explore the Blog →
          </Link>
          <a
            href="https://jsonplaceholder.typicode.com"
            target="_blank"
            rel="noopener noreferrer"
            className={styles.ctaGhost}
          >
            View API source ↗
          </a>
        </div>
      </section>

      {/* Features */}
      <section className={styles.features}>
        {FEATURES.map((f) => (
          <div key={f.title} className={styles.featureCard}>
            <div className={styles.featureIcon}>{f.icon}</div>
            <h3 className={styles.featureTitle}>{f.title}</h3>
            <p className={styles.featureDesc}>{f.desc}</p>
          </div>
        ))}
      </section>
    </main>
  );
}

const FEATURES = [
  {
    icon: "⚡",
    title: "Live API via Axios",
    desc: "Posts are fetched in real time from JSONPlaceholder using Axios with proper error handling.",
  },
  {
    icon: "∞",
    title: "Infinite Scroll",
    desc: "IntersectionObserver triggers automatic page loads as you scroll — no buttons needed.",
  },
  {
    icon: "💀",
    title: "Skeleton Loaders",
    desc: "Shimmering skeleton cards replace spinners for a premium loading experience.",
  },
  {
    icon: "🛡️",
    title: "Error States",
    desc: "Network failures are caught and displayed with a retry button so users are never stuck.",
  },
  {
    icon: "🔍",
    title: "Post Detail",
    desc: "Each post has a dedicated page fetching the post body and its comments live.",
  },
  {
    icon: "🎨",
    title: "React Router v7",
    desc: "Nested routes, useParams, and useNavigate power seamless navigation between pages.",
  },
];
