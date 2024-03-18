import pygame, sys, color, Map, heapq

pygame.init()
clock = pygame.time.Clock()

def heuristic(pos1, pos2):
    rect = [abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1])]
    return min(rect)*14+abs(rect[0]-rect[1])*10

if __name__ == "__main__":
    size = (width, height) = (800, 800)
    screen = pygame.display.set_mode(size)
    screen.fill(color.white)

# Create Map
    map = Map.Map(size, 20)
    map.gridon()

    switch_mode = False

    while map.mode != 4:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and switch_mode == False:
                switch_mode = True
                map.mode = 2

        map.mode = map.createMap() 
        screen.fill(color.white) 
        map.draw(screen)

        pygame.display.flip()

# Find shortest path with Astar
    neighbors = ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))

    visited_point = []
    connections = []
    map.matrix[map.start[0]][map.start[1]] = [0, heuristic(map.start, map.end)]
    connections.append([sum(map.matrix[map.start[0]][map.start[1]]), map.start, map.start])

    solved = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        clock.tick(60)

        if len(connections) == 0:
            break

        curr = min(connections)
        connections.remove(curr)
        visited_point.append(curr)
        node = curr[1]

        if node == map.end:
            solved = True
            break

        for i in neighbors:
            new_node = [node[0]+i[0], node[1]+i[1]]
            if map.matrix[new_node[0]][new_node[1]] == 1:
                map.matrix[new_node[0]][new_node[1]] = [heuristic(new_node, node)+map.matrix[node[0]][node[1]][0], heuristic(new_node, map.end)]
                connections.append([sum(map.matrix[new_node[0]][new_node[1]]), new_node, node])
                map.fill_cell(new_node, color.red)
            elif map.matrix[new_node[0]][new_node[1]] == 0:
                pass
            else:
                f = [heuristic(new_node, node)+map.matrix[node[0]][node[1]][0], heuristic(new_node, map.end)]
                if sum(f) < sum(map.matrix[new_node[0]][new_node[1]]):
                    map.matrix[new_node[0]][new_node[1]] = f
                    for index, cnt in enumerate(connections):
                        if cnt[1] == new_node:
                            connections[index] = [sum(f), new_node, node]
                            break
        map.matrix[node[0]][node[1]] = 0
        screen.fill(color.white) 
        map.draw(screen)

        pygame.display.flip()

# Show path
    if solved == False:
        print('There no path')
    else:
        v = map.end
        idx = len(visited_point) - 1

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if v != map.start:
                for i in range(idx, -1, -1):
                    if visited_point[i][1] == v:
                        v = visited_point[i][2]
                        l = i
                        map.fill_cell(v, color.darkgreen)
                        break

            screen.fill(color.white) 
            map.fill_cell(map.start, color.green)
            map.fill_cell(map.end, color.blue)
            map.gridon()
            map.draw(screen)

            pygame.display.flip()
