import { useState, useEffect } from "react";
import { Outlet, useSearchParams } from "react-router-dom";
import CategoryFilter from "../components/CategoryFilter";
import styles from "./BlogLayout.module.css";

export default function BlogLayout() {
  const [searchParams, setSearchParams] = useSearchParams();
  const activeCategory = searchParams.get("category") || "All";

  function handleCategoryChange(cat) {
    setSearchParams(cat === "All" ? {} : { category: cat });
  }

  return (
    <div className={styles.layout}>
      <div className={styles.header}>
        <h1 className={styles.title}>The Blog</h1>
        <p className={styles.subtitle}>
          Explore stories across technology, design, science, and more.
        </p>
        <CategoryFilter
          activeCategory={activeCategory}
          onCategoryChange={handleCategoryChange}
        />
      </div>
      <Outlet context={{ activeCategory }} />
    </div>
  );
}
