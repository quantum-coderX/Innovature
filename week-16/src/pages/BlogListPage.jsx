import PostCard from "../components/PostCard";
import SkeletonCard from "../components/SkeletonCard";
import ErrorBanner from "../components/ErrorBanner";
import { useInfinitePosts } from "../hooks/useInfinitePosts";
import { useSentinel } from "../hooks/useSentinel";
import styles from "./BlogListPage.module.css";

const SKELETON_COUNT = 12;

export default function BlogListPage() {
  const { posts, loading, error, hasMore, loadMore, retry } = useInfinitePosts();

  // Sentinel triggers next page load when it scrolls into view
  const sentinelRef = useSentinel(loadMore, {
    enabled: hasMore && !loading && !error,
  });

  const isInitialLoad = loading && posts.length === 0;

  return (
    <section className={styles.section}>
      {/* Post count badge */}
      {posts.length > 0 && (
        <p className={styles.count}>
          Showing <strong>{posts.length}</strong> posts loaded
        </p>
      )}

      {/* Grid */}
      <div className={styles.grid}>
        {/* Real posts */}
        {posts.map((post) => (
          <PostCard key={post.id} post={post} />
        ))}

        {/* Skeleton placeholders on initial load or next-page load */}
        {loading &&
          Array.from({ length: SKELETON_COUNT }).map((_, i) => (
            <SkeletonCard key={`sk-${i}`} />
          ))}
      </div>

      {/* Inline error when we already have some posts */}
      {error && <ErrorBanner message={error} onRetry={retry} />}

      {/* Sentinel div — watched by IntersectionObserver */}
      {hasMore && !error && <div ref={sentinelRef} className={styles.sentinel} />}

      {/* "You've reached the end" */}
      {!hasMore && !loading && (
        <div className={styles.end}>
          <span className={styles.endLine} />
          <span className={styles.endText}>You've read everything ✦</span>
          <span className={styles.endLine} />
        </div>
      )}

      {/* Inline spinner between pages */}
      {loading && posts.length > 0 && (
        <div className={styles.spinnerWrap}>
          <div className={styles.spinner} />
        </div>
      )}
    </section>
  );
}
