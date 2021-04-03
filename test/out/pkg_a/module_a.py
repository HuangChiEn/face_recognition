from ..pkg_b import module_b

def hallo_a():
    print("hallo module A")
    
def hallo_pkg():
    module_b.hallo_b()