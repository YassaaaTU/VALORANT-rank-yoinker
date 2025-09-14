# Overlay Configuration Guide

## Quick Setup

The overlay works out of the box with sensible defaults. After running the app once, you can customize these settings in your `config.json` file:

```json
{
  "flags": {
    "overlay_enabled": true
  },
  "overlay": {
    "hotkey": "F9",
    "transparency": 0.9,
    "x": 100,
    "y": 100, 
    "width": 600,
    "height": 400
  }
}
```

## Configuration Options

### Basic Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `overlay_enabled` | `true` | Enable/disable the overlay feature entirely |
| `hotkey` | `"F9"` | Key to toggle overlay visibility |
| `transparency` | `0.9` | Overlay transparency (0.0 = invisible, 1.0 = opaque) |

### Position & Size

| Setting | Default | Description |
|---------|---------|-------------|
| `x` | `100` | Horizontal position on screen (pixels from left) |
| `y` | `100` | Vertical position on screen (pixels from top) |
| `width` | `600` | Overlay window width in pixels |
| `height` | `400` | Overlay window height in pixels |

## Customization Examples

### Different Hotkeys
```json
"overlay": {
  "hotkey": "F10",        // F10 key
  "hotkey": "ctrl+shift+o" // Ctrl+Shift+O combination
}
```

### More/Less Transparent
```json
"overlay": {
  "transparency": 0.7,    // More transparent (subtle)
  "transparency": 0.95    // Less transparent (more visible)
}
```

### Different Positions
```json
"overlay": {
  "x": 50,     // Close to left edge
  "y": 50,     // Close to top edge
  "width": 800, // Wider overlay
  "height": 300 // Shorter overlay
}
```

### Corner Positions
```json
// Top-right corner (approximate for 1920x1080)
"overlay": {
  "x": 1300,
  "y": 50,
  "width": 600,
  "height": 400
}

// Bottom-left corner
"overlay": {
  "x": 50,
  "y": 650,
  "width": 600, 
  "height": 400
}
```

## Multi-Monitor Setup

For multi-monitor setups, you can position the overlay on different screens:

```json
// Second monitor (approximate for dual 1920x1080 setup)
"overlay": {
  "x": 2020,  // Past the first monitor's width
  "y": 100,
  "width": 600,
  "height": 400
}
```

## Gaming-Optimized Settings

### Minimal Impact Setup
```json
"overlay": {
  "hotkey": "F9",
  "transparency": 0.75,   // Very subtle
  "x": 50,                // Out of main game area  
  "y": 50,
  "width": 500,           // Compact size
  "height": 350
}
```

### High Visibility Setup
```json
"overlay": {
  "hotkey": "F9", 
  "transparency": 0.95,   // Very visible
  "x": 100,
  "y": 100,
  "width": 700,           // Large size
  "height": 500
}
```

## Troubleshooting Configurations

### Overlay appears off-screen
Reset position to default:
```json
"overlay": {
  "x": 100,
  "y": 100
}
```

### Overlay too small/large for your resolution
Adjust based on your screen size:
```json
// For 1440p (2560x1440)
"overlay": {
  "width": 800,
  "height": 500
}

// For 4K (3840x2160) 
"overlay": {
  "width": 1000,
  "height": 600
}
```

### Hotkey conflicts with other software
Try different keys:
```json
"overlay": {
  "hotkey": "F11",        // Less commonly used
  "hotkey": "ctrl+alt+v", // More complex combination
  "hotkey": "end"         // Single key alternative
}
```

## Tips

1. **Start with defaults** - The default settings work well for most users
2. **Test positioning** - Use the drag handle to find your preferred position first
3. **Save automatically** - The overlay remembers where you move it
4. **Game-specific** - You might want different positions for different games
5. **Performance** - Lower transparency values may improve performance on older systems

## Advanced Users

You can also modify the overlay appearance by editing `src/overlay.py` directly:
- Change colors and themes
- Modify fonts and sizes  
- Adjust layout and spacing
- Add custom information displays