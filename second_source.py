size = 0

table = []

def check_input_size():
    global size
    size =  int(input("Enter the size: "))
    while size < 3:
        size = int(input("The size must be greater than 2: "))
    return size

def specify_turn_player(p_player=0):
    if p_player:
        turn_player = "o" if p_player == "x" else "x"
        print(f"Now it is '{turn_player}' turn ")
    else: 
        import random
        turn_player = random.choice(["x","o"])
        print(f"First player is '{turn_player}'") 
    return turn_player

def create_board_game(free=0):
    global size
    global table 
    counter = 1
    if free != 0:
        table = []
    row = []
    for i in range(size):
        for j in range(size):
            row.append(counter)
            counter += 1
        table.append(row)
        row = []
    return table

def update_board_game(turn_player=0,number=0):
    global table
    global size
    if len(table) == 0:
        create_board_game()
    for j in range(size):
        if number in table[j]:
                table[j].insert(table[j].index(number),turn_player)
                table[j].remove(number)
    return table

def show_board_game():
    global size
    global table
    if len(table) == 0:
        update_board_game()    
    for i in range(size):
        for j in range(size):
            if table[i][j] == "x":
                print(f"\033[38;5;190m{table[i][j]}\033[0;0m",end="\t")
            elif table[i][j] == "o":
                print(f"\033[38;5;196m{table[i][j]}\033[0;0m",end="\t")
            else:
                print(table[i][j],end="\t")
        print()

def check_available_number():
    global table
    global size
    available_number = []
    for i in range(size):
        available_number += list(filter(lambda n: n != "x" and n != "o",table[i]))
    return available_number

def get_input():
    global table
    global size
    num = input("Enter the number: ")
    if num.isdigit(): num = int(num)
    while num not in check_available_number() and num != "q":
            num = input("This number has already been chosen or out of range please try another number: ")
            if num.isdigit(): num = int(num)
    return num
 
def check_winning_condition_horizental(turn_player):
    global table
    global size
    win = False
    for i in range(size):
        if len(list(filter(lambda n: n == turn_player ,table[i]))) == size:
            win = True
            break
    return win

def check_winning_condition_vertical(turn_player):
    global table
    global size
    win = False
    v_c = [[table[j][i] for j in range(size)] for i in range(size)]
    for i in range(size):
        if len(list(filter(lambda n: n == turn_player ,v_c[i]))) == size:
            win = True
            break
    output = v_c if turn_player == 0 else win
    return output

def check_winning_condition_diagonal(turn_player):
    global size
    global table
    d_c = [[table[i][i] for i in range(size)],[table[i][j] for i,j in enumerate(range(size-1,-1,-1))]]
    win = False
    for i in range(2):
        if len(list(filter(lambda n: n == turn_player ,d_c[i]))) == size:
            win = True
            break
    output = d_c if turn_player == 0 else win
    return output

def check_winning_condition(turn_player,mode=0):
      win = False
      if check_winning_condition_diagonal(turn_player) or check_winning_condition_horizental(turn_player) or check_winning_condition_vertical(turn_player):
            if mode == "p2p":
                print(f"Congratulation {turn_player} win.")
                show_board_game()
                clear_text()
            win = True
      return win

def check_ending_game(picked):
    global table
    d_c,v_c = check_winning_condition_diagonal(0),check_winning_condition_vertical(0)
    all_number = [*d_c,*table,*v_c]
    availalbe_number = list(filter(lambda n: "x" in n and "o" in n, all_number))
    equal = False
    if len(availalbe_number) == len(all_number):
        print("Game Over")
        show_board_game()
        clear_text()
        equal = True
    output = availalbe_number if picked == 0 else equal
    return output 

def check_not_winning_game(picked):
    global table
    pc_name = "o" if picked == "x" else "x"
    d_c,v_c = check_winning_condition_diagonal(0),check_winning_condition_vertical(0)
    all_number = [*d_c,*table,*v_c]
    availalbe_number = list(filter(lambda n: pc_name in n, all_number))
    equal = False
    if len(availalbe_number) == len(all_number):
        print("Sorry You can't win.")
        show_board_game()
        clear_text()
        equal = True         
    return equal

def play_with_two_player(turn_player=0,count=0):
    import os
    previous_player = "o" if turn_player == "x" else "x"
    turn_player = 0 if turn_player == 0 else previous_player
    count = 1 if count == 0 else count
    while count <= size*size:
        turn_player = specify_turn_player(turn_player)
        print("\n")
        show_board_game()
        print("\n")
        if check_ending_game(1):
                break
        a = get_input()
        os.system("clear")
        if a == "q":
            b = input("Do you want to save?: ")
            if b == "yes":
                save_game("p2p",turn_player,count)
            else:
                clear_text()
            break
        update_board_game(turn_player,a)
        if check_winning_condition(turn_player,"p2p") or check_ending_game(1):
                break
        count += 1

def pick_random_number_easy():
    import random
    global chart
    number = random.choice(check_available_number())
    return number

def create_number_list_for_pc(picked,check_table):
    global table
    global size
    d_c = check_winning_condition_diagonal(0)
    v_c = check_winning_condition_vertical(0)
    num = []
    all_number = [*d_c,*table,*v_c]
    for i in range(size*2 +2):
        if len(list(filter(lambda n: n == picked ,all_number[i]))) == check_table:
                num += list(filter(lambda n: n != "x" and n != "o" ,all_number[i]))
    return num

