import time

from .bases import Consumer, Link
from .mine import Mine
from .transformer import Transformer

def main():
    print("#" * 80)
    imine = Mine("iM", "i", 1)
    cmine = Mine("cM", "c", 1)
    transformer = Transformer("T", ["i", "i", "c"], "g")
    for consumer in transformer.consumers.values():
        consumer.maxbuffer = 8
    ilink = Link("iL", 1)
    ilink.connect(imine, transformer.consumers["i"])
    clink = Link("cL", 1)
    clink.connect(cmine, transformer.consumers["c"])
    tickables = [transformer, cmine, clink, imine, ilink]
    for step in range(20):
        print("# Step", step)
        # time.sleep(0.2)
        for tickable in tickables:
            tickable.tick()
    print("Crafted", transformer.crafted, "items")

if __name__ == "__main__":
    main()
