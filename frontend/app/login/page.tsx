"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Invalid credentials");
        return;
      }

      // Save tokens to localStorage
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      localStorage.setItem("user_role", data.role);
      localStorage.setItem("full_name", data.full_name);

      // Redirect based on role
      const roleRoutes: Record<string, string> = {
        super_admin:     "/dashboard/admin",
        branch_admin:    "/dashboard/branch",
        counsellor:      "/dashboard/crm",
        trainer:         "/dashboard/trainer",
        student:         "/dashboard/student",
        parent:          "/dashboard/parent",
        hr:              "/dashboard/hr",
        finance:         "/dashboard/finance",
        franchise_owner: "/dashboard/franchise",
      };

      router.push(roleRoutes[data.role] || "/dashboard");

    } catch {
      setError("Cannot connect to server. Make sure backend is running.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#f5f5f0] flex items-center justify-center px-4 font-sans">

      {/* Background grid pattern */}
      <div
        className="fixed inset-0 pointer-events-none opacity-30"
        style={{
          backgroundImage: `linear-gradient(#d1d1cc 1px, transparent 1px),
                            linear-gradient(90deg, #d1d1cc 1px, transparent 1px)`,
          backgroundSize: "40px 40px",
        }}
      />

      <div className="relative w-full max-w-sm">

        {/* Logo */}
        <div className="flex items-center gap-3 mb-8">
          <div className="w-9 h-9 bg-[#1a1a1a] rounded-lg flex items-center justify-center">
            <svg width="18" height="18" fill="none" viewBox="0 0 24 24">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"
                stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <div>
            <p className="text-sm font-semibold text-[#1a1a1a] leading-tight">Pinesphere ERP</p>
            <p className="text-xs text-[#888] leading-tight">AI Training Institute</p>
          </div>
        </div>

        {/* Card */}
        <div className="bg-white border border-[#e5e5e0] rounded-2xl p-8 shadow-sm">
          <h1 className="text-xl font-semibold text-[#1a1a1a] mb-1">Sign in</h1>
          <p className="text-sm text-[#888] mb-6">Enter your credentials to continue</p>

          <form onSubmit={handleLogin} className="space-y-4">

            {/* Email */}
            <div>
              <label className="block text-xs font-medium text-[#555] mb-1.5">
                Email address
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@pinesphere.com"
                required
                className="w-full h-10 px-3 text-sm bg-[#fafaf8] border border-[#e5e5e0]
                           rounded-lg outline-none text-[#1a1a1a] placeholder:text-[#bbb]
                           focus:border-[#1a1a1a] focus:bg-white transition-colors"
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-xs font-medium text-[#555] mb-1.5">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                  className="w-full h-10 px-3 pr-10 text-sm bg-[#fafaf8] border border-[#e5e5e0]
                             rounded-lg outline-none text-[#1a1a1a] placeholder:text-[#bbb]
                             focus:border-[#1a1a1a] focus:bg-white transition-colors"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-[#aaa]
                             hover:text-[#555] transition-colors"
                  aria-label="Toggle password"
                >
                  {showPassword ? (
                    <svg width="16" height="16" fill="none" viewBox="0 0 24 24">
                      <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24M1 1l22 22"
                        stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                    </svg>
                  ) : (
                    <svg width="16" height="16" fill="none" viewBox="0 0 24 24">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"
                        stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="2"/>
                    </svg>
                  )}
                </button>
              </div>
            </div>

            {/* Error */}
            {error && (
              <div className="flex items-center gap-2 bg-red-50 border border-red-200
                              text-red-600 text-xs rounded-lg px-3 py-2.5">
                <svg width="14" height="14" fill="none" viewBox="0 0 24 24" className="shrink-0">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
                  <path d="M12 8v4M12 16h.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                </svg>
                {error}
              </div>
            )}

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="w-full h-10 bg-[#1a1a1a] hover:bg-[#333] disabled:bg-[#888]
                         text-white text-sm font-medium rounded-lg transition-colors
                         flex items-center justify-center gap-2 mt-2"
            >
              {loading ? (
                <>
                  <svg className="animate-spin" width="14" height="14" fill="none" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" strokeOpacity="0.3"/>
                    <path d="M12 2a10 10 0 0110 10" stroke="currentColor" strokeWidth="3" strokeLinecap="round"/>
                  </svg>
                  Signing in...
                </>
              ) : (
                "Sign in"
              )}
            </button>

          </form>
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-[#aaa] mt-6">
          Pinesphere © 2025 · All rights reserved
        </p>

      </div>
    </main>
  );
}