from out.pkg_a.module_a import hallo_pkg
import threading

#from .out.pkg_a import module_a
def main():
    hallo_pkg()

class tmp:
    def __init__(self):
        for idx in range(0, 10):
            print(idx)
            
        

if __name__ == "__main__":
    main()
    