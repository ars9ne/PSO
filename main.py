import matplotlib.pyplot as plt
import numpy as np
import random


fig, ax = plt.subplots()
ax.set_xlim([0, 100])
ax.set_ylim([0, 100])
hdist = 10

class Point(object):
    _id_counter = 0

    def __init__(self, x, y):
        self.id = Point._id_counter
        Point._id_counter += 1
        self.x = x
        self.y = y
        self.scat = ax.scatter(x, y, s=3*50, label=f"Point at ({x}, {y})")

        self.text = ax.text(x, y, f"{self.id}", fontsize=9, ha='right')

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
        self.text = ax.text(x, y, f"{self.id}", fontsize=9, ha='right')


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
        self.text.set_position((self.x, self.y))

    def detect_collision(self, points):
        for point in points:
            distance = np.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)
            if distance <= 3:
                self.record_collision(point.id)
                self.target_point = points[1] if point.id == 0 else points[0]
                return True
        return False

    def detect_nearby_agents(self, agents):
        for agent in agents:
            if agent.id != self.id:
                distance = np.sqrt((self.x - agent.x) ** 2 + (self.y - agent.y) ** 2)
                if distance <= hdist:
                    if agent.steps_since_collisions[1] + hdist < self.steps_since_collisions[1]:
                        self.steps_since_collisions[1] = agent.steps_since_collisions[1] + hdist
                        if (agent.steps_since_collisions[1] < self.steps_since_collisions[1] + hdist):
                            self.turn_towards(agent.x, agent.y)
                    elif agent.steps_since_collisions[0] + hdist < self.steps_since_collisions[0]:
                        self.steps_since_collisions[0] = agent.steps_since_collisions[0] + hdist
                        if (
                                agent.steps_since_collisions[1] < self.steps_since_collisions[1] + hdist):
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
        target_point_id = self.target_point.id if self.target_point else None
        # pass print(f"Agent {self.id} шагов после столкновения: {self.steps_since_collisions} TARGET POINT ID: {target_point_id}")
        pass

points = [Point(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(2)]
agents = [Agent(random.uniform(0, 100), random.uniform(0, 100), target_point=points[0]) for _ in range(50)]


def update_agents():
    for agent in agents:
        agent.update_position(points)
        agent.detect_nearby_agents(agents)
        agent.announce()
    fig.canvas.draw_idle()
    plt.pause(0.01)
    #print('\n')





max_iterations = 500000
for _ in range(max_iterations):
    update_agents()


ax.legend()
plt.show()