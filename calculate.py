from asteval import Interpreter
calc = Interpreter()

def sqrt(x):
    return int(calc(f"sqrt{x}"))

def ev(x):
    return int(calc(x))

print(ev("3**3"))
