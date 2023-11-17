import matplotlib.pyplot as plt
import numpy as np
import random


fig, ax = plt.subplots()
ax.set_xlim([0, 100])
ax.set_ylim([0, 100])


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.scat = ax.scatter(x, y, s=3*50, label=f"Point at ({x}, {y})")


class Agent(object):
    _id_counter = 0

    def __init__(self, x, y, target_point=None):
        self.id = Agent._id_counter
        Agent._id_counter += 1
        self.x = x
        self.y = y
        self.target_point = target_point
        self.scat = ax.scatter(x, y, label=f"Agent {self.id}")
        angle = random.uniform(0, 2 * np.pi)
        self.directionx = np.cos(angle)
        self.directiony = np.sin(angle)
        self.steps_since_collisions = [0, 0]

    def update_position(self, points):
        self.steps_since_collisions = [x + 1 for x in self.steps_since_collisions]
        self.x += self.directionx
        self.y += self.directiony
        if self.x > 100 or self.x < 0 or self.detect_collision(points):
            self.directionx *= -1
            self.x = max(min(self.x, 100), 0)
        if self.y > 100 or self.y < 0 or self.detect_collision(points):
            self.directiony *= -1
            self.y = max(min(self.y, 100), 0)
        self.scat.set_offsets((self.x, self.y))

    def detect_collision(self, points):
        for point in points:
            distance = np.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)
            if distance <= 3:
                self.record_collision(0)
                self.target_point = point
                return True
        return False

    def detect_nearby_agents(self, agents):
        for agent in agents:
            if agent.id != self.id:
                distance = np.sqrt((self.x - agent.x) ** 2 + (self.y - agent.y) ** 2)
                if distance <= 10:
                    self.record_collision(1)
                    if agent.steps_since_collisions[1] < self.steps_since_collisions[1]:
                        self.steps_since_collisions[1] = agent.steps_since_collisions[1]
                        if agent.target_point == self.target_point:
                            self.turn_towards(agent.x, agent.y)

    def turn_towards(self, x, y):
        self.directionx = x - self.x
        self.directiony = y - self.y
        length = np.sqrt(self.directionx**2 + self.directiony**2)
        self.directionx /= length
        self.directiony /= length

    def record_collision(self, index):
        self.steps_since_collisions[index] = 0

    def announce(self):
        print(f"Agent {self.id} шагов после столкновения: {self.steps_since_collisions}")


points = [Point(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(2)]
agents = [Agent(random.uniform(0, 100), random.uniform(0, 100), target_point=points[0]) for _ in range(50)]


def update_agents():
    for agent in agents:
        agent.update_position(points)
        agent.detect_nearby_agents(agents)
        agent.announce()
    fig.canvas.draw_idle()
    plt.pause(0.1)





max_iterations = 5000
for _ in range(max_iterations):
    update_agents()


ax.legend()
plt.show()
