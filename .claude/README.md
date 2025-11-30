# Curiana Radio - Claude Expert Agents

This folder contains specialized expert agents to help with different aspects of the Curiana Radio project.

## Available Agents

Invoke these agents in your Claude Code conversation using slash commands:

### `/nextjs-expert`
Next.js 14+ specialist for App Router, Server Components, routing, and performance optimization.
- Use for: Routing decisions, component architecture, data fetching, build optimization

### `/ui-expert`
CSS/Tailwind/Design implementation specialist for visual aesthetics and responsive design.
- Use for: Layout implementation, styling decisions, animations, responsive design, accessibility

### `/github-expert`
Git workflow and GitHub management specialist for version control and deployment.
- Use for: Commit strategies, branching, CI/CD setup, deployment configuration

### `/architecture-expert`
Software architecture specialist for system design and scalable project structure.
- Use for: File organization, component boundaries, content modeling, architectural decisions

### `/typescript-expert`
TypeScript specialist for type-safe development and modern TS patterns.
- Use for: Type definitions, type safety patterns, configuration, error handling

## How to Use

1. **Single Agent**: `/nextjs-expert` - Invokes Next.js expert context
2. **Chain Agents**: Get architectural advice first, then implementation details
3. **Specific Questions**: Ask targeted questions after invoking the relevant expert

## Example Workflow

```
You: /architecture-expert
You: How should I structure the content for different editions?

[Get architectural guidance]

You: /nextjs-expert
You: Based on that architecture, what's the best routing pattern?

[Get Next.js implementation details]

You: /typescript-expert
You: What types should I define for the edition content?

[Get type definitions]
```

## Agent Philosophy

Each agent is contextually aware of:
- The Curiana Radio project vision and aesthetics
- Mobile-first, performance-oriented approach
- Content-driven architecture needs
- Balance between simplicity and expressiveness

Use these agents to get expert guidance without losing project context.
