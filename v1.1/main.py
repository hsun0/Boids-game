import pygame
import numpy as np
import random
import math
import ctypes
from ctypes import Structure, c_float, c_int, POINTER
import os
import sys
import platform  # 添加這行
from dataclasses import dataclass
from typing import List, Tuple, Optional
@dataclass
class SimConfig:
    # Canvas settings
    CANVAS_WIDTH: int = 1000
    CANVAS_HEIGHT: int = 800
    
    # Boid settings
    BOID_SIZE: int = 6
    BOID_COUNT: int = 150
    MASS_RANGE: Tuple[float, float] = (0.8, 1.2)
    
    # Movement parameters
    VISION_RADIUS: float = 100.0
    MAX_SPEED: float = 8.0
    MIN_SPEED: float = 2.0
    SEPARATION_FACTOR: float = 0.05
    ALIGNMENT_FACTOR: float = 0.02
    COHESION_FACTOR: float = 0.01
    COLOR_AVOIDANCE_FACTOR: float = 1.0
    ENERGY_FACTOR: float = 0.01
    
    # Life simulation parameters
    REPRODUCTION_CHANCE: float = 0.001
    DEATH_CHANCE: float = 0.0005
    COLOR_CHANGE_CHANCE: float = 0.0001
    ENERGY_DECAY: float = 0.001
    CROWDING_THRESHOLD: int = 20
    
    # Food settings
    FOOD_COUNT: int = 200
    FOOD_RESPAWN_CHANCE: float = 0.03
    
    # Visual settings
    COLORS: Tuple = ((255, 0, 0), (0, 255, 0), (0, 255, 255))
    
    def create_simulation_params(self) -> 'SimulationParams':
        """Create simulation parameters structure for C++ code"""
        return SimulationParams(
            vision_radius=c_float(self.VISION_RADIUS),
            max_speed=c_float(self.MAX_SPEED),
            min_speed=c_float(self.MIN_SPEED),
            separation_factor=c_float(self.SEPARATION_FACTOR),
            alignment_factor=c_float(self.ALIGNMENT_FACTOR),
            cohesion_factor=c_float(self.COHESION_FACTOR),
            color_avoidance_factor=c_float(self.COLOR_AVOIDANCE_FACTOR),
            energy_factor=c_float(self.ENERGY_FACTOR)
        )

class Vector2(Structure):
    _fields_ = [
        ("x", c_float),
        ("y", c_float)
    ]

class SimulationParams(Structure):
    _fields_ = [
        ("vision_radius", c_float),
        ("max_speed", c_float),
        ("min_speed", c_float),
        ("separation_factor", c_float),
        ("alignment_factor", c_float),
        ("cohesion_factor", c_float),
        ("color_avoidance_factor", c_float),
        ("energy_factor", c_float)
    ]

class BoidStruct(Structure):
    _fields_ = [
        ("pos", Vector2),
        ("vel", Vector2),
        ("energy", c_float),
        ("color", c_int),
        ("mass", c_float)
    ]

