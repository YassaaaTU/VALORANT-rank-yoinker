try:
    import tkinter as tk
    from tkinter import ttk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    # Create dummy classes for when tkinter is not available
    class tk:
        class Tk: pass
        class Frame: pass
        class Label: pass
        class Button: pass
        class Canvas: pass
        BOTH = RAISED = X = BOTTOM = LEFT = RIGHT = TOP = None
    class ttk:
        class Scrollbar: pass

import threading
import time
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
import json
from typing import Dict, List, Any, Optional


class GameOverlay:
    """Native desktop overlay for VALORANT rank yoinker"""
    
    def __init__(self, log_function, config):
        self.log = log_function
        self.config = config
        self.root = None
        self.is_visible = False
        self.overlay_data = {}
        self.hotkey = self.config.get_overlay_setting("hotkey")
        self.transparency = self.config.get_overlay_setting("transparency")
        self.position_x = self.config.get_overlay_setting("x")
        self.position_y = self.config.get_overlay_setting("y")
        self.width = self.config.get_overlay_setting("width")
        self.height = self.config.get_overlay_setting("height")
        self._overlay_thread = None
        self._running = False
        
    def initialize(self):
        """Initialize the overlay in a separate thread"""
        if not TKINTER_AVAILABLE:
            self.log("tkinter not available - overlay disabled")
            return False
            
        if not KEYBOARD_AVAILABLE:
            self.log("keyboard library not available - overlay hotkey disabled")
            
        self._running = True
        
        # Check if we have a display available
        try:
            test_root = tk.Tk()
            test_root.withdraw()
            test_root.destroy()
        except tk.TclError as e:
            if "no display" in str(e).lower():
                self.log("No display available - overlay disabled")
                return False
            else:
                self.log(f"Display check failed: {e}")
                return False
        except Exception as e:
            self.log(f"Failed to check display availability: {e}")
            return False
            
        self._overlay_thread = threading.Thread(target=self._create_overlay_window, daemon=True)
        self._overlay_thread.start()
        
        # Set up global hotkey for toggling overlay
        if KEYBOARD_AVAILABLE:
            try:
                keyboard.add_hotkey(self.hotkey, self.toggle_visibility)
                self.log(f"Overlay hotkey set to: {self.hotkey}")
            except Exception as e:
                self.log(f"Failed to set hotkey {self.hotkey}: {e}")
        else:
            self.log("Keyboard library not available - hotkey disabled")
            
        return True
            
    def _create_overlay_window(self):
        """Create the main overlay window"""
        self.root = tk.Tk()
        self.root.title("VALORANT Overlay")
        
        # Configure window properties for overlay
        self.root.geometry(f"{self.width}x{self.height}+{self.position_x}+{self.position_y}")
        self.root.attributes("-topmost", True)  # Always on top
        self.root.attributes("-alpha", self.transparency)  # Transparency
        self.root.overrideredirect(True)  # Remove window decorations
        
        # Make window background dark with slight transparency
        self.root.configure(bg='#1a1a1a')
        
        # Create main frame with scrollable content
        self.main_frame = tk.Frame(self.root, bg='#1a1a1a')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title label
        self.title_label = tk.Label(
            self.main_frame, 
            text="VALORANT Rank Yoinker - No Data", 
            font=("Arial", 12, "bold"),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        self.title_label.pack(pady=(0, 10))
        
        # Create scrollable frame for player data
        self.create_scrollable_frame()
        
        # Control buttons frame
        self.controls_frame = tk.Frame(self.main_frame, bg='#1a1a1a')
        self.controls_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        # Toggle button
        self.toggle_btn = tk.Button(
            self.controls_frame,
            text=f"Hide ({self.hotkey})",
            command=self.toggle_visibility,
            bg='#333333',
            fg='#ffffff',
            font=("Arial", 8)
        )
        self.toggle_btn.pack(side=tk.LEFT)
        
        # Move handle (for repositioning)
        self.move_handle = tk.Label(
            self.controls_frame,
            text="≡≡≡ DRAG ≡≡≡",
            bg='#444444',
            fg='#ffffff',
            font=("Arial", 8)
        )
        self.move_handle.pack(side=tk.RIGHT)
        
        # Bind drag functionality
        self.move_handle.bind("<Button-1>", self._start_move)
        self.move_handle.bind("<B1-Motion>", self._do_move)
        self.move_handle.bind("<ButtonRelease-1>", self._stop_move)
        
        # Initially hide the overlay
        self.root.withdraw()
        
        # Start the tkinter main loop
        self.root.mainloop()
        
    def create_scrollable_frame(self):
        """Create a scrollable frame for player data"""
        # Canvas and scrollbar for scrolling
        canvas = tk.Canvas(self.main_frame, bg='#1a1a1a', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        
        self.scrollable_frame = tk.Frame(canvas, bg='#1a1a1a')
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def _start_move(self, event):
        """Start moving the overlay window"""
        self._move_start_x = event.x_root
        self._move_start_y = event.y_root
        
    def _do_move(self, event):
        """Move the overlay window"""
        x = self.root.winfo_x() + (event.x_root - self._move_start_x)
        y = self.root.winfo_y() + (event.y_root - self._move_start_y)
        self.root.geometry(f"+{x}+{y}")
        self._move_start_x = event.x_root
        self._move_start_y = event.y_root
        
    def _stop_move(self, event):
        """Stop moving and save position"""
        self.position_x = self.root.winfo_x()
        self.position_y = self.root.winfo_y()
        # Save position to config if possible
        self._save_position()
        
    def _save_position(self):
        """Save overlay position to config"""
        try:
            # Try to update config file if it exists
            try:
                with open("config.json", "r") as f:
                    config = json.load(f)
                    
                if "overlay" not in config:
                    config["overlay"] = {}
                    
                config["overlay"].update({
                    "x": self.position_x,
                    "y": self.position_y
                })
                
                with open("config.json", "w") as f:
                    json.dump(config, f, indent=4)
                    
            except (FileNotFoundError, json.JSONDecodeError):
                pass  # Config file doesn't exist or is invalid
                
        except Exception as e:
            self.log(f"Failed to save overlay position: {e}")
    
    def toggle_visibility(self):
        """Toggle overlay visibility"""
        if not self.root:
            return
            
        if self.is_visible:
            self.root.withdraw()
            self.is_visible = False
            self.log("Overlay hidden")
        else:
            self.root.deiconify()
            self.root.attributes("-topmost", True)  # Ensure it stays on top
            self.is_visible = True
            self.log("Overlay shown")
            
    def update_data(self, game_state: str, players_data: Dict[str, Any], match_info: Optional[Dict] = None):
        """Update overlay with new player data"""
        if not self.root or not self._running:
            return
            
        self.overlay_data = {
            "game_state": game_state,
            "players": players_data,
            "match_info": match_info or {}
        }
        
        # Update UI in main thread
        self.root.after(0, self._update_ui)
        
    def _update_ui(self):
        """Update the UI with current data"""
        if not self.overlay_data:
            return
            
        # Update title
        game_state = self.overlay_data.get("game_state", "UNKNOWN")
        state_colors = {
            "INGAME": "#ff4444",
            "PREGAME": "#44ff44", 
            "MENUS": "#ffff44"
        }
        
        title_text = f"VALORANT - {game_state}"
        self.title_label.config(text=title_text)
        
        # Clear existing player widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        # Display player data
        players = self.overlay_data.get("players", {})
        
        if not players:
            no_data_label = tk.Label(
                self.scrollable_frame,
                text="No player data available",
                font=("Arial", 10),
                fg='#888888',
                bg='#1a1a1a'
            )
            no_data_label.pack(pady=20)
            return
            
        # Create player entries
        for idx, (puuid, player_data) in enumerate(players.items()):
            self._create_player_widget(player_data, idx)
            
    def _create_player_widget(self, player_data: Dict[str, Any], index: int):
        """Create a widget for individual player data"""
        # Player frame
        player_frame = tk.Frame(self.scrollable_frame, bg='#2a2a2a', relief=tk.RAISED, bd=1)
        player_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Player name and agent
        name_agent = f"{player_data.get('name', 'Unknown')} ({player_data.get('agent', 'Unknown')})"
        name_label = tk.Label(
            player_frame,
            text=name_agent,
            font=("Arial", 10, "bold"),
            fg='#ffffff',
            bg='#2a2a2a',
            anchor='w'
        )
        name_label.pack(fill=tk.X, padx=5, pady=2)
        
        # Rank and RR
        rank_text = f"Rank: {self._get_rank_name(player_data.get('rank', 0))} ({player_data.get('rr', 0)} RR)"
        rank_label = tk.Label(
            player_frame,
            text=rank_text,
            font=("Arial", 9),
            fg='#cccccc',
            bg='#2a2a2a',
            anchor='w'
        )
        rank_label.pack(fill=tk.X, padx=5)
        
        # Stats
        stats_text = f"Level: {player_data.get('level', 'N/A')} | "
        stats_text += f"HS%: {player_data.get('headshotPercentage', 'N/A')} | "
        stats_text += f"K/D: {player_data.get('kd', 'N/A')} | "
        stats_text += f"Win%: {player_data.get('winPercentage', 'N/A')}"
        
        stats_label = tk.Label(
            player_frame,
            text=stats_text,
            font=("Arial", 8),
            fg='#aaaaaa',
            bg='#2a2a2a',
            anchor='w'
        )
        stats_label.pack(fill=tk.X, padx=5, pady=(0, 2))
        
    def _get_rank_name(self, rank_number: int) -> str:
        """Convert rank number to rank name"""
        rank_names = [
            'Unranked', 'Unranked', 'Unranked',
            'Iron 1', 'Iron 2', 'Iron 3',
            'Bronze 1', 'Bronze 2', 'Bronze 3',
            'Silver 1', 'Silver 2', 'Silver 3', 
            'Gold 1', 'Gold 2', 'Gold 3',
            'Platinum 1', 'Platinum 2', 'Platinum 3',
            'Diamond 1', 'Diamond 2', 'Diamond 3',
            'Ascendant 1', 'Ascendant 2', 'Ascendant 3',
            'Immortal 1', 'Immortal 2', 'Immortal 3',
            'Radiant'
        ]
        
        if 0 <= rank_number < len(rank_names):
            return rank_names[rank_number]
        return 'Unknown'
        
    def cleanup(self):
        """Cleanup resources"""
        self._running = False
        if KEYBOARD_AVAILABLE:
            try:
                keyboard.unhook_all_hotkeys()
            except:
                pass
            
        if self.root:
            self.root.quit()