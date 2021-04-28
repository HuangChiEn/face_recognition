from ..pkg_b import module_b

def hallo_a():
    print("hallo module A")
    
def hallo_pkg():
    module_b.hallo_b()
    
if __name__ == "__main__":
    hallo_pkg()