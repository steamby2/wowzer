import cv2 as cv
import numpy as np
import pyautogui
import time
from threading import Thread
import os
import random

# Import our combat module and configuration
from grinding.combat import LowLevelHunterCombat
from grinding.config import TARGETS, ELWYNN_STARTING_WAYPOINTS, SETTINGS, DETECTION


class GrindingAgent:
    def __init__(self, main_agent):
        self.main_agent = main_agent
        
        # Initialize combat manager
        self.combat_manager = LowLevelHunterCombat(main_agent)
        
        # Load template images for detection
        self.here_path = os.path.dirname(os.path.realpath(__file__))
        self.enemy_templates = self._load_enemy_templates()
        self.loot_template = self._load_image('assets/ui/loot.png')
        
        # State tracking
        self.is_grinding = False
        self.target_found = False
        self.in_combat = False
        self.target_location = None
        self.grinding_thread = None
        
        # Stats tracking
        self.kills = 0
        self.deaths = 0
        self.loot_collected = 0
        self.start_time = 0
        
        print("Grinding Agent initialized for a Level 1 Hunter in Elwynn Forest")
    
    def _load_enemy_templates(self):
        """Load enemy template images from assets folder"""
        templates = {}
        enemy_dir = os.path.join(self.here_path, 'assets', 'enemies')
        
        # Check if directory exists
        if not os.path.exists(enemy_dir):
            os.makedirs(enemy_dir, exist_ok=True)
            print(f"Created directory: {enemy_dir}")
            print("Please add enemy template images to this directory")
            return templates
        
        # Load any PNG files in the directory
        for filename in os.listdir(enemy_dir):
            if filename.endswith('.png'):
                enemy_name = filename[:-4]  # Remove .png extension
                image_path = os.path.join(enemy_dir, filename)
                templates[enemy_name] = cv.imread(image_path)
                print(f"Loaded enemy template: {enemy_name}")
        
        if not templates:
            print("WARNING: No enemy templates found. Please add template images.")
        
        return templates
    
    def _load_image(self, relative_path):
        """Load a single image from assets folder"""
        full_path = os.path.join(self.here_path, relative_path)
        if os.path.exists(full_path):
            return cv.imread(full_path)
        else:
            parent_dir = os.path.dirname(full_path)
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
            print(f"WARNING: Image not found at {full_path}")
            return None
    
    def start_grinding(self):
        """Start the grinding process"""
        print("Starting grinding sequence...")
        self.is_grinding = True
        self.start_time = time.time()
        
        # Main grinding loop
        while self.is_grinding:
            # Make sure we have screen capture
            if self.main_agent.cur_img is None:
                print("No screen capture available. Waiting...")
                time.sleep(1)
                continue
            
            # Check player health
            if not self._check_health():
                self._rest()
                continue
            
            # Look for targets if not in combat
            if not self.in_combat:
                if not self.find_target():
                    self._move_and_search()
                    time.sleep(1)  # Prevent CPU hogging
                    continue
                else:
                    self.approach_target()
                    self.engage_combat()
            
            # If in combat, monitor combat state
            else:
                if self._check_combat_ended():
                    self.in_combat = False
                    self.kills += 1
                    print(f"Combat ended. Total kills: {self.kills}")
                    self._loot()
            
            # Small pause to prevent CPU overuse
            time.sleep(0.5)
    
    def find_target(self):
        """Scan screen for enemy targets"""
        print("Scanning for targets...")
        
        if not self.enemy_templates or self.main_agent.cur_img is None:
            return False
        
        best_match = None
        best_match_value = 0
        best_match_name = None
        
        # Try to find each enemy type in our templates
        for enemy_name, template in self.enemy_templates.items():
            if template is None:
                continue
                
            try:
                # Use template matching
                result = cv.matchTemplate(
                    self.main_agent.cur_img,
                    template,
                    cv.TM_CCOEFF_NORMED
                )
                
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
                
                # If match confidence is high enough and better than previous matches
                if max_val > DETECTION["enemy_confidence"] and max_val > best_match_value:
                    best_match = max_loc
                    best_match_value = max_val
                    best_match_name = enemy_name
            except Exception as e:
                print(f"Error matching template for {enemy_name}: {e}")
        
        # If we found a good match
        if best_match:
            self.target_location = best_match
            self.target_found = True
            print(f"Target found: {best_match_name} at {best_match} with confidence {best_match_value:.2f}")
            return True
        
        self.target_found = False
        return False
    
    def approach_target(self):
        """Move character to the target"""
        if not self.target_found or self.target_location is None:
            return
            
        print(f"Approaching target at {self.target_location}")
        
        # Calculate center of target (adjust based on your template size)
        h, w = 50, 50  # Default size - should match your template
        target_x = self.target_location[0] + w//2
        target_y = self.target_location[1] + h//2
        
        # Move mouse to target and right-click to target
        pyautogui.moveTo(target_x, target_y, 0.3, pyautogui.easeOutQuad)
        time.sleep(0.1)
        pyautogui.rightClick()
        time.sleep(0.5)
    
    def engage_combat(self):
        """Start combat with the current target"""
        print("Engaging combat...")
        self.in_combat = True
        
        # Start combat using our combat manager
        self.combat_manager.start_combat(self.target_location)
    
    def _check_health(self):
        """Check if health is sufficient to continue"""
        # Placeholder - should implement pixel detection of health bar
        # For now, always return True
        return True
    
    def _check_combat_ended(self):
        """Check if current combat has ended"""
        # This should check the UI for combat state
        # For now, delegate to combat manager
        return not self.combat_manager.in_combat
    
    def _loot(self):
        """Loot items from defeated enemies"""
        print("Attempting to loot...")
        
        # Wait for loot to be available
        time.sleep(1.0)
        
        # If we have a loot icon template, search for it
        if self.loot_template is not None and self.main_agent.cur_img is not None:
            try:
                result = cv.matchTemplate(
                    self.main_agent.cur_img,
                    self.loot_template,
                    cv.TM_CCOEFF_NORMED
                )
                
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
                
                if max_val > 0.6:  # Threshold for loot icon detection
                    # Move to loot location and click
                    h, w = self.loot_template.shape[:2]
                    loot_x = max_loc[0] + w//2
                    loot_y = max_loc[1] + h//2
                    
                    pyautogui.moveTo(loot_x, loot_y, 0.3)
                    pyautogui.rightClick()
                    
                    # Wait for loot window and press spacebar to loot all
                    time.sleep(0.5)
                    pyautogui.press('space')
                    
                    self.loot_collected += 1
                    print(f"Loot collected! Total: {self.loot_collected}")
                    return
            except Exception as e:
                print(f"Error during looting: {e}")
        
        # If no loot template or not found, try to loot near the last target location
        if self.target_location:
            # Move slightly to where the corpse should be
            loot_x = self.target_location[0] + random.randint(-10, 10)
            loot_y = self.target_location[1] + random.randint(-5, 5)
            
            pyautogui.moveTo(loot_x, loot_y, 0.3)
            pyautogui.rightClick()
            
            # Wait for loot window and press spacebar to loot all
            time.sleep(0.5)
            pyautogui.press('space')
    
    def _move_and_search(self):
        """Move around to find new targets"""
        print("Moving to find new targets...")
        
        # Simple movement - move forward for a short time
        pyautogui.keyDown('w')
        time.sleep(random.uniform(0.8, 1.5))
        pyautogui.keyUp('w')
        
        # Random turn to explore the area
        if random.random() < 0.4:  # 40% chance to turn
            turn_key = 'a' if random.random() < 0.5 else 'd'
            turn_time = random.uniform(0.1, 0.5)  # Random turn amount
            
            pyautogui.keyDown(turn_key)
            time.sleep(turn_time)
            pyautogui.keyUp(turn_key)
    
    def _rest(self):
        """Rest to recover health/mana"""
        print("Resting to recover...")
        
        # Sit down to recover faster if needed
        # pyautogui.press('x')  # Assuming 'x' is sit/stand
        
        # Wait for recovery
        time.sleep(5)
        
        # Stand up if needed
        # pyautogui.press('x')
    
    def stop_grinding(self):
        """Stop the grinding process"""
        print("Stopping grinding sequence...")
        if self.is_grinding:
            elapsed_time = time.time() - self.start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            
            print("\n===== Grinding Session Stats =====")
            print(f"Session duration: {minutes}m {seconds}s")
            print(f"Total kills: {self.kills}")
            print(f"Total loot collected: {self.loot_collected}")
            print(f"Deaths: {self.deaths}")
            print(f"Kills per minute: {self.kills / (elapsed_time / 60):.2f}")
            print("=================================\n")
            
        self.is_grinding = False
        self.combat_manager.in_combat = False
    
    def run(self):
        """Run the grinding agent in a separate thread"""
        if self.main_agent.cur_img is None:
            print("Image capture not found! Did you start the screen capture thread?")
            print("Please press 'S' first to start screen capture.")
            return
            
        print("Starting grinding thread in 5 seconds...")
        print("Make sure your character is in a safe position.")
        print("Press 'Q' at any time to stop the bot.")
        time.sleep(5)
        
        self.grinding_thread = Thread(
            target=self.start_grinding,
            args=(),
            name="grinding thread",
            daemon=True
        )
        self.grinding_thread.start()