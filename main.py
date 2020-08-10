import numpy as np
import pygame

def main(num_plates):
    pygame.init()
    run = True
    WHITE = pygame.color.Color(255, 248, 214)

    s_height = 400
    s_width = 800
    size = [s_width, s_height]
    screen = pygame.display.set_mode(size)
    screen.fill(WHITE)
    selected = None

    list_plates = []

    clock = pygame.time.Clock()


    class Region:
        range = pygame.Rect(0, 0, 0, 0)

        def __init__(self, n):
            self.n = n
            if n == 1:
                self.range = pygame.Rect(0, 0, s_width / 3, s_height)
            elif n == 2:
                self.range = pygame.Rect(s_width / 3, 0, s_width / 3, s_height)
            elif n == 3:
                self.range = pygame.Rect(s_width * 2 / 3, 0, s_width / 3, s_height)

        # rects = []
        def get_rects(self):
            rects = []
            def func(x):
                return x.y
            for r in list_plates:
                if self.range.collidepoint(r.center):
                    rects.append(r)
            rects = sorted(rects, key=func)
            rects.reverse()
            return rects

        # y_height = 0
        def get_height(self):
            n = len(self.get_rects()) - 1
            return 350 - (20 * n)


    class HanoiGame:
        reg1 = Region(1)
        reg2 = Region(2)
        reg3 = Region(3)
        game_end = False
        game_started = False
        n = 0

        def __init__(self, n):
            x = 20
            y_pos = 350
            h = 20
            self.n = n
            for i in range(n):
                min_w = 50
                max_w = 300
                w_diff = max_w - min_w
                y = y_pos - i * 20
                w = np.flip(np.arange(min_w, max_w, w_diff / n, dtype=int))[i]
                if i > 0:
                    x = x + (w_diff / n) - (w_diff / (n * 2))

                p = pygame.Rect((x, y), (w, h))
                list_plates.append(p)

        def get_region(self, coor):
            if self.reg1.range.collidepoint(coor):
                return self.reg1
            elif self.reg2.range.collidepoint(coor):
                return self.reg2
            elif self.reg3.range.collidepoint(coor):
                return self.reg3
            else:
                return None

    h = HanoiGame(num_plates)
    while run:
        n = h.n
        if h.reg1.get_rects() != list_plates:
            h.game_started = True
        for event in pygame.event.get():

            # --- global events ---
            if event.type == pygame.QUIT:
                run = False
                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif not h.game_started and int(pygame.key.name(event.key)):
                    print("new game")
                    main(int(pygame.key.name(event.key)))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    rects = h.get_region(event.pos).get_rects()
                    for i, r in enumerate(rects):
                        if r.y == 350 - ((len(rects) - 1) * 20):
                            if r.collidepoint(event.pos):
                                selected = r
                                selected_offset_x = r.x - event.pos[0]
                                selected_offset_y = r.y - event.pos[1]
                    if h.game_end:
                        if playrect.collidepoint(event.pos):
                            if event.pos[0] > 365:
                                main(num_plates)
                            else:
                                run = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if selected is not None:
                        rect = selected
                        region = h.get_region(rect.center)
                        x_middle = region.range.centerx
                        rect.centerx = x_middle
                        rect.y = region.get_height()
                        selected = None

            elif event.type == pygame.MOUSEMOTION:
                if selected is not None:  # selected can be `0` so `is not None` is required
                    # move object
                    selected.x = event.pos[0] + selected_offset_x
                    selected.y = event.pos[1] + selected_offset_y

            # --- objects events ---

            '''
           button.handle_event(event)
           '''

            # --- updates ---

            # empty

            # --- draws ---

        screen.fill(WHITE)
        # ---- end game ----
        if h.reg3.get_rects() == list_plates:
            h.game_end = True
            font = pygame.font.Font('freesansbold.ttf', 32)
            smaller = pygame.font.Font('freesansbold.ttf', 20)
            text = font.render('You Win!!', True, (242, 142, 70))
            play_again = smaller.render('Quit   Play Again', True, (212, 124, 61))
            textRect = text.get_rect()
            playrect = play_again.get_rect()
            textRect.center = (s_width // 2, s_height // 2)
            playrect.center = (s_width/2, s_height / 2 + 40)
            screen.blit(text, textRect)
            screen.blit(play_again, playrect)

        '''
        button.draw(screen)    
        '''

        # draw rects
        for ind in range(len(list_plates)):
            colr = pygame.color.Color(255, 255, 102)
            dark_colr = pygame.color.Color(16, 145, 140)
            r = int(np.arange(dark_colr.r, colr.r, (colr.r - dark_colr.r) / n, dtype=int)[ind])
            g = int(np.arange(dark_colr.g, colr.g, (colr.g - dark_colr.g) / n, dtype=int)[ind])
            b = int(np.arange(dark_colr.b, colr.b, (colr.b - dark_colr.b) / n, dtype=int)[ind])
            dcolr = pygame.color.Color(r, g, b)

            pygame.draw.rect(screen, dcolr, list_plates[ind])

        # e = Region(1)
        # f = Region(2)
        # g = Region(3)
        # print(e.get_rects())
        # # print(e.range.collidepoint(list_plates[1].center))
        # # pygame.draw.rect(screen, (0, 255, 0), e.range)
        # # pygame.draw.rect(screen, (0, 0, 255), f.range)
        # # pygame.draw.rect(screen, (255, 0, 0), g.range)

        pygame.display.update()

        # --- FPS ---

        # clock.tick(25)

    pygame.display.quit()
    pygame.quit()

main(3)