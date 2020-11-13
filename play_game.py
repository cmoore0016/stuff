import json
import time
start_time = time.time()

x = 0
def main():
    # TODO: allow them to choose from multiple JSON files?
    with open('adventure.json') as fp:
        game = json.load(fp)
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)

hidden_turned_visible = []
def play(rooms):
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    items_in_room = {}
    # The things the player has collected.
    stuff = []
    stuff.append('cell phone')
    while True:
        # Figure out what room we're in -- current_place is a name:
        here = rooms[current_place]
        # Print the description:
        print(here["description"])
        if current_place == 'supply_closet':
            giant_switch_1()
        
        #figure out the items in the room using dict 'items_in_room'
        #where the keys are room names and the value is a list of the items:
        if current_place not in items_in_room:
            items_in_room[current_place] = here['roomitems']
        
        #print the items in the room:
        if len(items_in_room[current_place])>0:
            print("There is: -", ', '.join(items_in_room[current_place]), "- in the room")
        else:
            print("There are no items in the room.")
        '''
        roomthings = []
        for thing in here['roomitems']:
            if thing not in stuff:
                roomthings.append(thing)
        if len(roomthings)>0:
            print("There is: -", ', '.join(roomthings), "- in the room")
        else:
            print("There are no items in the room.")
        '''
            
        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        visable_exits = find_visable_exits(here, current_place)
        # Print out numbers for them to choose:
        for i, exit in enumerate(visable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
    
        if action == "help":
            print_instructions()
            continue
        
        if action == "stuff":
            print("Your Stuff: ")
            for i in stuff:
                print(">>", i)
            print("")
            continue
        
        if action == "time":
            elapsed_time = time.time() - start_time
            min = 0
            if elapsed_time >= 60:
                min = int(elapsed_time//60)
                sec = int(elapsed_time - min*60)
            else:
                sec = int(elapsed_time)
            print("You have been playing for", min, "min and", sec, "sec")
            continue

        if action == "take":   
            to_take = items_in_room[current_place]
            for s in to_take:
                stuff.append(s)
            taken = items_in_room[current_place]
            print("You took:", ', '.join(items_in_room[current_place]))
            items_in_room[current_place] = ''
            continue
        
        if action == "drop":
            print("Your Stuff: ")
            for i in stuff:
                print(">>", i)
            print("")
            dropitem = (input("What would you like to drop?: "))
            if dropitem in stuff:
                print(dropitem, "has been dropped")
                stuff.remove(dropitem)
                items_after_drop = []
                items_after_drop.append(dropitem)
                items_in_room[current_place] = items_after_drop
            else:
                print("This item isn't in your stuff")
            continue
        
        if action == "search":
            if len(hidden_exits_in_room)>0:
                for i in hidden_exits_in_room:
                    print("You found a hidden exit!:", i['description'])
                    usable.append(i)
                    hidden_turned_visible.append(i)
            else:
                print("There are no hidden exits in this room.")
            continue
    
        try:
            num = int(action) - 1
            selected = visable_exits[num]
        
            print("...")
            x = 1

        except:
            print("I don't understand '{}'...".format(action))
        
        if x == 1:
            with open('adventure.json') as fp:
                game = json.load(fp)
            if selected['lockability'] == 'unlocked':
                current_place = selected['destination']
            elif ((current_place == 'staircase') and (((game[current_place])['exits'])[1] == selected) and (position == 'up')):
                current_place = selected['destination']
            else:
                print("The door is locked!")
        x = 0
        
    print("")
    print("")
    print("===  YOU WIN  ===")
    print("=== GAME OVER ===")

def find_visable_exits(room, current):
    global hidden_turned_visible
    global hidden_exits_in_room
    global usable
    global hidden_exits
    usable = []
    hidden_exits = []
    #print (usable) ##
    n = 0
    ex_dict = room['exits']
    #TODO: Make lists 'hidden_exits' and 'usable' work in this function 'find_visible_exits'
    #and in 'search' command
    if True:
        ####
        
        #LIST 'ex_dict':
                #list of all exits out of the room
                #used as a placeholder for 'room['exits']'
        #LIST 'usable':
                #list of visible exits in the current room
        #LIST 'hidden_exits':
                #list of hidden exits in the current room
        #LIST 'hidden_turned_visible':
                #list of exits that were hidden, searched for, and are now visible.
                    #use this list so that the list 'usable' of usable exits will be composed of
                    #the exits already visible + the exits in the room in the list hidden_turned_visible
        #LIST 'hidden_exits_in_room':
                #list of hidden exits in the current room. 
                #placeholder list equal to 'hidden_exits' for 'search' command
        
        while n < len(ex_dict):
            if ex_dict[n]['visibility'] == 'hidden':
                hidden_exits.append(ex_dict[n])
            else:
                usable.append(ex_dict[n])
            n += 1
        for ex in hidden_turned_visible:
            if ex['currentroom'] == current:
                if ex not in usable:
                    usable.append(ex)
                if ex in hidden_exits:
                    hidden_exits.remove(ex)
        hidden_exits_in_room = []
        for i in hidden_exits:
            i['currentroom'] = current
            hidden_exits_in_room.append(i)     
        return (usable)
    
    
def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print(" - Type 'time' to see how much time has passed in your adventure.")
    print(" - Type 'take' to pick up the items in a room.")
    print("=== Instructions ===")
    print("")

position = 'down'
def giant_switch_1():
    global position
    print('the switch is', position)
    choice = input('There is a giant switch: would you like to flip it? (yes/no) > ')
    if choice == 'yes':
        if position == 'up':
            position = 'down'
        else:
            position = 'up'
        print('The switch is now', position)
    elif choice == 'no':
        print('ok')
    else:
        giant_switch_1()
    if position == 'up':
        pass

    


if __name__ == '__main__':
    main()