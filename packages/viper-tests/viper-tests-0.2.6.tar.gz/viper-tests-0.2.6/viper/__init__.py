from colorama import Fore, Style
import time

""" Viper: A modern testing framework """

class Viper:
    """ The Main Testing Framework """
    def __init__(self, name):
        self.name = name
        self.tests = []
        self.passed = 0
        
    def importFromFile(self, data):
        """
        Import from another file\n
        :param list data: A list of tests from another file. 
        """
        for test in data:
            self.test(test["name"], test["functionOutput"], test["desiredOutput"])
    
    def test(self, name, function, output):
        """
        Create a test\n
        :param str name: A short description of the test\n
        :param function: The function that will be tested\n
        :param output: The desired output
        """
        try:
            self.tests.append({
                "name" : name,
                "functionOutput" : function,
                "desiredOutput" : output
            })
        except KeyboardInterrupt:
            pass

    def engine(self, test):
        if type(test["desiredOutput"]) == list:
            if test["functionOutput"] in test["desiredOutput"]:
                return True
            else:
                return False
        else:
            if test["functionOutput"] == test["desiredOutput"]:
                return True
            else:
                return False

    def evaluate(self):
        """ Evaluate all the tests """
        try:
            print("This is Viper, a modern testing framework, created by Aarush Gupta (https://aarushgupta.tk)")
            total = len(self.tests)
            print(f"Running tests from tests collection: \"{self.name}\"...")
            start = time.perf_counter()
            for test in self.tests:
                message = f"Testing \"{test['name']}\"... "
                print(message, end = "\r")
                time.sleep(0.75)
                if self.engine(test):
                    print(message + Fore.GREEN + "Passed" + Style.RESET_ALL)
                    self.passed += 1
                else:
                    print(message + Fore.RED + "Failed" + Style.RESET_ALL)
                    print(f"   Desired Output: {test['desiredOutput']} | Test Ouput: {test['functionOutput']}")
            end = time.perf_counter()
            time.sleep(0.75)
            print(f"\nRan {total} test(s) in {end - start:0.4f} seconds")
            print(f"{self.passed}/{total} passed")
        except KeyboardInterrupt:
            pass