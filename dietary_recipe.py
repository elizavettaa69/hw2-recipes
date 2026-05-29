from recipe import Recipe
from ingredient import Ingredient

class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type
    
    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент масштабирования должен быть положительным числом")
        
        new_ingredients = []
        for ing in self.ingredients:
            new_ing = Ingredient(ing.name, ing.quantity * ratio, ing.unit)
            new_ingredients.append(new_ing)
        
        return DietaryRecipe(self.title, self.diet_type, new_ingredients)
    
    def __str__(self):
        parent_str = super().__str__()
        return f"[{self.diet_type}] {parent_str}"