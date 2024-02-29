DROP TABLE IF EXISTS Recipes;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;

CREATE table Recipes (
	id int AUTO_INCREMENT NOT NULL,
    recipe_name varchar(50) NOT NULL,
    serving_size int NOT NULL DEFAULT 2,
    ingredients varchar(300) NOT NULL,
    steps varchar(700),
    PRIMARY KEY (id)
);

INSERT INTO Recipes (recipe_name, serving_size, ingredients, steps)
VALUES('tomato egg', 2, 'tomato, egg, salt', '1. add oil 2. whisk eggs in a bowl with a pinch of salt 3. stir fry eggs when pan is hot 4. put eggs aside 5. stir fry tomatoes until soft and juicy 6. add in eggs and cook for 10 seconds');


SELECT * from Recipes;