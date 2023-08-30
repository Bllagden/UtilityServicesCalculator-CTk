from controller import ControllerAPI
from view import MainWindow

if __name__ == "__main__":
    app = MainWindow(ControllerAPI())
    app.mainloop()
