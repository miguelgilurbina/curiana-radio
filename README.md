# Curiana Radio 📻

**88.8 FM - Transmisión Cultural desde Abya Yala**

A monthly newsletter experience delivered as immersive web pages. Each edition is a standalone journey combining curated music, experimental narrative, AI-generated visuals, and reflections on technology and culture.

---

## Project Status

**Current Phase**: Planning Complete ✅
**Next Phase**: Foundation Setup (Week 1)
**Launch Target**: TBD (6-week development cycle)

---

## Quick Links

- **[Project Plan](./PROJECT_PLAN.md)** - Complete architecture, phases, and implementation details
- **[Questions & Feedback](./QUESTIONS_AND_FEEDBACK.md)** - Critical decisions and next steps
- **[Expert Agents](./.claude/README.md)** - Specialized Claude agents for development assistance

---

## What is Curiana Radio?

Curiana Radio is not a traditional website. It's an **experience per visit**.

Each monthly edition explores a theme through:
- 🎵 **Jai Sounds**: Curated music with deep-dive reviews
- 📖 **Hybrid Narratives**: Experimental storytelling + AI exploration
- 🤔 **Reflections**: Technology, identity, and cultural transformation
- 🎨 **Visual Experiences**: AI-generated art, immersive design

### Philosophy

Rooted in Caquetío heritage and Abya Yala wisdom, Curiana Radio explores the intersection of:
- Ancestral knowledge and technological futures
- Music as transformational medium
- AI as tool for personal/spiritual exploration
- Fluid, multidimensional identity

**It's like tuning into a special frequency from another place and time.**

---

## Technical Overview

### Stack (Planned)

- **Framework**: Next.js 14+ (App Router)
- **Content**: MDX (Markdown + JSX)
- **Styling**: Tailwind CSS + CSS Modules
- **Language**: TypeScript (strict mode)
- **Deployment**: Vercel
- **Version Control**: Git + GitHub

### Architecture Highlights

- **File-based routing**: Each edition at `/1`, `/2`, `/3`...
- **Static generation**: Fast, SEO-friendly pages
- **Mobile-first**: Optimized for small screens
- **Performance budget**: <100KB JS, <2s load time
- **Modular components**: Reusable sections for rapid edition creation

---

## Project Structure (Planned)

```
curiana-radio/
├── .claude/                  # Expert agents for development
├── content/
│   └── editions/
│       ├── 01/               # Edition #1 content
│       ├── 02/               # Edition #2 content
│       └── ...
├── src/
│   ├── app/                  # Next.js App Router
│   ├── components/           # React components
│   ├── lib/                  # Utilities
│   ├── types/                # TypeScript definitions
│   └── styles/               # CSS Modules & theme
├── public/                   # Static assets
├── PROJECT_PLAN.md           # Detailed planning document
└── QUESTIONS_AND_FEEDBACK.md # Decision points
```

---

## Expert Agent System

This project includes 5 specialized Claude agents to assist with development:

- `/nextjs-expert` - Next.js & App Router specialist
- `/ui-expert` - CSS/Tailwind/Design implementation
- `/github-expert` - Git workflow & deployment
- `/architecture-expert` - System design & structure
- `/typescript-expert` - Type safety & TS patterns

See [.claude/README.md](./.claude/README.md) for details.

---

## Development Phases

### Phase 0: Foundation (Week 1)
Project initialization, tooling setup, base configuration

### Phase 1: Core Layout (Week 2)
Navigation, footer, background, typography system

### Phase 2: Content Infrastructure (Week 2-3)
MDX rendering, dynamic routing, content loading

### Phase 3: Section Components (Week 3-4)
Intro, Jai Sounds, Hybrid, Closing sections

### Phase 4: Edition #1 (Week 4)
First complete edition with real content

### Phase 5: Archive & Landing (Week 5)
Archive page, landing page, navigation

### Phase 6: Polish & Performance (Week 5-6)
Optimization, testing, final touches

### Phase 7: Launch (Week 6+)
Deploy and iterate based on feedback

Full details in [PROJECT_PLAN.md](./PROJECT_PLAN.md)

---

## Design Principles

1. **Viewport as Canvas**: Full-screen, immersive experiences
2. **Mobile-First**: Optimized for small screens
3. **Content is King**: Design serves the reading experience
4. **Performance Matters**: Fast loading, smooth animations
5. **Experimental Spirit**: Room for creative exploration
6. **Accessible**: Keyboard navigation, screen readers, contrast

### Visual Identity

- **Colors**: Earth tones (sand, rust) + deep blue
- **Typography**: Serif for body + sans for UI
- **Spacing**: Generous, breathing room
- **Mood**: Mystical-technological, minimalist but rich
- **Icon**: 88.8 FM frequency badge

---

## Getting Started (After Setup)

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

---

## Content Creation Workflow (Future)

1. Duplicate previous edition folder
2. Update metadata.json
3. Write content in MDX files
4. Add images to assets/
5. Test locally
6. Create git branch
7. Deploy preview on Vercel
8. Review and merge

---

## Next Steps

1. **Review** [QUESTIONS_AND_FEEDBACK.md](./QUESTIONS_AND_FEEDBACK.md)
2. **Answer critical questions** (Q1, Q4, Q7, Q13, Q15)
3. **Approve project plan** or suggest adjustments
4. **Begin Phase 0** (Foundation Setup)

---

## Contributing

Currently a solo project. Contribution guidelines will be added as the project evolves.

---

## License

TBD (To be determined based on cultural and creative considerations)

---

## Contact

Project by Miguel Gil Urbina
For inquiries about Curiana Radio: [Contact info TBD]

---

**Curiana Radio - 88.8 FM**
*Sintoniza la frecuencia. Tune in to the frequency.*

---

*This README will be updated as the project progresses.*
