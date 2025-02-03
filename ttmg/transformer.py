from .bases import Consumer, Producer, Debugable, Link


class Transformer(Debugable):
    def __init__(self, name, ingredients, product):
        super().__init__(name)
        self.ingredients = ingredients
        self.consumers = {
            ingredient: Consumer(f"Consumer({ingredient}) for {name}")
            for ingredient in ingredients
        }
        self.producer = Producer(name, product)
        self.crafted = 0

    def tick(self):
        self.debug("  inbuffer", [consumer.inbuffer for consumer in self.consumers.values()])
        if self.ready():
            self.debug("   YAY I CAN RECIPE")
            self.prepare_recipe()  # This consumes the ingredients
            self.producer.tick()
            self.crafted += 1

    def prepare_recipe(self):
        recipe_ingredients = []
        for item_type in self.ingredients:
            recipe_ingredients.append(self.get_ingredient(item_type))
        return recipe_ingredients

    def ready(self):
        recipe_ingredients = self.prepare_recipe()
        self.debug("MY RECIPE IS", recipe_ingredients)
        missing = any(item is None for item in recipe_ingredients)
        # Put them back
        for item in recipe_ingredients:
            if item is not None:
                self.consumers[item].inbuffer.append(item)
        if missing:
            self.debug("  missing ingredients:", recipe_ingredients)
            return False
        return True

    def get_ingredient(self, ingredient):
        if ingredient not in self.consumers:
            self.debug(" cannot get ingredient with no consumer", ingredient)
            return None
        if self.consumers[ingredient].inbuffer:
            return self.consumers[ingredient].inbuffer.pop()
        return None

