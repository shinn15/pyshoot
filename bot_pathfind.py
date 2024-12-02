from collections import deque

class bot_pathfind:
	def __init__(self,game):
		self.game=game
		self.map = game.map.map_mini
		self.ways = [-1,0],[0,-1],[1,0],[0,1],[-1,-1],[1,-1],[1,1],[-1,1]
		self.graph={}
		self.get_graph()
#to run
	def get_path(self,start,goal):
		self.visited = self.bot_bfs(start,goal,self.graph)
		path=[goal]
		step= self.visited.get(goal,start)

		while step and step != start:
			path.append(step)
			step = self.visited[step]
		return path[-1]

#bot path find logic
	def bot_bfs(self,start,goal,graph):
		quee=deque([start])
		visited={start:None}

		while quee:
			curr_node = quee.popleft()
			if curr_node == goal:
				break
			nxt_nodes = graph[curr_node]

			#bot move next
			for nxt_node in nxt_nodes:
				if nxt_node not in visited and nxt_node not in self.game.object_handler.bot_pos:
					quee.append(nxt_node)
					visited[nxt_node] = curr_node

		return visited

	def get_nxt_node(self,x,y):
		return [(x+dx,y+dy) for dx,dy in self.ways if (x+dx,y+dy) not in self.game.map.world_map]


	def get_graph(self):
		for y, row in enumerate(self.map):
			for x, col in enumerate(row):
				if not col:
					self.graph[(x,y)]= self.graph.get((x,y),[])+self.get_nxt_node(x,y)