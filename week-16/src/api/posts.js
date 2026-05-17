import axios from "axios";

const BASE = "https://jsonplaceholder.typicode.com";

const api = axios.create({ baseURL: BASE });

/**
 * Fetch a paginated slice of posts.
 * JSONPlaceholder supports _page and _limit query params.
 */
export async function fetchPosts({ page = 1, limit = 12 } = {}) {
  const res = await api.get("/posts", {
    params: { _page: page, _limit: limit },
  });
  // Total count exposed in the X-Total-Count header
  const total = parseInt(res.headers["x-total-count"] || "100", 10);
  return { posts: res.data, total };
}

/**
 * Fetch a single post by id.
 */
export async function fetchPost(id) {
  const res = await api.get(`/posts/${id}`);
  return res.data;
}

/**
 * Fetch comments for a post.
 */
export async function fetchComments(postId) {
  const res = await api.get(`/posts/${postId}/comments`);
  return res.data;
}

/**
 * Fetch a user by id (for author information).
 */
export async function fetchUser(userId) {
  const res = await api.get(`/users/${userId}`);
  return res.data;
}
