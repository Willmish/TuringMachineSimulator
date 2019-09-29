from typing import List, Dict
import time, os, sys


# If you create new machines (text files), do it as in the example file, leaving an empty line at the end
class TuringMachine:
    def __init__(self, alphabet: tuple = ('0', '1', '#')) -> None:
        self._alphabet: tuple = alphabet
        # Records the tape on the right of the origin
        self.tapeR: List[str] = []
        # Records the tape on the left of the origin
        self.tapeL: List[str] = []
        self.states: List[str] = []
        self.transitions: Dict[(str, str): (str, str, str)] = {}  # from, letter, replace, action, to
        self.startState: str = ''
        self.acceptingStates: List[str] = []

    def addStates(self, states: List[str]) -> None:
        # adds states with no overlaps
        self.states += [i for i in states if i not in self.states]

    def addTransition(self, tran: (str, str, str, str, str)) -> None:
        # add Transition in the format: from tran[0], to tran[2],
        # for tran[1] input, replace with tran[3], action: tran[4]
        self.transitions[(tran[0], tran[1])] = (tran[2], tran[3], tran[4])

    def setStartState(self, state: str) -> None:
        # sets the starting state
        self.startState = state

    def setAcceptingStates(self, states: List[str]) -> None:
        self.acceptingStates += states

    def addTape(self, tape: List[str]) -> None:
        # add tapes to the right
        self.tapeR += tape

    def eraseTape(self):
        self.tapeL = []
        self.tapeR = []

    def writeTape(self, i: int, letter: str) -> None:
        if i < 0:
            # if the value needs to be written on the left
            self.tapeL[-1 * i - 1] = letter
        else:
            self.tapeR[i] = letter

    def readTape(self, i: int) -> str:
        if i < 0:
            i = -1 * i - 1
            while len(self.tapeL) < i + 1:
                # Fills with Empty up to the reading point
                self.tapeL.append('#')
            return self.tapeL[i]
        while len(self.tapeR) <= i:  # Same ^^^
            self.tapeR.append('#')
        return self.tapeR[i]

    def __str__(self) -> str:
        # Neatly prints all transitions of the Turing Machine :)
        output: str = ''
        for key in self.transitions:
            output += str(key)
            output += str(self.transitions[key]) + '\n'
        return output


class Simulator:
    def __init__(self, t: TuringMachine) -> None:
        self.t: TuringMachine = t
        self.currentState: str = t.startState
        self.currentI: int = 1

    def step(self) -> str:
        inp: str = self.t.readTape(self.currentI)

        if (self.currentState, inp) in self.t.transitions:
            # IF NO TRANSITION AVAILABLE FOR THE GIVEN INPUT - STAY (FINISH)
            tran: tuple = self.t.transitions[(self.currentState, inp)]  # from, letter, to, replace, action
            self.currentState = tran[1]
            self.t.writeTape(self.currentI, tran[0])
            # Resolve movement of the read/write head
            if tran[2] == '>':
                self.currentI += 1
            elif tran[2] == '<':
                self.currentI -= 1
        # Returns whether the program has finished and got accepted (or not)
        else:
            return str(self.currentState in self.t.acceptingStates)
        return 'stepped'


