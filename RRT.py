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

    pygame.init()
    map = RRTMap(start, goal, dimensions, obsdim, obsnum)
    graph = RRTGraph(start, goal, dimensions, obsdim, obsnum)

    obstacles = graph.makeObs()

    map.drawMap(obstacles)

    while (1):
        pygame.display.update()     # 画面を更新
        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタンが押されたら終了
                pygame.quit()       # Pygameの終了(画面閉じられる)
                sys.exit()          # システム終了(プログラム終了)


if __name__ == '__main__':
    main()