from ingredient import Ingredient

class Recipe:
    def __init__(self, title: str, ingredients=None):
        self.title = title
        self.ingredients = ingredients if ingredients is not None else []
    
    def add_ingredient(self, ingredient: Ingredient):
        "Добавляем ингредиент, если уже есть - суммируем"
        for i in self.ingredients:
            if i == ingredient:  # сработает __eq__ из Ingredient
                i.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)
    
    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int, float)) and ratio > 0
    
    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент масштабирования должен быть положительным")
        
        new_ingredients = []
        for ing in self.ingredients:
            new_ing = Ingredient(ing.name, ing.quantity * ratio, ing.unit)
            new_ingredients.append(new_ing)
        
        return Recipe(self.title, new_ingredients)
    
    def __len__(self):
        return len(self.ingredients)
    
    def __str__(self):
        if not self.ingredients:
            return f"{self.title}:\n  (нет ингредиентов)"
        
        ingredients_str = "\n".join(f"  {i}" for i in self.ingredients)
        return f"{self.title}:\n{ingredients_str}"


if __name__ == "__main__":
    # Простая проверка
    пицца = Recipe("Пицца Маргарита")
    пицца.add_ingredient(Ingredient("Мука", 300, "г"))
    пицца.add_ingredient(Ingredient("Сыр", 200, "г"))
    print(пицца)
    print(f"Количество ингредиентов: {len(пицца)}")