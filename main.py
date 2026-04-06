"""
Arrow : initial condition adjustment
< & > : fine adjustment
1 : toggle information display
2 : toggle vector display
3 : toggle distance display
"""

import pygame
import random
import math
import sys
from constants import *

class Stars:
    def generate(self, num: int):
        star_cords = []
        for i in range(num):
            x = random.randint(0, WINDOW_WIDTH + 300)
            y = random.randint(0, WINDOW_HEIGHT + 300)
            star_cords.append((x, y))
        return star_cords

class Earth:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("images/earth.png"), EARTH_SIZE)
        self.x, self.y = EARTH_CENTER[0] - EARTH_WIDTH / 2, EARTH_CENTER[1]  - EARTH_HEIGHT / 2
        self.mass = EARTH_MASS
        self.radius = EARTH_RADIUS

class Rocket:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("images/rocket.png"), ROCKET_SIZE)
        self.mass = ROCKET_MASS
        self.initialize()
    def initialize(self):
        self.x, self.y = EARTH_CENTER[0] - ROCKET_WIDTH // 2, EARTH_CENTER[1] - ROCKET_HEIGHT // 2 - EARTH_RADIUS
        self.vx, self.vy = 0, 0
        self.currentSpeed = 0
        self.grounded = True
        self.distance = 0
    def move(self, earth: Earth):
        self.x += self.vx * dt / KM_PER_PIXEL
        self.y += self.vy * dt / KM_PER_PIXEL
        
        earthCX = earth.x + EARTH_WIDTH // 2
        earthCY = earth.y + EARTH_HEIGHT // 2

        rocketCX = self.x + ROCKET_WIDTH // 2
        rocketCY = self.y + ROCKET_HEIGHT // 2

        dirX = earthCX - rocketCX
        dirY = earthCY - rocketCY

        r = math.sqrt(dirX ** 2 + dirY ** 2)
        if r <= earth.radius:
            nx = dirX / r
            ny = dirY / r

            self.x = earthCX - nx * earth.radius - ROCKET_WIDTH // 2
            self.y = earthCY - ny * earth.radius - ROCKET_HEIGHT // 2
            self.grounded = True
            self.vx = 0
            self.vy = 0

class PhysicsEngine:
    @staticmethod
    def pull(rocket: Rocket, earth: Earth):
        earthCX = earth.x + EARTH_WIDTH // 2
        earthCY = earth.y + EARTH_HEIGHT // 2

        rocketCX = rocket.x + ROCKET_WIDTH // 2
        rocketCY = rocket.y + ROCKET_HEIGHT // 2

        dirX = earthCX - rocketCX
        dirY = earthCY - rocketCY

        dist_pixel = math.sqrt(dirX ** 2 + dirY ** 2)
        r = dist_pixel * KM_PER_PIXEL
        
        forceMagnitude = G * rocket.mass * earth.mass / r ** 2 / 1000000
        
        fx = dirX / dist_pixel * forceMagnitude
        fy = dirY / dist_pixel * forceMagnitude
        PhysicsEngine.exertForce(fx, fy, rocket)
    @staticmethod
    def exertForce(forceX: float, forceY: float, rocket: Rocket):
        ax = forceX / rocket.mass
        ay = forceY / rocket.mass
        rocket.vx += ax * dt
        rocket.vy += ay * dt
        
