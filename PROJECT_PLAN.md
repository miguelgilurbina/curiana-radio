# Curiana Radio - Project Planning & Architecture

## Executive Summary

Curiana Radio is a cultural newsletter experience delivered as immersive web pages. Each monthly edition is a standalone, full-viewport journey combining curated music, experimental narrative, AI-generated visuals, and reflections on technology and culture. The project prioritizes intimate, personal reading experiences over traditional web navigation patterns.

**Core Philosophy**: Each visit is an experience, not just content consumption.

---

## 1. Architecture Overview

### 1.1 Technology Stack Recommendation

**Framework**: Next.js 14+ (App Router)
- **Why**: Built-in performance optimization, file-based routing, excellent MDX support, image optimization, metadata API, and exceptional mobile performance
- **Rendering**: Hybrid (Static for content, dynamic where needed)
- **Deployment**: Vercel (seamless Next.js integration, preview deployments)

**Content Management**: MDX (Markdown + JSX)
- **Why**: Combines readable markdown with embeddable React components, perfect for mixing rich text with Spotify embeds, images, and interactive elements
- **Storage**: File-based content in `/content` directory

**Styling**: Tailwind CSS + CSS Modules (hybrid approach)
- **Tailwind**: Rapid UI development, utility-first for layouts and spacing
- **CSS Modules**: Custom animations, complex typography, unique visual effects
- **Why**: Tailwind for speed and consistency, CSS Modules for artistic expression

**TypeScript**: Strict mode enabled
- **Why**: Type safety for content structure, component props, and configuration prevents errors when creating multiple editions

### 1.2 File & Folder Structure

```
curiana-radio/
│
├── .claude/                          # Expert agents for development
│   ├── commands/
│   │   ├── nextjs-expert.md
│   │   ├── ui-expert.md
│   │   ├── github-expert.md
│   │   ├── architecture-expert.md
│   │   └── typescript-expert.md
│   └── README.md
│
├── public/                           # Static assets
│   ├── images/                       # AI-generated visuals, logo
│   ├── fonts/                        # Custom web fonts (if any)
│   └── favicon.ico
│
├── content/                          # Edition content (MDX files)
│   ├── editions/
│   │   ├── 01/
│   │   │   ├── metadata.json        # Edition metadata (title, date, theme)
│   │   │   ├── intro.mdx            # Intro section (~150 words)
│   │   │   ├── jai-sounds.mdx       # Music curation (~400 words)
│   │   │   ├── hybrid.mdx           # Narrative + tech section (~700 words)
│   │   │   ├── closing.mdx          # Closing reflection (~100 words)
│   │   │   └── assets/              # Edition-specific images
│   │   │
│   │   ├── 02/
│   │   │   └── [same structure]
│   │   └── ...
│   │
│   └── archive.json                 # List of all editions for archive page
│
├── src/
│   ├── app/                         # Next.js App Router
│   │   ├── layout.tsx               # Root layout (fonts, metadata)
│   │   ├── page.tsx                 # Landing page (latest edition + archive link)
│   │   ├── globals.css              # Global styles, CSS variables
│   │   │
│   │   ├── [edition]/               # Dynamic route for editions
│   │   │   ├── page.tsx             # Edition page template
│   │   │   ├── loading.tsx          # Loading state
│   │   │   └── error.tsx            # Error boundary
│   │   │
│   │   ├── archivo/                 # Archive page
│   │   │   └── page.tsx
│   │   │
│   │   └── sobre/                   # About page (optional for MVP)
│   │       └── page.tsx
│   │
│   ├── components/                  # React components
│   │   ├── layout/
│   │   │   ├── Navigation.tsx       # Minimal navigation component
│   │   │   ├── Footer.tsx           # Footer with frequency (88.8 FM)
│   │   │   └── Background.tsx       # Animated background component
│   │   │
│   │   ├── sections/                # Content section components
│   │   │   ├── IntroSection.tsx     # Intro rendering component
│   │   │   ├── JaiSoundsSection.tsx # Music section with Spotify embed
│   │   │   ├── HybridSection.tsx    # Narrative + tech section
│   │   │   ├── ClosingSection.tsx   # Closing reflection
│   │   │   └── RabbitHole.tsx       # Expandable/collapsible content
│   │   │
│   │   ├── ui/                      # Reusable UI components
│   │   │   ├── SpotifyEmbed.tsx     # Spotify playlist embed
│   │   │   ├── ImageGallery.tsx     # AI image display component
│   │   │   ├── Typography.tsx       # Text components with styles
│   │   │   └── FrequencyBadge.tsx   # 88.8 FM visual element
│   │   │
│   │   └── archive/
│   │       └── EditionCard.tsx      # Archive listing card component
│   │
│   ├── lib/                         # Utility functions
│   │   ├── content.ts               # MDX loading and parsing utilities
│   │   ├── metadata.ts              # Metadata generation helpers
│   │   └── utils.ts                 # General utility functions
│   │
│   ├── types/                       # TypeScript type definitions
│   │   ├── edition.ts               # Edition content types
│   │   ├── section.ts               # Section-specific types
│   │   └── index.ts                 # Exported types
│   │
│   └── styles/                      # CSS Modules and theme
│       ├── theme.css                # CSS custom properties (colors, fonts)
│       ├── animations.module.css    # Custom animations
│       └── typography.module.css    # Advanced typography styles
│
├── .gitignore
├── .eslintrc.json
├── next.config.js                   # Next.js configuration (MDX support)
├── tailwind.config.ts               # Tailwind theme customization
├── tsconfig.json                    # TypeScript configuration
├── package.json
└── README.md                        # Project documentation
```

