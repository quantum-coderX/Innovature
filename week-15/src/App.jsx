import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import HomePage from "./pages/HomePage";
import BlogLayout from "./pages/BlogLayout";
import BlogListPage from "./pages/BlogListPage";
import PostPage from "./pages/PostPage";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        {/* Home */}
        <Route path="/" element={<HomePage />} />

        {/* Blog — nested routes */}
        <Route path="/blog" element={<BlogLayout />}>
          {/* Index: /blog → paginated list */}
          <Route index element={<BlogListPage />} />
          {/* Single post: /blog/post/:postId — route parameter */}
          <Route path="post/:postId" element={<PostPage />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
