import pyautogui
import time
import random

class LowLevelHunterCombat:
    """Gestion de combat simplifiée pour un Hunter niveau 1"""
    
    def __init__(self, main_agent):
        self.main_agent = main_agent
        self.in_combat = False
        self.target_acquired = False
        self.last_ability_time = {}
        
    def start_combat(self, target_location):
        """Commence le combat avec une cible"""
        print("Commencer le combat avec la cible")
        
        # Cibler l'ennemi (clic droit)
        if target_location:
            target_x = target_location[0] + random.randint(-5, 5)  # Ajouter une petite variation
            target_y = target_location[1] + random.randint(-5, 5)
            
            # Se déplacer vers la cible mais garder distance
            pyautogui.moveTo(target_x, target_y, duration=0.3)
            pyautogui.rightClick()  # Cible l'ennemi
            time.sleep(0.5)
            
            # Reculer légèrement pour maintenir la distance (Hunter)
            self._maintain_distance()
            
            # Commencer à attaquer
            self._use_ability("auto_shot", "1")
            self.in_combat = True
            self.target_acquired = True
            
            # Boucle de combat principale
            self._combat_loop()
    
    def _combat_loop(self):
        """Boucle principale de combat pour Hunter niveau 1"""
        start_time = time.time()
        
        while self.in_combat and time.time() - start_time < 30:  # Timeout de sécurité
            # Vérifier si la cible est morte
            if self._target_is_dead():
                print("Cible éliminée!")
                self.in_combat = False
                break
            
            # Vérifier si notre santé est basse
            if self._health_is_low():
                print("Santé basse, reculer!")
                self._retreat()
                continue
            
            # Boucle de combat très simple pour niveau 1
            # Si au corps à corps, utiliser Raptor Strike
            if self._is_in_melee_range() and self._can_use_ability("raptor_strike", 6):
                self._use_ability("raptor_strike", "2")
            
            # Sinon, continuer à utiliser Auto Shot
            else:
                # Auto Shot devrait continuer automatiquement si activé
                # Mais on peut le réactiver pour être sûr
                if self._can_use_ability("auto_shot", 0.5):  # Un petit délai pour éviter le spam
                    self._use_ability("auto_shot", "1")
            
            # Maintenir la distance optimale
            self._maintain_distance()
            
            # Petite pause pour éviter de surcharger
            time.sleep(0.5)
        
        # Sortie de combat
        if time.time() - start_time >= 30:
            print("Combat timeout - forcer sortie")
            self._reset_combat()
    
    def _maintain_distance(self):
        """Maintient une distance optimale pour un Hunter"""
        # Pour un Hunter, on veut rester à distance
        # Un step back aléatoire de temps en temps
        if random.random() < 0.3:  # 30% de chances
            pyautogui.keyDown('s')
            time.sleep(random.uniform(0.2, 0.5))
            pyautogui.keyUp('s')
            
            # Parfois faire un strafe au lieu de reculer
            if random.random() < 0.3:
                key = 'q' if random.random() < 0.5 else 'e'  # strafe left or right
                pyautogui.keyDown(key)
                time.sleep(random.uniform(0.2, 0.4))
                pyautogui.keyUp(key)
    
    def _retreat(self):
        """Battre en retraite si la santé est basse"""
        # Sauter en arrière pour créer de la distance
        pyautogui.keyDown('s')
        time.sleep(0.5)
        pyautogui.press('space')  # Sauter
        time.sleep(0.8)
        pyautogui.keyUp('s')
    
    def _use_ability(self, ability_name, key):
        """Utilise une capacité spécifique"""
        print(f"Utilisation de {ability_name}")
        pyautogui.press(key)
        self.last_ability_time[ability_name] = time.time()
    
    def _can_use_ability(self, ability_name, cooldown):
        """Vérifie si une capacité peut être utilisée (hors cooldown)"""
        current_time = time.time()
        last_use = self.last_ability_time.get(ability_name, 0)
        return current_time - last_use >= cooldown
    
    def _target_is_dead(self):
        """Vérifie si la cible est morte"""
        # En réalité, on voudrait vérifier la barre de vie de la cible
        # Pour un prototype simple, on utilise une probabilité basée
        # sur le temps écoulé depuis le début du combat
        combat_time = time.time() - self.last_ability_time.get("auto_shot", time.time())
        
        # Plus le combat dure longtemps, plus il est probable que l'ennemi soit mort
        if combat_time > 15:
            return random.random() < 0.9  # 90% de chance d'être mort après 15 secondes
        elif combat_time > 10:
            return random.random() < 0.7  # 70% de chance d'être mort après 10 secondes
        elif combat_time > 5:
            return random.random() < 0.3  # 30% de chance d'être mort après 5 secondes
            
        return False
    
    def _health_is_low(self):
        """Vérifie si la santé du joueur est basse"""
        # À implémenter avec détection réelle de la barre de vie
        # Pour l'instant, une chance aléatoire faible
        return random.random() < 0.05  # 5% de chance que la santé soit considérée basse
    
    def _is_in_melee_range(self):
        """Vérifie si le joueur est au corps à corps avec la cible"""
        # À implémenter avec détection réelle
        # Pour l'instant, aléatoire
        return random.random() < 0.2  # 20% de chance d'être au corps à corps
    
    def _reset_combat(self):
        """Réinitialise l'état de combat"""
        self.in_combat = False
        self.target_acquired = False
        
        # S'assurer que toutes les touches sont relâchées
        for key in ['w', 'a', 's', 'd', 'q', 'e']:
            pyautogui.keyUp(key)