class Boid:
    def __init__(self, x: float, y: float, color: Tuple[int, int, int], config: SimConfig):
        self.config = config
        self.pos = np.array([x, y], dtype=np.float32)
        self.color = color
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(config.MIN_SPEED, config.MAX_SPEED)
        self.vel = np.array([math.cos(angle), math.sin(angle)], dtype=np.float32) * speed
        self.energy = 100.0
        self.mass = random.uniform(*config.MASS_RANGE)
        self.age = 0

    def eat(self, amount: float) -> None:
        self.energy = min(100, self.energy + amount)

    def to_struct(self) -> BoidStruct:
        pos = Vector2(float(self.pos[0]), float(self.pos[1]))
        vel = Vector2(float(self.vel[0]), float(self.vel[1]))
        return BoidStruct(
            pos=pos,
            vel=vel,
            energy=c_float(self.energy),
            color=c_int(self.config.COLORS.index(self.color)),
            mass=c_float(self.mass)
        )

    def from_struct(self, struct: BoidStruct) -> None:
        self.pos[0] = struct.pos.x
        self.pos[1] = struct.pos.y
        self.vel[0] = struct.vel.x
        self.vel[1] = struct.vel.y
        self.energy = struct.energy

    def draw(self, screen: pygame.Surface) -> None:
        # 根據能量調整顏色亮度
        color = list(self.color)
        energy_factor = self.energy / 100.0
        color = tuple(int(c * energy_factor) for c in color)
        
        # 根據質量調整大小
        size = self.config.BOID_SIZE * math.sqrt(self.mass)
        
        angle = math.atan2(self.vel[1], self.vel[0])
        points = [
            (int(self.pos[0] + size * math.cos(angle)), 
             int(self.pos[1] + size * math.sin(angle))),
            (int(self.pos[0] + size * math.cos(angle + 2.5)), 
             int(self.pos[1] + size * math.sin(angle + 2.5))),
            (int(self.pos[0] + size * math.cos(angle - 2.5)), 
             int(self.pos[1] + size * math.sin(angle - 2.5)))
        ]
        pygame.draw.polygon(screen, color, points)
class Food:
    def __init__(self, pos: np.ndarray):
        self.pos = pos
    
    @classmethod
    def random(cls, config: SimConfig) -> 'Food':
        return cls(np.array([
            random.uniform(0, config.CANVAS_WIDTH),
            random.uniform(0, config.CANVAS_HEIGHT)
        ], dtype=np.float32))

