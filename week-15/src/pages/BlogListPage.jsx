import { useState, useEffect } from "react";
import { useOutletContext, useSearchParams } from "react-router-dom";
import PostCard from "../components/PostCard";
import Pagination from "../components/Pagination";
import { posts, POSTS_PER_PAGE } from "../data/posts";
import styles from "./BlogListPage.module.css";

export default function BlogListPage() {
  const { activeCategory } = useOutletContext();
  const [searchParams, setSearchParams] = useSearchParams();
  const currentPage = parseInt(searchParams.get("page") || "1", 10);

  // Filter posts
  const filtered =
    activeCategory === "All"
      ? posts
      : posts.filter((p) => p.category === activeCategory);

  const totalPages = Math.ceil(filtered.length / POSTS_PER_PAGE);

  // Reset to page 1 when category changes
  useEffect(() => {
    const cat = searchParams.get("category");
    const page = searchParams.get("page");
    if (page && parseInt(page) > 1) {
      const params = cat ? { category: cat } : {};
      setSearchParams(params);
    }
  }, [activeCategory]);

  const pagePosts = filtered.slice(
    (currentPage - 1) * POSTS_PER_PAGE,
    currentPage * POSTS_PER_PAGE
  );

  function handlePageChange(page) {
    const cat = searchParams.get("category");
    const params = {};
    if (cat) params.category = cat;
    if (page > 1) params.page = page.toString();
    setSearchParams(params);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return (
    <section>
      {filtered.length === 0 ? (
        <div className={styles.empty}>
          <span className={styles.emptyIcon}>🔍</span>
          <p>No posts found in this category.</p>
        </div>
      ) : (
        <>
          <p className={styles.resultCount}>
            Showing{" "}
            <strong>
              {(currentPage - 1) * POSTS_PER_PAGE + 1}–
              {Math.min(currentPage * POSTS_PER_PAGE, filtered.length)}
            </strong>{" "}
            of <strong>{filtered.length}</strong> posts
          </p>

          <div className={styles.grid}>
            {pagePosts.map((post) => (
              <PostCard key={post.id} post={post} />
            ))}
          </div>

          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={handlePageChange}
          />
        </>
      )}
    </section>
  );
}