def pick_random_number_medium(picked):
    global size
    num = create_number_list_for_pc(picked,size-1)
    number = pick_random_number_easy() if len(num) == 0 else num[0]      
    return number

def pick_random_number_hard(picked):
    global size
    pc_name = "o" if picked == "x" else "x"
    num = create_number_list_for_pc(pc_name,size-1)
    number = pick_random_number_medium(picked) if len(num) == 0 else num[0]   
    return number

def run_player_mode(difficulty,picked,count):
    import os
    print(f"It is your ({picked}) turn")
    print("\n")
    show_board_game()
    print("\n")
    a = get_input()
    os.system("clear")
    if a == "q":            
        b = input("Do you want to save?: ")
        if b == "yes":
            save_game(difficulty,picked,count)
        else:
            clear_text()
        return True
    else:
      update_board_game(picked,a)
      if check_winning_condition(picked):
                  print(f"Congratulation You win.")      
                  show_board_game()
                  clear_text()
                  return True

def run_computer_mode(picked,difficulty = "expert"):
    pc_list = "x" if picked == "o" else "o"
    match difficulty:
        case "easy":
            num_pc = pick_random_number_easy()
        case "medium":
            num_pc = pick_random_number_medium(picked)
        case "hard":
            num_pc = pick_random_number_hard(picked)
        case "expert":
            num_pc = pick_random_number_expert(picked)       
    update_board_game(pc_list,num_pc)
    if check_winning_condition(pc_list):
        print(f"You lose.")
        show_board_game()
        clear_text()
        return True

def choose_mode_game():
    global size
    type = input("choose type game(P2P,PC): ").lower()
    size = check_input_size()    
    if type == "p2p":
        play_with_two_player()
    else: 
        difficulty = input("Enter difficulty(easy,medium,hard,expert): ").lower()
        match difficulty:
                case "easy":
                    play_with_computer(difficulty)

                case "medium":
                    play_with_computer(difficulty)

                case "hard":
                    play_with_computer(difficulty)

                case "expert":
                    play_with_computer(difficulty)

def play_with_computer(difficulty,sign=0,count=0):
    import os
    picked = input("Pick 'x' or 'o': ") if sign == 0 else sign
    count = 1 if count == 0 else count
    first_player = specify_turn_player() if sign == 0 else sign
    input()
    while count <= size * size:
        if first_player == picked:
            if count > 1 and check_not_winning_game(picked) or run_player_mode(difficulty,picked,count):
                break
            os.system("clear")
            if run_computer_mode(picked,difficulty):
                break
        else:
            show_board_game()
            if check_not_winning_game(picked) or run_computer_mode(picked,difficulty):
                break                  
            os.system("clear")
            if check_not_winning_game(picked) or run_player_mode(difficulty,picked,count):
                break                 
        if check_ending_game(picked):
            break  
        count += 1
    print("End Game")

def save_game(difficulty,picked,count):
    global table
    global size
    with open("Game.txt","w") as f1: 
        for i in range(size):
            for j in range(size):
                f1.write(f"{table[i][j]}\t")
            f1.write("\n")
        f1.write(f"{difficulty}\n{picked}\n{count}")
    print("Your game has been saved.")

def continue_game():
    global table
    global size
    import re
    with open("Game.txt","r") as f1:
        content = f1.read()
        tab = re.split("[\t|\n]",content)
        size = tab.index("")
        table = [[j if j == "x" or j == "o" else int(j) for j in tab[i:size+i] if j != ""]for i in range(0,size*size,size+1)]
        difficulty,picked,count = tab[-3],tab[-2],int(tab[-1])
        if difficulty == "p2p":
            play_with_two_player(picked,count)
        else:
            play_with_computer(difficulty,picked,count)

def clear_text():
    import os
    if os.path.exists("Game.txt"):
        os.remove("Game.txt")

def pick_random_number_expert(picked):
    import random
    global table
    global size
    d_c,v_c = check_winning_condition_diagonal(0),check_winning_condition_vertical(0)
    num = []        
    count_d,count_n = (0,0)
    all_number = list(filter(lambda n: n not in check_ending_game(0),[*d_c,*table,*v_c])) 
    for j in range(size-1,0,-1):
        count_d,count_n = (0,0)
        for i in range(len(all_number)):
            if len(list(filter(lambda n: n == picked ,all_number[i]))) == j:
                if all_number[i] in d_c and count_d == 0:
                    num.append(list(filter(lambda n: n != "x" and n != "o" ,all_number[i])))
                    count_d += 1
                elif all_number[i] in d_c and count_d > 0:
                    num[0] += list(filter(lambda n: n != "x" and n != "o" ,all_number[i]))
                elif count_n == 0:
                    num.append(list(filter(lambda n: n != "x" and n != "o" ,all_number[i])))
                    count_n += 1
                else:
                    num[len(num)-1] += list(filter(lambda n: n != "x" and n != "o" ,all_number[i]))
    for i in num:
        if len(i) == 0:
            num.remove(i) 
    number = pick_random_number_easy() if len(num) == 0 else random.choice(num[0])
    return number