import styles from "./Pagination.module.css";

export default function Pagination({ currentPage, totalPages, onPageChange }) {
  const pages = Array.from({ length: totalPages }, (_, i) => i + 1);

  if (totalPages <= 1) return null;

  return (
    <nav className={styles.pagination} aria-label="Blog pagination">
      <button
        id="prev-page-btn"
        className={styles.arrow}
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        aria-label="Previous page"
      >
        ←
      </button>

      <div className={styles.pages}>
        {pages.map((page) => (
          <button
            key={page}
            id={`page-btn-${page}`}
            className={`${styles.page} ${
              page === currentPage ? styles.active : ""
            }`}
            onClick={() => onPageChange(page)}
            aria-current={page === currentPage ? "page" : undefined}
          >
            {page}
          </button>
        ))}
      </div>

      <button
        id="next-page-btn"
        className={styles.arrow}
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        aria-label="Next page"
      >
        →
      </button>
    </nav>
  );
}
