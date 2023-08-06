# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


class Tutorial:

    def __init__(self, current_step=0):
        self.current_step = current_step

    def first_step(self):
        self.current_step = 1

        print("Create a package. The __init__.py file is used to mark which classes you want the user to access through"
              " the package interface. Create a setup.py (and setup.cfg (?)), README.md and LICENSE (in outside level"
              ". More information in"
              "https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56"
              "and https://packaging.python.org/tutorials/packaging-projects/")

    def second_step(self):
        self.current_step = 2

        print('Navigate with CMD to package level. Run:'
              'python seup.py sdist bdist_wheel')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
