# Week 16 — API Calls: Live Blog App

> **Topics:** Fetch & Axios · Loading & Error States · `useEffect` hook · Infinite Scroll (Bonus)

## Live App
Run locally with:
```bash
npm install
npm run dev
```

Then open [http://localhost:5174](http://localhost:5174)

---

## Assignment Checklist

| Requirement | Status |
|---|---|
| Fetch posts with **Axios** | ✅ `src/api/posts.js` |
| Handle **loading** state (skeleton cards) | ✅ `SkeletonCard.jsx` |
| Handle **error** state (banner + retry) | ✅ `ErrorBanner.jsx` |
| **Bonus: Infinite scroll** | ✅ `IntersectionObserver` sentinel |
| Single post page (useEffect + Axios) | ✅ `PostPage.jsx` |
| Comments fetched live | ✅ `fetchComments()` |
| Author info fetched live | ✅ `fetchUser()` |

---

## Architecture

```
src/
├── api/
│   └── posts.js           # Axios instance + fetchPosts / fetchPost / fetchComments / fetchUser
├── hooks/
│   ├── useInfinitePosts.js  # Infinite-scroll state machine (page, posts, loading, error)
│   └── useSentinel.js       # IntersectionObserver hook
├── components/
│   ├── Navbar.jsx / .module.css
│   ├── PostCard.jsx / .module.css   # Live API card with deterministic gradients
│   ├── SkeletonCard.jsx / .module.css  # Shimmer placeholder
│   └── ErrorBanner.jsx / .module.css   # Error state with retry
└── pages/
    ├── HomePage.jsx / .module.css
    ├── BlogLayout.jsx / .module.css
    ├── BlogListPage.jsx / .module.css  # Infinite scroll + skeleton grid
    └── PostPage.jsx / .module.css      # Single post + comments
```

---

## Key Concepts Demonstrated

### 1. Axios API Layer (`src/api/posts.js`)
```js
const api = axios.create({ baseURL: "https://jsonplaceholder.typicode.com" });

export async function fetchPosts({ page, limit }) {
  const res = await api.get("/posts", { params: { _page: page, _limit: limit } });
  const total = parseInt(res.headers["x-total-count"], 10);
  return { posts: res.data, total };
}
```

### 2. Loading & Error States (`PostPage.jsx`)
```jsx
useEffect(() => {
  setLoading(true);
  fetchPost(id)
    .then(setPost)
    .catch(err => setError(err.message))
    .finally(() => setLoading(false));
}, [id]);

if (loading) return <SkeletonLoader />;
if (error)   return <ErrorBanner message={error} onRetry={() => navigate(0)} />;
```

### 3. Infinite Scroll (Bonus)
```js
// useSentinel.js — IntersectionObserver
const observer = new IntersectionObserver(([entry]) => {
  if (entry.isIntersecting) onIntersect();   // → loadMore()
});
observer.observe(sentinelDiv);
```
A 1px sentinel `<div>` at the bottom of the list fires `loadMore()` which increments `page`, triggering the next Axios fetch.

---

## API Source
All data comes from **[JSONPlaceholder](https://jsonplaceholder.typicode.com)** — a free, open REST API with 100 posts, 10 users, and 500 comments.
