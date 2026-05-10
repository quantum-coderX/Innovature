import { categories } from "../data/posts";
import styles from "./CategoryFilter.module.css";

export default function CategoryFilter({ activeCategory, onCategoryChange }) {
  return (
    <div className={styles.filterBar} role="tablist" aria-label="Filter by category">
      {categories.map((cat) => (
        <button
          key={cat}
          id={`filter-${cat.toLowerCase()}`}
          role="tab"
          aria-selected={activeCategory === cat}
          className={`${styles.chip} ${
            activeCategory === cat ? styles.active : ""
          }`}
          onClick={() => onCategoryChange(cat)}
        >
          {cat}
        </button>
      ))}
    </div>
  );
}
