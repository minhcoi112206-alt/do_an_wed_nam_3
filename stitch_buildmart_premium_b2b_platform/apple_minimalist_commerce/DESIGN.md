---
name: Apple Minimalist Commerce
colors:
  surface: '#f9f9fb'
  surface-dim: '#d9dadc'
  surface-bright: '#f9f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f5'
  surface-container: '#eeeef0'
  surface-container-high: '#e8e8ea'
  surface-container-highest: '#e2e2e4'
  on-surface: '#1a1c1d'
  on-surface-variant: '#414753'
  inverse-surface: '#2f3132'
  inverse-on-surface: '#f0f0f2'
  outline: '#717785'
  outline-variant: '#c1c6d6'
  surface-tint: '#005cbb'
  primary: '#0059b5'
  on-primary: '#ffffff'
  primary-container: '#0071e3'
  on-primary-container: '#fcfbff'
  inverse-primary: '#abc7ff'
  secondary: '#5f5e60'
  on-secondary: '#ffffff'
  secondary-container: '#e2dfe1'
  on-secondary-container: '#636264'
  tertiary: '#5a5b5f'
  on-tertiary: '#ffffff'
  tertiary-container: '#737378'
  on-tertiary-container: '#fcfaff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d7e2ff'
  primary-fixed-dim: '#abc7ff'
  on-primary-fixed: '#001b3f'
  on-primary-fixed-variant: '#00458f'
  secondary-fixed: '#e4e2e4'
  secondary-fixed-dim: '#c8c6c8'
  on-secondary-fixed: '#1b1b1d'
  on-secondary-fixed-variant: '#474649'
  tertiary-fixed: '#e3e2e7'
  tertiary-fixed-dim: '#c7c6cb'
  on-tertiary-fixed: '#1a1b1f'
  on-tertiary-fixed-variant: '#46464b'
  background: '#f9f9fb'
  on-background: '#1a1c1d'
  surface-variant: '#e2e2e4'
typography:
  display-hero:
    fontFamily: Inter
    fontSize: 56px
    fontWeight: '700'
    lineHeight: 60px
    letterSpacing: -0.025em
  display-hero-mobile:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-xl:
    fontFamily: Inter
    fontSize: 44px
    fontWeight: '600'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Inter
    fontSize: 30px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.015em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 38px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 30px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 19px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-lg:
    fontFamily: Inter
    fontSize: 17px
    fontWeight: '400'
    lineHeight: 26px
    letterSpacing: -0.01em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: -0.005em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0em
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-eyebrow:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.06em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 3rem
  margin-mobile: 1.25rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
  space-2xl: 4rem
  space-3xl: 6rem
---

## Brand & Style

This design system delivers an editorial, high-precision retail experience modeled after premium Cupertino industrial design aesthetics. Crafted specifically for an authorized Apple premium reseller storefront, the interface serves as a stage where hardware craftsmanship takes precedence over interface noise.

### Core Visual Principles
- **Atmospheric Restraint:** Interface furniture recedes into the background. Negative space is functional, creating breathing room that directs focus to industrial finishes, titanium edges, and Super Retina displays.
- **Micro-tactile Precision:** Interactions mirror native iOS/macOS fluid dynamics, featuring rapid deceleration, subtle optical feedback, and organic squircle boundaries.
- **Glass & Light Fidelity:** Translucency is calibrated through hardware-accelerated frosted surfaces, creating clear spatial hierarchies without visual clutter.

## Colors

The color architecture relies on high-purity neutrals paired with a single focused interactive accent, echoing flagship retail visual standards.

### Palette Architecture
- **Primary Accent (`#0071E3`):** Reserved strictly for primary calls-to-action (Buy, Pre-order), interactive links, and focus rings. High accessibility contrast against both light canvas and dark containers.
- **Dark Surface & Primary Text (`#1D1D1F`):** Deep volcanic slate for high-priority typography, hero product cards, and dark theme elements.
- **Secondary Neutral (`#86868B`):** Calibrated intermediate slate used for metadata, spec labels, subtitles, and inactive controls.
- **Light Surface Canvas (`#F5F5F7`):** The signature off-white retail backdrop providing gentle separation for pure white (`#FFFFFF`) card containers.
- **True Black Matrix (`#000000` / `#121212`):** Ground levels for the dark-mode aesthetic, used on Pro-tier device showcases and header glass bars.

### Surface Color Logic
- **Canvas Base:** `#F5F5F7` (Light Mode) / `#000000` (Dark Mode)
- **Elevated Card Surface:** `#FFFFFF` (Light Mode) / `#121212` with 1px `rgba(255, 255, 255, 0.08)` stroke (Dark Mode)
- **Glass Overlays:** `rgba(255, 255, 255, 0.8)` with `backdrop-filter: blur(20px)` on light mode; `rgba(29, 29, 31, 0.72)` with blur on dark mode.

## Typography

The type hierarchy prioritizes high visual impact at large scales while maintaining legibility in dense specification tables and checkout flows.

### Structural Directives
- **Proportional Tracking:** Tracking tightens progressively as font size increases (down to `-0.025em` for `display-hero`) to maintain cohesion in Vietnamese and Latin titles.
- **Eyebrow Annotations:** `label-eyebrow` must always be rendered uppercase with `0.06em` letter spacing (e.g., "MỚI", "CHÍNH HÃNG VN/A", "IPHONE 16 PRO").
- **Pricing Notation:** Currency values use `headline-md` or `headline-lg` with standard numeric weights; the `₫` currency symbol inherits `body-md` sizing aligned to the cap line.

## Layout & Spacing

A 12-column adaptive system balances expansive hero billboards with systematic product comparison grids.

