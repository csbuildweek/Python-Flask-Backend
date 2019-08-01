from util import Stack, Queue  # These may come in handy
import json


class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}
    def add_vertex(self, vertex):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex] = set()
    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("That vertex does not exist!")


    # Print each vertex in breadth-first order
    # beginning from starting_vertex.
    
    # Breadth First Traversal
    def bft(self, starting_vertex):  
        print('BFT')
        # store visited nodes
        visited = set()
        # create an empty queue and enqueue the starting vertex
        queue = Queue()
        queue.enqueue(starting_vertex)
        # while queue is not empty
        while queue.size() > 0:
            # dequeue and store the first vertex
            vertex = queue.dequeue()
            # if that vertex hasn't been visited
            if vertex not in visited:
                # mark it as visited
                visited.add(vertex)
                # print vertex
                print(vertex)
                # add all of it's neighbors to the back of the queue
                for neighbor in self.vertices[vertex]:
                    queue.enqueue(neighbor)





    # Print each vertex in depth-first order
    # beginning from starting_vertex.

    # Depth First Traversal
    def dft(self, starting_vertex): 
        print("Start DFT")
        # create an empty set to store visited nodes
        visited = set()
        # create an empty stack and push the starting vertex on the stack
        stack = Stack()
        stack.push(starting_vertex)
        # while the stack is not empty
        while stack.size() > 0:
            # pop the first vertex
            vertex = stack.pop()
            # if that vertex hasn't been visited
            if vertex not in visited:
                # mark it as visited (add to visited set)
                visited.add(vertex)
                # print vertex
                print(vertex)
                # loop through edges
                for neighbor in self.vertices[vertex]:
                    # push edges to stack
                    stack.push(neighbor)




    def dft_recursive(self, starting_vertex, visited=None):
        if visited is None:
            visited = set()
        # if starting_vertex is not in the visited set
        if starting_vertex not in visited:
            # mark node as visited
            visited.add(starting_vertex)
            # print starting vertex
            print(starting_vertex)
            # call recursive for each child and send visited list
            for neighbor in self.vertices[starting_vertex]:
                self.dft_recursive(neighbor, visited)


    def bfs(self, starting_vertex, destination_vertex):
        # Return a list containing the shortest path from
        # starting_vertex to destination_vertex in breadth-first order.

        # Create an empty set to store visited nodes
        visited = set()
        # Create an empty Queue and enqueue A PATH TO the starting vertex
        queue = Queue()
        queue.enqueue([starting_vertex])
        # While the queue is not empty...
        while queue.size() > 0:
            # Dequeue the first PATH
            path = queue.dequeue()
            # GRAB THE VERTEX FROM THE END OF THE PATH
            vertex = path[-1]
            # IF VERTEX = TARGET, RETURN PATH
            if vertex == destination_vertex:
                return path
            # If that vertex has not been visited...
            if vertex not in visited:
                # Mark it as visited
                visited.add(vertex)
                # Then add A PATH TO all of its neighbors to the back of the queue
                for neighbor in self.vertices[vertex]:
                    # Copy the path
                    path_copy = list(path)
                    # Append neighbor to the back of the copy
                    path_copy.append(neighbor)
                    # Enqueue copy
                    queue.enqueue(path_copy)



    def dfs(self, starting_vertex, destination_vertex):
        # Return a list containing a path from
        # starting_vertex to destination_vertex in
        # depth-first order.

        visited = set()
        stack = Stack()
        stack.push([starting_vertex])
        while stack.size() > 0:
            path = stack.pop()
            vertex = path[-1]
            if vertex == destination_vertex:
                return path
            if vertex not in visited:
                visited.add(vertex)
                for neighbor in self.vertices[vertex]:
                    path_copy = list(path)
                    path_copy.append(neighbor)
                    stack.push(path_copy)

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    with open('map.txt') as json_file:
        data = dict(json.load(json_file))
        for room in data:
            graph.add_vertex(str(room))
        for room in graph.vertices:

            if 'n' in data[room][1]:
                graph.add_edge(room, str(data[room][1]['n']))
            if 'e' in data[room][1]:
                graph.add_edge(room, str(data[room][1]['e']))
            if 's' in data[room][1]:
                graph.add_edge(room, str(data[room][1]['s']))
            if 'w' in data[room][1]:
                graph.add_edge(room, str(data[room][1]['w']))
        # print(graph.vertices)
print(graph.bfs('164', '467'))