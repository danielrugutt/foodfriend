-- INCLUDING THIS BECAUSE I WILL PROBABLY MESS UP
-- UNCOMMENT AND RUN AS NEEDED
-- DROP TABLE recipe CASCADE CONSTRAINTS;
-- DROP TABLE user_data CASCADE CONSTRAINTS;
-- DROP TABLE nutrition CASCADE CONSTRAINTS;
-- DROP TABLE ingredient CASCADE CONSTRAINTS;
-- DROP TABLE recipeIngredient CASCADE CONSTRAINTS;
-- DROP TABLE plannedMeal CASCADE CONSTRAINTS;
-- DROP TABLE plannedDay CASCADE CONSTRAINTS;
-- DROP TABLE dietaryPreference CASCADE CONSTRAINTS;
-- DROP TABLE recipeList CASCADE CONSTRAINTS;

-- not including recipeBuilder, spoonacularRecipe, spoonacularAdapter, recipePrototype, search, factorymethod, exporter, exporttype, pdfexporter, emailexporter

-- done
CREATE TABLE Recipe
(
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    cooking_time INTEGER,
    servings INTEGER,
    cuisine TEXT,
    steps BLOB,
    diet BLOB,
    intolerances BLOB
    -- recipeingredients and nutrition have their own tables
);

-- done
-- cannot be called "user" unfortunately
CREATE TABLE UserData
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT2 NOT NULL
    -- recipelist, plannedday, and dietarypreferences have their own tables
);

-- done
CREATE TABLE Nutrition
(
    calories FLOAT,
    totalFat FLOAT,
    saturatedFat FLOAT,
    transFat FLOAT,
    cholesterol FLOAT,
    sodium FLOAT,
    carbohydrates FLOAT,
    protein FLOAT,
    recipe_id INTEGER NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES Recipe(id) ON DELETE CASCADE,
    PRIMARY KEY (recipe_id)
);

CREATE TABLE Ingredient
(
    id INTEGER NOT NULL AUTOINCREMENT,
    name TEXT NOT NULL,
    type ?????
);

-- done
CREATE TABLE RecipeIngredient
(
    quantity NUMBER NOT NULL,
    unit TEXT,
    recipe_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES Recipe(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES Ingredient(id) ON DELETE CASCADE,
    PRIMARY KEY (recipe_id, ingredient_id)
);

-- done
CREATE TABLE PlannedDay
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    calendar_day DATE NOT NULL UNIQUE
);

-- done
CREATE TABLE PlannedMeal
(
    id INTEGER PRIMARY KEY AUTOINCREMENT
    planned_day_id INTEGER
    time DATETIME NOT NULL,
    title TEXT NOT NULL,
    notes TEXT,
    recipe_id INTEGER NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES Recipe(id) ON DELETE CASCADE,
    FOREIGN KEY (planned_day_id) REFERENCES PlannedDay(id) ON DELETE CASCADE,
    PRIMARY KEY (plannedDay)
);


CREATE TABLE DietaryPreference
(
    user_id INTEGER NOT NULL,

    FOREIGN KEY (user_id) REFERENCES UserData(id) ON DELETE CASCADE,
    PRIMARY KEY(user_id)
);

-- done
CREATE TABLE RecipeList
(
    list_name TEXT,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES Recipe(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES UserData(id) ON DELETE CASCADE,
    PRIMARY KEY(user_id, recipe_id)
);
