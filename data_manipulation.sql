DROP TABLE IF EXISTS Recipes;
/*!40101 SET @saved_cs_client = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;

CREATE table Recipes (
	id int AUTO_INCREMENT NOT NULL,
    name varchar(50),
    serving_size int NOT NULL DEFAULT 2,
    ingredients varchar(100) NOT NULL,
    steps varchar(500)
);

INSERT INTO Recipes (serving_size, ingredients, steps)
VALUES(2, 'tomato, egg, salt', '1. add oil 2. whisk eggs in a bowl with a pinch of salt 3. stir fry eggs when pan is hot 4. put eggs aside 5. stir fry tomatoes until soft and juicy 6. add in eggs and cook for 10 seconds');CREATE table Recipes (
    serving_size int NOT NULL DEFAULT 2,
    ingredients varchar(100) NOT NULL,
    steps varchar(500)
);

SELECT * from Recipes;