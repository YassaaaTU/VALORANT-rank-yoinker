#!/usr/bin/env python3
"""
Desktop Overlay Demo for VALORANT Rank Yoinker

This script demonstrates how the overlay feature works with mock data.
It creates a semi-transparent, always-on-top window displaying player information.

Usage: python overlay_demo.py
Press F9 to toggle overlay visibility (if keyboard support is available)
"""

import time
import sys
import os
import threading

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Mock classes for demo purposes
class DemoConfig:
    """Mock config class that provides overlay settings"""
    
    def get_overlay_setting(self, key):
        settings = {
            "hotkey": "F9",
            "transparency": 0.85,
            "x": 150,
            "y": 150,
            "width": 650,
            "height": 450
        }
        return settings.get(key)
    
    def get_feature_flag(self, key):
        return True

def create_demo_player_data():
    """Create realistic demo player data"""
    return {
        "player_001": {
            "name": "ProGamer2024",
            "agent": "Jett",
            "rank": 18,  # Diamond 3
            "rr": 73,
            "level": 142,
            "headshotPercentage": "31%",
            "kd": "1.4",
            "winPercentage": "68% (25)",
            "team": "Blue"
        },
        "player_002": {
            "name": "ValorantAce",
            "agent": "Sage", 
            "rank": 15,  # Platinum 3
            "rr": 45,
            "level": 89,
            "headshotPercentage": "24%",
            "kd": "1.1",
            "winPercentage": "72% (18)",
            "team": "Blue"
        },
        "player_003": {
            "name": "SniperElite",
            "agent": "Chamber",
            "rank": 20,  # Diamond 1
            "rr": 12,
            "level": 203,
            "headshotPercentage": "41%",
            "kd": "1.8",
            "winPercentage": "58% (31)",
            "team": "Blue"
        },
        "player_004": {
            "name": "FlashMaster",
            "agent": "Phoenix",
            "rank": 16,  # Platinum 1
            "rr": 89,
            "level": 67,
            "headshotPercentage": "29%",
            "kd": "1.2",
            "winPercentage": "65% (20)",
            "team": "Blue"
        },
        "player_005": {
            "name": "SmokeKing",
            "agent": "Omen",
            "rank": 17,  # Platinum 2
            "rr": 56,
            "level": 156,
            "headshotPercentage": "27%",
            "kd": "0.9",
            "winPercentage": "70% (23)",
            "team": "Blue"
        },
        "player_006": {
            "name": "EnemyPlayer1",
            "agent": "Reyna",
            "rank": 19,  # Diamond 2
            "rr": 34,
            "level": 178,
            "headshotPercentage": "35%",
            "kd": "1.6",
            "winPercentage": "62% (29)",
            "team": "Red"
        },
        "player_007": {
            "name": "OpponentTwo",
            "agent": "Cypher",
            "rank": 14,  # Gold 2
            "rr": 78,
            "level": 45,
            "headshotPercentage": "22%",
            "kd": "1.0",
            "winPercentage": "59% (17)",
            "team": "Red"
        },
        "player_008": {
            "name": "EnemySniper",
            "agent": "Sova",
            "rank": 21,  # Diamond 3
            "rr": 91,
            "level": 234,
            "headshotPercentage": "38%",
            "kd": "1.7",
            "winPercentage": "71% (35)",
            "team": "Red"
        }
    }

def demo_log(message):
    """Demo logging function"""
    print(f"[OVERLAY]: {message}")