**Key Architectural Decisions**:

1. **Content-first structure**: `/content/editions` mirrors the URL structure (`/1`, `/2`), making it intuitive to add new editions
2. **Separation of concerns**: Content (MDX) separate from presentation (components) separate from layout (App Router)
3. **Component modularity**: Each section type is a reusable component, allowing different combinations per edition
4. **Type safety**: Dedicated `/types` folder ensures consistent data structures across editions
5. **Static asset optimization**: `/public` for static files, Next.js handles optimization automatically

---

## 2. Core Components Description

### 2.1 Layout Components

#### **Navigation**
- **Purpose**: Minimal, non-intrusive navigation that doesn't break immersion
- **Elements**:
  - Logo/brand mark (top-left or centered)
  - Current edition number (e.g., "#1")
  - Link to "Archivo" (archive)
  - Optional: frequency badge (88.8 FM) as identity marker
- **Behavior**:
  - Subtle, possibly auto-hides on scroll (mobile)
  - Always accessible but not dominant
  - Smooth transitions between states

#### **Background**
- **Purpose**: Set the mood without competing with content
- **MVP Implementation**: Animated gradient (earth tones + deep blue)
- **Parameters**:
  - Speed of animation (subtle, slow)
  - Color stops configurable per edition
  - Contrast-safe (text always readable)
- **Future**: Generative/procedural backgrounds, responsive to user interaction

#### **Footer**
- **Purpose**: Grounding element, project identity
- **Elements**:
  - Frequency notation (88.8 FM)
  - Copyright/attribution
  - Optional: newsletter signup (future)
- **Behavior**: Fixed or appears at end of scroll

### 2.2 Section Components

#### **IntroSection**
- **Purpose**: Establish tone and theme for the edition
- **Content**: ~150 words of reflective/poetic text
- **Design Characteristics**:
  - Large, expressive typography
  - Generous spacing above/below
  - Centered or asymmetric layout (varies per edition)
  - Animation: Fade-in on load
- **Flexibility**: Accepts custom styling per edition

#### **JaiSoundsSection** (Music Curation)
- **Purpose**: Present 5 curated tracks with context
- **Content**:
  - Section title
  - 5 mini-reviews (~80 words each)
  - Embedded Spotify playlist
  - Link to "Rabbit Hole" (extended content)
- **Structure**:
  - Track list (vertical on mobile, could be grid on desktop)
  - Each track: Title, artist, micro-review
  - Spotify embed below track list
- **Rabbit Hole**: Collapsible section with deeper music analysis, genre connections, etc.

#### **HybridSection** (Narrative + Tech Exploration)
- **Purpose**: Long-form content mixing storytelling with technical/AI insights
- **Content**: ~700 words, may include:
  - AI-generated images
  - Code snippets (syntax highlighted)
  - Pull quotes
  - Side notes
- **Design Characteristics**:
  - Optimal line length for reading (60-75 characters)
  - Rhythm: text blocks interspersed with visuals
  - Images: Full-bleed or floating, depending on aesthetic
