# 🔐 Google OAuth Implementation Plan

## Project: Learn English Zero
## Date: December 18, 2025

---

## 📋 Overview

Implement Google OAuth login using Supabase Auth for:
- **Frontend:** `learnenglishzero.io.vn` (Next.js on Vercel)
- **Backend:** `api.learnenglishzero.io.vn` (FastAPI on Railway)
- **Auth Provider:** Supabase (Google OAuth)

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Frontend     │     │    Supabase     │     │     Google      │
│    (Next.js)    │────▶│     Auth        │────▶│     OAuth       │
│                 │◀────│                 │◀────│                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │
         │                      │
         ▼                      ▼
┌─────────────────┐     ┌─────────────────┐
│    Backend      │     │    Supabase     │
│    (FastAPI)    │────▶│    Database     │
│                 │     │    (users)      │
└─────────────────┘     └─────────────────┘
```

---

## ✅ TODO Checklist

### Phase 1: Supabase Configuration ✅
- [x] Create Google OAuth credentials in Google Cloud Console
- [x] Configure Google provider in Supabase Dashboard
- [x] Add redirect URIs

### Phase 2: Backend Implementation
- [ ] Create auth router (`/api/auth/*`)
- [ ] Implement token verification endpoint
- [ ] Implement user profile endpoint
- [ ] Add JWT middleware for protected routes
- [ ] Update User model if needed
- [ ] Add auth documentation

### Phase 3: Frontend Implementation
- [ ] Install Supabase client (`@supabase/supabase-js`)
- [ ] Create Supabase client configuration
- [ ] Create AuthContext for state management
- [ ] Implement Login page with Google button
- [ ] Implement Auth callback page
- [ ] Implement Logout functionality
- [ ] Add protected route wrapper
- [ ] Create user profile display component

### Phase 4: Testing
- [ ] Test login flow locally
- [ ] Test login flow on production
- [ ] Test token refresh
- [ ] Test logout
- [ ] Test protected routes

### Phase 5: Security Review
- [ ] Verify CORS configuration
- [ ] Verify redirect URI whitelist
- [ ] Rotate Google Client Secret (exposed in chat)
- [ ] Add rate limiting to auth endpoints
- [ ] Review RLS policies in Supabase

---

## 🔑 Credentials (Reference Only)

| Service | Key | Location |
|---------|-----|----------|
| Google Client ID | `762354688712-...` | Google Cloud Console |
| Google Client Secret | `GOCSPX-...` | Google Cloud Console |
| Supabase URL | `https://mgztjcjelknkpwlipqxi.supabase.co` | Supabase Dashboard |
| Supabase Anon Key | `eyJ...` | Supabase Dashboard → API |

⚠️ **NEVER commit secrets to git!** Use environment variables.

---

## 📁 Files to Create/Modify

### Backend (`learn_english_from_zero_for_vietnamese_backend`)
```
app/
├── routers/
│   └── auth.py              # NEW: Auth endpoints
├── middleware/
│   └── auth.py              # NEW: JWT verification middleware
├── schemas/
│   └── auth.py              # NEW: Auth request/response schemas
├── services/
│   └── auth.py              # NEW: Auth business logic
└── main.py                  # MODIFY: Add auth router
```

### Frontend (`learn_english_from_zero_for_vietnamese_frontend`)
```
lib/
├── supabase.ts              # NEW: Supabase client
└── auth-context.tsx         # NEW: Auth state management
app/
├── login/
│   └── page.tsx             # NEW: Login page
├── auth/
│   └── callback/
│       └── page.tsx         # NEW: OAuth callback
├── profile/
│   └── page.tsx             # NEW: User profile (protected)
└── components/
    ├── LoginButton.tsx      # NEW: Google login button
    ├── LogoutButton.tsx     # NEW: Logout button
    └── ProtectedRoute.tsx   # NEW: Route guard
```

---

## 🚀 Implementation Order

1. **Backend First:** Create auth endpoints
2. **Frontend Second:** Create login UI and auth flow
3. **Test Locally:** Verify everything works on localhost
4. **Deploy:** Push to production
5. **Test Production:** Verify production OAuth flow

---

## 📚 References

- [Supabase Auth Docs](https://supabase.com/docs/guides/auth)
- [Supabase Google OAuth](https://supabase.com/docs/guides/auth/social-login/auth-google)
- [Next.js + Supabase](https://supabase.com/docs/guides/getting-started/quickstarts/nextjs)
