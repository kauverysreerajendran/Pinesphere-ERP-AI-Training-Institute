// lib/auth.ts
// Helper functions for auth — import these anywhere in your Next.js app

export function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access_token");
}

export function getUserRole(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("user_role");
}

export function getFullName(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("full_name");
}

export function isLoggedIn(): boolean {
  return !!getAccessToken();
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user_role");
  localStorage.removeItem("full_name");
  window.location.href = "/login";
}

// Use this for all authenticated API calls
export async function apiFetch(path: string, options: RequestInit = {}) {
  const token = getAccessToken();

  const res = await fetch(`http://localhost:8000${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...options.headers,
    },
  });

  // Token expired — redirect to login
  if (res.status === 401) {
    logout();
    return null;
  }

  return res;
}