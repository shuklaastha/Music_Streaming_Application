BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER NOT NULL,
	"username"	VARCHAR(80) NOT NULL,
	"email"	VARCHAR(120) NOT NULL,
	"password"	VARCHAR(120) NOT NULL,
	UNIQUE("email"),
	UNIQUE("username"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "manager" (
	"m_id"	INTEGER NOT NULL,
	"m_name"	VARCHAR(50) NOT NULL,
	"m_email"	VARCHAR(20) NOT NULL,
	"m_password"	VARCHAR(10) NOT NULL,
	UNIQUE("m_email"),
	PRIMARY KEY("m_id")
);
CREATE TABLE IF NOT EXISTS "product" (
	"product_id"	INTEGER NOT NULL,
	"product_name"	VARCHAR NOT NULL,
	"quantity"	INTEGER NOT NULL,
	"out_of_stock"	BOOLEAN NOT NULL,
	"category"	VARCHAR NOT NULL,
	"unit"	VARCHAR NOT NULL,
	"price_per_unit"	FLOAT NOT NULL,
	PRIMARY KEY("product_id")
);
CREATE TABLE IF NOT EXISTS "category" (
	"id"	INTEGER NOT NULL,
	"category_name"	VARCHAR(255) NOT NULL,
	UNIQUE("category_name"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "uom" (
	"unit_id"	INTEGER NOT NULL,
	"unit_name"	VARCHAR NOT NULL,
	PRIMARY KEY("unit_id")
);
CREATE TABLE IF NOT EXISTS "order" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"overall_total"	FLOAT NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("user_id") REFERENCES "user"("id")
);
CREATE TABLE IF NOT EXISTS "cart_item" (
	"id"	INTEGER NOT NULL,
	"product_id"	INTEGER NOT NULL,
	"order_id"	INTEGER,
	"quantity"	INTEGER NOT NULL,
	"total_price"	FLOAT NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("product_id") REFERENCES "product"("product_id"),
	FOREIGN KEY("order_id") REFERENCES "order"("id")
);
CREATE TABLE IF NOT EXISTS "order_item" (
	"id"	INTEGER NOT NULL,
	"order_id"	INTEGER NOT NULL,
	"product_id"	INTEGER NOT NULL,
	"quantity"	INTEGER NOT NULL,
	"total_price"	FLOAT NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("order_id") REFERENCES "order"("id"),
	FOREIGN KEY("product_id") REFERENCES "product"("product_id")
);
CREATE TABLE IF NOT EXISTS "monthly_sales" (
	"id"	INTEGER NOT NULL,
	"month"	VARCHAR(20) NOT NULL,
	"sales_amount"	FLOAT NOT NULL,
	PRIMARY KEY("id")
);
INSERT INTO "user" ("id","username","email","password") VALUES (1,'Karunesh','chaturvediaman19927@gmail.com','1234');
INSERT INTO "user" ("id","username","email","password") VALUES (2,'Aalu','aalu@gmail.com','1234');
INSERT INTO "user" ("id","username","email","password") VALUES (3,'parth','parthwww@gmail.com','1234');
INSERT INTO "manager" ("m_id","m_name","m_email","m_password") VALUES (1,'Karunesh','chaturvediaman1997@gmail.com','aman@1234');
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (2,'Tomato',8,0,'Vegetable','Kg',25.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (3,'Onion',10,0,'Vegetable','Kg',35.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (4,'Cabbage',-4,1,'Vegetable','Kg',40.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (5,'Carrot',9,0,'Vegetable','Kg',30.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (6,'Cauliflower',8,0,'Vegetable','Kg',40.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (7,'Cucumbers',22,0,'Vegetable','Kg',40.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (8,'Beans',18,0,'Vegetable','Kg',80.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (9,'Mushroom',28,0,'Vegetable','250g',45.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (10,'Apple',26,0,'Fruit','Kg',200.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (11,'Guava',9,0,'Fruit','Kg',80.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (12,'Mango',30,0,'Fruit','Kg',120.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (13,'Orange',13,0,'Fruit','Kg',80.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (14,'Papaya',30,0,'Fruit','Kg',60.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (15,'Dragonfruit',18,0,'Fruit','Kg',180.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (16,'Pineapple',10,0,'Fruit','Kg',70.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (17,'pomegranate',12,0,'Fruit','Kg',160.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (18,'Watermelon',13,0,'Fruit','Kg',70.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (19,'Pear',30,0,'Fruit','Kg',120.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (20,'Milk',28,0,'Dairy','L',65.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (21,'Curd',34,0,'Dairy','500ml',20.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (22,'Paneer',27,0,'Dairy','250g',90.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (23,'Butter',28,0,'Dairy','250g',180.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (24,'Maggi',28,0,'Snacks','250g',50.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (25,'Biscuit',35,0,'Snacks','75g',10.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (26,'Aloo Bhujiya',10,0,'Snacks','500g',90.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (27,'Moong Daal',18,0,'Snacks','250g',60.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (28,'KitKat',24,0,'Snacks','50g',50.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (29,'Dairy Milk',30,0,'Snacks','50g',55.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (30,'Lays',20,0,'Snacks','50g',20.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (31,'Banana chips',30,0,'Snacks','150g',100.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (32,'Rice',48,0,'Food_Grains','Kg',65.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (33,'Daal',40,0,'Food_Grains','Kg',90.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (34,'Ghee',20,0,'Food_Grains','500g',320.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (35,'Peanuts',20,0,'Food_Grains','Kg',200.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (36,'Sugar',29,0,'Food_Grains','Kg',60.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (37,'Atta',30,0,'Food_Grains','10Kg',410.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (38,'Atta',20,0,'Food_Grains','2Kg',100.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (39,'Cashew',19,0,'Food_Grains','100g',95.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (40,'Rice Bran Oil',20,0,'Food_Grains','L',144.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (41,'Salt',36,0,'Food_Grains','Kg',26.0);
INSERT INTO "product" ("product_id","product_name","quantity","out_of_stock","category","unit","price_per_unit") VALUES (43,'Choclate',10,0,'Snacks','50g',50.0);
INSERT INTO "category" ("id","category_name") VALUES (5,'Snacks');
INSERT INTO "category" ("id","category_name") VALUES (6,'Fruit');
INSERT INTO "category" ("id","category_name") VALUES (8,'Food_Grains');
INSERT INTO "category" ("id","category_name") VALUES (9,'Dairy');
INSERT INTO "category" ("id","category_name") VALUES (10,'Vegetable');
INSERT INTO "order" ("id","user_id","overall_total") VALUES (1,1,860.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (2,2,220.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (3,1,325.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (4,1,440.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (5,1,520.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (6,1,355.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (7,1,400.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (8,3,260.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (9,3,592.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (10,1,100.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (11,1,100.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (12,1,100.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (13,1,215.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (14,1,487.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (15,1,380.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (16,1,100.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (17,2,525.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (18,1,350.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (19,3,280.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (20,1,390.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (21,1,140.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (22,1,320.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (23,1,120.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (24,1,75.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (25,1,210.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (26,1,140.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (27,1,535.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (28,1,240.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (29,1,140.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (30,1,320.0);
INSERT INTO "order" ("id","user_id","overall_total") VALUES (31,1,120.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (1,1,11,2,160.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (2,1,15,2,360.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (3,1,17,2,320.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (4,1,21,1,20.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (5,2,32,2,130.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (6,2,2,2,50.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (7,2,6,1,40.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (8,3,22,2,180.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (9,3,5,1,30.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (10,3,3,1,35.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (11,3,6,2,80.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (12,4,6,1,40.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (13,4,10,2,400.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (14,5,11,1,80.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (15,5,17,1,160.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (16,5,16,4,280.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (17,6,14,3,180.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (18,6,3,5,175.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (19,7,4,10,400.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (20,8,3,2,70.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (21,8,9,2,90.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (22,8,11,1,80.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (23,8,21,1,20.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (24,9,11,1,80.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (25,9,23,2,360.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (26,9,28,2,100.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (27,9,41,2,52.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (28,10,3,1,35.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (29,10,2,1,25.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (30,10,6,1,40.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (31,11,2,1,25.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (32,11,3,1,35.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (33,11,4,1,40.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (34,12,2,1,25.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (35,12,3,1,35.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (36,12,4,1,40.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (37,13,3,1,35.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (38,13,5,3,90.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (39,13,9,2,90.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (40,14,17,2,320.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (41,14,25,2,20.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (42,14,39,1,95.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (43,14,41,2,52.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (44,15,36,1,60.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (45,15,9,2,90.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (46,15,18,2,140.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (47,15,22,1,90.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (48,16,14,1,60.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (49,16,21,2,40.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (50,17,9,1,45.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (51,17,6,2,80.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (52,17,16,2,140.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (53,17,21,2,40.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (54,17,28,2,100.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (55,17,27,2,120.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (56,18,2,2,50.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (57,18,11,2,160.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (58,18,16,2,140.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (59,19,2,2,50.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (60,19,25,3,30.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (61,19,24,2,100.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (62,19,28,2,100.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (63,20,3,2,70.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (64,20,17,2,320.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (65,21,3,2,70.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (66,21,5,1,30.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (67,21,4,1,40.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (68,22,8,2,160.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (69,22,17,1,160.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (70,23,4,3,120.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (71,24,3,1,35.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (72,24,4,1,40.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (73,25,20,2,130.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (74,25,4,2,80.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (75,26,16,2,140.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (76,27,10,2,400.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (77,27,14,1,60.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (78,27,4,1,40.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (79,27,3,1,35.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (80,28,11,1,80.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (81,28,13,2,160.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (82,29,3,4,140.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (83,30,4,8,320.0);
INSERT INTO "order_item" ("id","order_id","product_id","quantity","total_price") VALUES (84,31,4,3,120.0);
INSERT INTO "monthly_sales" ("id","month","sales_amount") VALUES (1,'January',1200.0);
INSERT INTO "monthly_sales" ("id","month","sales_amount") VALUES (2,'Fedruary',1400.0);
INSERT INTO "monthly_sales" ("id","month","sales_amount") VALUES (3,'March',1300.0);
INSERT INTO "monthly_sales" ("id","month","sales_amount") VALUES (4,'April',1350.0);
INSERT INTO "monthly_sales" ("id","month","sales_amount") VALUES (5,'May',1500.0);
INSERT INTO "monthly_sales" ("id","month","sales_amount") VALUES (6,'June',1700.0);
INSERT INTO "monthly_sales" ("id","month","sales_amount") VALUES (7,'July',1600.0);
INSERT INTO "monthly_sales" ("id","month","sales_amount") VALUES (8,'August',1750.0);
INSERT INTO "monthly_sales" ("id","month","sales_amount") VALUES (9,'September',2000.0);
COMMIT;
