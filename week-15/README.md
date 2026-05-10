# Week 15 - Inkwell Blog Platform

**Topic:** React Router, Nested Routes, Search Params, Pagination

Week 15 is a polished blog-style React app built with **Vite** and **React Router**. It includes a landing page, a paginated blog index, category filtering, and individual post pages with related content.

---

## Getting Started

```bash
npm install
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## Features

| Feature | Implementation |
|---|---|
| Home page | Hero section, featured post cards, and simple blog stats |
| Blog listing | Paginated article grid driven by `page` search params |
| Category filter | `category` search param updates the list without leaving the route |
| Post details | Dynamic route at `/blog/post/:postId` |
| Related posts | Shows up to three posts from the same category |
| Navigation | Top navbar with `Home` and `Blog` routes |
| Fallback routing | Unknown routes redirect back to `/` |

---

## Routes

- `/` - Home page
- `/blog` - Blog layout with category filter and paginated post list
- `/blog/post/:postId` - Single post page

---

## Project Structure

```text
week-15/
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.js
├── public/
└── src/
    ├── App.jsx
    ├── main.ts
    ├── index.css
    ├── data/posts.js
    ├── components/
    │   ├── Navbar.jsx
    │   ├── CategoryFilter.jsx
    │   ├── Pagination.jsx
    │   └── PostCard.jsx
    └── pages/
        ├── HomePage.jsx
        ├── BlogLayout.jsx
        ├── BlogListPage.jsx
        └── PostPage.jsx
```

---

## Notes

- `BlogLayout` reads the active category from the URL and passes it to the list page.
- `BlogListPage` uses `useSearchParams` to keep pagination and category state in the URL.
- `PostPage` renders a selected post, related posts, and a simple markdown-style content parser.