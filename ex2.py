# calc.py:
import Pyro4

@Pyro4.expose
class Calculator:
    def add(self, num1, num2):
        return num1 + num2

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b
    
    def div(self, a, b):
        try:
            return a / b
        except:
            return "Can't divide by Zero.."
        
# server.py:
import Pyro4
from calc import Calculator

daemon = Pyro4.Daemon()
calc_uri = daemon.register(Calculator)

name_server = Pyro4.locateNS()
name_server.register("ex2.calculator", calc_uri)

print(f"<SERVER> Calculator for RMI Accesible via 'ex2.calculator' or {calc_uri}")

daemon.requestLoop()

# client.py:
import Pyro4

name_server = Pyro4.locateNS()

calc_uri = name_server.lookup("ex2.calculator")

# Get the RMI Obj
calc_rmi = Pyro4.Proxy(calc_uri)

a = 10
b = 12

print(f"Two numbers are: {a}, {b}")

print(f"Add: {calc_rmi.add(a, b)}")
print(f"Sub: {calc_rmi.sub(a, b)}")
print(f"Mul: {calc_rmi.mul(a, b)}")
print(f"Div: {calc_rmi.div(a, b)}")
	
