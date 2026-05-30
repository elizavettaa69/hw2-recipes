from ingredient import Ingredient
from recipe import Recipe

class ShoppingList:
    def __init__(self):
        self._items = []  
    
    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        
        scaled_recipe = recipe.scale(portions)
        
        for ing in scaled_recipe.ingredients:
            self._items.append((ing, recipe.title))
    
    def remove_recipe(self, title: str):
        self._items = [item for item in self._items if item[1] != title]
    
    def get_list(self):
        summary = {}
        for ing, recipe_title in self._items:
            key = (ing.name, ing.unit)
            if key in summary:
                summary[key] += ing.quantity
            else:
                summary[key] = ing.quantity
        
        result = []
        for (name, unit), quantity in summary.items():
            result.append(Ingredient(name, quantity, unit))
        
        result.sort(key=lambda x: x.name)
        return result
    
    def __add__(self, other):
        new_list = ShoppingList()
        new_list._items = self._items.copy() + other._items.copy()
        return new_list