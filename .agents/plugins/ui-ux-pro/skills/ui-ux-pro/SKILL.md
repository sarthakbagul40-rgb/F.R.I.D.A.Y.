---
name: ui-ux-pro
description: >-
  Expert UI/UX Pro design intelligence, design tokens, color harmonies, typography scales,
  responsive layouts, glassmorphism, micro-animations, and frontend component architecture.
  Use when designing or building web apps, mobile interfaces, dashboards, or styling components.
---

# UI/UX Pro Design Intelligence & Engineering Guide

This skill equips agents with senior-level UI/UX architecture principles, aesthetic excellence, design tokens, and frontend implementation standards.

---

## 1. Core Aesthetic Principles (Zero-Boring UI)

1. **Rich Visual Hierarchy**:
   - Never use flat, uninspired solids for primary backgrounds. Use subtle radial/mesh gradients, dark-mode surfaces with elevation depth (`rgba(255,255,255,0.03)` to `rgba(255,255,255,0.08)`), and soft borders (`1px solid rgba(255,255,255,0.1)`).
2. **Harmonious Color Palettes**:
   - **Primary Accents**: Tailored HSL values (e.g., Cyber Cyan `hsl(185, 100%, 50%)`, Electric Violet `hsl(265, 90%, 65%)`, Emerald Glow `hsl(150, 80%, 45%)`).
   - **Dark Canvas**: Deep rich charcoal/slate (`hsl(220, 20%, 8%)` to `hsl(220, 25%, 4%)`) instead of pure `#000000` (except for OLED black high-contrast zones).
3. **Modern Typography**:
   - Pair crisp modern geometric display fonts (Rajdhani, Orbitron, Outfit, Syne, Inter) with ultra-legible body typography.
   - Use fluid typography with `clamp()` for responsive viewport scaling.

---

## 2. Style Presets Catalog

### A. Glassmorphism & Cybernetic HUD
* **Backdrop Filter**: `backdrop-filter: blur(12px) saturate(180%);`
* **Surface**: `background: rgba(15, 23, 42, 0.65);`
* **Border**: `1px solid rgba(56, 189, 248, 0.2);`
* **Box Shadow**: `0 8px 32px 0 rgba(0, 0, 0, 0.37), inset 0 0 12px rgba(56, 189, 248, 0.05);`

### B. Bento Grid Layout
* Responsive CSS Grid with `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))`
* Unequal span items (`grid-column: span 2`, `grid-row: span 2`) to create compelling visual rhythm.
* Card padding: 24px–32px with rounded corners (`16px`–`24px`).

### C. Micro-Interactions & Transitions
* **Hover Lift**: `transform: translateY(-2px); box-shadow: 0 12px 24px -6px rgba(0, 0, 0, 0.4);`
* **Spring Timing**: `transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);`
* **Active Press**: `transform: translateY(0px) scale(0.98);`

---

## 3. UI/UX Pro Design Checklist

- [ ] **Contrast Ratio**: Meets WCAG 2.1 AAA standards for text against backgrounds.
- [ ] **Touch Targets**: All clickable buttons and interactive items have a minimum touch footprint of 44x44px.
- [ ] **State Handling**: Distinct styles for `:hover`, `:focus-visible` (clear outline ring), `:active`, and `:disabled`.
- [ ] **Feedback Loops**: Instant visual feedback for async actions (pulse loaders, skeleton screens, progress bars).
- [ ] **Responsive Breakpoints**: Seamless adaptability across Mobile (<640px), Tablet (641-1024px), and Desktop (>1024px).
