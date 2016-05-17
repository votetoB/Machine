#  -*- coding: utf-8 -*-
import pygame
import math
from trace import Trace, Point, SupportPoint, SupportTrace
MARKER_COLOR = (255, 255, 255)
ET_COLOR = (255, 255, 0)
DEFAULT_COLOR = (0, 255, 0)
KNOWN_COLOR = (255, 0, 128)
ALIEN_COLOR = (0, 255, 255)
DISASTER_COLOR = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MARKS = [u'Г', u'В', u'А', u'К', u'Ш']


class Bio:
    def __init__(self):
        self.radius = 250
        self.center = 350, 260
        self.KT = self.radius, self.radius
        self.time = 0
        # angle in degrees
        self.sweep_line_angle = 0
        self.traces = []
        self.support_traces = []
        self.current_temp_places = []
        self.init_traces()
        self.current_places = []
        self.signs = []
        self.traces_are_visible = False
        self.temp_places_are_visible = False
        self.tasks_stack = []
        self.tasks_line = dict.fromkeys(range(0, 360))

    @staticmethod
    def get_point_angle_0(point):
        point1 = point[0] - 250, point[1] - 250
        answer = int((math.acos(point1[1] / (point1[0] ** 2 + point1[1] ** 2) ** 0.5) - 0) % (2 * math.pi) * 180 / math.pi)
        if point1[0] < 0:
            return answer + 90
        else:
            return (90 - answer) % 360

    def get_point_angle_diff(self, point):
        return (math.acos(point[1] / (point[0] ** 2 + point[1] ** 2) ** 0.5) -
                self.get_angle_in_radians()) % (2 * math.pi)

    def allow_task(self, s):
        if s == 'first_enter':
            return len(self.tasks_stack) < 2 and len(self.support_traces) < 1
        elif s == 'simple_correction':
            return len(self.tasks_stack) < 2 and len(self.support_traces) > 0
        elif s == 'special_correction1':
            return len(self.tasks_stack) < 2 and len(self.support_traces) > 0 and len(self.support_traces[0].points) > 1
        elif s == 'special_correction2':
            return len(self.tasks_stack) < 2 and len(self.support_traces) > 0

        raise Exception

    def analyze_line(self):
        if self.tasks_line[self.sweep_line_angle]:
            task = self.tasks_line[self.sweep_line_angle]
            print task[0]
            if task[0] == 'first_enter':
                points = list()
                points.append(SupportPoint(task[1][0], task[1][1], 1, (0, 0)))
                new_t = SupportTrace(points)
                new_t.ET = task[1]
                new_t.energy = 5
                self.support_traces.append(new_t)
                self.tasks_line[self.sweep_line_angle] = ["support"]

            elif task[0] == 'simple_correction':
                # УЖАСНЫЙ КОСТЫЛЬ
                self.tasks_line = dict.fromkeys(range(0, 360))

                sup_trace = self.support_traces[0]
                vec_x, vec_y = task[1][0] - sup_trace.points[-1].x, task[1][1] - sup_trace.points[-1].y
                sup_trace.points.append(SupportPoint(task[1][0], task[1][1], 1, (vec_x, vec_y)))
                sup_trace.ET = task[1][0] + vec_x, task[1][1] + vec_y
                sup_trace.energy = 5
                self.tasks_line[self.sweep_line_angle] = ["support"]

            elif task[0] == 'special_correction1':
                # УЖАСНЫЙ КОСТЫЛЬ
                self.tasks_line = dict.fromkeys(range(0, 360))
                sup_trace = self.support_traces[0]
                sup_trace.points[-1].x, sup_trace.points[-1].y = task[1]
                sup_trace.ET = self.KT[0] + sup_trace.points[-1].vector[0], self.KT[1] + sup_trace.points[-1].vector[1]
                sup_trace.energy = 5
                self.tasks_line[self.sweep_line_angle] = ["support"]

            elif task[0] == 'special_correction2':
                print "NOT ENOUGH MEMORY"

            elif task[0] == "support":
                trace = self.support_traces[0]
                if len(trace.points) == 1:
                    trace.energy -= 1
                else:
                    trace.points.append(SupportPoint(trace.ET[0], trace.ET[1], trace.points[-1].s, trace.points[-1].vector))
                    trace.ET = trace.ET[0] + trace.points[-2].vector[0], trace.ET[1] + trace.points[-2].vector[1]
                    trace.energy -= 1

                self.tasks_line[self.sweep_line_angle] = None
                if trace.energy == 0:
                    self.support_traces = []
                    return
                else:
                    if (self.get_point_angle_0(trace.ET) - self.sweep_line_angle) % 360 < 30:
                        self.tasks_line[self.get_point_angle_0(trace.ET)] = ["support"]
                    else:
                        self.tasks_line[self.get_point_angle_0(trace.ET)] = ["support_delayed"]
            elif task[0] == "support_delayed":
                task[0] = "support"



    def analyze_stack(self):
        task = self.tasks_stack[0]
        if self.allow_task(task[0]):
            self.signs.append([u"П", task[1]])

            angle = self.get_point_angle_0(task[1])
            while self.tasks_line[angle] is not None:
                angle = (angle + 1) % 360
            self.tasks_line[angle] = task
        else:
            self.signs.append(['O', task[1]])

        self.tasks_stack.remove(task)

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
                        self.current_places.append((pm_x + self.radius, pm_y + self.radius, tr.points[i-1].s))

    @staticmethod
    def write_text_label(surface, sign):
        if not sign:
            return surface
        if len(sign[0]) == 0:
            return surface
        font_size = 9
        myFont = pygame.font.SysFont("Arial", font_size)
        myText = myFont.render(sign[0], 1, DEFAULT_COLOR)
        surface.blit(myText, sign[1])

    def draw(self, surface, machine):
        s = pygame.Surface((self.radius * 2, self.radius * 2))
        s.fill(WHITE)

        pygame.draw.circle(s, BLACK, (self.radius, self.radius), self.radius)

        if machine.is_on:
            if self.traces_are_visible:
                for t in self.traces:
                    for k in range(1, len(t.points)):
                        if t.points[k - 1].s == 1:
                            tr_color = KNOWN_COLOR
                        elif t.points[k - 1].s == 2:
                            tr_color = ALIEN_COLOR
                        else:
                            tr_color = DISASTER_COLOR
                        pygame.draw.aaline(s, tr_color, (t.points[k-1].x + self.radius, t.points[k-1].y + self.radius),
                                           (t.points[k].x + self.radius, t.points[k].y + self.radius))

            angle_in_radians = self.get_angle_in_radians()

            pygame.draw.aaline(s, DEFAULT_COLOR, (self.radius, self.radius), (self.radius * (1 + math.cos(angle_in_radians)),
                                                                          self.radius * (1 + math.sin(angle_in_radians))))

            if self.temp_places_are_visible:
                for c_p in self.current_temp_places:
                    pygame.draw.circle(s, (125, 125, 255), (int(c_p[0]), int(c_p[1])), 2)

            for s_t in self.support_traces:
                for k in range(1, len(s_t.points)):
                    if s_t.points[k - 1].s == 1:
                        tr_color = KNOWN_COLOR
                    elif s_t.points[k - 1].s == 2:
                        tr_color = ALIEN_COLOR
                    else:
                        tr_color = DISASTER_COLOR
                    pygame.draw.aaline(s, tr_color, (s_t.points[k-1].x, s_t.points[k-1].y),
                                       (s_t.points[k].x, s_t.points[k].y))

                Bio.write_text_label(s, ("+" + MARKS[-s_t.energy], s_t.ET))

                if s_t.ET:
                    pygame.draw.circle(s, ET_COLOR, s_t.ET, 1)

            for sign in self.signs:
                Bio.write_text_label(s, sign)

            for c_p in self.current_places:
                self.draw_sign(s, c_p)

            pygame.draw.circle(s, MARKER_COLOR, self.KT, 2)

        surface.blit(s, (self.center[0] - self.radius, self.center[1] - self.radius))

    def draw_sign(self, s, point):
        """
        Draws ECHO signal
        :param s: surface
        :param point: point where to draw
        :return: None
        """
        angle = Bio.get_point_angle_0(point)
        center = 250, 250
        r = math.hypot(center[0] - point[0], center[1] - point[1])
        pygame.draw.arc(s, DEFAULT_COLOR, (center[0] - r, center[1] - r, 2 * r, 2 * r), -angle/180.0 * math.pi, -(angle - 5)/180.0 * math.pi, 2)

        # angle = math.acos(point[1] / (point[0] ** 2 + point[1] ** 2) ** 0.5)
        # start_point = 250 + 250 * math.cos(angle - 3 / 100.0), 250 + 250 * math.sin(angle - 3 / 100.0)
        # print start_point
        # for i in range(-2, 3):
        #     cur_point = 250 + 250 * math.cos(angle + i/100.0), 250 + 250 * math.sin(angle + i/100.0)
        #     pygame.draw.line(s, DEFAULT_COLOR, start_point, cur_point, 1)
        #     start_point = cur_point
        # color = DEFAULT_COLOR
        #
        # if point[2] == 1:
        #     # KNOWN
        #     color = KNOWN_COLOR
        # elif point[2] == 2:
        #     # ALIEN
        #     color = ALIEN_COLOR
        # elif point[2] == 3:
        #     # DISASTER
        #     color = DISASTER_COLOR

        ## pygame.draw.circle(s, DISASTER_COLOR, (int(point[0]), int(point[1])), 2)

    def tick(self):
        self.sweep_line_angle += 1
        self.sweep_line_angle %= 360
        self.time += 1
        self.prepare_next_circle()
        self.get_traces_collisions()
        if self.tasks_stack:
            self.analyze_stack()
        self.analyze_line()

    def prepare_next_circle(self):
        # Убирем предыдущие эхосигналы
        for c_p in self.current_places:
            if (math.acos(c_p[1] / (c_p[0] ** 2 + c_p[1] ** 2) ** 0.5) -
                    self.get_angle_in_radians()) % (2 * math.pi) < 0.1:
                self.current_places.remove(c_p)
                break

        # Трассы поддержки
        for t in self.support_traces:
            # Убираем лишние квитанции трасс
            if t.sign:
                c_p = t.sign[1][0] - self.radius, t.sign[1][1] - self.radius
                if (math.acos(c_p[1] / (c_p[0] ** 2 + c_p[1] ** 2) ** 0.5) -
                        self.get_angle_in_radians()) % (2 * math.pi) < 1:
                    t.sign = None
                    break
        # Убираем лишние квитанции оператору
        for sign in self.signs:
            c_p = sign[1][0] - self.radius, sign[1][1] - self.radius
            if (math.acos(c_p[1] / (c_p[0] ** 2 + c_p[1] ** 2) ** 0.5) -
                    self.get_angle_in_radians()) % (2 * math.pi) < 1:
                self.signs.remove(sign)
                break

    def on_click(self, pos):
        self.KT = pos[0] - (self.center[0] - self.radius), pos[1] - (self.center[1] - self.radius)

    def collides(self, pos):
        return math.sqrt((self.center[0] - pos[0]) ** 2 + (self.center[1] - pos[1]) ** 2) <= self.radius