- **Rabbit Hole**: Technical deep-dive (prompts, process, tools used)

#### **ClosingSection**
- **Purpose**: Reflective ending, invitation to ponder
- **Content**: ~100 words
- **Design Characteristics**:
  - Centered, minimal
  - Could include a question or call to future action
  - Smooth transition to footer

#### **RabbitHole** (Reusable)
- **Purpose**: Expandable content that doesn't interrupt flow
- **Behavior**:
  - Click/tap to expand (accordion-style)
  - Or: Link to sub-page (e.g., `/1/sounds-deep-dive`)
  - Visual indicator: 🐇 icon or "Dive deeper →"
- **Implementation Options**:
  - **Option A**: Client-side expansion (accordion)
  - **Option B**: Separate route (better for long content, SEO)
- **MVP Recommendation**: Accordion (simpler, keeps user on page)

### 2.3 UI Components

#### **SpotifyEmbed**
- **Purpose**: Embed Spotify playlists seamlessly
- **Props**: Playlist ID, optional height/theme
- **Responsive**: Adjusts to mobile/desktop screens
- **Performance**: Lazy-loaded iframe

#### **ImageGallery**
- **Purpose**: Display AI-generated images with context
- **Features**:
  - Lightbox/modal view (optional)
  - Lazy loading
  - Captions/alt text for accessibility
- **Layout**: Flexible (single, grid, full-bleed)

#### **Typography**
- **Purpose**: Pre-styled text components for consistency
- **Components**:
  - `<Heading>` (H1, H2, H3 with consistent styles)
  - `<BodyText>` (optimized paragraph component)
  - `<Quote>` (pull quotes, blockquotes)
  - `<Caption>` (image captions, side notes)
- **Why**: Ensures typographic consistency across editions

#### **FrequencyBadge**
- **Purpose**: Visual identity element (88.8 FM)
- **Placement**: Navigation, footer, or as decorative element
- **Style**: Vintage radio-inspired but minimal

### 2.4 Archive Components

#### **EditionCard**
- **Purpose**: Represent each edition in the archive listing
- **Content**:
  - Edition number
  - Title/theme
  - Publication date
  - Thumbnail image (optional)
  - Short description (1-2 sentences)
- **Interaction**: Click/tap navigates to edition
- **Layout**: Grid on desktop, stacked on mobile

---

## 3. Implementation Phases

### Phase 0: Foundation Setup (Week 1)
**Goal**: Project initialization and tooling configuration

**Tasks**:
1. Initialize Next.js 14 project with TypeScript
2. Configure Tailwind CSS with custom theme
3. Set up ESLint and Prettier
4. Configure git workflow (branching strategy, commit conventions)
5. Set up Vercel deployment (main branch auto-deploy)
6. Create base folder structure
7. Define TypeScript types for Edition content structure
8. Set up MDX support in Next.js config

**Deliverables**:
- Empty but fully configured project
- `types/edition.ts` with content structure defined
- `tailwind.config.ts` with custom colors and fonts
- Working deployment pipeline

**Technical Considerations**:
- Use Next.js 14+ App Router (not Pages Router)
- Enable TypeScript strict mode
- Configure Tailwind with custom color palette (earth tones + blue)
- Set up path aliases (`@/components`, `@/lib`, etc.) in tsconfig

---

### Phase 1: Core Layout & Navigation (Week 2)
**Goal**: Establish the visual framework and navigation system

**Tasks**:
1. Create root layout with global styles
2. Build Navigation component (logo, edition number, archive link)
3. Build Footer component (88.8 FM badge)
4. Create Background component (animated gradient)
5. Design and implement typography system (CSS custom properties)
6. Create landing page (`/` route) - placeholder for now
7. Set up responsive breakpoints and mobile-first approach

**Deliverables**:
- Functional layout that wraps all pages
- Navigation and footer working
- Animated background (subtle gradient)
- Typography scale defined and tested

**Technical Considerations**:
- Use CSS custom properties for colors, fonts, spacing
- Implement dark mode support in theme (optional for MVP)
- Ensure 60fps background animation (GPU-accelerated)
- Test on real mobile devices for touch interactions

---

### Phase 2: Content Infrastructure (Week 2-3)
**Goal**: Build the system for creating and rendering edition content

