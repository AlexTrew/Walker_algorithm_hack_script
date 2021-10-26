import tkinter as tk
import random as rand
import math

class room:
    
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.exits = []
        

#note, distinguish between road origin and road block. Road origins will contain the length and direction of a road. From this, we can place a prefab'd road in godot 

def walk_rooms(no_of_rooms):

    grid_size = 40
    
    #initialise grid

    grid = []

    for x in range(0,grid_size):
        x_arr = []
        for y in range(0,grid_size):
            x_arr.append(room("empty",x,y))
        grid.append(x_arr)
    
    #create central square

 

    cursor_x = 20
    cursor_y = 20

    grid[cursor_x][cursor_y].type="square_origin"
    grid[cursor_x][cursor_y].x= cursor_x
    grid[cursor_x][cursor_y].y= cursor_y

    grid[cursor_x+1][cursor_y].type = "square"
    grid[cursor_x][cursor_y+1].type = "square"
    grid[cursor_x+1][cursor_y+1].type = "square"

    spawned_rooms = 0
    
    road_dist_count = 0

    walk_direction = rand.randint(1,4)

    road_type = "road1"

    start_x = cursor_x
    start_y = cursor_y

    road_dist = rand.randint(2,3)

    possible_special_rooms = []

    while spawned_rooms < no_of_rooms:
        

        if road_dist_count > road_dist:
            road_dist = rand.randint(2,3)
            walk_direction = rand.randint(1,4)
            spawned_rooms += 1
            road_dist_count = 0
            if rand.randint(0,6) > 4:
                cursor_x = start_x
                cursor_y = start_y


        #track previous room
        prev_x = cursor_x
        prev_y = cursor_y

        #1=north 2=east 3=south 4=west
        if walk_direction == 1:
            if cursor_y == 99:
                walk_direction = 3
            else:
                cursor_y += 1
        elif walk_direction == 2:
            if cursor_x == 99:
                walk_direction = 4
            else:
                cursor_x += 1
        elif walk_direction == 3:
            if cursor_y == 0:
                walk_direction = 1
            else:
                cursor_y -= 1
        elif walk_direction == 4:
            if cursor_x == 0:
                walk_direction = 2
            else:
                cursor_x -= 1


        #if we are starting a new room, tell the old room to crate an exit to the new one, and vice versa
        if road_dist_count == 0 and grid[cursor_x][cursor_y].type == "empty":
            
            if road_type == "road1":
                road_type = "road2"
            else:
                road_type = "road1"    
            grid[cursor_x][cursor_y].type = road_type
            grid[cursor_x][cursor_y].exits.append(grid[prev_x][prev_y])
            grid[prev_x][prev_y].exits.append(grid[cursor_x][cursor_y])
            road_dist_count += 1

        #else continue walking the current room if there is sufficient empty space
        elif grid[cursor_x][cursor_y].type == "empty":
            grid[cursor_x][cursor_y].type = road_type
            road_dist_count += 1

            #randomly add adjacent special rooms for later processing

            if rand.randint(0,1) == 1:
                if walk_direction == 1 or walk_direction == 3:
                    if grid[cursor_x+1][cursor_y].type == "empty":
                        grid[cursor_x+1][cursor_y].type == "possible_start_end"
                        possible_special_rooms.append(grid[cursor_x+1][cursor_y])
                        grid[cursor_x+1][cursor_y].exits.append(grid[cursor_x][cursor_y])
                    else:
                        grid[cursor_x-1][cursor_y].type == "possible_start_end"
                        possible_special_rooms.append(grid[cursor_x-1][cursor_y])
                        grid[cursor_x-1][cursor_y].exits.append(grid[cursor_x][cursor_y])
                elif walk_direction == 2 or walk_direction == 4:
                    if grid[cursor_x][cursor_y+1].type == "empty":
                        grid[cursor_x][cursor_y+1].type == "possible_start_end"
                        possible_special_rooms.append(grid[cursor_x][cursor_y+1])
                        grid[cursor_x][cursor_y+1].exits.append(grid[cursor_x][cursor_y])
                    elif grid[cursor_x][cursor_y-1].type == "empty":
                        grid[cursor_x][cursor_y-1].type == "possible_start_end"
                        possible_special_rooms.append(grid[cursor_x][cursor_y-1])
                        grid[cursor_x][cursor_y-1].exits.append(grid[cursor_x][cursor_y])
                

        #else walk back randomly through the existing rooms until empty space is found
        else:
            walk_direction = rand.randint(1,4)
            road_dist_count = 0
        
    
       #calculate distances between possible special rooms

    max_dist = 0

    r1 = room
    r2 = room

    for r in possible_special_rooms:
        for comp_room in possible_special_rooms:
            dist = math.sqrt(math.pow(r.x - comp_room.x,2) + math.pow(r.y - comp_room.y,2))

            if dist >= max_dist:
                max_dist = dist
                r1 = r
                r2 = comp_room

    r1.type = "start"
    r2.type = "end"

    r1.exits[0].exits.append(r1)
    r2.exits[0].exits.append(r2)

    return grid

def draw_map(grid):

        window = tk.Tk()
        window.title("Nether Reich mapgen prototype")
        canv = tk.Canvas(window, width=1000, height=1000, bg="white")
        canv.pack()

        for x in range(len(grid)):
            for y in range(0,len(grid[x])):
                if grid[x][y].type != "empty":
                    if grid[x][y].type == "square_origin":
                        canv.create_rectangle(x*10,y*10,(x*10)+20,(y*10)+20, fill="red")
                    elif grid[x][y].type == "road1":
                        canv.create_rectangle(x*10,y*10,(x*10)+10,(y*10)+10, fill="blue")
                    elif grid[x][y].type == "road2":
                        canv.create_rectangle(x*10,y*10,(x*10)+10,(y*10)+10, fill="yellow")
                    elif grid[x][y].type == "start":
                        canv.create_rectangle(x*10,y*10,(x*10)+10,(y*10)+10, fill="green")
                        canv.create_text(x*10+5,y*10+5,text="S")
                    elif grid[x][y].type == "end":
                        canv.create_rectangle(x*10,y*10,(x*10)+10,(y*10)+10, fill="orange")
                        canv.create_text(x*10+5,y*10+5, text="E")
                    for adj_room in grid[x][y].exits:
                        canv.create_line((x*10)+5, (y*10)+5, (adj_room.x)*10+5, (adj_room.y)*10+5)
                                
        window.mainloop()     


def main():
        grid = walk_rooms(10)
        draw_map(grid)

if __name__ == '__main__':
        main()
