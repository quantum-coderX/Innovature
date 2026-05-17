import { useState, useEffect, useCallback, useRef } from "react";
import { fetchPosts } from "../api/posts";

const LIMIT = 12;

/**
 * useInfinitePosts — fetches pages of posts and accumulates them.
 * Exposes a `loadMore` callback triggered by the IntersectionObserver sentinel.
 */
export function useInfinitePosts() {
  const [posts, setPosts] = useState([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  // Track which pages have been successfully fetched
  const fetchedPages = useRef(new Set());

  const loadMore = useCallback(() => {
    setPage((p) => p + 1);
  }, []);

  useEffect(() => {
    // Skip if this page has already been fetched
    if (fetchedPages.current.has(page)) return;

    setLoading(true);
    setError(null);

    fetchPosts({ page, limit: LIMIT })
      .then(({ posts: newPosts, total: t }) => {
        fetchedPages.current.add(page);
        setPosts((prev) => {
          const ids = new Set(prev.map((p) => p.id));
          const unique = newPosts.filter((p) => !ids.has(p.id));
          return [...prev, ...unique];
        });
        setTotal(t);
      })
      .catch((err) => {
        setError(err.message || "Failed to fetch posts.");
        // Do NOT add to fetchedPages — allows retry via retry()
      })
      .finally(() => setLoading(false));
  }, [page]);

  /** Force-retry the current failed page */
  const retry = useCallback(() => {
    // Remove from fetched set so the effect will fire again
    fetchedPages.current.delete(page);
    setError(null);
    // Toggle page briefly to re-trigger the effect
    setPage((p) => p - 0.001);
    setTimeout(() => setPage((p) => Math.round(p)), 0);
  }, [page]);

  const hasMore = total === null || posts.length < total;

  return { posts, loading, error, hasMore, loadMore, retry };
}
