import pytest
from ingredient import Ingredient
from recipe import Recipe
from dietary_recipe import DietaryRecipe
from shopping_list import ShoppingList

#  Тесты для Ingredient

def test_ingredient_creation():
    ing = Ingredient("Мука", 500, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500
    assert ing.unit == "г"

def test_ingredient_creation_negative_quantity():
    with pytest.raises(ValueError, match="Количество должно быть положительным"):
        Ingredient("Мука", -100, "г")

def test_ingredient_str():
    ing = Ingredient("Мука", 500, "г")
    assert str(ing) == "Мука: 500.0 г"

def test_ingredient_repr():
    ing = Ingredient("Мука", 500, "г")
    assert repr(ing) == "Ingredient('Мука', 500.0, 'г')"

def test_ingredient_eq():
    ing1 = Ingredient("Мука", 500, "г")
    ing2 = Ingredient("Мука", 1000, "г")
    ing3 = Ingredient("Сахар", 500, "г")
    ing4 = Ingredient("Мука", 500, "мл")
    assert ing1 == ing2
    assert ing1 != ing3
    assert ing1 != ing4

def test_ingredient_quantity_validation():
    ing = Ingredient("Мука", 100, "г")
    with pytest.raises(ValueError):
        ing.quantity = -50

def test_ingredient_quantity_setter_positive():
    ing = Ingredient("Мука", 100, "г")
    ing.quantity = 200
    assert ing.quantity == 200

# тесты для Recipe

def test_recipe_creation():
    recipe = Recipe("Пицца", [])
    assert recipe.title == "Пицца"
    assert recipe.ingredients == []


def test_recipe_add_ingredient():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    assert len(recipe) == 1

def test_recipe_add_duplicate():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))
    assert len(recipe) == 1
    for ing in recipe.ingredients:
        if ing.name == "Мука":
            assert ing.quantity == 500

def test_recipe_scale():
    recipe = Recipe("Пицца", [])
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    recipe.add_ingredient(Ingredient("Сыр", 200, "г"))
    scaled = recipe.scale(2)
    
    assert scaled.ingredients[0].quantity == 600
    assert scaled.ingredients[1].quantity == 400
    assert recipe.ingredients[0].quantity == 300  
    assert isinstance(scaled, Recipe) 

def test_recipe_scale_invalid():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    with pytest.raises(ValueError):
        recipe.scale(0)

def test_recipe_scale_zero():
    recipe = Recipe("Пицца", [])
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    
    with pytest.raises(ValueError, match="положительным"):
        recipe.scale(0)

def test_recipe_scale_negative():
    recipe = Recipe("Пицца", [])
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    
    with pytest.raises(ValueError, match="положительным"):
        recipe.scale(-2)

def test_recipe_len():
    recipe = Recipe("Пицца", [])
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    recipe.add_ingredient(Ingredient("Сыр", 200, "г"))
    assert len(recipe) == 2

def test_recipe_is_valid_ratio():
    assert Recipe.is_valid_ratio(2.5) == True
    assert Recipe.is_valid_ratio(1) == True
    assert Recipe.is_valid_ratio(0) == False
    assert Recipe.is_valid_ratio(-5) == False
    assert Recipe.is_valid_ratio("не число") == False


# тесты для диетических рецептов

def test_dietary_recipe():
    recipe = DietaryRecipe("Салат", "веган")
    recipe.add_ingredient(Ingredient("Огурец", 100, "г"))
    assert recipe.diet_type == "веган"
    assert "[веган]" in str(recipe)
    
    scaled = recipe.scale(2)
    assert isinstance(scaled, DietaryRecipe)
    assert scaled.diet_type == "веган"

def test_dietary_recipe_creation():
    recipe = DietaryRecipe("Салат", "веган", [])
    recipe.add_ingredient(Ingredient("Огурец", 100, "г"))
    
    assert recipe.title == "Салат"
    assert recipe.diet_type == "веган"
    assert len(recipe) == 1