class UI:
    def __init__(self) -> None:
        self.t: TuringMachine = None
        self.s: Simulator = None

    # Doesn't need to have access to anything from the class - interacts with the user
    @staticmethod
    def getInput() -> str:
        return input("\n>>> ")

    @staticmethod
    def clear():
        # clears the console
        print('\n\n\n\n\n\n')
        os.system("cls")
        # for linux change to clear ^^^
        print('\n\n\n\n\n\n\n\n')

    def startUser(self) -> None:
        # Function I started coding, but then I realised that reading from files is cooler and faster
        print("Welcome to Turing Machine Simulator!\n"
              "Enter the alphabet for your Turing Machine (separated by spaces): ")
        alph: str = UI.getInput()
        arr: List[str] = alph.split(' ')
        arr += ['#']
        newTuple: tuple = tuple(i for i in arr)
        self.t = TuringMachine(newTuple)
        self.s = Simulator(self.t)
        # TODO delete these prints
        print(newTuple)
        print(type(newTuple))
        print(type(self.t))

    # etc, not finished!!

    def changeInput(self) -> None:
        # Changes the default input of the current Turing Machine
        # (OR leaves it as it is)
        i = 0
        tape: str = ''
        while i < len(self.s.t.tapeR):
            # Store the current input in tape
            tape += self.s.t.tapeR[i] + ' '
            i += 1
        print("Current Input Tape: " + tape)
        print("Would you like to change machine's input? (y/n)")
        inp = self.getInput()
        if inp == 'y':
            print("Please enter new input:")
            inp = self.getInput()
            self.s.t.eraseTape()
            # clear the tapes
            tape: List = [i for i in inp if i in self.s.t._alphabet]  # omits all characters not in the alphabet
            self.s.t.addTape(['#'])  # adds an empty sign on the beginning
            self.s.t.addTape(tape)

    def startFile(self):
        self.clear()
        print("Welcome to Turing Machine Simulator!\n"
              "Choose a file to run: \n"
              "1. end2zero\n"
              "2. div3\n"
              "3. palindCheck")
        # currently available files ^^ (I wrote end2zero and palindCheck, div3 isn't mine!)
        files: Dict = {
            '1': 'end2zero',
            '2': 'div3',
            '3': 'palindCheck'
        }
        file_index = self.getInput()
        if file_index in files:
            f = open(files[file_index], 'r')
        # if the file_index is valid, open the file,
        # otherwise, stop the program
        else:
            print("File index out of range!")
            return None
        nextL: str = ''
        for line in f:
            # Divides current line and puts it in an array (deleting the \n sign)
            arr: List[str] = line[:len(line) - 1].split(' ')
            # Reads and interprets all the inputs (Using a format designed by me :) )
            if nextL == 'alphabet':
                newTuple: tuple = tuple(i for i in arr)
                self.t = TuringMachine(newTuple)
                nextL = ''
            elif nextL == 'tape':
                self.t.addTape(arr)
                nextL = ''
            elif nextL == 'states':
                self.t.addStates(arr)
                nextL = ''
            elif nextL == 'starting state':
                self.t.setStartState(arr[0])
                nextL = ''
            elif nextL == 'accepting states':
                self.t.setAcceptingStates(arr)
                nextL = ''
            elif nextL == 'transitions':
                self.t.addTransition(tuple(arr))
            else:
                nextL = line[:len(line) - 2]
        self.s = Simulator(self.t)
        f.close()
        self.changeInput()
        self.display()

    def displayTape(self):
        # neat tape displayer (looks nice, I wanted to add a nice box for it,
        # but I didn't have enough time)
        self.clear()
        outputArr: str = ''
        for i in range(self.s.currentI - 10, self.s.currentI + 10):
            # Outputs the current files contents, 10 chars to the left and right
            outputArr += self.s.t.readTape(i) + ' '

        print(20 * ' ' + 'X')  # head indicator
        print(outputArr)
        print("Current State: " + self.s.currentState)
        print("Current Index on tape: " + str(self.s.currentI))
        print("Accepting states: " + str(self.s.t.acceptingStates))

    def handleStep(self, run: bool = False) -> bool:
        # Look up Simulator.step() method if ur confused
        st = self.s.step()
        if run:
            self.displayTape()
        if st == 'True':
            # If the machine finished in an accepting state
            print("Accepted! Program terminating...")
            return True
        elif st == 'False':
            print("Rejected! Program terminating...")
            return True
        if not run:
            # running means that the program doesn't require
            # you to write 's' whenever you want to step, it runs
            # automatically
            # if program is not running, show the menu, etc.
            self.display()
        return False

    def display(self) -> None:
        self.displayTape()
        print("Enter \'s\' to step by one or 'run' followed by an int (k)"
              " value (time in 0.1s between steps [k*0.1s])\n"
              "after a space to run the program Press 'q' to exit: ")
        inp: str = self.getInput()
        if inp == 's':
            # if user wants to step:
            self.handleStep()
        elif inp.split()[0] == 'run':
            # If user wants to run:
            arr = inp.split()
            if len(arr) <= 1:
                # stop, user hasn;t entered a speed factor
                return None
            t: float = .100 * int(arr[1])
            while not self.handleStep(True):
                # Loop while program hasn't finished
                sys.stdout.flush()
                time.sleep(t)

        elif inp == 'q':
            return None


ui: UI = UI()
# create the UI
ui.startFile()
# start the program
os.system("pause")
# pause the program
