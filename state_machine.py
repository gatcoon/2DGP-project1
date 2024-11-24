from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_UP

# 이벤트 정의
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def jump_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def land(e):
    return e[0] == 'LAND'


class StateMachine:
    def __init__(self, obj):
        self.obj = obj
        self.event_queue = []

    def start(self, initial_state):
        self.cur_state = initial_state
        self.cur_state.enter(self.obj, ('START', None))

    def add_event(self, event):
        self.event_queue.append(event)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def update(self):
        self.cur_state.do(self.obj)
        if self.event_queue:
            event = self.event_queue.pop(0)
            self.handle_event(event)

    def draw(self):
        self.cur_state.draw(self.obj)

    def handle_event(self, event):
        for condition, next_state in self.transitions[self.cur_state].items():
            if condition(event):
                self.cur_state.exit(self.obj, event)
                self.cur_state = next_state
                self.cur_state.enter(self.obj, event)
                return