def test_dietary_recipe_str():
    recipe = DietaryRecipe("Салат", "веган", [])
    recipe.add_ingredient(Ingredient("Огурец", 100, "г"))
    
    assert "[веган]" in str(recipe)
    assert "Салат" in str(recipe)

def test_dietary_recipe_scale_uses_super():
    recipe = DietaryRecipe("Салат", "веган", [])
    recipe.add_ingredient(Ingredient("Огурец", 100, "г"))
    scaled = recipe.scale(2)
    assert scaled.ingredients[0].quantity == 200

def test_dietary_recipe_scale_returns_dietary():
    recipe = DietaryRecipe("Салат", "веган", [])
    recipe.add_ingredient(Ingredient("Огурец", 100, "г"))
    scaled = recipe.scale(2)
    assert isinstance(scaled, DietaryRecipe)
    assert scaled.diet_type == "веган"
    assert scaled.ingredients[0].quantity == 200

# тесты для списка покупок

def test_shopping_list_add_recipe():
    recipe = Recipe("Пицца", [])
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    shopping = ShoppingList()
    shopping.add_recipe(recipe, 2)
    assert len(shopping._items) == 1
    assert shopping._items[0][1] == "Пицца"

def test_shopping_list_invalid_portions():
    recipe = Recipe("Пицца")
    shopping = ShoppingList()
    with pytest.raises(ValueError):
        shopping.add_recipe(recipe, 0)

def test_shopping_list_remove():
    recipe1 = Recipe("Пицца", [])
    recipe1.add_ingredient(Ingredient("Мука", 300, "г"))
    recipe2 = Recipe("Салат", [])
    recipe2.add_ingredient(Ingredient("Огурец", 100, "г"))
    
    shopping = ShoppingList()
    shopping.add_recipe(recipe1, 1)
    shopping.add_recipe(recipe2, 1)
    
    assert len(shopping._items) == 2
    shopping.remove_recipe("Пицца")
    assert len(shopping._items) == 1
    assert shopping._items[0][1] == "Салат"

def test_shopping_list_get_list_sums():
    pizza = Recipe("Пицца")
    pizza.add_ingredient(Ingredient("Мука", 300, "г"))
    bread = Recipe("Хлеб")
    bread.add_ingredient(Ingredient("Мука", 200, "г"))
    
    shopping = ShoppingList()
    shopping.add_recipe(pizza, 1)
    shopping.add_recipe(bread, 1)
    result = shopping.get_list()
    assert len(result) == 1
    assert result[0].quantity == 500

def test_shopping_list_add_two_lists():
    list1 = ShoppingList()
    list2 = ShoppingList()
    
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    list1.add_recipe(recipe, 1)
    list2.add_recipe(recipe, 1)
    combined = list1 + list2

    assert len(combined._items) == 2

def test_shopping_list_add_combines_lists():
    list1 = ShoppingList()
    list2 = ShoppingList()
    recipe = Recipe("Пицца", [])
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    list1.add_recipe(recipe, 1)
    list2.add_recipe(recipe, 1)
    combined = list1 + list2

    assert len(combined._items) == 2
    assert len(list1._items) == 1 
    assert len(list2._items) == 1  

def test_shopping_list_get_list_sorted_by_name():
    shopping = ShoppingList()
    
    recipe1 = Recipe("Рецепт1", [])
    recipe1.add_ingredient(Ingredient("Сыр", 200, "г"))
    recipe2 = Recipe("Рецепт2", [])
    recipe2.add_ingredient(Ingredient("Мука", 300, "г"))
    recipe3 = Recipe("Рецепт3", [])
    recipe3.add_ingredient(Ingredient("Банан", 100, "г"))
    shopping.add_recipe(recipe1, 1)
    shopping.add_recipe(recipe2, 1)
    shopping.add_recipe(recipe3, 1)
    result = shopping.get_list()
    names = [ing.name for ing in result]
    
    assert names == sorted(names) 