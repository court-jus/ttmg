from .bases import Consumer, Producer, Debugable, Link


class Transformer(Debugable):
    def __init__(self, name, ingredients, product):
        super().__init__(name)
        self.consumer = Consumer(name, ingredients)
        self.producer = Producer(name, product)

    def tick(self):
        self.debug("  inbuffer", self.consumer.inbuffer)
        if self.consumer.ready():
            self.debug("   YAY I CAN RECIPE")
            self.consumer.prepare_recipe()  # This consumes the ingredients
            self.producer.tick()

