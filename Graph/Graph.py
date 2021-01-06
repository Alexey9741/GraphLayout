from Point import Point
import random
import math
import numpy as np


class Vertex():
    """Graph vertex"""
    def __init__(self,name):
        self.name=name
        self.pos=Point(0,0)
        self.id=None              #id for drawing on Tkinter canvas
        self.name_id=None   
        self.rad=0
        self.root=False

    def __eq__(self,other):
        return self.name==other.name

    def __ne__(self,other):
        return self.name!=other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

class Edge():
    """Undirected graph edge"""
    def __init__(self,v,u):
        self.v=v
        self.u=u
        self.id=None

    def __eq__(self,other):
        return [self.v,self.u]==[other.v,other.u] or [self.v,self.u]==[other.u,other.v] 
    

class Graph():
    """Undirected graph without multiple edges and loops"""

    def __init__(self,vertexes=None):
        """vertexes is dict, keys-vertexes, values- lists of adjacent vertices"""
        if(vertexes==None):
            vertexes={}
        self.vertexes=vertexes

    def __eq__(self,other):
        return self.vertexes==other.vertexes

    def get_vertexes(self):
        """get vertexes list"""
        return list(self.vertexes.keys())

    def get_edges(self):
        """get edges list"""
        edges=[]
        for vertex in self.vertexes:
            for neighbour in self.vertexes[vertex]:
                if Edge(neighbour,vertex) not in edges:
                    edges.append(Edge(vertex,neighbour))

        return edges

    def get_incident_edges(self,v):
        """returns a list of edges incident to vertex v"""
        edges=[]
        pos=list(self.vertexes.keys()).index(v)
        for i,u in enumerate(self.vertexes[v]):
            if i<pos:
                edges.append(Edge(u,v))
            else:
                edges.append(Edge(v,u))

        return edges
        
            
    def add_vertex(self,v):
        """Adding a vertex"""
        if v not in self.vertexes.keys():
            self.vertexes[v]=[]

    def add_edge(self,edge):
        """Adding an edge. If any of the vertices is not included in the graph, it will be added to the graph"""
        if edge.v!=edge.u:
            self.add_vertex(edge.v)
            self.add_vertex(edge.u)
            if edge.u not in self.vertexes[edge.v]:
                self.vertexes[edge.v].append(edge.u)
            if edge.v not in self.vertexes[edge.u]:
                self.vertexes[edge.u].append(edge.v)


 
    def floyd(self,length=100):                                             
        """Finding the distance matrix using Floyd's algorithm"""

        n=len(self.vertexes.keys())
        D=np.zeros((n,n))
        for i,v in enumerate(self.vertexes):
            for j,u in enumerate(self.vertexes):
                if i!=j:
                    if u in self.vertexes[v]:
                        D[i][j]=length
                    else:
                        D[i][j]=math.inf

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if D[i][k]<math.inf and D[k][j]<math.inf:
                        D[i][j]=min(D[i][j],D[i][k]+D[k][j])

        return D


    def get_str(self):
        """Returns the graph as a dict with string keys and string value lists"""
        g={}
        for v in self.vertexes:
            adjacent=[]
            for u in self.vertexes[v]:
                adjacent.append(str(u.name))
            g[str(v.name)]=adjacent

        return g
            

    def __mul__(self,other):
        """Direct product of two graphs"""
        self_str=self.get_str()
        other_str=other.get_str()

        g={}

        for v in self.vertexes:
            for u in other.vertexes:
                vertex_name='('+str(v.name)+','+str(u.name)+')'
                g[Vertex(vertex_name)]=[]



        def vertex_patrition(two_vertex_str):
            """Splitting a vertex of a graph consisting of the product of two graphs into two vertices from the corresponding graphs"""
            stack=[]
            v1,v2='',''
            for i,s in enumerate(two_vertex_str):
                if s=='(':
                    stack.append(s)

                if s==')':
                    stack.pop()

                if s==',' and len(stack)==0:
                    v2=two_vertex_str[i+1:]
                    break

                v1+=s
          
            return v1,v2

        for v in g:
            for u in g:
                if v!=u:
                    x1,y1=vertex_patrition(v.name[1:-1])        
                    x2,y2=vertex_patrition(u.name[1:-1])

                    if x1==x2 and y1 in other_str[y2] or y1==y2 and x1 in self_str[x2]:
                        g[v].append(u)

        return Graph(g)

    def bfs(self,a,visit=print):
        """BFS from a given vertex a"""
        visited={}
        for v in self.vertexes:
            visited[v]=False

        Q=[]

        def BFS(a):
            visited[a]=True
            visit(a)
            Q.append(a)
            while len(Q):
                x=Q.pop(0)
                for y in self.vertexes[x]:
                    if visited[y]==False:
                        visit(y)
                        visited[y]=True
                        Q.append(y)

        BFS(a)
        for v in self.vertexes:
            if visited[v]==False:
                BFS(v)

    def get_bfs_tree(self,a):
        a.root=True
        visited={}
        for v in self.vertexes:
            visited[v]=False

        Q=[]

        fathers={}

        def BFS(a):
            visited[a]=True
            fathers[a]=a
            Q.append(a)
            while len(Q):
                x=Q.pop(0)
                for y in self.vertexes[x]:
                    if visited[y]==False:
                        fathers[y]=x
                        visited[y]=True
                        Q.append(y)


        BFS(a)
        for v in self.vertexes:
            if visited[v]==False:
                BFS(v)

        for x,Fx in fathers.items():
            print('Father('+str(x.name)+')=',Fx.name)


        g={}
        for vertex in fathers:
            g[vertex]=[fathers[vertex]]
            for son in fathers:
                if fathers[son]==vertex:
                    g[vertex].append(son)

        return Graph(g)

    def dfs(self,a,visit=print):
        visited={}
        for v in self.vertexes:
            visited[v]=False

        S=[]

        def DFS(a):
            visited[a]=True
            visit(a)
            S.append(a)
            while len(S):
                x=S[-1]
                unvisited=0
                for y in self.vertexes[x]:
                    if visited[y]==False:
                        visited[y]=True
                        unvisited+=1
                        visit(y)
                        S.append(y)
                        break
                if unvisited==0:
                    S.pop(-1)

        DFS(a)
        for v in self.vertexes:
            if visited[v]==False:
                DFS(v)

    def get_dfs_tree(self,a):
        a.root=True
        visited={}
        for v in self.vertexes:
            visited[v]=False

        S=[]

        fathers={}

        def DFS(a):
            visited[a]=True
            fathers[a]=a
            S.append(a)
            while len(S):
                x=S[-1]
                unvisited=0
                for y in self.vertexes[x]:
                    if visited[y]==False:
                        visited[y]=True
                        unvisited+=1
                        fathers[y]=x
                        S.append(y)
                        break
                if unvisited==0:
                    S.pop(-1)

        DFS(a)
        for v in self.vertexes:
            if visited[v]==False:
                DFS(v)

        for x,Fx in fathers.items():
            print('Father('+str(x.name)+')=',Fx.name)


        g={}
        for vertex in fathers:
            g[vertex]=[fathers[vertex]]
            for son in fathers:
                if fathers[son]==vertex:
                    g[vertex].append(son)

        return Graph(g)


