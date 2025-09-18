Calc.py:
import Pyro4
@Pyro4.expose
class Calculator:
def add(self, num1, num2):
return num1 + num2
def sub(self, num1, num2):
return num1 - num2
def mul(self, num1, num2):
return num1 * num2
def div(self, num1, num2):
try:
return num1 / num2
except:
return "Cant Divide by Zero..."

Client.py:
import Pyro4
name_server = Pyro4.locateNS()
calc_uri = name_server.lookup("ex2.calculator")
# Get the RMI object
calc_rmi = Pyro4.Proxy(calc_uri)
num1 = 10
num2 = 12
print("Two Numbers are: {}, {}".format(num1, num2))
print(f"Add: {calc_rmi.add(num1, num2)}")
print(f"Subtract: {calc_rmi.sub(num1, num2)}")
print(f"Multiply: {calc_rmi.mul(num1, num2)}")
print(f"Divide: {calc_rmi.div(num1, num2)}")

Server.py:
import Pyro4
from calc import Calculator
daemon = Pyro4.Daemon()
calc_uri = daemon.register(Calculator)
# Use a name server to regsiter for a namespace.
name_server = Pyro4.locateNS()
name_server.register("ex2.calculator", calc_uri)
print(f"<SERVER> Calculator for RMI Accessible via 'ex2.calculator' or {calc_uri}")
daemon.requestLoop()