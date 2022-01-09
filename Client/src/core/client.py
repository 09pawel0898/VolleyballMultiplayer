from src.core.states.stateManager import *
from src.states.mainmenu.mainMenuState import MainMenuState
from src.states.gameplay.gameplayState import *
from src.core.resources.texture import *
from src.networking.serverAPI.user import User, user

class Client:
    user : User = user

    def __init__(self, viewport_x: int, viewport_y: int) -> None:
        self._window = pygame.display.set_mode([viewport_x, viewport_y])
        pygame.display.set_caption("Volleyball")
        self._running = False
        self._texture_manager = ResourceManager[Texture]()
        self._context = Context(self._window, self._texture_manager)
        self._state_manager = StateManager(self._context)
        self._init_states()
        self._get_ticks_last_frame = 0.0
        self._dt = 0

    def _init_states(self):
        self._state_manager.register_state("MainMenuState",MainMenuState)
        self._state_manager.register_state("GameplayState",GameplayState)

    def _update(self,delta_time: Optional[float] = None) -> None:
        if delta_time is not None:
            self._state_manager.on_update(delta_time)
        else:
            curr_time = pygame.time.get_ticks()
            dt = (curr_time - self._get_ticks_last_frame) / 1000.0
            self._get_ticks_last_frame = curr_time
            self._state_manager.on_update(dt)


    def _render(self) -> None:
        self._window.fill((255, 255, 255))
        self._state_manager.on_render()
        pygame.display.flip()


    def _process_events(self) -> None:
        temp_events = pygame.event.get()
        self._state_manager.on_event(temp_events)
        for event in temp_events:
            if event.type == pygame.QUIT:
                self._running = False


    def run(self) -> None:
        self._running = True
        self._state_manager.push_state("MainMenuState")
        clock = pygame.time.Clock()
        pygame.init()
        while self._running:
            self._dt = clock.tick(60)
            self._process_events()
            self._update(self._dt)
            self._render()
        pygame.quit()
