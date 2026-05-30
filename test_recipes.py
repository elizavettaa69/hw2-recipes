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

def test_ingredient_str():
    ing = Ingredient("Мука", 500, "г")
    assert str(ing) == "Мука: 500.0 г"

def test_ingredient_eq():
    ing1 = Ingredient("Мука", 500, "г")
    ing2 = Ingredient("Мука", 1000, "г")
    ing3 = Ingredient("Сахар", 500, "г")
    assert ing1 == ing2
    assert ing1 != ing3

def test_ingredient_quantity_validation():
    ing = Ingredient("Мука", 100, "г")
    with pytest.raises(ValueError):
        ing.quantity = -50

# тесты для Recipe

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
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    scaled = recipe.scale(2)
    assert scaled.ingredients[0].quantity == 600
    assert recipe.ingredients[0].quantity == 300  

def test_recipe_scale_invalid():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    with pytest.raises(ValueError):
        recipe.scale(0)

# тесты для диетических рецептов

def test_dietary_recipe():
    recipe = DietaryRecipe("Салат", "веган")
    recipe.add_ingredient(Ingredient("Огурец", 100, "г"))
    assert recipe.diet_type == "веган"
    assert "[веган]" in str(recipe)
    
    scaled = recipe.scale(2)
    assert isinstance(scaled, DietaryRecipe)
    assert scaled.diet_type == "веган"

# тесты для списка покупок

def test_shopping_list_add():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    
    shopping = ShoppingList()
    shopping.add_recipe(recipe, 2)
    assert len(shopping._items) == 1

def test_shopping_list_invalid_portions():
    recipe = Recipe("Пицца")
    shopping = ShoppingList()
    with pytest.raises(ValueError):
        shopping.add_recipe(recipe, 0)

def test_shopping_list_remove():
    recipe1 = Recipe("Пицца")
    recipe1.add_ingredient(Ingredient("Мука", 300, "г"))
    recipe2 = Recipe("Салат")
    recipe2.add_ingredient(Ingredient("Огурец", 100, "г"))
    
    shopping = ShoppingList()
    shopping.add_recipe(recipe1, 1)
    shopping.add_recipe(recipe2, 1)
    
    assert len(shopping._items) == 2
    shopping.remove_recipe("Пицца")
    assert len(shopping._items) == 1

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