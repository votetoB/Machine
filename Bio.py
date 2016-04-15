import pygame
import math
from trace import Trace, Point


class Bio:
    def __init__(self):
        self.radius = 250
        self.center = 350, 260
        self.KT = self.radius, self.radius
        self.time = 0
        # angle in degrees
        self.sweep_line_angle = 0
        self.traces = []
        self.current_temp_places = []
        self.init_traces()
        self.current_places = []

        self.traces_are_visible = False
        self.temp_places_are_visible = False

    def swap_traces_visibility(self):
        self.traces_are_visible = 1 - self.traces_are_visible

    def swap_temp_places_visibility(self):
        self.temp_places_are_visible = 1 - self.temp_places_are_visible

    def get_angle_in_radians(self):
        return (self.sweep_line_angle * math.pi) / 180

    def init_traces(self):
        with open('1.tra', 'r') as f:
            trace_number = int(f.readline())
            for trace_counter in range(trace_number):
                t = Trace()
                point_number = int(f.readline())
                points = []
                for point_counter in range(point_number):
                    point_s = f.readline()[:-1]
                    point = Point([int(x) for x in point_s.split(' ')])
                    points.append(point)
                t.points = points
                self.traces.append(t)
                self.current_temp_places.append(None)


    def get_traces_collisions(self):
        for tr in self.traces:
            for i in range(1, len(tr.points)):
                if tr.points[i].t > self.time > tr.points[i-1].t:

                    p0 = tr.points[i-1]
                    p1 = tr.points[i]
                    k = (self.time - p0.t) / float(p1.t - p0.t)
                    pm_x = p0.x + (p1.x - p0.x) * k
                    pm_y = p0.y + (p1.y - p0.y) * k
                    self.current_temp_places[0] = pm_x + self.radius, pm_y + self.radius
                    if abs(math.atan2(pm_y, pm_x) - self.get_angle_in_radians()) < 0.01:
                        self.current_places.append((pm_x + self.radius, pm_y + self.radius))

    def draw(self, surface):
        s = pygame.Surface((self.radius * 2, self.radius * 2))
        s.fill((255,255,255))

        pygame.draw.circle(s, (0, 0, 0), (self.radius, self.radius), self.radius)

        if self.traces_are_visible:
            for t in self.traces:
                pointlist = []
                for p in t.points:
                    pointlist.append((p.x + self.radius, p.y + self.radius))

                pygame.draw.aalines(s, (0, 0, 255), 0, pointlist)

        angle_in_radians = self.get_angle_in_radians()

        pygame.draw.aaline(s, (0, 255, 0), (self.radius, self.radius), (self.radius * (1 + math.cos(angle_in_radians)),
                                                                      self.radius * (1 + math.sin(angle_in_radians))))

        pygame.draw.circle(s, (255, 255, 0), self.KT, 2)

        if self.temp_places_are_visible:
            for c_p in self.current_temp_places:
                pygame.draw.circle(s, (125, 125, 255), (int(c_p[0]), int(c_p[1])), 2)
        for c_p in self.current_places:
            pygame.draw.circle(s, (255, 0, 255), (int(c_p[0]), int(c_p[1])), 2)

        surface.blit(s, (self.center[0] - self.radius, self.center[1] - self.radius))

    def tick(self):
        self.sweep_line_angle += 1
        self.sweep_line_angle %= 360
        self.time += 1
        self.remove_needless_points()
        self.get_traces_collisions()

    def remove_needless_points(self):
        for c_p in self.current_places:
            if (math.acos(c_p[1] / (c_p[0] ** 2 + c_p[1] ** 2) ** 0.5) - self.get_angle_in_radians()) % (2 * math.pi) < 1:
                self.current_places.remove(c_p)
                return


    def on_click(self, pos):
        self.KT = pos[0] - (self.center[0] - self.radius), pos[1] - (self.center[1] - self.radius)

    def collides(self, pos):
        return math.sqrt((self.center[0] - pos[0]) ** 2 + (self.center[1] - pos[1]) ** 2) <= self.radius