**Tasks**:
1. Set up MDX parsing and rendering utilities (`lib/content.ts`)
2. Create `/content/editions/01/` folder structure
3. Build dynamic route `[edition]/page.tsx`
4. Implement metadata extraction from edition files
5. Create MDX components mapping for custom elements
6. Write content loading functions (server-side)
7. Build error handling for missing editions

**Deliverables**:
- Functional content loading system
- Dynamic routing working (`/1`, `/2`, etc.)
- MDX files render correctly with custom components
- Error page for invalid edition numbers

**Technical Considerations**:
- Use Next.js Server Components for content loading (better performance)
- Cache MDX parsing results
- Implement proper error boundaries
- Type-safe content structure (TypeScript interfaces)

---

### Phase 3: Section Components (Week 3-4)
**Goal**: Build all content section components

**Tasks**:
1. **IntroSection**: Typography-focused, fade-in animation
2. **JaiSoundsSection**: Track list + Spotify embed
3. **HybridSection**: Long-form text with image support
4. **ClosingSection**: Minimal, centered reflection
5. **RabbitHole**: Expandable accordion component
6. Test each component with dummy content
7. Ensure responsive behavior on all screen sizes

**Deliverables**:
- All 4 section components functional and styled
- RabbitHole accordion working smoothly
- Responsive across mobile/tablet/desktop
- Accessibility (keyboard navigation, screen readers)

**Technical Considerations**:
- Use Tailwind for layout, CSS Modules for animations
- Implement smooth scroll to sections (optional)
- Lazy-load images in HybridSection
- Test reading experience on mobile (line length, font size)

---

### Phase 4: Edition #1 Content Creation (Week 4)
**Goal**: Write and publish the first complete edition

**Tasks**:
1. Write Edition #1 content in MDX files
2. Source/create AI-generated images for Hybrid section
3. Create Spotify playlist and embed
4. Test entire reading experience end-to-end
5. Optimize images (Next.js Image component)
6. Write metadata (title, description, OG image)
7. Preview on mobile devices

**Deliverables**:
- Complete Edition #1 published at `/1`
- All sections rendered with real content
- Images optimized and loading properly
- Social sharing preview working (Open Graph)

**Technical Considerations**:
- Use `next/image` for all images (auto-optimization)
- Test performance (Lighthouse score, Core Web Vitals)
- Ensure Spotify embed doesn't block page load
- Validate accessibility (color contrast, alt text)

---

### Phase 5: Archive & Landing Pages (Week 5)
**Goal**: Complete the site navigation and discoverability

**Tasks**:
1. Build archive page (`/archivo`) listing all editions
2. Create EditionCard component with metadata
3. Update landing page (`/`) to show latest edition preview + archive link
4. Implement sorting (newest first)
5. Add pagination if needed (future-proofing)
6. Write "About" page content (optional for MVP)

**Deliverables**:
- Functional archive page showing all editions
- Landing page with clear call-to-action
- Navigation between landing, editions, and archive working

**Technical Considerations**:
- Archive should be statically generated for speed
- Consider grid layout for archive (masonry optional)
- Implement filtering by theme/date (future enhancement)

---

### Phase 6: Polish & Performance (Week 5-6)
**Goal**: Refine the experience and optimize for production

**Tasks**:
1. Performance audit (Lighthouse, Web Vitals)
2. Optimize fonts (subset, preload, font-display)
3. Implement loading states (skeleton screens)
4. Add micro-interactions (hover effects, transitions)
5. Cross-browser testing (Chrome, Safari, Firefox)
6. Mobile usability testing (real devices)
7. SEO optimization (sitemap, robots.txt, metadata)
8. Analytics setup (optional: privacy-focused like Plausible)

**Deliverables**:
- Lighthouse score 90+ across all metrics
- Smooth animations and transitions
- Site tested on iOS and Android
- SEO basics in place

**Technical Considerations**:
- Aim for <2s First Contentful Paint on mobile
- Use `loading="lazy"` for images below fold
- Minimize JavaScript bundle (check with `next build`)
- Implement proper caching headers

---

### Phase 7: Launch & Post-MVP Iteration (Ongoing)
**Goal**: Publish and gather feedback for improvements

