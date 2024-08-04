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
    interaction = 0

    pygame.init()
    map = RRTMap(start, goal, dimensions, obsdim, obsnum)
    graph = RRTGraph(start, goal, dimensions, obsdim, obsnum)

    obstacles = graph.makeObs()

    map.drawMap(obstacles)

    while(True):
        x, y = graph.sample_envir()
        n = graph.number_of_nodes()
        graph.add_node(n, x, y)
        x1, y1 = graph.x[n], graph.y[n]
        x2, y2 = graph.x[n-1], graph.y[n-1]
        if(graph.isFree()):
            pygame.draw.circle(map.map, map.red, (graph.x[n], graph.y[n]), map.nodeRad, map.nodeThickness)
            if graph.crossObstacle(x1, x2, y1, y2):
                pygame.draw.line(map.map, map.blue, (x1, y1), (x2, y2), map.edgeThickness)

        # 描画を更新
        pygame.display.update()
        pygame.event.clear()
        pygame.event.wait(0)

        # システムを終了する
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    main()