def run_demo():
    """Run the overlay demo"""
    print("=" * 60)
    print("VALORANT Rank Yoinker - Desktop Overlay Demo")
    print("=" * 60)
    print()
    
    try:
        from overlay import GameOverlay, TKINTER_AVAILABLE, KEYBOARD_AVAILABLE
        
        if not TKINTER_AVAILABLE:
            print("❌ tkinter is not available in this environment")
            print("   The overlay requires a GUI environment with tkinter support")
            print("   This is typically available on:")
            print("   - Windows with Python from python.org")
            print("   - macOS with Python from python.org or Homebrew")
            print("   - Linux with python3-tk package installed")
            print()
            print("💡 To install tkinter on Linux:")
            print("   sudo apt-get install python3-tk  # Ubuntu/Debian")
            print("   sudo yum install tkinter          # CentOS/RHEL")
            print()
            return False
        
        if not KEYBOARD_AVAILABLE:
            print("⚠️  keyboard library not available - hotkeys will be disabled")
            print()
        
        # Create demo config and overlay (start visible for demo)
        config = DemoConfig()
        overlay = GameOverlay(demo_log, config, start_visible=True)  # Force visible for demo
        
        print("🚀 Initializing overlay...")
        if not overlay.initialize():
            print("❌ Failed to initialize overlay")
            return False
            
        print("✅ Overlay initialized successfully!")
        print("📱 The overlay window should now be VISIBLE on your screen!")
        print("   Look for a semi-transparent dark window titled 'VALORANT Overlay'")
        print()
        print("📊 Loading demo player data...")
        
        # Wait for overlay to fully initialize
        time.sleep(2)
        
        # Force overlay to be visible (for demo)
        overlay.force_show()
        
        # Update with demo data
        demo_players = create_demo_player_data()
        overlay.update_data(
            "INGAME", 
            demo_players,
            {
                "map": "Bind",
                "mode": "Competitive",
                "server": "na-central-1.aws.val.com"
            }
        )
        
        print("✅ Demo data loaded!")
        print()
        print("🎮 DEMO INSTRUCTIONS:")
        print("=" * 40)
        print("• The overlay window should now be VISIBLE on your screen!")
        print("• Look for a semi-transparent dark window with player data")
        if KEYBOARD_AVAILABLE:
            print(f"• Press {config.get_overlay_setting('hotkey')} to toggle overlay visibility")
        else:
            print("• Hotkeys disabled (keyboard library not available)")
        print("• Drag the '≡≡≡ DRAG ≡≡≡' handle to move the overlay")
        print("• Click 'Hide' button to hide overlay")
        print("• Press Ctrl+C here to exit demo")
        print()
        print("📊 The overlay shows:")
        print("• Player names and agents")
        print("• Current ranks and RR")
        print("• Player levels and stats")
        print("• Headshot %, K/D, Win rate")
        print()
        print("🎯 This is exactly how it works in-game!")
        print("   The overlay will display real player data from VALORANT")
        print("   when running with the main application.")
        print()
        
        if not KEYBOARD_AVAILABLE:
            print("⚠️  NOTE: Keyboard library not available in this environment")
            print("   In a normal desktop environment with 'pip install keyboard',")
            print("   you would be able to use hotkeys to toggle the overlay.")
            print()
        
        # Simulate some data updates
        def update_demo_data():
            game_states = ["PREGAME", "INGAME", "INGAME", "MENUS"]
            state_idx = 1
            
            while True:
                time.sleep(15)  # Update every 15 seconds
                if state_idx < len(game_states):
                    current_state = game_states[state_idx] 
                    demo_log(f"Updating to game state: {current_state}")
                    overlay.update_data(current_state, demo_players, {
                        "map": "Bind",
                        "mode": "Competitive"
                    })
                    state_idx += 1
                else:
                    break
        
        # Start demo updates in background
        update_thread = threading.Thread(target=update_demo_data, daemon=True)
        update_thread.start()
        
        try:
            print("⏳ Demo running... (Press Ctrl+C to exit)")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Demo stopping...")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're running from the correct directory")
        return False
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            overlay.cleanup()
            print("✅ Overlay cleaned up")
        except:
            pass
        print("👋 Demo finished!")
        
    return True

if __name__ == "__main__":
    success = run_demo()
    if not success:
        print("\n💡 The overlay feature is designed for desktop environments")
        print("   with GUI support. In production, it works great for:")
        print("   • Gaming PCs with Windows")
        print("   • Desktop Linux with GUI")
        print("   • macOS systems")
        print("\n🎮 When available, the overlay provides an excellent")
        print("   gaming experience for VALORANT rank checking!")
        sys.exit(1)