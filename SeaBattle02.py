#!/usr/bin/env python
# -*-coding:utf-8-*-
import random

ABCJ = "ABCDEFGHIJ"
ALL_TARGETS = [i + str(j) for i in ABCJ for j in range(1, 11)]
SHIPS = ["OOOO", "OOO", "OOO", "OO", "OO", "OO", "O", "O", "O", "O"]
MISSED_SYMBOL = "*"  # "•" is better, but may cause errors in Python 2x since non-ASCII


class Player:
    def __init__(self, who="PC"):
        self.field = [
            ["  ", " ", "A", " ", "B", " ", "C", " ", "D", " ", "E", " ", "F", " ", "G", " ", "H", " ", "I", " ", "J",
             " "],
            ["  ", " ", "_", " ", "_", " ", "_", " ", "_", " ", "_", " ", "_", " ", "_", " ", "_", " ", "_", " ", "_",
             " "]]
        for i in range(1, 11):
            self.field.append(
                [str(i) + " " * (2 - len(str(i))), "|", "_", "|", "_", "|", "_", "|", "_", "|", "_", "|", "_", "|", "_",
                 "|", "_", "|", "_", "|", "_", "|"])
        self.who = who
        self.alive = True
        self.possible_targets = ALL_TARGETS[:]
        self.suggested_targets = []  # list of coordinates if enemy's ship was hit but not sank

    def ship_placement(self, how="randomly"):
        for ship in SHIPS:
            ship_length = len(ship)

            while True:
                if how == "randomly":
                    end1 = random.choice(ALL_TARGETS)
                else:
                    end1 = input("Give first coordinate of [" + ship + "] : ").upper()

                if end1 in ALL_TARGETS:
                    if self.possible_ends(end1, ship_length):
                        if ship_length == 1:
                            end2 = end1  # for [0] ships
                        break
                    elif how == "manually":
                        print("Not possible to put this ship beginning from point ", end1)
                elif how == "manually":
                    print("Not possible to put this ship beginning from point ", end1)
            while True and ship_length > 1:
                if how == "randomly":
                    end2 = random.choice(self.possible_ends(end1, ship_length))
                else:
                    print("Possible ends ", self.possible_ends(end1, ship_length))
                    end2 = input("Give last coordinate of [" + ship + "] ship: ").upper()
                if (end2 in ALL_TARGETS) and (end2 in self.possible_ends(end1, ship_length)):
                    break
                    # actual ship placement after all checks are done
            edge1 = [int(end1[1:]) + 1, ABCJ.find(end1[0]) * 2 + 2]
            edge2 = [int(end2[1:]) + 1, ABCJ.find(end2[0]) * 2 + 2]
            if edge1[1] == edge2[1]:
                for x in range(0, abs(edge1[0] - edge2[0]) + 1):
                    self.field[min(edge1[0], edge2[0]) + x][edge1[1]] = "O"
            if edge1[0] == edge2[0]:
                for x in range(0, abs(edge1[1] - edge2[1]) + 2, 2):
                    self.field[edge1[0]][min(edge1[1], edge2[1]) + x] = "O"

            self.forbid(end1, "O", "z",
                        "dead")  # mark forbidden neighbour cells with 'z' to avoid next ship placement there
            if how == "manually":
                display_fields()

    def possible_ends(self, start, ship_len):
        """checks whether inputed start point of ship (i.e.[000]) has possible ends on field, returns list of such ends (0-1-2-3 or 4 values like A5)"""
        result = []
        col_number = ABCJ.find(start[0]) * 2 + 2
        row_number = int(start[1:]) + 1

        if self.field[row_number][col_number] != "_":
            return []
        elif ship_len == 1 and self.field[row_number][col_number] == "_":
            return start

        for arrow in [[0, 2], [1, 0], [0, -2], [-1, 0]]:  #'right','down','left','up'
            col_num = col_number
            row_num = row_number
            for x in range(1, ship_len):
                col_num += arrow[1]
                row_num += arrow[0]
                if row_num < 2 or row_num > 11 or col_num < 2 or col_num > 20 or self.field[row_num][col_num] != "_":
                    break
                elif x == ship_len - 1:
                    result.append(ABCJ[int((col_num - 2) / 2)] + str(row_num - 1))

        return result

    def forbid(self, shot, target="X", marker="z", ship_is="dead"):
        """gives list of forbidden coordinates near dead or hurted ship, while mark this cells with 'z' sign """
        col_number = ABCJ.find(shot[0]) * 2 + 2
        row_number = int(shot[1:]) + 1
        result = []
        my_queue = []
        history = []
        my_queue.append((row_number, col_number))
        history.append((row_number, col_number))

        while my_queue:
            for arrow in [[0, 2], [1, 0], [0, -2], [-1, 0]]:  # 'right','down','left','up'
                row_num = my_queue[0][0] + arrow[0]
                col_num = my_queue[0][1] + arrow[1]

                if row_num < 2 or row_num > 11 or col_num < 2 or col_num > 20:
                    continue

                if self.field[row_num][col_num] == target and tuple((row_num, col_num)) not in history:
                    history.append((row_num, col_num))
                    my_queue.append((row_num, col_num))

                if ship_is == "dead" and self.field[row_num][col_num] == "_":
                    self.field[row_num][col_num] = marker
                    result.append(
                        ABCJ[int((col_num - 2) / 2)] + str(row_num - 1))  # CHECK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            for arrow in [[-1, 2], [1, 2], [1, -2], [-1, -2]]:  # 'right-up','right-down','left-down','left-up'
                row_num = my_queue[0][0] + arrow[0]
                col_num = my_queue[0][1] + arrow[1]

                if row_num < 2 or row_num > 11 or col_num < 2 or col_num > 20:
                    continue
                elif self.field[row_num][col_num] == "_":
                    self.field[row_num][col_num] = marker
                    result.append(
                        ABCJ[int((col_num - 2) / 2)] + str(row_num - 1))  # CHECK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            my_queue.pop(0)

        return result

    def ship_status_check(self, shot):
        result = "dead."
        col_number = ABCJ.find(shot[0]) * 2 + 2
        row_number = int(shot[1:]) + 1
        my_queue = []
        history = []
        my_queue.append((row_number, col_number))
        history.append((row_number, col_number))

        while my_queue:
            for arrow in [[0, 2], [1, 0], [0, -2], [-1, 0]]:  # 'right','down','left','up'
                row_num = my_queue[0][0] + arrow[0]
                col_num = my_queue[0][1] + arrow[1]

                if row_num < 2 or row_num > 11 or col_num < 2 or col_num > 20:
                    continue
                if (self.field[row_num][col_num] == "O" or self.field[row_num][col_num] == "X") and tuple(
                        (row_num, col_num)) not in history:
                    history.append((row_num, col_num))
                    my_queue.append((row_num, col_num))
                    if self.field[row_num][col_num] == "O":
                        result = "hurted"
            my_queue.pop(0)

        return " Ship " + result

    def is_alive_check(self):
        """checks whether player still has "O" ships and is alive (do nothing) or dead (self.alive = False)"""
        for i in range(len(self.field)):
            if "O" in self.field[i]:
                break
            if i == len(comp.field) - 1:
                self.alive = False