class Drawer:
    def __init__(self, screen: pygame.surface.Surface, stars: list, earth: Earth, rocket: Rocket, bar: pygame.Rect):
        self.screen = screen
        self.stars = stars
        self.earth = earth
        self.rocket = rocket
        self.bar = bar
        self.font = pygame.font.SysFont("Menlo", 24)
        self.font2 = pygame.font.SysFont("Menlo", 20)
        self.drawInfo = True
        self.vectorDisplay = True
        self.distanceDisplay = True
    def draw(self, angle: int, speed: float, boostingForce: float, timeElapsed: int):
        self.screen.fill((0, 0, 0))
        self.draw_stars()
        # pygame.draw.circle(self.screen, (255, 255, 255), (EARTH_CENTER), 160)
        if self.distanceDisplay: self.drawDistance()
        self.screen.blit(self.earth.image, (self.earth.x, self.earth.y))
        self.screen.blit(self.rocket.image, (self.rocket.x, self.rocket.y))
        pygame.draw.rect(self.screen, (255, 255, 255), self.bar, 3)
        self.draw_arrows_and_angle(angle)
        self.addText(angle, speed, boostingForce, timeElapsed)
        pygame.display.flip()
    def drawDistance(self):
        x1 = self.rocket.x + ROCKET_WIDTH // 2
        y1 = self.rocket.y + ROCKET_HEIGHT // 2
        x2 = self.earth.x + EARTH_RADIUS
        y2 = self.earth.y + EARTH_RADIUS
        xCords = []
        for i in range(DLDN):
            xCords.append(x1 + (x2 - x1) / DLDN * i)
        
        yCords = []
        for i in range(DLDN):
            yCords.append(y1 + (y2 - y1) / DLDN * i)
        
        for i in range(0, len(xCords) - 1, 3):
            pygame.draw.line(self.screen, (0, 255, 0), (xCords[i], yCords[i]), (xCords[i+1], yCords[i+1]), 1)
    def addText(self, angle: float, speed: float, boostingForce: float, timeElapsed: int):
        self.displayInitial(angle, speed, boostingForce)
        self.displayCalc(timeElapsed)
    def displayInitial(self, angle:float, speed: float, boostingForce: float):
        angle_text1 = self.font.render(f"Angle: {angle}°", True, (255, 255, 255))
        self.screen.blit(angle_text1, (10, 2.5))


        speed_text = self.font.render(f"Speed: {speed:.2f}km/s", True, (255, 255, 255))
        self.screen.blit(speed_text, (10, 42.5))

        force_text = self.font.render(f"Boost Force: {boostingForce:.2f}N", True, (255, 255, 255))
        self.screen.blit(force_text, (10, 82.5))
    def displayCalc(self, timeElapsed: int):
        timePassed = round(timeElapsed / FPS * TIME_SCALE / 3600 / 24)
        timeText = self.font2.render(f"Time Passed: {timePassed}days", True, (255, 255, 255))
        self.screen.blit(timeText, (WINDOW_WIDTH - timeText.get_width(), 2.5))

        earth_center_x = self.earth.x + EARTH_RADIUS
        earth_center_y = self.earth.y + EARTH_RADIUS

        rocket_center_x = self.rocket.x + ROCKET_WIDTH // 2
        rocket_center_y = self.rocket.y + ROCKET_HEIGHT // 2

        distance = Calculator.distance(rocket_center_x, rocket_center_y, earth_center_x, earth_center_y)
        self.rocket.distance = distance * KM_PER_PIXEL

        self.rocket.currentSpeed = round(Calculator.magnitude(self.rocket.vx, self.rocket.vy), 2)

        escapeSpeed = math.sqrt(2 * G * self.earth.mass / self.rocket.distance) / 1000

        kineticEnergy = Calculator.kineticEnergy(self.rocket.mass, self.rocket.currentSpeed * 1000)
        potentialEnergy = Calculator.potentialEnergy(self.rocket.mass, self.earth.mass, self.rocket.distance)

        if self.drawInfo:
            distanceText = self.font2.render(f"Distance: {self.rocket.distance:,.0f}km", True, (255, 255, 255))
            self.screen.blit(distanceText, (WINDOW_WIDTH - distanceText.get_width(), 32.5))

            currentSpeedText = self.font2.render(f"Speed: {self.rocket.currentSpeed:.3f}km/s", True, (255, 255, 255))
            self.screen.blit(currentSpeedText, (WINDOW_WIDTH - currentSpeedText.get_width(), 62.5))

            escapeSpeedText = self.font2.render(f"Escape Speed: {escapeSpeed:,.3f}km/s", True, (255, 255, 255))
            self.screen.blit(escapeSpeedText, (WINDOW_WIDTH - escapeSpeedText.get_width(), 92.5))
            kineticEnergyText = self.font2.render(f"K.E.: {kineticEnergy:,.1f}J", True, (255, 255, 255))
            self.screen.blit(kineticEnergyText, (WINDOW_WIDTH - kineticEnergyText.get_width(), WINDOW_HEIGHT - 62.5))

            potentialEnergyText = self.font2.render(f"P.E.: {potentialEnergy:,.1f}J", True, (255, 255, 255))
            self.screen.blit(potentialEnergyText, (WINDOW_WIDTH - potentialEnergyText.get_width(), WINDOW_HEIGHT - 32.5))

        status = ""
        if self.rocket.currentSpeed > escapeSpeed: status = "Escape"
        elif self.rocket.distance <= EARTH_RADIUS * KM_PER_PIXEL + 100: status = "Crash"
        else: status = "Orbit"
        statusText = self.font2.render(f"Status: {status}", True, (255, 255, 255))
        if self.drawInfo: self.screen.blit(statusText, (WINDOW_WIDTH - statusText.get_width(), 122.5))
        else: self.screen.blit(statusText, (WINDOW_WIDTH - statusText.get_width(), 32.5))

    def draw_arrows_and_angle(self, angle: int):
        x, y = self.rocket.x + ROCKET_WIDTH // 2, self.rocket.y + ROCKET_HEIGHT // 2
        # pygame.draw.line(self.screen, (255, 255, 255), (x, y), (x, y - ARROW_LENGTH), 2)
        # pygame.draw.polygon(self.screen, (255, 255, 255), [(x, y - ARROW_LENGTH), (x - 5, y - ARROW_LENGTH + 5), (x + 5, y - ARROW_LENGTH + 5)])

        # pygame.draw.line(self.screen, (255, 255, 255), (x, y), (x + ARROW_LENGTH, y), 2)
        # pygame.draw.polygon(self.screen, (255, 255, 255), [(x + ARROW_LENGTH, y), (x + ARROW_LENGTH - 5, y - 5), (x + ARROW_LENGTH - 5, y + 5)])
        if self.vectorDisplay: self.draw_dynamic_arrow(angle, x, y)
    def draw_dynamic_arrow(self, angle: int, x: int, y: int):
        rad = math.radians(angle)

        dx = math.cos(rad)
        dy = -math.sin(rad)

        speed = self.rocket.currentSpeed
        if self.rocket.grounded: speed = 10
        end_x = x + speed * ARROW_SCALE * dx
        end_y = y + speed * ARROW_SCALE * dy

        pygame.draw.line( self.screen, (255, 255, 255), (x, y), (end_x, end_y), 2)

        head_length = 7
        head_width = 6
        perp_x = -dy
        perp_y = dx
        left_x = end_x - head_length * dx + head_width * perp_x
        left_y = end_y - head_length * dy + head_width * perp_y
        right_x = end_x - head_length * dx - head_width * perp_x
        right_y = end_y - head_length * dy - head_width * perp_y

        pygame.draw.polygon(self.screen, (255, 255, 255), [(end_x, end_y), (left_x, left_y), (right_x, right_y)])
    def draw_stars(self):
        for x, y in self.stars:
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 1)

