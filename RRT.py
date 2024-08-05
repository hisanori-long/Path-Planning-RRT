import pygame
from pygame.locals import *
from RRTbase import RRTGraph
from RRTbase import RRTMap
import sys


def main():
    dimensions = (600, 1000) # maph, mapw
    start = (50, 50)
    goal = (510, 510)
    obsdim = 30
    obsnum = 50
    iteration = 0

    pygame.init()
    map = RRTMap(start, goal, dimensions, obsdim, obsnum)
    graph = RRTGraph(start, goal, dimensions, obsdim, obsnum)

    obstacles = graph.makeObs()

    map.drawMap(obstacles)

    while (not graph.path_to_goal()):
        if iteration % 10 == 0:
            X, Y, Parent = graph.bias(goal)
            pygame.draw.circle(map.map, map.grey, (X[-1], Y[-1]), map.nodeRad + 2, 0)
            pygame.draw.line(map.map, map.blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]), map.edgeThickness)

        else:
            X, Y, Parent = graph.expand()
            pygame.draw.circle(map.map, map.grey, (X[-1], Y[-1]), map.nodeRad + 2, 0)
            pygame.draw.line(map.map, map.blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]), map.edgeThickness)

        if iteration % 1 == 0:
            pygame.display.update()
            pygame.event.wait(20)
        iteration += 1

    map.drawPath(graph.getPathCoords())

    while True:

        # 描画を更新
        pygame.display.update()
        pygame.event.clear()
        pygame.event.wait(0)

        # システムを終了する
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            else:
                main()


if __name__ == '__main__':
    main()