**Tasks**:
1. Final production deployment
2. Share with initial audience (social, email)
3. Gather feedback on reading experience
4. Monitor analytics (if implemented)
5. Create edition #2 using the established workflow
6. Document content creation process for future editions

**Deliverables**:
- Live site accessible at production URL
- Edition #1 published and shared
- Feedback collected
- Workflow documented for creating new editions

**Technical Considerations**:
- Monitor error rates (Vercel analytics)
- Set up alerts for downtime
- Create content template for future editions
- Plan for experimental features (Phase 2 enhancements)

---

## 4. Technical Considerations Per Phase

### Phase 0 - Foundation
- **Next.js Version**: 14.1+ for latest App Router features
- **Node Version**: 18+ (check with `.nvmrc` file)
- **Package Manager**: pnpm (faster, more efficient) or npm
- **MDX Integration**: `@next/mdx` plugin or `next-mdx-remote` for more control
- **Deployment**: Vercel (native Next.js support, preview branches)

### Phase 1 - Layout
- **Animation Library**: Consider Framer Motion for complex animations (Phase 2), CSS-only for MVP
- **Font Strategy**: System fonts for speed (San Francisco, Segoe UI) or Google Fonts (subset)
- **Color System**: Define in `globals.css` as CSS custom properties for easy theming
- **Responsive Approach**: Mobile-first breakpoints (640px, 768px, 1024px)

### Phase 2 - Content Infrastructure
- **MDX Rendering**: Server-side rendering for SEO, client components where interactive
- **Content Validation**: Use Zod or similar to validate MDX frontmatter structure
- **File Organization**: Keep edition content isolated (makes moving to CMS easier later)
- **Caching Strategy**: Static generation for editions (ISR if content updates needed)

### Phase 3 - Components
- **Component Library**: Build custom components, avoid heavy UI libraries (maintain unique aesthetic)
- **Accessibility**: Use semantic HTML, ARIA labels, keyboard navigation
- **State Management**: React hooks (useState, useReducer) sufficient for MVP, no external state library needed
- **Image Handling**: `next/image` with blur placeholder for smooth loading

### Phase 4 - Content
- **Image Formats**: WebP for modern browsers, JPEG fallback (Next.js handles automatically)
- **Spotify Embeds**: Use official Spotify embed API, consider privacy implications (GDPR)
- **Content Length**: Test reading time on mobile, consider "estimated read time" indicator
- **Typography**: Ensure 1.5-1.6 line height for body text, comfortable reading on small screens

### Phase 5 - Archive
- **Data Source**: JSON file for MVP, could migrate to database if >20 editions
- **Sorting/Filtering**: Client-side for MVP (small dataset), server-side later
- **Thumbnails**: Auto-generate from edition content or custom per edition

### Phase 6 - Performance
- **Critical Metrics**:
  - First Contentful Paint: <1.5s
  - Largest Contentful Paint: <2.5s
  - Cumulative Layout Shift: <0.1
  - Time to Interactive: <3.5s
- **Bundle Size**: Keep JavaScript <100KB (gzipped)
- **Image Optimization**: Use responsive images, correct formats
- **Font Loading**: `font-display: swap` to prevent invisible text

### Phase 7 - Post-Launch
- **Monitoring**: Track Core Web Vitals, error rates
- **A/B Testing**: Test different layouts for engagement (future)
- **Feedback Loop**: Include subtle feedback mechanism (email, social, form)

---

## 5. MVP Feature Checklist

### Must-Have (MVP Requirements)

**Content & Structure**:
- [ ] Edition #1 fully written and published at `/1`
- [ ] All 4 sections rendered (Intro, Jai Sounds, Hybrid, Closing)
- [ ] Spotify playlist embedded and functional
- [ ] At least 2 AI-generated images in Hybrid section
- [ ] 1 Rabbit Hole content piece (expandable)

**Design & UX**:
- [ ] Mobile-first responsive design working perfectly
- [ ] Animated gradient background (subtle, 60fps)
- [ ] Custom typography system implemented (serif + sans)
- [ ] Navigation minimal and non-intrusive
- [ ] Footer with 88.8 FM frequency badge
- [ ] Color palette matches brand (earth tones + deep blue)
- [ ] Smooth scroll experience

