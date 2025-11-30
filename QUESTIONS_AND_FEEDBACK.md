# Clarifying Questions & Feedback

## What I've Set Up

1. **GitHub Repository**: Cloned `curiana-radio` (currently empty)
2. **Expert Agent System**: Created 5 specialized agents in `.claude/commands/`:
   - `/nextjs-expert` - Next.js & App Router specialist
   - `/ui-expert` - CSS/Tailwind/Design specialist
   - `/github-expert` - Git workflow & deployment
   - `/architecture-expert` - System design & structure
   - `/typescript-expert` - Type safety & TS patterns
3. **Comprehensive Planning Document**: `PROJECT_PLAN.md` with full architecture, phases, and best practices

---

## Critical Questions (Please Answer Before We Start Coding)

### 1. Content & Structure

**Q1: Edition Naming Convention**
- **Option A**: Pure numbers (`#1`, `#2`, `#3`)
- **Option B**: Numbers + Titles (`#1: Radio Silence`, `#2: Digital Frequencies`)
- **Impact**: Affects SEO, social sharing, and archive presentation
- **My Recommendation**: Option B (more context for sharing, better SEO)

**Q2: Rabbit Hole Implementation**
- **Option A**: Accordion/collapsible (stays on same page, simpler)
- **Option B**: Sub-pages (e.g., `/1/sounds-deep-dive`, better for long content)
- **Impact**: Development complexity vs. user experience
- **My Recommendation**: Start with Option A for MVP, migrate to B if content is >500 words

**Q3: About Page in MVP?**
- Should we include `/sobre` (About) page in the initial launch?
- **Impact**: Scope of MVP, helpful for first-time visitors
- **My Recommendation**: Yes, but keep it minimal (200-300 words)

---

### 2. Design Decisions

**Q4: Typography - Custom Fonts?**
- **Option A**: System fonts (fastest, no loading time)
  - Serif: Georgia, Times New Roman
  - Sans: SF Pro (iOS), Segoe UI (Windows)
- **Option B**: Google Fonts (good quality, free)
  - Serif: Crimson Text, Lora, Merriweather
  - Sans: Inter, Work Sans, DM Sans
- **Option C**: Premium fonts (highest quality, cost)
  - Services: Adobe Fonts, fonts.com
- **Impact**: Performance (loading time) vs. aesthetic uniqueness
- **My Recommendation**: Option B (Google Fonts) - Lora (serif) + Inter (sans) with font subsetting

**Q5: Background Variation Per Edition**
- **Option A**: Same animated gradient for all editions (consistent brand)
- **Option B**: Unique gradient colors per edition (within brand palette)
- **Option C**: Completely different backgrounds per edition (max experimentation)
- **Impact**: Brand consistency vs. creative freedom
- **My Recommendation**: Option B (variations within earth/blue palette)

**Q6: Navigation Behavior on Mobile**
- **Option A**: Always visible (fixed header)
- **Option B**: Auto-hide on scroll down, show on scroll up
- **Option C**: Integrated into content (no fixed nav)
- **Impact**: Screen real estate vs. accessibility
- **My Recommendation**: Option B (auto-hide, common pattern in immersive experiences)

---

### 3. Technical Choices

**Q7: MDX Integration**
- **Option A**: `@next/mdx` (official Next.js plugin, simpler setup)
- **Option B**: `next-mdx-remote` (more flexible, remote content support)
- **Impact**: Ease of setup vs. future flexibility (CMS migration)
- **My Recommendation**: Option B (easier to migrate to CMS later, better separation of content/code)

**Q8: Animation Strategy**
- **Option A**: CSS-only animations (lightweight, no dependencies)
- **Option B**: Framer Motion (powerful, smoother animations, +30KB bundle)
- **Impact**: Bundle size vs. animation quality
- **My Recommendation**:
  - MVP: CSS-only for backgrounds, simple transitions
  - Post-MVP: Add Framer Motion for advanced interactions

