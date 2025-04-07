CREATE TABLE Recipe
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    cooking_time INTEGER,
    servings INTEGER,
    cuisine TEXT,
    steps BLOB,
    diet BLOB,
    intolerances BLOB
    -- recipeingredients and nutrition have their own tables
);

-- CREATE TABLE Ingredient
-- (
--     id INTEGER NOT NULL AUTOINCREMENT,
--     name TEXT NOT NULL,
--     quantity TEXT NOT NULL,
-- );
--
-- CREATE TABLE RecipeIngredient
-- (
--     quantity NUMBER NOT NULL,
--     unit TEXT,
--     recipe_id INTEGER NOT NULL,
--     -- ADD INGREDIENT ID BACK LATER
--     -- ingredient_id INTEGER NOT NULL,
--     FOREIGN KEY (recipe_id) REFERENCES Recipe(id) ON DELETE CASCADE,
--     -- FOREIGN KEY (ingredient_id) REFERENCES Ingredient(id) ON DELETE CASCADE,
--     PRIMARY KEY (recipe_id)
--     -- PRIMARY KEY (ingredient_id)
-- );

CREATE TABLE TestIngredient
(
    name TEXT NOT NULL,
    quantity TEXT NOT NULL,
    unit TEXT,
    recipe_id INTEGER NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES Recipe(id) ON DELETE CASCADE,
    PRIMARY KEY (recipe_id, name)
);

CREATE TABLE UserData
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT2 NOT NULL
    -- recipelist, plannedday, and dietarypreferences have their own tables
);

CREATE TABLE DietaryPreference
(
    user_id INTEGER NOT NULL,
    max_sugar INTEGER,
    intolerances BLOB,
    diet BLOB,
    excludedIngredient BLOB,
    excludedCuisine BLOB,
    FOREIGN KEY (user_id) REFERENCES UserData(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id)
);