**Technical**:
- [ ] Next.js 14 App Router functional
- [ ] TypeScript with strict mode, no errors
- [ ] MDX content loading and rendering correctly
- [ ] Dynamic routing for editions (`/[edition]`)
- [ ] Error handling for invalid routes
- [ ] Images optimized with next/image
- [ ] Metadata/SEO for social sharing

**Pages**:
- [ ] Landing page (`/`) with latest edition preview
- [ ] Edition page (`/1`) fully functional
- [ ] Archive page (`/archivo`) listing Edition #1
- [ ] 404 page for invalid editions

**Performance**:
- [ ] Lighthouse score 80+ (Mobile)
- [ ] Lighthouse score 90+ (Desktop)
- [ ] Page load <3s on 4G mobile
- [ ] No layout shift during load (CLS <0.1)

**Deployment**:
- [ ] Live on Vercel at production URL
- [ ] HTTPS enabled
- [ ] Custom domain configured (if applicable)
- [ ] Preview deployments working for new branches

### Nice-to-Have (Post-MVP)

**Content Enhancements**:
- [ ] Edition #2 published (validates workflow)
- [ ] "About" page explaining Curiana Radio philosophy
- [ ] Newsletter signup form (email collection)
- [ ] Rabbit Hole navigation to sub-pages (not just accordion)

**Design Enhancements**:
- [ ] Custom fonts (non-system) loaded optimally
- [ ] Advanced animations (Framer Motion)
- [ ] Dark mode support
- [ ] Reading progress indicator

**Technical Enhancements**:
- [ ] Generative backgrounds (Mandelbrot, noise patterns)
- [ ] Content search functionality
- [ ] RSS feed for new editions
- [ ] Sitemap auto-generation
- [ ] Analytics (privacy-focused)

**Interactive Features**:
- [ ] Social sharing buttons per section
- [ ] Comments or reactions (minimal)
- [ ] Audio version of content (text-to-speech or recorded)
- [ ] Language toggle (Spanish/English)

---

## 6. Best Practices & Recommendations

### 6.1 Content Workflow

**Creating New Editions**:
1. Duplicate previous edition folder (`/content/editions/02`)
2. Update `metadata.json` with new title, date, theme
3. Write content in MDX files (use template)
4. Add images to `assets/` folder
5. Test locally (`npm run dev`)
6. Create git branch (`edition-02`)
7. Deploy preview on Vercel
8. Review on mobile device
9. Merge to main, auto-deploy

**Content Templates**:
- Create a `/content/templates/` folder with boilerplate MDX files
- Each template includes structure hints and word count guides
- Speeds up writing process, ensures consistency

### 6.2 Code Quality

**TypeScript Practices**:
- Define strict types for all content structures
- Use discriminated unions for different section types
- Avoid `any` types, use `unknown` if uncertain
- Create utility types for common patterns

**Component Design**:
- Single Responsibility: One component, one job
- Composition over complexity: Combine small components
- Props interface for every component
- Document component purpose with JSDoc comments

**Performance**:
- Use Server Components by default, Client Components only when needed (interactivity)
- Implement code splitting for large components
- Lazy load content below the fold
- Optimize images aggressively

### 6.3 Version Control

**Git Workflow**:
- **Main branch**: Always production-ready
- **Feature branches**: `feature/rabbit-hole-component`
- **Edition branches**: `edition-02`, `edition-03`
- **Hotfix branches**: `hotfix/mobile-nav-bug`

**Commit Conventions**:
- Use conventional commits: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`
- Example: `feat: add RabbitHole accordion component`
- Example: `content: publish edition #1`

**Pull Requests**:
- Every edition goes through PR (preview deployment)
- Code review checklist: Performance, accessibility, mobile test
- Require Vercel preview link before merge

### 6.4 Design System

**Maintain Consistency**:
- Document design tokens (colors, fonts, spacing) in README
- Create a `/docs/design-system.md` file
- Screenshot each component for visual reference
- Update design system as project evolves

**Experimentation**:
- Each edition can have unique variations (backgrounds, layouts)
- Keep core identity consistent (typography, colors, frequency badge)
- Test experimental features on edition branches before merging patterns

### 6.5 Accessibility

