---
name: HSBC Fund Assistant
colors:
  surface: '#fcf8ff'
  surface-dim: '#dad7f3'
  surface-bright: '#fcf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f2ff'
  surface-container: '#efecff'
  surface-container-high: '#e8e5ff'
  surface-container-highest: '#e2e0fc'
  on-surface: '#1a1a2e'
  on-surface-variant: '#5e3f3b'
  inverse-surface: '#2f2e43'
  inverse-on-surface: '#f2efff'
  outline: '#936e69'
  outline-variant: '#e8bcb6'
  surface-tint: '#c0000d'
  primary: '#ad000b'
  on-primary: '#ffffff'
  primary-container: '#db0011'
  on-primary-container: '#ffebe8'
  inverse-primary: '#ffb4aa'
  secondary: '#b90e13'
  on-secondary: '#ffffff'
  secondary-container: '#dd2f29'
  on-secondary-container: '#fffbff'
  tertiary: '#4a556a'
  on-tertiary: '#ffffff'
  tertiary-container: '#626d83'
  on-tertiary-container: '#eaefff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad5'
  primary-fixed-dim: '#ffb4aa'
  on-primary-fixed: '#410001'
  on-primary-fixed-variant: '#930007'
  secondary-fixed: '#ffdad5'
  secondary-fixed-dim: '#ffb4aa'
  on-secondary-fixed: '#410002'
  on-secondary-fixed-variant: '#930009'
  tertiary-fixed: '#d7e3fc'
  tertiary-fixed-dim: '#bbc7df'
  on-tertiary-fixed: '#101c2e'
  on-tertiary-fixed-variant: '#3c475b'
  background: '#fcf8ff'
  on-background: '#1a1a2e'
  surface-variant: '#e2e0fc'
  sidebar-navy: '#0A1628'
  assistant-bubble: '#F0F0F5'
  background-subtle: '#F8F8FA'
  text-muted: '#8E8E93'
  warning-amber: '#FFF3CD'
  link-blue: '#0066CC'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  app-title:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '700'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  caption:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 1440px
  sidebar-width: 280px
  gutter: 24px
  margin-mobile: 16px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style
The design system for the **HSBC Fund Assistant** is built upon a foundation of **Corporate-Premium Minimalism**. It is designed to evoke absolute trust, precision, and authority, reflecting HSBC’s global banking heritage while providing a modern, AI-augmented experience for fund analysis.

The visual style is **Corporate / Modern** with a focus on high-density information delivered through a clean, systematic interface. We prioritize functional clarity over decorative elements, using "HSBC Red" sparingly to signal intent and status. The interface balances sharp architectural lines (representing stability) with specific 12px radii for interaction surfaces (representing accessibility and the "assistant" nature of the tool).

## Colors
The color strategy utilizes a "Precision Red" approach. **HSBC Red** is the primary signal color, reserved for critical actions, active states, and brand markers. 

- **Primary & Secondary:** Used for brand identity and high-priority interactions.
- **Surface Palette:** We utilize a triple-layer gray system. `White` for the primary work area, `Warm Gray` for container backgrounds, and `Light Gray` specifically for assistant dialogue surfaces to differentiate AI-generated content from user content.
- **Sidebar & Navigation:** `Deep Navy` is used for the primary navigation rail to provide a sophisticated, grounded frame for the application.
- **Functional Colors:** `Link Blue` is reserved for citations and external fund documentation. `Amber Warning` is used strictly for regulatory disclaimers and financial risk notices.

## Typography
The typography system uses **Inter** to achieve a neutral, systematic, and highly legible appearance across complex data tables and chat interfaces. 

- **Hierarchy:** We use a tight scale where the `App Title` (18px Bold) serves as the primary anchor for header sections. 
- **Readability:** The `Body-md` (15px) is the workhorse for assistant responses, optimized for long-form financial analysis. 
- **Secondary Data:** `Label-sm` and `Caption` (12px) are used for timestamps, citation indices, and metadata. 
- **Scale:** On mobile devices, `headline-lg` should scale down to 20px (`headline-md`) to ensure financial charts and tables remain the focus.

## Layout & Spacing
The design system employs a **Fixed Grid** approach for the main content area to maintain the structural integrity of financial reports, flanked by a fixed-width sidebar.

- **Sidebar:** A consistent `280px` width using `Deep Navy` background.
- **Content Area:** A 12-column grid with `24px` gutters. Content is centered with a max-width of `1440px`.
- **Rhythm:** An 8px linear scale governs all internal padding and margins. 
- **Chat Layout:** Assistant bubbles are left-aligned with a max-width of 70% of the container. User inputs are right-aligned to create a clear conversational flow.
- **Mobile Adaption:** At the 768px breakpoint, the sidebar collapses into a hamburger menu, and horizontal margins reduce to 16px.

## Elevation & Depth
In alignment with the "Corporate-Premium" style, this design system avoids heavy shadows, instead using **Tonal Layers** and **Low-Contrast Outlines** to define hierarchy.

- **Level 0 (Base):** `White` (#FFFFFF) for the main workspace.
- **Level 1 (Surface):** `Warm Gray` (#F8F8FA) for cards and secondary panels, defined by a 1px border in `Light Gray`.
- **Level 2 (Interaction):** Only the primary Red buttons or active chat inputs use a very subtle, diffused shadow (0px 4px 12px rgba(0,0,0,0.05)) to suggest interactivity.
- **Assistant Bubbles:** These use a flat `Light Gray` fill without shadows to maintain a "document-style" factual appearance rather than a playful social appearance.

## Shapes
The shape language is a hybrid of **Functional Rigidity** and **Conversational Softness**.

- **Global UI Elements:** Buttons, input fields, and containers use a standard `8px` (Rounded) corner radius to feel professional and stable.
- **Chat Bubbles:** Specifically use a `12px` radius to provide a softer, more approachable look for AI dialogue, distinguishing the "Assistant" from the "System."
- **HSBC Hexagon:** The iconic hexagon logo should always maintain its sharp 60-degree angles; it is the only element that ignores the roundedness rules to preserve brand heritage.

## Components
- **Buttons:** Primary buttons are `HSBC Red` with white text, 8px radius, and bold 14px labels. Hover states transition to `Secondary Dark Red`. Secondary buttons use a `1px` border of `Charcoal` with no fill.
- **Chat Bubbles:** Assistant bubbles use `Light Gray` background with `Charcoal` text. User bubbles use a subtle `Deep Navy` outline with `Charcoal` text to remain professional.
- **Input Fields:** Search and chat inputs are white with a `1px` border of `Light Gray`. On focus, the border changes to `HSBC Red`.
- **Cards (Fund Cards):** High-density cards with a `Warm Gray` background, featuring a sparkline chart and the fund name in `App Title` styling.
- **Citations:** Small, superscripted numbers in `Link Blue` that reveal a tooltip or scroll to the source documentation when clicked.
- **Disclaimers:** Full-width banners using `Amber Warning` background with 12px `Charcoal` text, typically placed at the bottom of fund analysis reports.