class Calculator:
    @staticmethod
    def split(angle: float, magnitude: float):
        theta = math.radians(angle)
        return (magnitude * math.cos(theta), magnitude * -math.sin(theta))
    @staticmethod
    def magnitude(x: float, y: float):
        return math.sqrt(x**2 + y**2)
    @staticmethod
    def angle(x: float, y: float):
        rad = math.atan2(-y, x)
        deg = math.degrees(rad)
        if deg < 0:
            deg += 360
        return round(deg)
    @staticmethod
    def distance(x1, y1, x2, y2):
        return Calculator.magnitude(abs(x2 - x1), abs(y2 - y1))
    @staticmethod
    def kineticEnergy(mass: int, speed: float):
        return mass * speed ** 2 / 2
    @staticmethod
    def potentialEnergy(mass1: int, mass2: int, r: float):
        if r == 0: return 0
        return -G * mass1 * mass2 / (r * 1000)

class Simulator:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.star_generator = Stars()
        self.stars = self.star_generator.generate(400)
        self.earth = Earth()
        self.rocket = Rocket()

        self.initialize()
    def initialize(self):
        self.option = 1
        self.bar = pygame.Rect(0, 0, 300, 35)    
        self.drawer = Drawer(self.screen, self.stars, self.earth, self.rocket, self.bar)
        self.angle = 45
        self.speed = 9.2
        self.boostForce = 50
        self.timeElasped = 0
        self.firingVx, self.firingVy = 0, 0
        self.spaceDownForFire = False

        self.rocket.initialize()
    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(FPS)
            self.update()
            self.drawer.draw(self.angle, self.speed, self.boostForce, self.timeElasped)
    def update(self):
        self.timeElasped += 1
        self.handle_events()
        self.rocket.move(self.earth)
        if not self.rocket.grounded:
            PhysicsEngine.pull(self.rocket, self.earth)
            if self.timeElasped * dt / TIME_SCALE <= MAINTAIN_TIME:
                self.rocket.vx += self.firingVx / MAINTAIN_TIME / FPS
                self.rocket.vy += self.firingVy / MAINTAIN_TIME / FPS
            self.angle = Calculator.angle(self.rocket.vx, self.rocket.vy)
            print(f"angle: {self.angle}")
    def adjustCondition(self, sign: int):
        if self.option == 1:
            if self.angle < 0: self.angle += 360
            if self.angle > 360: self.angle -= 360
            self.angle = round(self.angle - sign, 1)
        elif self.option == 2:
            if self.speed + sign / 20 < 0: return
            self.speed = round(self.speed + sign / 20, 2)
        elif self.option == 3:
            if self.boostForce + sign < 0: return
            self.boostForce = round(self.boostForce + sign, 2)
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.option <= 1: continue
                    self.option -= 1
                    self.bar.y -= 40
                if event.key == pygame.K_DOWN:
                    if self.option >= 3: continue
                    self.option += 1
                    self.bar.y += 40
                if event.key == pygame.K_COMMA:
                    self.adjustCondition(-1)
                if event.key == pygame.K_PERIOD:
                    self.adjustCondition(1)
                if event.key == pygame.K_SPACE and self.rocket.grounded:
                    self.fire()
                    self.spaceDownForFire = True
                if event.key == pygame.K_l:
                    print(self.rocket.x, self.rocket.y)
                if event.key == pygame.K_r:
                    self.initialize()
                
                if event.key == pygame.K_1:
                    self.toggleInfo()
                if event.key == pygame.K_2:
                    self.toggleVectorDisplay()
                if event.key == pygame.K_3:
                    self.toggleDistDisplay()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.spaceDownForFire = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.adjustCondition(-1)
        if keys[pygame.K_RIGHT]:
            self.adjustCondition(1)
        
        if not self.spaceDownForFire and not self.rocket.grounded and keys[pygame.K_SPACE]:
            self.boost()
    def toggleInfo(self):
        self.drawer.drawInfo = not self.drawer.drawInfo
    def toggleVectorDisplay(self):
        self.drawer.vectorDisplay = not self.drawer.vectorDisplay
    def toggleDistDisplay(self):
        self.drawer.distanceDisplay = not self.drawer.distanceDisplay
    def boost(self):
        print("boosting!")
        fx, fy = Calculator.split(self.angle, self.boostForce)
        PhysicsEngine.exertForce(fx, fy, self.rocket)
    def fire(self):
        print("fire!")
        self.timeElasped = 0
        self.firingVx, self.firingVy = Calculator.split(self.angle, self.speed)
        # PhysicsEngine.exertForce(fx * self.rocket.mass, fy * self.rocket.mass, self.rocket)
        # self.rocket.vx, self.rocket.vy = self.firingVx, self.firingVy
        self.rocket.grounded = False
    def terminate(self):
        pygame.quit()
        sys.exit()

def main():
    simulator = Simulator()
    simulator.run()

if __name__ == "__main__":
    main()