**Checklist**:
- [ ] Semantic HTML (`<article>`, `<section>`, `<nav>`)
- [ ] Alt text for all images (descriptive, not decorative)
- [ ] Color contrast ratio 4.5:1 minimum (WCAG AA)
- [ ] Keyboard navigation (tab order, focus visible)
- [ ] Screen reader testing (VoiceOver, NVDA)
- [ ] Skip to content link for keyboard users
- [ ] ARIA labels where needed (modals, complex UI)

### 6.6 SEO

**On-Page SEO**:
- Unique title and description per edition
- Open Graph images (1200x630px) for social sharing
- Structured data (JSON-LD) for articles
- Canonical URLs for each edition
- Clean, descriptive URLs (`/1`, `/2`, not `/edition?id=1`)

**Technical SEO**:
- Sitemap.xml (auto-generated by Next.js)
- Robots.txt (allow all for public content)
- Fast page speed (Google ranking factor)
- Mobile-friendly (responsive design)

### 6.7 Performance Budget

**Limits**:
- JavaScript bundle: <150KB (gzipped)
- CSS bundle: <50KB (gzipped)
- Images per edition: <2MB total (optimized)
- Third-party scripts: Minimize (Spotify embed is essential)

**Monitoring**:
- Check Lighthouse before every edition publish
- Use Vercel Analytics to track Core Web Vitals
- Set up alerts if metrics degrade

### 6.8 Documentation

