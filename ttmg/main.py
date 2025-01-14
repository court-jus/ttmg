import time

from .bases import Consumer, Link
from .mine import Mine
from .transformer import Transformer

def main():
    imine = Mine("iM", "i", 1)
    cmine = Mine("cM", "c", 2)
    transformer = Transformer("T", ["i", "i", "c"], "g")
    ilink = Link("iL", 2)
    ilink.connect(imine, transformer.consumer)
    clink = Link("cL", 1)
    clink.connect(cmine, transformer.consumer)
    tickables = [transformer, imine, cmine, ilink, clink]
    for step in range(20):
        print("# Step", step)
        time.sleep(0.2)
        for tickable in tickables:
            tickable.tick()

if __name__ == "__main__":
    main()