def display_fields(hide_z=True):
    print()
    print("    Your enemy's field", " " * 10, "Your field", " " * 13, "Game log")
    print('|' * str(comp.field).count('O') + '.' * (20 - str(comp.field).count('O')) + \
     " " * 8 + '|' * str(human.field).count('O') + '.' * (20 - str(human.field).count('O')))
    for i in range(len(human.field)):
        enemy_field_row = ""
        your_field_row = ""
        for j in range(len(human.field[0])):
            if hide_z:
                your_field_row += human.field[i][j].replace("z", "_")
                enemy_field_row += comp.field[i][j].replace("O", "_").replace("z", "_")
            else:
                your_field_row += human.field[i][j]
                enemy_field_row += comp.field[i][j].replace("O", "_")
        if len(game_log) > i:
            your_field_row += " " * 3 + game_log[-i-1]
        print(enemy_field_row + " " * 5 + your_field_row)


if __name__ == '__main__':
    print("Welcome to SeaBattle game!")
    human = Player(who="human")
    comp = Player()
    game_log = []
    display_fields()
    if input("enter M to place your ships manually or any other for automatic placement: ").upper() == "M":
        human.ship_placement("manually")
    else:
        human.ship_placement("randomly")
    comp.ship_placement("randomly")

    # ----------------------Game--------------------------------------------------------------- #
    while True:
        while human.alive and comp.alive:  # human player turn
            display_fields()
            while True:  # waiting for valid target
                shot = input("Give target coordinate in range A1-J10, Q to loose: ").upper()
                if shot == "Q":
                    human.alive = False
                    break
                if shot in ALL_TARGETS:
                    break
            if shot != "Q":
                game_log += [str(len(game_log) + 1) + ": you   " + shot]
            else:
                shot = "A1"  # for correct closure
            col_num = ABCJ.find(shot[0]) * 2 + 2
            row_num = int(shot[1:]) + 1

            if comp.field[row_num][col_num] == "O":
                comp.field[row_num][col_num] = "X"
                game_log[-1] += comp.ship_status_check(shot)
                comp.is_alive_check()
            elif comp.field[row_num][col_num] == "X":
                break
            else:
                comp.field[row_num][col_num] = MISSED_SYMBOL
                break

        while human.alive and comp.alive:  # comp player turn

            if comp.suggested_targets:
                shot = comp.suggested_targets.pop()
            else:
                shot = random.choice(comp.possible_targets)
                comp.possible_targets.remove(shot)
                # todo: delete impossible next shoots by Forbid
            game_log += [str(len(game_log) + 1) + ": comp  " + shot]

            col_num = ABCJ.find(shot[0]) * 2 + 2
            row_num = int(shot[1:]) + 1

            if human.field[row_num][col_num] == "O":
                human.field[row_num][col_num] = "X"
                human.is_alive_check()
            else:
                human.field[row_num][col_num] = MISSED_SYMBOL
                break

        if not (comp.alive and human.alive):
            display_fields()
            if not comp.alive:
                print("---=== You won! ===---")
            else:
                print("You lose")
            if input("Would you like to play again? y/n [y] : ") not in ['n', 'N', 'no', 'No', 'NO']:
                human = Player(who="human")
                comp = Player()
                game_log = []
                display_fields()
                if input("enter M to place your ships manually or any other for automatic placement: ").upper() == "M":
                    human.ship_placement("manually")
                else:
                    human.ship_placement("randomly")
                comp.ship_placement("randomly")
            else:
                break
