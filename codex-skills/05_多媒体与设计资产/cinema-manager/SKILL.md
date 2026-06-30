---
name: cinema-manager
description: "个人影音库管理与搜索工具，支持根据分辨率/音轨/字幕排序筛选影视资源、自动转存夸克网盘、按 Plex/Infuse 标准重命名与分类归档。"
---

# Cinema Manager 🎬

Manage your personal movie and TV show library automatically. Search, quality-rank, download, and organize media files.

- **Project Homepage**: https://github.com/DavidBB-L/cinema-manager

## Installation

```bash
# Clone the repository
git clone https://github.com/DavidBB-L/cinema-manager.git

# Install dependencies
npm install -g cinema-manager
```

## Features

- **Multi-Source Search**: Search across multiple film and TV resource plugins.
- **Smart Quality Ranking**: Ranks search results automatically by checking:
  - Resolution (4K, 1080p, etc.)
  - Video Codec (HEVC/H.265, AVC/H.264)
  - Dynamic Range (HDR10, Dolby Vision, SDR)
  - Audio Quality (Dolby Atmos, TrueHD, DTS:X, 5.1)
  - Subtitles (Embedded, External Chinese subtitles)
- **Auto-Save to Quark Drive**: Auto-transfer matching resources directly to Quark (夸克网盘) cloud accounts.
- **Plex/Infuse Naming Convention**: Restructures media file directories and filenames automatically into standard formats:
  - Movies: `Movie Name (Year).ext`
  - TV Shows: `Show Name/Season XX/Show Name - SXXEXX.ext`
- **Genre Classification**: Automatic classification of downloaded files into folders based on movie genres.

## Usage Guide

### 1. Media Library Scan & Auto-Rename
```bash
cinema-manager organize --path "/path/to/my/downloads"
```

### 2. Film Resource Search & Quark Auto-save
```bash
cinema-manager search "The Matrix Resurrections" --save-to-quark
```
