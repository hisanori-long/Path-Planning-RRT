import pygame
import random
import math

class RRTMap:
    def __init__(self, start, goal, MapDimensions, obsdim, obsnum):
        self.start = start
        self.goal = goal
        self.MapDimensions = MapDimensions
        self.Maph, self.Mapw = MapDimensions

        # window settings
        self.mapWindowName = "RRT Path Planning"
        pygame.display.set_caption(self.mapWindowName)
        self.map = pygame.display.set_mode((self.Mapw, self.Maph))
        self.map.fill((255, 255, 255))
        self.nodeRad = 2
        self.nodeThickness = 0
        self.edgeThickness = 1

        self.obstacles = []
        self.obsDim = obsdim
        self.obsNum = obsnum

        # colors
        self.grey = (70, 70, 70)
        self.blue = (0, 0, 250)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)




    def drawMap(self, obstacles):
        pygame.draw.circle(self.map, self.green, self.start, self.nodeRad + 5, 0)
        pygame.draw.circle(self.map, self.red, self.goal, self.nodeRad + 20, 1)
        self.drawObs(obstacles)

    def drawPath(self, path):
        for node in path:
            pygame.draw.circle(self.map, self.red, node, self.nodeRad + 2, 0)


    def drawObs(self, obstacles):
        obstaclesList = obstacles.copy()
        while (len(obstaclesList) > 0):
            obstacle = obstaclesList.pop(0)
            pygame.draw.rect(self.map, self.grey, obstacle)



class RRTGraph:
    def __init__(self, start, goal, MapDimensions, obsdim, obsnum):
        (x, y) = start
        self.start = start
        self.goal = goal
        self.goalFlag = False
        self.maph, self.mapw = MapDimensions
        self.x = [] # ツリーのx座標を格納
        self.y = [] # ツリーのy座標を格納
        self.parent = [] # 親ノードのインデックスを格納
        # initialize the tree
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)
        # the obstacles
        self.obstacles = []
        self.obsDim = obsdim
        self.obsNum = obsnum
        # path
        self.goalstate = None
        self.path = []



    def makeRandomRect(self):
        uppercornex = int(random.uniform(0, self.mapw - self.obsDim))
        uppercorney = int(random.uniform(0, self.maph - self.obsDim))

        return (uppercornex, uppercorney)

    def makeObs(self):
        obs = []

        for i in range(0, self.obsNum):
            rectang = None
            startgoalcol = True
            while startgoalcol:
                upper = self.makeRandomRect()
                rectang = pygame.Rect(upper, (self.obsDim, self.obsDim))
                if rectang.collidepoint(self.start) or rectang.collidepoint(self.goal):
                    startgoalcol = True
                else:
                    startgoalcol = False
            obs.append(rectang)
        self.obstacles = obs.copy()
        return obs

    def add_node(self, n, x, y):
        self.x.insert(n, x)
        self.y.append(y)

    def remove_node(self, n):
        self.x.pop(n)
        self.y.pop(n)

    def add_edge(self, parent, child):
        self.parent.insert(child, parent)

    # nは子ノードのインデックス
    def remove_edge(self, n):
        self.parent.pop(n)

    def number_of_nodes(self):
        return len(self.x)

    def distance(self, n1, n2):
        (x1, y1) = (self.x[n1], self.y[n1])
        (x2, y2) = (self.x[n2], self.y[n2])
        px = (float(x1) - float(x2)) ** 2
        py = (float(y1) - float(y2)) ** 2
        return (px + py) ** 0.5

    def sample_envir(self):
        x = int(random.uniform(0, self.mapw))
        y = int(random.uniform(0, self.maph))
        return x, y

    # ノードnから最も近いノードのインデックスを返す
    def nearest(self, n):
        dmin = self.distance(0, n)
        nnear = 0
        for i in range(0, n):
            if self.distance(i, n) < dmin:
                dmin = self.distance(i, n)
                nnear = i
        return nnear

    # 最後に追加したノードが障害物と重なっていないか確認
    def isFree(self):
        n = self.number_of_nodes() - 1
        (x, y) = (self.x[n], self.y[n])
        obs = self.obstacles.copy()
        while len(obs)>0:
            rectang = obs.pop(0)
            if rectang.collidepoint(x, y): 
                self.remove_node(n)
                return False
        return True

    def crossObstacle(self, x1, x2, y1, y2) -> bool:
        obs = self.obstacles.copy()
        while len(obs) > 0:
            rectang = obs.pop(0)
            for i in range(0, 101):
                u = i /100
                x = x1 * u + x2 * (1 - u)
                y = y1 * u + y2 * (1 - u)
                if rectang.collidepoint(x, y): # 交差している
                    return True
        return False

    def connect(self, n1, n2) -> bool:
        (x1, y1) = (self.x[n1], self.y[n1])
        (x2, y2) = (self.x[n2], self.y[n2])
        if self.crossObstacle(x1, x2, y1, y2):
            self.remove_node(n2)
            return False
        else:
            self.add_edge(n1, n2)
            return True

    # ノードnnearをノードnrandに向かわせる
    # dmaxは最大移動距離
    def step(self, nnear, nrand, dmax=35):
        d = self.distance(nnear, nrand)
        if d > dmax:
            u = dmax / d
            (xnear, ynear) = (self.x[nnear], self.y[nnear])
            (xrand, yrand) = (self.x[nrand], self.y[nrand])
            (px, py) = (xrand - xnear, yrand - ynear)
            theta = math.atan2(py, px)
            (x, y) = (int(xnear + dmax * math.cos(theta)), int(ynear + dmax * math.sin(theta)))
            self.remove_node(nrand)
            if abs(x - self.goal[0]) < dmax and abs(y - self.goal[1]) < dmax: # ゴールに到達
                self.add_node(nrand, self.goal[0], self.goal[1])
                self.goalstate = nrand
                self.goalFlag = True
            else:
                self.add_node(nrand, x, y) 

    def path_to_goal(self):
        if self.goalFlag:
            self.path = []
            self.path.append(self.goalstate)
            newpos = self.parent[self.goalstate]
            while (newpos != 0):
                self.path.append(newpos)
                newpos = self.parent[newpos]
            self.path.append(0)
        return self.goalFlag

    def getPathCoords(self):
        pathCoords = []
        for node in self.path:
            x, y = (self.x[node], self.y[node])
            pathCoords.append((x, y))
        return pathCoords

    # ゴールに一直線に向かう
    def bias(self, ngoal):
        n = self.number_of_nodes()
        self.add_node(n, ngoal[0], ngoal[1])
        nnear = self.nearest(n) # ゴールに最も近いノード
        self.step(nnear, n) 
        self.connect(nnear, n)
        return self.x, self.y, self.parent

    # ノードをランダムに追加し、最近傍ノードに向かわせる
    def expand(self):
        n = self.number_of_nodes()
        x, y = self.sample_envir() # ランダムな座標を生成
        self.add_node(n, x, y)
        if self.isFree(): # 生成したランダムな座標が障害物と重なっていない
            xnearest = self.nearest(n) # 生成したランダムなノードに最も近いノードを取得
            self.step(xnearest, n)
            self.connect(xnearest, n)
        return self.x, self.y, self.parent

    def cost(self):
        pass


