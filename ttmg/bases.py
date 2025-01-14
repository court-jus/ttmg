class Debugable:
    def __init__(self, name):
        self.name = name

    def debug(self, *a, **kw):
        print(" ", self.name, a, kw)


class Link(Debugable):
    def __init__(self, name, speed):
        self.maxitems = 5
        self.items = [None] * self.maxitems
        self.speed = speed
        self.inbound = None
        self.outbound = None
        super().__init__(name)

    def connect(self, inbound, outbound):
        self.inbound = inbound
        self.outbound = outbound

    def send(self, item):
        self.items.append(item)

    def tick(self):
        for _ in range(self.speed):
            self.debug("in the link:",self.items)
            # Send item 0 to outbound
            sent_item = False
            if self.outbound and self.items:
                if self.items[0] in self.outbound.ingredients and len(self.outbound.inbuffer) < self.outbound.maxbuffer:
                    item = self.items.pop(0)
                    self.outbound.send(item)
                    sent_item = True
            # Compress
            if sent_item:
                self.items.append(None)
            else:
                first_hole = None
                for idx, item in enumerate(self.items):
                    if item is None:
                        first_hole = idx
                        break
                if first_hole is not None:
                    self.items.pop(idx)
                    self.items.append(None)
                    self.debug("  compress", self.items)
            # If full return
            if len(self.items) >= self.maxitems and self.items[len(self.items) - 1] is not None:
                return
            # Pick item from inbound
            if self.inbound:
                self.items[len(self.items) - 1] = self.inbound.pick()


class Linkable(Debugable):
    def __init__(self, name):
        self.links = []
        super().__init__(name)


class Producer(Linkable):
    def __init__(self, name, product, productivity=1):
        self.product = product
        self.outbuffer = []
        self.maxbuffer = 4
        self.productivity = productivity
        super().__init__(name)

    def pick(self):
        if not self.outbuffer:
            self.debug("nothing to pick")
            return
        item = self.outbuffer.pop(0)
        self.debug("picked", item)
        return item

    def tick(self):
        for _ in range(self.productivity):
            if len(self.outbuffer) >= self.maxbuffer:
                return
            self.produce()

    def produce(self):
        self.outbuffer.append(self.product)
        self.debug("produced", self.product, "outbuffer:", self.outbuffer)

class Consumer(Linkable):
    def __init__(self, name, ingredients):
        self.ingredients = ingredients
        self.inbuffer = []
        self.maxbuffer = 4
        super().__init__(name)

    def send(self, product):
        self.debug("received", product)
        self.inbuffer.append(product)

    def tick(self):
        self.debug("inbuffer", self.inbuffer)

    def prepare_recipe(self):
        recipe_ingredients = []
        for item_type in self.ingredients:
            recipe_ingredients.append(self.get_ingredient(item_type))
        return recipe_ingredients

    def ready(self):
        recipe_ingredients = self.prepare_recipe()
        missing = any(item is None for item in recipe_ingredients)
        # Put them back
        for item in recipe_ingredients:
            if item is not None:
                self.inbuffer.append(item)
        if missing:
            self.debug("  missing ingredients:", recipe_ingredients)
            return False
        return True

    def get_ingredient(self, ingredient):
        for idx, item in enumerate(self.inbuffer):
            if item == ingredient:
                break
        else:
            return None
        return self.inbuffer.pop(idx)

