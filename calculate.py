from asteval import Interpreter
calc = Interpreter()

def sqrt(x):
    return calc(f"sqrt{x}")

def ev(x):
    return calc(x)

print(ev("3**3"))