class GenerateGraph():
    """Generation of some special graphs of the appropriate dimension"""

    def Kn(self,n):
        g={}
        vertexes=[Vertex(i) for i in range(n)]
        for i in range(n):
            neighbors=[]
            for j in range(n):
                if i!=j:
                    neighbors.append(vertexes[j])
            g[vertexes[i]]=neighbors

        return Graph(g)

    def Kpq(self,p,q):
        g={}
        vertexes=[Vertex(i) for i in range(p+q)]
        for i in range(p):
            neighbors=[]
            for j in range(p,p+q):
                neighbors.append(vertexes[j])
            g[vertexes[i]]=neighbors

        for i in range(p,p+q):
            neighbors=[]
            for j in range(p):
                neighbors.append(vertexes[j])
            g[vertexes[i]]=neighbors 

        return Graph(g)

    def Cn(self,n):
        if n<3:
            return Graph()
        g={}
        vertexes=[Vertex(i) for i in range(n)]
        g[vertexes[0]]=[vertexes[1],vertexes[n-1]]
        for i in range(1,n-1):
            g[vertexes[i]]=[vertexes[i-1],vertexes[i+1]]

        g[vertexes[n-1]]=[vertexes[0],vertexes[n-2]]

        return Graph(g)

    def On(self,n):
        g={}
        for i in range(n):
            g[Vertex(i)]=[]

        return Graph(g)

    def Pn(self,n):
        if n==0:
            return Graph()
        if n==1:
            return self.On(1)
        g={}
        vertexes=[Vertex(i) for i in range(n)]
        g[vertexes[0]]=[vertexes[1]]
        for i in range(1,n-1):
            g[vertexes[i]]=[vertexes[i-1],vertexes[i+1]]
        g[vertexes[n-1]]=[vertexes[n-2]]
        return Graph(g)

    def Qn(self,n,vertex_marking=False):
        if n<1:
            return Graph()
        g=self.Pn(2)
        for i in range(n-1):
            g*=self.Pn(2)
        
        # change the vertex names to binary numbers
        if vertex_marking:
            g_str=g.get_str()
            old_names=g_str.keys()
            new_names=[]
            for name in old_names:
                new_name=''
                for ch in name:
                    if ch=='0'or ch=='1':
                        new_name+=ch

                new_names.append(new_name)

            binary_g={}
            vertexes=[Vertex(new_name) for new_name in new_names]
            for v in vertexes:
                binary_g[v]=[]
            for v,old_name in zip(vertexes,old_names):
                for u,name in zip(vertexes,old_names):
                    if name in g_str[old_name]:
                        binary_g[v].append(u)

            return Graph(binary_g)

        return g





