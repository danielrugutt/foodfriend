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
)