**Q9: Image Hosting**
- **Option A**: Store in `/public` folder (simple, all in repo)
- **Option B**: External CDN (Cloudinary, Imgix - better performance, transformations)
- **Impact**: Simplicity vs. performance & features
- **My Recommendation**:
  - MVP: Option A (keep it simple)
  - Post-MVP: Option B if images exceed 50MB total

**Q10: Analytics from Day One?**
- **Option A**: No analytics (privacy-first, one less thing to set up)
- **Option B**: Privacy-focused analytics (Plausible, Fathom - $9-14/month)
- **Option C**: Google Analytics (free, but privacy concerns)
- **Impact**: Data-driven decisions vs. simplicity & privacy
- **My Recommendation**: Option B (Plausible) - knowing reader behavior helps improve experience

---

### 4. Content Workflow

**Q11: Edition Content Editing**
- **Option A**: Write MDX directly in VS Code / code editor
- **Option B**: Use Markdown-friendly editor (Obsidian, Notion, then copy)
- **Option C**: Set up GUI content editor (Tina CMS, Sanity Studio)
- **Impact**: Learning curve vs. writing comfort
- **My Recommendation**:
  - MVP: Option A (direct MDX editing)
  - Provide templates with clear comments
  - Option C if non-technical collaborators join

**Q12: Content Review Process**
- **Option A**: Edit directly on main branch (fastest, solo workflow)
- **Option B**: Create branch → Vercel preview → review → merge (safer, collaborative)
- **Impact**: Speed vs. safety & review process
- **My Recommendation**: Option B (even solo, good habit, prevents mistakes going live)

---

### 5. Scope & Timeline

**Q13: MVP Definition**
- **Minimal MVP**: Edition #1 + basic archive + landing
- **Complete MVP**: Edition #1 + Edition #2 + archive + about + newsletter signup
- **Which do you prefer?**
- **My Recommendation**: Minimal MVP first, then add Edition #2 within 2 weeks (validates workflow)

**Q14: Timeline Expectations**
- Based on the 7-phase plan (6 weeks total):
  - **Phase 0-2** (Weeks 1-3): Foundation, layout, content infrastructure
  - **Phase 3-4** (Weeks 3-4): Components + Edition #1 content
  - **Phase 5-6** (Weeks 5-6): Archive, polish, performance
- **Is this timeline realistic for your availability?**
- **Should we compress or extend?**

**Q15: Development Mode**
- **Option A**: I code everything end-to-end (you review and provide feedback)
- **Option B**: We pair on critical decisions, I implement based on your input
- **Option C**: You want to code alongside me (I guide and assist)
- **Which mode works best for you?**

---

## Feedback & Observations

### Strengths of Your Vision

1. **Clear Conceptual Identity**: "Tuning into a frequency" is a powerful metaphor that guides design decisions
2. **Content-First Approach**: Prioritizing the reading experience over flashy features is wise
3. **Cultural Significance**: Grounding in Caquetío heritage gives the project depth and purpose
4. **Scalable Simplicity**: Starting with file-based content is pragmatic, allows for CMS migration later
5. **Experimental Spirit**: Building in room for experimentation (backgrounds, interactions) keeps it fresh

### Potential Challenges & How to Address

1. **Challenge: Balancing "Experimental" with "Readable"**
   - **Risk**: Design might overpower content
   - **Solution**: Establish hierarchy early - content is always primary, design serves the story
   - **Test**: If background/animations distract from reading, dial them back

2. **Challenge: Performance with Rich Media**
   - **Risk**: AI images, Spotify embeds, animations could slow mobile experience
   - **Solution**: Strict performance budget (outlined in plan), lazy loading, optimization
   - **Test**: Real device testing on 4G network, Lighthouse scores >85

3. **Challenge: Content Creation Velocity**
   - **Risk**: Monthly schedule might be hard to sustain with quality content
   - **Solution**:
     - Build efficient templates
     - Allow shorter editions if needed (not every piece needs 1400 words)
     - Consider bi-monthly if monthly becomes unsustainable
   - **Philosophy**: Better to publish 6 great editions/year than 12 mediocre ones