class BoidSimulation:
    def __init__(self):
        self.config = SimConfig()
        self._init_pygame()
        self._load_dll()
        self.boids = self._create_initial_boids()
        self.foods = self._create_initial_foods()
        self.boid_array = (BoidStruct * self.config.BOID_COUNT)()
        self.sim_params = self.config.create_simulation_params()  # 使用新的方法
        self.paused = False
        self.show_debug = False

    def _create_initial_boids(self) -> List[Boid]:
        """Create the initial population of boids"""
        return [
            Boid(
                random.uniform(0, self.config.CANVAS_WIDTH),
                random.uniform(0, self.config.CANVAS_HEIGHT),
                random.choice(self.config.COLORS),
                self.config
            )
            for _ in range(self.config.BOID_COUNT)
        ]

    def _create_initial_foods(self) -> List[Food]:
        """Create the initial set of food particles"""
        return [Food.random(self.config) for _ in range(self.config.FOOD_COUNT)]

    def _create_simulation_params(self) -> SimulationParams:
        """Create simulation parameters structure"""
        return SimulationParams(
            vision_radius=c_float(self.config.VISION_RADIUS),
            max_speed=c_float(self.config.MAX_SPEED),
            min_speed=c_float(self.config.MIN_SPEED),
            separation_factor=c_float(0.05),
            alignment_factor=c_float(0.02),
            cohesion_factor=c_float(0.01),
            color_avoidance_factor=c_float(1.0),
            energy_factor=c_float(0.01)
        )

    def _init_pygame(self) -> None:
        """Initialize Pygame and create the display window"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.config.CANVAS_WIDTH, self.config.CANVAS_HEIGHT))
        pygame.display.set_caption("Enhanced Boids Life Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def _load_dll(self) -> None:
        """Load the C++ library based on platform"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        system = platform.system()

        if system == "Windows":
            lib_name = "boids.dll"
        elif system == "Darwin":  # macOS
            lib_name = "libboids.dylib"
        elif system == "Linux":
            lib_name = "libboids.so"
        else:
            raise OSError(f"Unsupported platform: {system}")

        lib_path = os.path.join(current_dir, lib_name)
        
        try:
            # Use CDLL for Windows, RTLD_GLOBAL flag for Unix-based systems
            if system == "Windows":
                self.boids_dll = ctypes.CDLL(lib_path)
            else:
                self.boids_dll = ctypes.CDLL(lib_path, ctypes.RTLD_GLOBAL)

            # Set up function argument types
            self.boids_dll.update_boids.argtypes = [
                POINTER(BoidStruct),
                c_int,
                c_float,
                c_float,
                POINTER(SimulationParams)
            ]
        except OSError as e:
            print(f"Error loading library: {e}")
            print(f"Attempted to load: {lib_path}")
            print("Falling back to Python-only mode")
            self.boids_dll = None

    def handle_events(self) -> bool:
        """Handle Pygame events and return False if should quit"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_d:
                    self.show_debug = not self.show_debug
                elif event.key == pygame.K_f:
                    pos = pygame.mouse.get_pos()
                    self.foods.append(Food(np.array(pos, dtype=np.float32)))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.boids.append(Boid(pos[0], pos[1], 
                                     random.choice(self.config.COLORS), 
                                     self.config))
        return True

    def update(self) -> None:
        """Update simulation state with fallback to Python if DLL fails"""
        if self.paused:
            return

        if self.boids_dll is not None:
            # Update C++ structures
            for i, boid in enumerate(self.boids[:self.config.BOID_COUNT]):
                self.boid_array[i] = boid.to_struct()

            try:
                # Call C++ update function
                self.boids_dll.update_boids(
                    self.boid_array,
                    min(len(self.boids), self.config.BOID_COUNT),
                    c_float(self.config.CANVAS_WIDTH),
                    c_float(self.config.CANVAS_HEIGHT),
                    ctypes.byref(self.sim_params)
                )

                # Update boids from C++ results
                for i, boid in enumerate(self.boids[:self.config.BOID_COUNT]):
                    boid.from_struct(self.boid_array[i])

            except Exception as e:
                print(f"Error in C++ update: {e}")
                self._update_python()
        else:
            self._update_python()

        # Process boids
        new_boids = self._process_boids()
        self._handle_food(new_boids)
        self.boids = new_boids

    def _process_boids(self) -> List[Boid]:
        """Process boids and return the new list of surviving boids"""
        new_boids = []
        
        for i, boid in enumerate(self.boids):
            if i < self.config.BOID_COUNT:
                boid.from_struct(self.boid_array[i])
            
            boid.age += 1
            boid.energy -= self.config.ENERGY_DECAY * boid.mass

            if self._should_reproduce(boid):
                child = self._reproduce_boid(boid)
                new_boids.append(child)
                boid.energy -= 40

            if self._should_survive(boid):
                if random.random() < self.config.COLOR_CHANGE_CHANCE:
                    boid.color = random.choice([c for c in self.config.COLORS if c != boid.color])
                if random.random() < 0.001:
                    boid.mass = max(0.5, min(2.0, boid.mass + random.uniform(-0.1, 0.1)))
                new_boids.append(boid)

        return new_boids

    def _should_reproduce(self, boid: Boid) -> bool:
        """Determine if a boid should reproduce"""
        base_chance = self.config.REPRODUCTION_CHANCE
        age_factor = min(1.0, boid.age / 1000)
        energy_factor = max(0, (boid.energy - 60) / 40)
        return (random.random() < base_chance * age_factor * energy_factor and 
                boid.energy > 60)

    def _should_survive(self, boid: Boid) -> bool:
        """Determine if a boid should survive"""
        death_chance = self.config.DEATH_CHANCE
        age_factor = max(1.0, boid.age / 2000)
        death_chance *= age_factor
        
        if boid.energy < 20:
            death_chance *= 2
        
        return (boid.energy > 0 and 
                random.random() >= death_chance)

    def _reproduce_boid(self, parent: Boid) -> Boid:
        """Create a new boid as offspring of the parent"""
        child = Boid(
            parent.pos[0] + random.uniform(-10, 10),
            parent.pos[1] + random.uniform(-10, 10),
            parent.color,
            self.config
        )
        child.mass = max(0.5, min(2.0, parent.mass + random.uniform(-0.1, 0.1)))
        child.energy = 50
        return child

    def _handle_food(self, boids: List[Boid]) -> None:
        """Handle food consumption and respawning"""
        for boid in boids:
            for food in self.foods[:]:
                dist = np.linalg.norm(boid.pos - food.pos)
                if dist < 5 * math.sqrt(boid.mass):
                    energy_gain = 20 / boid.mass
                    boid.eat(energy_gain)
                    self.foods.remove(food)

        while len(self.foods) < self.config.FOOD_COUNT:
            if random.random() < self.config.FOOD_RESPAWN_CHANCE:
                self.foods.append(Food.random(self.config))

    def draw(self) -> None:
        """Draw the current simulation state"""
        self.screen.fill((0, 0, 0))
        
        for food in self.foods:
            pygame.draw.circle(self.screen, (0, 255, 0), food.pos.astype(int), 2)
        
        for boid in self.boids:
            boid.draw(self.screen)
        
        if self.show_debug:
            self._draw_debug_info()
        
        pygame.display.flip()

    def _draw_debug_info(self) -> None:
        """Draw debug information on screen"""
        total_boids = len(self.boids)
        avg_energy = sum(b.energy for b in self.boids) / total_boids if total_boids > 0 else 0
        avg_mass = sum(b.mass for b in self.boids) / total_boids if total_boids > 0 else 0
        color_counts = {color: sum(1 for b in self.boids if b.color == color) 
                       for color in self.config.COLORS}
        
        y = 10
        texts = [
            f"Boids: {total_boids}",
            f"Food: {len(self.foods)}",
            f"Avg Energy: {avg_energy:.1f}",
            f"Avg Mass: {avg_mass:.2f}",
            "Paused" if self.paused else "Running"
        ]
        
        for color, count in color_counts.items():
            texts.append(f"Color {self.config.COLORS.index(color)}: {count}")
            
        for text in texts:
            surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(surface, (10, y))
            y += 30
    def _update_python(self) -> None:
        """Pure Python implementation of boid updates"""
        for boid in self.boids:
            separation = np.zeros(2)
            alignment = np.zeros(2)
            cohesion = np.zeros(2)
            food_attraction = np.zeros(2)
            
            nearby_count = 0
            for other in self.boids:
                if other is boid:
                    continue
                    
                dist = np.linalg.norm(other.pos - boid.pos)
                if dist < self.config.VISION_RADIUS:
                    nearby_count += 1
                    
                    if dist < self.config.VISION_RADIUS * 0.5:
                        separation += (boid.pos - other.pos) / (dist + 1e-6)
                    
                    alignment += other.vel
                    cohesion += other.pos
            
            for food in self.foods:
                dist = np.linalg.norm(food.pos - boid.pos)
                if dist < self.config.VISION_RADIUS:
                    food_attraction += (food.pos - boid.pos) / (dist + 1e-6)
            
            if nearby_count > 0:
                alignment /= nearby_count
                cohesion = cohesion/nearby_count - boid.pos
                
                for force in [separation, alignment, cohesion]:
                    if np.any(force):
                        force = force / np.linalg.norm(force)
                
                boid.vel += (separation * self.config.SEPARATION_FACTOR +
                            alignment * self.config.ALIGNMENT_FACTOR +
                            cohesion * self.config.COHESION_FACTOR +
                            food_attraction * self.config.ENERGY_FACTOR)
                
                speed = np.linalg.norm(boid.vel)
                if speed > self.config.MAX_SPEED:
                    boid.vel = boid.vel / speed * self.config.MAX_SPEED
                elif speed < self.config.MIN_SPEED:
                    boid.vel = boid.vel / speed * self.config.MIN_SPEED
            
            boid.pos += boid.vel
            boid.pos[0] = boid.pos[0] % self.config.CANVAS_WIDTH
            boid.pos[1] = boid.pos[1] % self.config.CANVAS_HEIGHT

    def run(self) -> None:
        """Main simulation loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    simulation = BoidSimulation()
    simulation.run()