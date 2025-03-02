import pyautogui
import numpy as np
import time
import cv2 as cv
import random


class Navigator:
    def __init__(self, main_agent):
        self.main_agent = main_agent
        
        # Waypoints - could be loaded from a configuration file
        self.waypoints = {
            "Elwynn Forest": [
                (100, 100),  # These are screen coordinates - would need to be set properly
                (200, 150),
                (300, 200),
                (250, 300)
            ],
            "Dun Morogh": [
                (150, 150),
                (250, 200),
                (350, 250),
                (300, 350)
            ],
            "Feralas": [
                (120, 120),
                (220, 170),
                (320, 220),
                (270, 320)
            ]
        }
        
        self.current_waypoint_index = 0
        self.stuck_detection_counter = 0
        self.last_position = None
        self.position_history = []  # For stuck detection
        
        # Minimap detection
        self.minimap_center = (1280, 100)  # Default - should be detected
        self.minimap_radius = 60
    
    def navigate_to_grinding_area(self):
        """Navigate to the appropriate grinding area based on zone"""
        zone = self.main_agent.zone
        print(f"Navigating to grinding area in {zone}...")
        
        if zone in self.waypoints:
            self._follow_waypoints(self.waypoints[zone])
        else:
            print(f"No waypoints defined for {zone}. Using random navigation.")
            self._random_navigation()
    
    def _follow_waypoints(self, waypoints):
        """Follow a series of waypoints"""
        if not waypoints:
            return
            
        self.current_waypoint_index = 0
        
        while self.current_waypoint_index < len(waypoints):
            current_waypoint = waypoints[self.current_waypoint_index]
            print(f"Moving to waypoint {self.current_waypoint_index+1}/{len(waypoints)}")
            
            self._move_to_point(current_waypoint)
            
            # Check if we reached the waypoint
            if self._is_at_target(current_waypoint):
                self.current_waypoint_index += 1
            
            # Check if stuck
            if self._is_stuck():
                self._handle_stuck()
            
            # Update position history for stuck detection
            self._update_position_history()
            
            # Small pause
            time.sleep(0.5)
    
    def _move_to_point(self, point):
        """Move character towards a specific point"""
        # Get current character position - this would need to be implemented
        # based on how position is determined in your game
        current_pos = self._get_character_position()
        
        if current_pos is None:
            print("Could not determine character position")
            return
        
        # Calculate direction
        dx = point[0] - current_pos[0]
        dy = point[1] - current_pos[1]
        
        # Adjust character orientation
        self._turn_character(dx, dy)
        
        # Move forward
        pyautogui.keyDown('w')
        time.sleep(1.0)  # Move for a short time
        pyautogui.keyUp('w')
    
    def _turn_character(self, dx, dy):
        """Turn character to face the right direction"""
        # This is a simplified version - would need proper minimap coordinate mapping
        
        # Determine angle
        angle = np.arctan2(dy, dx)
        
        # Convert to mouse movement - WoW uses mouse for character facing
        # Right-click and drag to turn
        pyautogui.mouseDown(button='right')
        pyautogui.move(int(dx/10), 0)  # Simplified - just turn based on x difference
        pyautogui.mouseUp(button='right')
    
    def _get_character_position(self):
        """Get character position from minimap or other indicators"""
        # This would need to be implemented based on your game's UI
        # For now, return a fake position
        
        # Could detect player position on minimap with template matching
        # or colored pixel detection
        
        # Placeholder: return random position for demonstration
        x = random.randint(100, 500)
        y = random.randint(100, 500)
        return (x, y)
    
    def _is_at_target(self, target):
        """Check if character has reached the target point"""
        current_pos = self._get_character_position()
        
        if current_pos is None:
            return False
        
        # Calculate distance
        distance = np.sqrt((target[0] - current_pos[0])**2 + (target[1] - current_pos[1])**2)
        
        # Check if close enough
        return distance < 20  # Threshold for "at target"
    
    def _update_position_history(self):
        """Update position history for stuck detection"""
        current_pos = self._get_character_position()
        
        if current_pos is not None:
            self.position_history.append(current_pos)
            
            # Keep history limited to recent positions
            if len(self.position_history) > 10:
                self.position_history.pop(0)
    
    def _is_stuck(self):
        """Detect if character is stuck"""
        if len(self.position_history) < 5:
            return False
        
        # Check if position has changed significantly in recent history
        x_positions = [pos[0] for pos in self.position_history[-5:]]
        y_positions = [pos[1] for pos in self.position_history[-5:]]
        
        x_variation = max(x_positions) - min(x_positions)
        y_variation = max(y_positions) - min(y_positions)
        
        # If character hasn't moved much, might be stuck
        return x_variation < 10 and y_variation < 10
    
    def _handle_stuck(self):
        """Handle stuck situation"""
        print("Character appears to be stuck. Attempting to free...")
        
        # First, try jumping
        pyautogui.press('space')
        
        # If still stuck, try moving backward and turning
        pyautogui.keyDown('s')
        time.sleep(1.5)
        pyautogui.keyUp('s')
        
        # Turn randomly
        turn_key = 'a' if random.random() < 0.5 else 'd'
        pyautogui.keyDown(turn_key)
        time.sleep(random.uniform(0.5, 1.5))
        pyautogui.keyUp(turn_key)
        
        # Try jumping again
        pyautogui.press('space')
        
        # Clear position history
        self.position_history = []
    
    def _random_navigation(self):
        """Navigate randomly when no waypoints are available"""
        print("Using random navigation pattern...")
        
        for _ in range(5):  # Do a few random moves
            # Move forward for random time
            pyautogui.keyDown('w')
            time.sleep(random.uniform(1.0, 3.0))
            pyautogui.keyUp('w')
            
            # Random turn
            turn_amount = random.uniform(-0.5, 0.5)
            turn_key = 'a' if turn_amount < 0 else 'd'
            pyautogui.keyDown(turn_key)
            time.sleep(abs(turn_amount))
            pyautogui.keyUp(turn_key)
            
            # Check for obstacles
            if random.random() < 0.2:  # Simulate obstacle detection
                print("Obstacle detected, adjusting path...")
                pyautogui.keyDown('s')
                time.sleep(0.5)
                pyautogui.keyUp('s')
    
    def return_to_vendor(self):
        """Navigate back to a vendor to sell items"""
        print("Returning to vendor...")
        
        # This could use a different set of waypoints to reach town
        # For simplicity, just using random navigation for now
        self._random_navigation()
            
    def find_safe_grinding_spot(self):
        """Find a safe area to grind in the current zone"""
        print("Scanning for a safe grinding spot...")
        
        # This would analyze the screen to find an area with:
        # 1. Appropriate mob density
        # 2. No hostile players (if PvP server)
        # 3. Not too close to dangerous elites
        
        # For now, just move around a bit
        self._random_navigation()
        
        return True  # Assume we found a spot
