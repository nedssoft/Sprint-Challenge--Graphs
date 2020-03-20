from room import Room
from player import Player
from world import World
from queue import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

def has_seen_rooms(room_id, seen_rooms):
    # Get the connected rooms
    rooms = room_graph[room_id][1].values()

    # Check if any of the rooms has not been seen
    for room in rooms:
        if room not in seen_rooms:
            return False
    return True 

def get_unseen_room(room_id, seen_rooms):
    # Get the connected rooms rom this room
    connected_rooms = room_graph[room_id][1].items()

    # Loop through the connected rooms
    for direction, room in connected_rooms:
        # Check if the room has not been seen before
        if room not in seen_rooms:
            # Add the direction to traversal_path
            traversal_path.append(direction)
            seen_rooms.add(room)
            return room

def re_explore(current_room, seen_rooms):
    visited = []
    paths = {}
    q = Queue()
    q.enqueue(current_room)
    paths[current_room] = [current_room]
    while q.size() > 0:
        room = q.dequeue()
        visited.append(room)
        for searched_room in room_graph[room][1].values():
            if searched_room in visited:
                continue
            new_path = paths[room].copy()
            new_path.append(searched_room)
            paths[searched_room] = new_path
            if not has_seen_rooms(searched_room, seen_rooms):
                un_explored_path = paths[searched_room]
                directions = []
                for i in range(len(un_explored_path) -1):
                    for direction, value in room_graph[un_explored_path[i]][1].items():
                        if value == un_explored_path[i + 1]:
                            directions.append(direction)
                    seen_rooms.add(un_explored_path[i + 1])
                return (directions, un_explored_path[len(un_explored_path) - 1])
            q.enqueue(searched_room)
    return None
# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = ['n', 's', 'e', 'w']

seen_rooms = set()
current_room = 0
while True:
    while not has_seen_rooms(current_room,seen_rooms):
        current_room = get_unseen_room(current_room,seen_rooms)
    explored_path = re_explore(current_room, seen_rooms)
    if explored_path:
        new_path = explored_path[0]
        traversal_path.extend(new_path)
        current_room = explored_path[1]
    else:
        break

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
