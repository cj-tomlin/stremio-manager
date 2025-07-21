# Stremio Manager: Proposed Architecture

This document outlines the next-generation architecture for the Stremio Manager, designed to provide a more robust, flexible, and feature-rich streaming experience.

## Core Principles

- **Self-Hosting:** Prioritize self-hosting key components to improve reliability and control.
- **Modularity:** Use a modular, multi-addon approach to easily add or remove content sources.
- **Customization:** Build custom solutions for specific needs, such as live sports, to avoid unnecessary bloat.

## System Components

### 1. Add-on Manager: AIOstreams

- **Purpose:** Acts as the central hub for managing all other Stremio add-ons.
- **Implementation:** We will integrate AIOstreams to allow for dynamic configuration of other add-ons.
- **Link:** [AIOstreams](https://beta.stremio-addons.net/addons/aiostreams)

### 2. Primary Torrent Source: Comet (Self-Hosted)

- **Purpose:** Provides the primary source of movie and TV show torrents.
- **Implementation:** We will self-host a Comet instance, which scrapes from various sources, including Torrentio, for maximum content availability.
- **Link:** [Comet GitHub](https://github.com/g0ldyy/comet)

### 3. Live Sports: Custom daddylive Add-on

- **Purpose:** Delivers live sports streams without the overhead of a larger, multi-purpose add-on.
- **Implementation:** We will develop a new, lightweight Stremio add-on that scrapes live sports streams directly from daddylive.

### 4. Curated Lists: AIOLists

- **Purpose:** Enhances content discovery with a wide variety of curated movie and TV show lists.
- **Implementation:** We will integrate the AIOLists add-on.
- **Link:** [AIOLists GitHub](https://github.com/SebastianMorel/AIOLists)

### 5. Subtitles: OpenSubtitles

- **Purpose:** Provides subtitles for all content.
- **Implementation:** We will continue to use the reliable and popular OpenSubtitles add-on.
- **Link:** [OpenSubtitles](https://opensubtitlesv3-pro.dexter21767.com/configure/)

### 6. USA TV

- **Purpose:** Provides USA TV streams.
- **Implementation:** We will continue to use the reliable and popular USA TV add-on.
- **Link:** [USA TV](https://beta.stremio-addons.net/addons/usa-tv)

## User Experience Goal

The primary goal is to provide a seamless, one-click setup for end-users. After linking their Trakt account, a user will receive a single Stremio installation link. This link will configure AIOstreams with all the necessary add-ons (Comet, AIOLists, OpenSubtitles, etc.) pre-configured, requiring no further action from the user.

## Next Steps

1.  **Research & Planning:** Further investigate the technical requirements for self-hosting Comet and developing a custom Stremio add-on.
2.  **Implementation:** Begin the development work, starting with the integration of AIOstreams and the self-hosted Comet instance.
3.  **Deployment:** Update the Docker-based deployment to include the new self-hosted components.

## Useful Links
- [Stremio Addon Guide](https://guides.viren070.me/)
- [Stremio Addon Store](https://beta.stremio-addons.net/)