4. **Challenge: Scope Creep**
   - **Risk**: Excitement about features (generative backgrounds, audio, interactivity) delays launch
   - **Solution**: Ruthless MVP prioritization
     - Phase 1: Beautiful, functional reading experience
     - Phase 2: Experimental features (post-launch)
   - **Reminder**: Done and published > perfect but unreleased

5. **Challenge: Solo Maintenance**
   - **Risk**: Code becomes hard to maintain as project grows
   - **Solution**:
     - TypeScript strict mode (catches errors early)
     - Clear folder structure (easy to navigate months later)
     - Document architectural decisions (future you will thank present you)
     - Component-based architecture (easy to update/replace)

### Suggestions for Enhancement (Post-MVP)

1. **Audio Experience**: Since it's "radio", consider:
   - Ambient background sounds (optional, user-controlled)
   - Narrated versions of essays
   - Audio snippets from track reviews

2. **Interactive Timeline**:
   - Visual timeline of all editions
   - Filter by theme, mood, musical genre
   - "Radio dial" metaphor for browsing

3. **Community Features**:
   - Reader playlists (submissions)
   - Collaborative editions (guest curators)
   - Discussion spaces (respectful, curated)

4. **Cross-Medium Integration**:
   - Instagram snippets from editions
   - Short video teasers
   - Physical zine versions (print-on-demand)

5. **Personalization** (Advanced):
   - Remember reading position
   - Save favorite editions
   - Custom color themes (within brand palette)

---

## Recommended Next Steps (After You Answer Questions)

### Immediate (This Week)
1. **Review & answer** the 15 questions above
2. **Approve or adjust** the project plan
3. **I initialize the Next.js project** (Phase 0)
4. **Set up Vercel** deployment pipeline
5. **Configure Tailwind** with your color palette

### Week 1-2 (Foundation + Layout)
6. **Build core layout** (navigation, footer, background)
7. **Define typography system** (based on your font choice)
8. **Create component templates**
9. **Test responsive design** on your devices

### Week 3-4 (Content Infrastructure + Edition #1)
10. **Build MDX rendering system**
11. **Create section components**
12. **You write Edition #1 content** (while I build components)
13. **Integrate Spotify playlist**
14. **Add AI-generated images**

### Week 5-6 (Polish + Launch)
15. **Build archive page**
16. **Performance optimization**
17. **Mobile device testing** (your phone, tablet)
18. **Final review & launch** 🚀

---

## Questions for You

1. **Which of the 15 questions above are most critical to answer now?**
2. **Are there any design decisions you've already made that I should know?**
3. **Do you have existing content (Edition #1 draft) or will we develop it alongside the site?**
4. **What's your preferred communication style during development?**
   - Frequent check-ins (daily updates)?
   - Milestone reviews (weekly)?
   - Async updates (I work, share progress, you review when available)?
5. **Any hard deadlines or launch targets?**
6. **Budget considerations?** (e.g., premium fonts, analytics tools, CDN services)

---

## How to Use This Document

1. **Read through all questions** (I know it's long, but each is important)
2. **Answer the ones marked "Critical"** (Q1, Q4, Q7, Q13, Q15)
3. **Provide gut reactions** to others (we can refine later)
4. **Share any additional context** I might have missed
5. **Once you respond**, I'll update the plan and we can start Phase 0

---

## Final Thoughts

Your vision for Curiana Radio is compelling and feasible. The project sits at a beautiful intersection of:
- **Cultural preservation** (Caquetío heritage, ancestral wisdom)
- **Technological exploration** (AI, generative art, web experiences)
- **Artistic expression** (music curation, narrative, design)

The technical architecture I've proposed supports this vision while keeping complexity manageable. We're building a platform for long-term creative exploration, not just a one-off website.

**Most important**: We can always iterate. MVP is about getting a beautiful, functional version live. Everything else can evolve based on how you use it and what resonates with readers.

Let's make Curiana Radio a reality. 📻✨

---

**Ready when you are. Let me know your answers and we'll start building.**