### Form Factor Adaptations
- **Desktop (≥ 1280px):** 12 columns, max-width `1280px` centered container, `margin: 3rem`, `gutter: 1.5rem`.
- **Tablet (768px – 1279px):** 8 columns, `margin: 2rem`, `gutter: 1.25rem`.
- **Mobile (< 768px):** 4 columns, `margin-mobile: 1.25rem`, `gutter-mobile: 1rem`.

### Rhythmic Padding System
- **Hero & Keynote Banners:** `space-3xl` (96px) vertical block padding for unconstrained product presentation.
- **Feature Showcase Sections:** `space-2xl` (64px) top and bottom separation.
- **Standard Card Interior:** `space-lg` (24px) for desktop; `space-md` (16px) for compact mobile variants.
- **Micro Gaps (Badges, Spec Pairs):** `space-xs` (4px) to `space-sm` (8px).

## Elevation & Depth

Spatial depth relies on diffused ambient occlusion and optical glass refraction rather than heavy directional drop shadows.

### Atmospheric Shadow Tiers
- **Tier 0 (Flat Canvas):** No shadow. Components blend seamlessly into `#F5F5F7` or `#FFFFFF`.
- **Tier 1 (Subtle Product Tile):** `box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04), 0 2px 6px -1px rgba(0, 0, 0, 0.02)`. Creates a crisp, elevated edge without muddy borders.
- **Tier 2 (Hover & Active Modals):** `box-shadow: 0 16px 36px -6px rgba(0, 0, 0, 0.08), 0 6px 12px -2px rgba(0, 0, 0, 0.03)`.
- **Tier 3 (Floating Sheet & Sticky Bar):** `box-shadow: 0 24px 48px -12px rgba(0, 0, 0, 0.12)`.

### Frosted Glassmorphism (Vibrant Blur)
- **Top Navigation Bar:** Sticky position with `background: rgba(255, 255, 255, 0.82)`, `backdrop-filter: blur(20px) saturate(180%)`, and border line `1px solid rgba(0, 0, 0, 0.06)`.
- **Floating Cart & Filter Bar:** `background: rgba(255, 255, 255, 0.88)` with `backdrop-filter: blur(24px)`.

## Shapes

The design uses continuous, progressive squircle curves consistent with modern industrial hardware radii.

### Radius Scale
- **Pill (`rounded-full`):** All actionable buttons, trade-in chips, filter toggles, and status tags (`border-radius: 9999px`).
- **Feature Large Surface (`rounded-3xl` / 24px):** Primary product cards, hero comparison frames, and media containers.
- **Component Medium Surface (`rounded-2xl` / 18px):** Modal sheets, accessory trays, dropdown menus, and text input boxes.
- **Interactive Micro Surface (`rounded-md` / 8px):** Color swatch pickers, storage capacity selectors, and thumbnail galleries.

## Components

### Buttons
- **Primary Action (Purchase / Trade-in):** Pill shape, `background: #0071E3`, text `#FFFFFF`, font `label-lg`. Padding: `12px 24px`. Hover: `background: #0077ED`. Active state compresses slightly via `transform: scale(0.98)`.
- **Secondary Action (Learn More):** Pill shape, `background: rgba(0, 113, 227, 0.08)`, text `#0071E3`. Hover: `background: rgba(0, 113, 227, 0.14)`.
- **Dark Inverted Action:** Pill shape, `background: #1D1D1F`, text `#FFFFFF`. Hover: `background: #333336`.
- **Ghost Action:** Borderless, `color: #0071E3`, with trailing chevron (`›`) micro-offset on hover.

### Product Showcase Cards
- **Structure:** Card surface `#FFFFFF` on `#F5F5F7` canvas, `border-radius: 24px`.
- **Card Hierarchy:**
  1. Eyebrow label (`label-eyebrow`, `#86868B`).
  2. Product title (`headline-md`, `#1D1D1F`).
  3. Short value proposition (`body-sm`, `#1D1D1F`).
  4. Pricing block (`body-sm` anchor with bold price).
  5. High-resolution transparent PNG centered with generous padding.
  6. Action footer with Primary Pill button alongside "Tìm hiểu thêm" ghost link.

### Chips & Selectors (Color & Storage)
- **Color Swatches:** 32px circular buttons with internal border `2px solid #FFFFFF` and outer active halo `2px solid #0071E3` spaced by 2px margin. Swatches display realistic titanium/glass finishes.
- **Storage Pills:** Rounded 16px container with dual typography: upper capacity (`128GB`, bold) and lower price delta (`label-md`). Selected state features 2px active `#0071E3` border with clear background.

### Input Fields & Controls
- **Text Inputs:** `height: 52px`, `border-radius: 14px`, `background: #FFFFFF`, `border: 1px solid #D2D2D7`. Focus: `border-color: #0071E3`, `box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.15)`.
- **Checkboxes & Radios:** Native-inspired squircle checkboxes with rounded-sm (4px) inner tick, filled with `#0071E3` upon validation.

### Specification & Comparison Lists
- **Spec Dividers:** Ultra-thin `1px solid rgba(0, 0, 0, 0.08)` hairline dividers.
- **Table Rhythm:** Alternating data cells with clear typography hierarchy: feature title in `body-sm` muted `#86868B`, technical metric in `headline-sm` `#1D1D1F`.

### VN/A Authenticity Badge
- **Indicator:** Glass pill badge with subtle gold or iridescent border: `border: 1px solid rgba(0, 113, 227, 0.2)`, `background: rgba(255, 255, 255, 0.7)`, containing localized Apple seal text: "Hàng Chính Hãng VN/A • Bảo Hành 12 Tháng Apple".