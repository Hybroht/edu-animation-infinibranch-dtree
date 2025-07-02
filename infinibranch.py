import pygame
import time

pygame.init()

WIDTH, HEIGHT = 900, 300
BACKGROUND_COLOR = (0, 0, 0)
NODE_COLOR = (0, 255, 0)
NODE_SIZE = 20
BRANCH_LENGTH = 60
BRANCH_WIDTH_SCALE = 0.5
MAX_LEVELS = 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fractal Decision Tree with Smooth Pan")


def lerp(start, end, t):
    return start + (end - start) * t


def draw_branch_segment(parent_x, parent_y, child_x, child_y, pan_x, pan_y):
    pygame.draw.line(screen, NODE_COLOR,
                     (parent_x + pan_x, parent_y + NODE_SIZE // 2 + pan_y),
                     (parent_x + pan_x, child_y - NODE_SIZE // 2 + pan_y), 2)
    pygame.draw.line(screen, NODE_COLOR,
                     (min(parent_x, child_x) + pan_x, child_y - NODE_SIZE // 2 + pan_y),
                     (max(parent_x, child_x) + pan_x, child_y - NODE_SIZE // 2 + pan_y), 2)
    pygame.draw.line(screen, NODE_COLOR,
                     (child_x + pan_x, child_y - NODE_SIZE // 2 + pan_y),
                     (child_x + pan_x, child_y + NODE_SIZE // 2 + pan_y), 2)


def draw_tree(x, y, level, max_level, nodes_last_level, pan_x=0, pan_y=0):
    if level > max_level:
        return

    draw_x = x + pan_x
    draw_y = y + pan_y

    pygame.draw.rect(screen, NODE_COLOR,
                     (draw_x - NODE_SIZE // 2, draw_y - NODE_SIZE // 2, NODE_SIZE, NODE_SIZE))

    if level == max_level:
        nodes_last_level.append((x, y))
        return

    horizontal_gap = BRANCH_LENGTH * (2 ** (MAX_LEVELS - level))
    child_y = y + BRANCH_LENGTH
    left_x = x - horizontal_gap*BRANCH_WIDTH_SCALE
    right_x = x + horizontal_gap*BRANCH_WIDTH_SCALE

    draw_branch_segment(x, y, left_x, child_y, pan_x, pan_y)
    draw_branch_segment(x, y, right_x, child_y, pan_x, pan_y)

    draw_tree(left_x, child_y, level + 1, max_level, nodes_last_level, pan_x, pan_y)
    draw_tree(right_x, child_y, level + 1, max_level, nodes_last_level, pan_x, pan_y)


def main():
    running = True
    current_level = 1
    last_update_time = time.time()
    pan_x, pan_y = 0, 0
    panning = False
    pan_duration = 2.0  # seconds to complete pan
    pan_start_time = None
    pan_start_x, pan_start_y = 0, 0
    pan_target_x, pan_target_y = 0, 0

    root_x = WIDTH // 2
    root_y = 0#HEIGHT // 6

    background_snapshot = None  # Global variable to hold the snapshot
    frame_number = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if background_snapshot:
            # Draw the saved background to keep old tree visible
            screen.blit(background_snapshot, (0, 0))
        else:
            # First time or after reset, clear screen
            screen.fill(BACKGROUND_COLOR)

        last_level_nodes = []
        draw_tree(root_x, root_y, 1, current_level, last_level_nodes, pan_x, pan_y)

        now = time.time()

        if not panning and now - last_update_time >= 2:
            if current_level < MAX_LEVELS:
                current_level += 1
                last_update_time = now
            else:
                panning = True
                pan_start_time = now
                pan_start_x, pan_start_y = pan_x, pan_y

                target_node_x, target_node_y = last_level_nodes[-1]
                pan_target_x = root_x - target_node_x
                pan_target_y = root_y - target_node_y

        if panning:
            background_snapshot = None
            elapsed = now - pan_start_time
            t = min(elapsed / pan_duration, 1.0)

            pan_x = lerp(pan_start_x, pan_target_x, t)
            pan_y = lerp(pan_start_y, pan_target_y, t)

            if t >= 1.0:
                # Before resetting pan, capture current screen as background
                background_snapshot = screen.copy()
                panning = False
                current_level = 1
                last_update_time = now
                pan_x, pan_y = 0, 0

        pygame.display.flip()
        pygame.time.delay(30)
        pygame.image.save(screen, f"frames/frame_{frame_number:04d}.png")
        frame_number += 1

    pygame.quit()


if __name__ == "__main__":
    main()