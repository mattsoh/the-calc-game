import math
from asteval import Interpreter
calc = Interpreter()
state_curr, state_prev, operator = "0", '0', ''
class Game:
    def __init__(self):
        operator_pressed = False
        self.label = ""
    def ev(self):
        global state_curr, state_prev, operator
        # copy below logic to actual gamee
        if self.label.isnumeric() or self.label == '.':
            if operator_pressed:
                state_curr = self.label
            else:
                state_curr += self.label
                state_curr = state_curr.lstrip('0')
            operator_pressed = False
        elif self.label == '√':
            state_curr = str(math.sqrt(float(state_curr)))
            operator_pressed = False
        elif self.label == '%':
            state_curr = str(float(state_curr) / 100)
            operator_pressed = False
        elif self.label == 'CE':
            state_curr = '0'
            operator_pressed = True
        elif self.label == 'C':
            state_curr = '0'
            state_prev = '0'
            operator = ''
            operator_pressed = False
        elif self.label in ['/', '*', '-', '+']:
            print("operator", operator)
            if operator != '':
                if operator_pressed:
                    operator = self.label
                    return
                state_prev = calc(state_prev + operator + state_curr)
                state_curr = state_prev
            else:
                state_prev = state_curr
                
            operator = self.label
            operator_pressed = True
            
game = Game()
print(state_prev, operator, state_curr)
while True:
    game.label = input()
    game.ev()
    print(state_prev, operator, state_curr)