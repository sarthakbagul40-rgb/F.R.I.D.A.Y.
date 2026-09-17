---
name: diagram-design
description: Editorial system architecture and workflow diagrams in self-contained HTML + SVG. Kills Mermaid slop.
---

# Diagram Design (Editorial HTML + SVG)

Editorial diagrams that designers and engineers appreciate. High contrast, crisp SVG geometry, balanced hierarchy, and zero Mermaid syntax errors.

## Core Principles
1. **Zero Mermaid Slop**: Never output raw Mermaid syntax. Output self-contained, inline SVG within clean dark-mode HTML that can be opened in any browser or displayed in F.R.I.D.A.Y.'s HUD.
2. **Typography & Hierarchy**: Use system fonts (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`) with explicit font weights (600 for headers, 400 for subtext).
3. **Curated Color Tokens**:
   - Background: Dark slate `#0a0b10` or translucent `#121520`.
   - Card Surfaces: `#1a1f2e` with subtle borders `#2b354f`.
   - Primary Accent: Stark Cyan `#00f2fe` or Cyber Indigo `#6366f1`.
   - Secondary Accent: Electric Emerald `#10b981` or Warm Coral `#f43f5e`.
   - Text Primary: `#f8fafc`.
   - Text Secondary: `#94a3b8`.
4. **Target Density**: Clean, spaced, uncluttered layout. Target visual density: 4/10.

## Supported Layout Types
- **Architecture Flow**: Box-and-connector data pipelines with directional arrows.
- **The Self-Improving Loop**: Circular flywheel diagrams with return feedback loops.
- **Microservice Swarm**: Central orchestrator with radiating subagent nodes.
- **Database Schema**: Entity attribute tables with PK/FK indicator badges.
- **State Machine**: State pill nodes with labelled transition edges.