**Project Documentation**:
- **README.md**: Project overview, setup instructions, deployment
- **CONTRIBUTING.md**: How to add new editions, component guide
- **CHANGELOG.md**: Track major changes, new features
- **/docs/**: Detailed design system, architecture decisions

**Code Documentation**:
- Component README for complex components
- Inline comments for non-obvious logic
- TypeScript types serve as documentation (descriptive names)

---

## 7. Scalability Considerations

### 7.1 Content Scaling

**Handling 50+ Editions**:
- Current file-based approach works up to ~50 editions
- Beyond that, consider headless CMS (Sanity, Contentful)
- Archive pagination (show 20 editions per page)
- Search/filter functionality (by theme, date, keyword)

**Content Reuse**:
- Create component library for recurring patterns
- Build templates for common layouts
- Document style guide for writers

### 7.2 Technical Scaling

**Code Organization**:
- Monorepo setup if multiple projects emerge (Turborepo)
- Shared component library (`@curiana/ui`)
- Design tokens package (`@curiana/theme`)

**Performance at Scale**:
- Implement ISR (Incremental Static Regeneration) if content updates post-publish
- Use edge caching (Vercel Edge Network)
- Consider CDN for images (Cloudinary, Imgix)

**Feature Flags**:
- Use environment variables for experimental features
- Test new interactions on staging before production
- A/B test design variations (if analytics implemented)

### 7.3 Team Scaling

**Solo to Team**:
- Current structure supports solo development
- Adding collaborators: Clear component ownership
- Code review process (already suggested with PRs)
- Style guide for consistency across contributors

**Collaboration Tools**:
- Linear/GitHub Issues for task tracking
- Figma for design mockups (if designer joins)
- Notion for content planning and editorial calendar

---

## 8. Risk Mitigation

### 8.1 Potential Risks

**Risk: Content Creation Bottleneck**
- **Mitigation**: Create efficient templates, batch writing sessions, accept imperfection
- **Fallback**: Publish bi-monthly if monthly is unsustainable

**Risk: Performance Degradation with Rich Content**
- **Mitigation**: Strict performance budget, image optimization, lazy loading
- **Monitoring**: Lighthouse CI on every deploy

**Risk: Design Becoming Stale**
- **Mitigation**: Allow experimentation per edition, iterate on core components
- **Strategy**: Small improvements each edition, major redesign annually

**Risk: Technical Debt from Rapid Development**
- **Mitigation**: Refactor during "slow" months, schedule tech debt sprints
- **Prevention**: Code review, TypeScript strict mode, testing

**Risk: Mobile Experience Suffers**
- **Mitigation**: Mobile-first design, test on real devices, prioritize performance
- **Validation**: User feedback, analytics on mobile usage

### 8.2 Backup & Recovery

**Content Backup**:
- Git repository is primary backup
- Vercel automatically backs up deployments
- Export MDX to external storage monthly (Google Drive, Notion)

**Disaster Recovery**:
- Re-deploy from git in <10 minutes
- Domain transfer plan (if needed)
- Content can be migrated to different framework/platform (MDX is portable)

---

## 9. Success Metrics

### 9.1 MVP Success Criteria

**Launch Metrics** (30 days post-launch):
- [ ] Edition #1 published and accessible
- [ ] 100+ unique visitors
- [ ] Avg. session duration >2 minutes (indicates reading)
- [ ] <5% bounce rate on edition pages
- [ ] Mobile traffic >60% (validates mobile-first approach)

**Technical Metrics**:
- [ ] Lighthouse score maintained >85
- [ ] Zero critical bugs reported
- [ ] Page load time <3s on 4G

**Content Metrics**:
- [ ] Edition #2 published (validates workflow)
- [ ] Positive feedback from 5+ readers
- [ ] Social shares >20 (organic reach)

### 9.2 Long-term Goals (6-12 months)

**Audience Growth**:
- 500+ subscribers (if newsletter signup added)
- 1000+ monthly visitors
- Returning visitor rate >30%

**Content Output**:
- 6-12 editions published
- Consistent monthly/bi-monthly schedule
- 1-2 experimental features tested (generative backgrounds, interactive)

**Community**:
- Reader contributions (guest sections, playlists)
- Active engagement (comments, shares, feedback)
- Collaboration with other cultural projects

---

## 10. Next Steps After Planning

### Immediate Actions (After Plan Approval):

1. **Set up development environment**
   - Install Node.js, pnpm/npm, VS Code
   - Configure git and GitHub
   - Set up Vercel account

2. **Initialize project** (Phase 0)
   - Run `npx create-next-app@latest`
   - Configure TypeScript, Tailwind, ESLint
   - Create folder structure
   - Push to GitHub

3. **Start Phase 1** (Core Layout)
   - Build navigation component
   - Implement background animation
   - Define typography system
   - Test responsive layout

4. **Weekly Check-ins**
   - Review progress against phase goals
   - Adjust timeline if needed
   - Prioritize ruthlessly (MVP scope creep is real)

5. **Document decisions**
   - Keep a development log
   - Note what works, what doesn't
   - Build knowledge base for future editions

---

## 11. Open Questions & Decision Points

Before starting implementation, consider these questions:

### Content Strategy
1. **Edition Naming**: Stick with numbers (`#1`, `#2`) or add titles (`#1: Radio Silence`)?
2. **Rabbit Hole Implementation**: Accordion (simpler) or sub-pages (better for long content)?
3. **About Page**: Include in MVP or defer to post-launch?

### Design Decisions
4. **Custom Fonts**: Invest in premium fonts or use high-quality free alternatives (Google Fonts)?
5. **Background Variation**: Same gradient for all editions or unique per edition?
6. **Navigation Position**: Fixed header or integrated into content flow?

### Technical Choices
7. **MDX Library**: `@next/mdx` (official) or `next-mdx-remote` (more flexible)?
8. **Animation Library**: CSS-only for MVP or integrate Framer Motion immediately?
9. **Image Hosting**: Keep in repo (`/public`) or use external CDN (Cloudinary)?

### Workflow
10. **Content Editing**: Write MDX in code editor or use GUI tool (Markdown editor)?
11. **Preview Environment**: Separate staging branch or rely on Vercel preview deployments?
12. **Analytics**: Add from day one (Plausible, Fathom) or wait for more traffic?

### Future-Proofing
13. **CMS Migration Path**: Design content structure to easily migrate to CMS later?
14. **Multilingual Support**: Prepare architecture for Spanish/English toggle?
15. **Monetization**: Consider newsletter signup, Patreon integration, or keep fully open?

---

## Conclusion

Curiana Radio is a culturally significant project with clear technical requirements. The architecture proposed balances **simplicity** (MVP can launch quickly) with **scalability** (easy to grow and experiment).

**Key Success Factors**:
- **Content-first architecture**: Adding new editions is trivial
- **Performance-obsessed**: Mobile experience is premium
- **Flexible design system**: Experimentation encouraged
- **Type-safe codebase**: Fewer bugs, easier maintenance
- **Developer experience**: Solo dev can manage and evolve

The phased approach ensures steady progress without overwhelming scope. Each phase delivers tangible value and builds toward the complete vision.

**Curiana Radio is ready to broadcast. 📻 88.8 FM**

---

*This planning document is a living document. Update it as architectural decisions are made, new challenges emerge, and the project evolves.*
