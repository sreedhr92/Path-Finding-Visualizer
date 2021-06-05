# Path-Finding-Visualizer 👀
* Implementation of various path finding algorithms in Python and path visualization tool to visualize the algorithm as it runs.

* This program was built to demonstrate the relative efficiency of different pathfinding algorithms in finding the shortest path between two points on a map.

* To represent the map, the program uses a grid of nodes, in which each node has up to four traversable edges: up, down, left and right. One node is designated the root node, and another the target node. In addition, a node can be marked as impassable, effectively creating an obstacle around which an algorithm must navigate.

* In order to generate a path, each algorithm utilises an open set, a collection of nodes representing the boundary of an increasing search area. The algorithm gradually expands the search area by evaluating one node at a time from its open set.




### Requirements
* Python 3.x
* Pygame

### Index of the Algorithms:

* **A\* Star Algorithm**

    * A* search also uses a List, and also assigns each Node a heuristic value. However, it adds this heuristic value to the cumulative cost (the path length) to generate the Node’s f-score. The Node with the lowest f-score is then chosen to be evaluated.


* **Greedy BFS(Best First Search) Algorithm**

    * Best-first search uses a List, assigning each Node a heuristic value based on its estimated distance from the target node, not taking into account any obstacles. This value is simply the rectilinear distance, or the sum of the horizontal and vertical offsets, between the two points.

* **BFS(Breadth First Search) Algorithm**
  
    * Breadth-first search uses a Queue, which functions much like a real-world queue in ensuring that Nodes are evaluated in the same order they were added.


## A* Star Algorithm
![2021-06-03-13-46-33](https://user-images.githubusercontent.com/53933590/120613311-bf052280-c473-11eb-9ad5-ebe276b05fac.gif)

## Greedy BFS(Best First Search) Algorithm
![2021-06-03-14-32-02](https://user-images.githubusercontent.com/53933590/120618387-a814ff00-c478-11eb-8c0f-26aa73285b2b.gif)

## General Working of the Algorithms 👾

* Evaluating a node involves first checking if it is the target node – if this is the case, a path has been found and the algorithm terminates. Failing this, the node is removed from the open set and marked as visited so that is will not be re-added (this prevents the algorithm from generating loops). Finally, each of the nodes immediate unvisited neighbours are added to the open set. Crucially, for each of these neighbouring nodes, the current node is marked as their predecessor.

* This search area continues to expand until either it reaches the target node (meaning a path was been found), or there are no new nodes to evaluate (meaning no path was found). If a path is found, it is then reconstructed based on the predecessor of each node, starting from the target node, and continuing until the root node is reached.