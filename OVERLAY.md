# VALORANT Rank Yoinker - Desktop Overlay Feature

## Overview

The desktop overlay feature provides a native, always-on-top window that displays VALORANT player information while you're in-game. This overlay is perfect for windowed fullscreen mode, allowing you to see rank, stats, and other player information without alt-tabbing.

## Features

- **Always-on-top transparent window** that displays over games
- **Hotkey toggle** (default: F9) to show/hide the overlay instantly
- **Draggable and repositionable** overlay window
- **Real-time updates** with the same data as the console application
- **Customizable transparency and positioning**
- **Automatic position saving** - overlay remembers where you moved it

## Requirements

- Python 3.7+ with tkinter support (usually included with Python)
- `keyboard` library for hotkey functionality (automatically installed)
- **Windows or Linux with GUI support** (macOS support may vary)

## Configuration

The overlay can be configured in your `config.json` file:

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

### Configuration Options

- `overlay_enabled`: Enable or disable the overlay feature
- `hotkey`: Key combination to toggle overlay visibility (default: "F9")
- `transparency`: Overlay transparency (0.0 = invisible, 1.0 = opaque)
- `x`, `y`: Initial overlay position on screen
- `width`, `height`: Overlay window dimensions

## Usage Instructions

1. **Start the application** as normal with `python main.py`
2. **Wait for overlay initialization** - you'll see a log message confirming overlay startup
3. **Press F9** (or your configured hotkey) to toggle the overlay on/off
4. **Drag the overlay** using the "≡≡≡ DRAG ≡≡≡" handle to reposition it
5. **The overlay automatically updates** with player information as you play

### In-Game Usage

The overlay works best with:
- **Windowed Fullscreen** VALORANT mode
- Games running in **windowed mode**
- **Borderless windowed** applications

### Controls

- **F9** (default): Toggle overlay visibility
- **Drag handle**: Move overlay to different position
- **Hide button**: Alternative way to hide overlay

## Display Information

The overlay shows the same information as the console application:

### For each player:
- **Name and Agent**
- **Current Rank and RR** (Rank Rating)
- **Player Level**
- **Headshot Percentage**
- **K/D Ratio**
- **Win Rate and Games Played**

### Match Information:
- **Game State** (In-Game, Agent Select, In-Menus)
- **Map and Mode** (when available)
- **Real-time updates** as match progresses

## Troubleshooting

### Overlay doesn't appear
- Check that tkinter is installed: `python -c "import tkinter; print('OK')"`
- Verify you have a GUI environment (not running in headless mode)
- Check logs for error messages about display availability

### Hotkey not working
- Ensure no other application is using the same hotkey
- Try changing the hotkey in config.json
- Check that the `keyboard` library is installed properly

### Overlay appears behind game
- Make sure you're using **windowed fullscreen** mode in VALORANT
- Try pressing the hotkey twice to refresh the overlay's "always on top" status
- Some exclusive fullscreen games may not support overlays

### Performance Impact
- The overlay is designed to be lightweight
- If you experience performance issues, try:
  - Increasing transparency (making overlay more transparent)
  - Reducing overlay size
  - Disabling overlay when not needed

## Customization

You can modify the overlay appearance by editing `src/overlay.py`:

- **Colors**: Change the color scheme in `_create_overlay_window()`
- **Font sizes**: Modify font specifications in player widget creation
- **Layout**: Adjust widget positioning and sizing
- **Data display**: Customize what information is shown

## Known Limitations

- **Exclusive fullscreen mode**: May not work with some exclusive fullscreen applications
- **Linux display managers**: Some window managers may handle "always on top" differently
- **Multiple monitors**: Overlay position is based on primary monitor coordinates
- **High DPI displays**: May require manual positioning adjustments

## Technical Details

The overlay uses:
- **tkinter** for the GUI framework (cross-platform, built into Python)
- **keyboard** library for global hotkey detection
- **Threading** to run overlay independently of main application
- **JSON configuration** for persistent settings

The overlay runs in a separate thread and communicates with the main application through shared data structures, ensuring minimal performance impact on the core VALORANT data collection functionality.