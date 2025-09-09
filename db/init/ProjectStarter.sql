-- A starter sql file to build database in MySQL Workbench

DROP DATABASE IF EXISTS `oma`;
CREATE DATABASE IF NOT EXISTS `oma`; 
USE `oma`;

-- Create dinners table 
DROP TABLE IF EXISTS `diners`;
CREATE TABLE `diners` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    diner VARCHAR(50) NOT NULL UNIQUE,
    phone CHAR(12) NOT NULL
);
-- Insert initial data with AI-generated customers
INSERT INTO `diners` (diner, phone)
VALUES 
	('Liam Sullivan', '347-891-2456'),
	('Sofia Rossi', '213-456-7890'),
	('Takumi Yamamoto', '646-998-3421'),
	('Amara Patel', '202-734-1122'),
	('Carlos Mendez', '415-667-9988'),
	('Chloe Dubois', '917-555-1342'),
	('Fatima Zahra', '303-281-7765'),
	('Ivan Petrov', '718-229-9001'),
	('Mei Chen', '929-321-4422'),
	('John Smith', '508-655-3311'),
	('Noura Fulan', '702-448-6712'),
	('Kim Jun', '562-889-0246'),
	('Anna Kowalska', '801-445-9021'),
	('Lucas Muller', '412-210-4567'),
	('Isabella Silva', '617-420-7654');

-- Create allergy list
-- If the allergen is other, the server will call the customer to confirm 
DROP TABLE IF EXISTS `allergies`;
CREATE TABLE `allergies` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dinerId INT NOT NULL,
    `type` ENUM('Dairy', 'Shellfish', 'Nuts', 'Eggs', 'Sesame', 'Wheat', 'Soy', 'Other'),
    `level` ENUM('Sensitive', 'Mild', 'Severe'),
    FOREIGN KEY (dinerId)
        REFERENCES diners (id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO `allergies`(dinerId, `type`, `level`)
VALUES
	(2, 'Shellfish', 'Severe'),
	(2, 'Nuts', 'Mild'),
	(5, 'Dairy', 'Sensitive'),
	(7, 'Wheat', 'Mild'),
	(11, 'Eggs', 'Severe'); 

 -- Create prices table/menu
 -- Each table is assigned a unique set of courses for the omakase experience 
DROP TABLE IF EXISTS `prices`;
CREATE TABLE `prices` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    class VARCHAR(50) NOT NULL UNIQUE,
    costPerPerson DECIMAL(8 , 2 ) NOT NULL CHECK (costPerPerson > 0)
);
INSERT INTO `prices` (class, costPerPerson)
VALUES 
	('Intro', 85.00),
	('Premium', 120.00),
	('Deluxe', 160.00),
	('Seasonal', 200.00);

-- Create rooms table to store detailed accessory and staff information
DROP TABLE IF EXISTS `rooms`;
CREATE TABLE rooms (
    room VARCHAR(50) PRIMARY KEY,
    TVProvided TINYINT NOT NULL,
    staff VARCHAR(50) DEFAULT 'Owner',
    classId INT NOT NULL,
    FOREIGN KEY (classId)
        REFERENCES prices (id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO `rooms` (room, TVprovided, staff, classId)
VALUES 
	('Sakura', 1, 'Chef Aki', 4),
	('Umi', 0, 'Chef Ken', 3),
	('Yuki', 1, 'Chef Hana', 2),
	('Tori', 0, 'Chef Ren', 1),
	('Kumo', 1, 'Chef Mei', 3),
	('Hana', 0, 'Chef Sota', 2),
	('Zen', 1, 'Chef Nori', 1),
	('Kai', 1, 'Chef Yuna', 4);


-- Create reservations table and initially insert 35 rows of AI-generated information
DROP TABLE IF EXISTS `reservations`;
CREATE TABLE `reservations` (
    dateAndTime DATETIME,
    room VARCHAR(50) NOT NULL,
    dinerId INT NOT NULL,
    totalDiners INT NOT NULL CHECK (totalDiners > 0),
    PRIMARY KEY (dateAndTime , room),
    FOREIGN KEY (room)
        REFERENCES rooms (room)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (dinerId)
        REFERENCES diners (id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO `reservations` (dateAndTime, room, dinerId, totalDiners)
VALUES
	('2025-07-02 17:00:00', 'Kumo', 11, 3),
	('2025-08-03 20:00:00', 'Hana', 9, 1),
	('2025-09-05 18:00:00', 'Kai', 3, 3),
	('2025-09-05 20:00:00', 'Kumo', 11, 2),
	('2025-09-10 18:00:00', 'Hana', 4, 4),
	('2025-09-12 18:00:00', 'Umi', 9, 6),
	('2025-09-13 18:00:00', 'Zen', 13, 6),
	('2025-09-14 17:30:00', 'Kumo', 9, 3),
	('2025-09-14 18:30:00', 'Hana', 2, 5),
	('2025-09-14 20:00:00', 'Yuki', 7, 5),
	('2025-09-15 18:00:00', 'Tori', 3, 1),
	('2025-09-15 19:30:00', 'Sakura', 6, 1),
	('2025-09-17 18:30:00', 'Umi', 8, 2),
	('2025-09-18 19:00:00', 'Tori', 12, 1),
	('2025-09-20 17:30:00', 'Sakura', 3, 6),
	('2025-09-21 17:00:00', 'Zen', 1, 4),
	('2025-09-23 18:30:00', 'Kai', 6, 3),
	('2025-09-26 18:00:00', 'Tori', 1, 1),
	('2025-09-26 18:30:00', 'Zen', 15, 6),
	('2025-09-29 17:30:00', 'Hana', 8, 3),
	('2025-10-01 19:30:00', 'Tori', 15, 4),
	('2025-10-02 18:30:00', 'Kai', 1, 3),
	('2025-10-04 18:00:00', 'Kai', 3, 5),
	('2025-10-06 20:00:00', 'Tori', 3, 1),
	('2025-10-08 20:00:00', 'Yuki', 14, 2),
	('2025-10-09 19:00:00', 'Umi', 10, 1),
	('2025-10-11 18:00:00', 'Zen', 14, 5),
	('2025-10-13 17:30:00', 'Yuki', 13, 1),
	('2025-10-15 20:00:00', 'Yuki', 3, 5),
	('2025-10-16 20:00:00', 'Zen', 1, 5),
	('2025-10-18 19:00:00', 'Kai', 6, 6),
	('2025-10-19 18:30:00', 'Tori', 14, 1),
	('2025-10-24 19:00:00', 'Zen', 2, 3),
	('2025-10-29 18:00:00', 'Yuki', 6, 6),
	('2025-10-30 17:30:00', 'Kumo', 8, 3);
    
    
-- ------------- Create Views --------------------
-- Create all details table
DROP VIEW IF EXISTS `all_details`;
CREATE VIEW `all_details` AS
    SELECT
        dateAndTime,
        rm.room,
        d.diner,
        d.phone,
        p.class,
        r.totalDiners,
        rm.staff,
        IF(a.dinerId is NOT NULL, 'Yes', 'No') AS allergy,
        CONCAT('$',
                CAST(p.costPerPerson * r.totalDiners AS DECIMAL (8 , 2 ))) AS bill
    FROM
        reservations r
            JOIN
        diners d ON r.dinerId = d.id
            JOIN
        rooms rm ON r.room = rm.room
            JOIN
        prices p ON rm.classId = p.id
			LEFT JOIN
		-- Filter out duplicate diners since a diner might have multiple allergies
        (SELECT DISTINCT dinerId FROM allergies) a ON a.dinerId = d.id
    ORDER BY dateAndTime;
        
-- Create total revenue by class
DROP VIEW IF EXISTS `total_revenue_by_class`;
CREATE VIEW `total_revenue_by_class` AS
    SELECT 
        class,
        totalDiners,
		totalRevenue,
		CONCAT('$', FORMAT(SUM(total) OVER (ORDER BY total DESC), 2)) AS rollingTotal
    FROM
		(
        SELECT 
			class,
			SUM(totalDiners) AS totalDiners,
			CONCAT('$',
					FORMAT(SUM(CAST(REPLACE(bill, '$', '') AS DECIMAL (8 , 2 ))),
						2)) AS totalRevenue,
			SUM(CAST(REPLACE(bill, '$', '') AS DECIMAL (8 , 2 ))) AS total
		FROM 
			all_details
		GROUP BY class   
        ) AS revenue;
        

-- ---------------- FOR diners ----------------- 
-- 1. Create getter function for looking up key based on diner name
DROP FUNCTION IF EXISTS `get_diner_id`;    
DELIMITER $$

CREATE FUNCTION `get_diner_id`(dinerName VARCHAR(50))
RETURNS INT DETERMINISTIC
BEGIN
	DECLARE foundDinerId INT DEFAULT -1;
    
	SELECT id INTO foundDinerId
    FROM diners
	WHERE diner = dinerName
    LIMIT 1;

    RETURN foundDinerId;
END$$

DELIMITER ;



-- 2. Create procedure to get all diners information
DROP PROCEDURE IF EXISTS `get_all_diners`;
DELIMITER $$
CREATE PROCEDURE `get_all_diners`()
BEGIN
	SELECT 
		*
	FROM 
		diners;
END $$
DELIMITER ;



-- 3. Create procedure to add diners
DROP PROCEDURE IF EXISTS `add_diner`;
DELIMITER $$
CREATE PROCEDURE `add_diner`(IN dinerName VARCHAR(50), IN phone CHAR(12))
BEGIN
	DECLARE verifyId INT;
	SET verifyId = get_diner_id(dinerName);
    
    IF verifyId = -1 THEN
		INSERT INTO diners (diner, phone)
		VALUES (dinerName, phone);
    END IF;
	-- Indicate successful insertion, it should return new id
	SELECT get_diner_id(dinerName) AS dinerId;
END $$
DELIMITER ;



-- 4. Create procedure for deleting diner
DROP PROCEDURE IF EXISTS `delete_diner`;
DELIMITER $$
CREATE PROCEDURE `delete_diner`(IN dinerName VARCHAR(50))
BEGIN
	DECLARE verifyId INT;
	SET verifyId = get_diner_id(dinerName);
    
    IF verifyId != -1 THEN
		DELETE FROM diners
		WHERE id = verifyId;
    END IF;
    
	-- Indicate successful deletion, it should return -1
	SELECT get_diner_id(dinerName) AS dinerId;
END $$
DELIMITER ;

    
-- ---------------- FOR prices -----------------     
-- 1. Create getter function for looking up key based on class name
DROP FUNCTION IF EXISTS `get_class_id`;    
DELIMITER $$

CREATE FUNCTION `get_class_id`(className VARCHAR(50))
RETURNS INT DETERMINISTIC
BEGIN
	DECLARE foundClassId INT DEFAULT -1;
    
	SELECT id INTO foundClassId
    FROM prices
	WHERE class = className
    LIMIT 1;

    RETURN foundClassId;
END$$

DELIMITER ; 



-- 2. Create procedure to get all prices information
DROP PROCEDURE IF EXISTS `get_all_prices`;
DELIMITER $$
CREATE PROCEDURE `get_all_prices`()
BEGIN
	SELECT 
		*
	FROM 
		prices;
END $$
DELIMITER ;



-- 3. Create procedure to add classes
DROP PROCEDURE IF EXISTS `add_class`;
DELIMITER $$
CREATE PROCEDURE `add_class`(IN className VARCHAR(50), IN price DECIMAL(8, 2))
BEGIN
	DECLARE verifyId INT;
	SET verifyId = get_class_id(className);
    
    IF verifyId = -1 THEN
		INSERT INTO prices (class, costPerPerson)
		VALUES (className, price);
    END IF;
	-- Indicate successful insertion
	SELECT get_class_id(className) AS classId;
END $$
DELIMITER ;



-- 4. Create procedure to update Class
DROP PROCEDURE IF EXISTS `update_class`;
DELIMITER $$
CREATE PROCEDURE `update_class`(IN oldClass VARCHAR(50), IN newClass VARCHAR(50), IN newPrice DECIMAL(8,2))
BEGIN
	DECLARE verifyId INT;
    DECLARE verifyNewId INT;
	SET verifyId = get_class_id(oldClass);
    SET verifyNewId = get_class_id(newClass);
    
    IF verifyId != -1 AND (verifyNewId = -1 OR newClass = oldClass) THEN
		UPDATE prices
        SET
			class = IFNULL(newClass, class),
            costPerPerson = IFNULL(newPrice, costPerPerson)
		WHERE id = verifyId;
    END IF;
END $$
DELIMITER ;

    
-- ---------------- FOR rooms -----------------     
-- 1. Create getter function to check existence based on room name
DROP FUNCTION IF EXISTS `get_room_existence`;    
DELIMITER $$

CREATE FUNCTION `get_room_existence`(roomName VARCHAR(50))
RETURNS INT DETERMINISTIC
BEGIN
	DECLARE foundRoom INT;
    -- If found, it will return 1 
	SELECT COUNT(roomName) INTO foundRoom
    FROM rooms
	WHERE room = roomName;
    
	-- If it is not found, foundRoom is 0 
    IF foundRoom = 0 THEN
    -- Change it into -1 to indicate non-existence  
		SET foundRoom = -1;
	END IF;
    RETURN foundRoom;
END$$
DELIMITER ;



-- 2. Get rooms table information.
-- Instead of getting the raw classId (int) and TVprovided(1 or 0)
-- It will present the class name of classId and yes or no of TVProvided to improve readability
DROP PROCEDURE IF EXISTS `get_all_rooms`;
DELIMITER $$
CREATE PROCEDURE `get_all_rooms`()
BEGIN
	SELECT 
		room,
        staff,
        p.class AS class,
        IF (TVProvided = 1, 'Yes', 'No') AS hasTV
	FROM 
		rooms r
	JOIN prices p
		ON r.classId = p.id
	ORDER BY room;
END $$
DELIMITER ;



-- 3. Create procedure to add rooms
DROP PROCEDURE IF EXISTS `add_room`;
DELIMITER $$
CREATE PROCEDURE `add_room`(IN roomName VARCHAR(50), IN tv TINYINT, IN className VARCHAR(50))
BEGIN
	-- If add room to business, default staff will be the owner for simplicity.
	DECLARE verifyClassId INT;
    DECLARE verifyRoom INT;
    
	SET verifyClassId = get_class_id(className);
    SET verifyRoom = get_room_existence(roomName);
    
    -- When class exists and room name does not exist, add new room
    IF verifyClassId != -1 AND verifyRoom = -1 THEN
		INSERT INTO rooms (room, TVProvided, classId)
		VALUES (roomName, tv, verifyClassId);
        SELECT get_room_existence(roomName) AS roomCreated;
	ELSEIF verifyClassId = -1 AND verifyRoom = -1 THEN
		SELECT -2 AS classNotValid;
	ELSEIF verifyClassId != -1 AND verifyRoom != -1 THEN
		SELECT -3 AS roomNameNotValid;
	ELSE 
		SELECT -4 AS classAndRoomNotValid;
    END IF;	
END $$
DELIMITER ;



-- 4. Create procedure to update Room
DROP PROCEDURE IF EXISTS `update_room`;
DELIMITER $$
CREATE PROCEDURE `update_room`(IN roomName VARCHAR(50), IN newRoom VARCHAR(50), IN tv INT, IN staffName VARCHAR(50), IN newClass VARCHAR(50))

BEGIN
	DECLARE verifyRoom INT;
    DECLARE verifyClass INT DEFAULT -1;
    DECLARE verifyNewRoom INT;
    SET verifyRoom = get_room_existence(roomName);
    SET verifyNewRoom = get_room_existence(newRoom);
	
    
    IF newClass IS NOT NULL THEN
		SET verifyClass = get_class_id(newClass);
    END IF;
    
    IF verifyRoom = 1 and (verifyNewRoom = -1 OR newRoom = roomName) THEN
		UPDATE rooms
        SET
			room = IFNULL(newRoom, room),
            TVProvided = IFNULL(tv, TVProvided),
            staff = IFNULL(staffName, staff),
            classId = IF(verifyClass = -1, classId, verifyClass) 
		WHERE room = roomName;
        SELECT 'Successfully updated' AS results;
	ELSE
		SELECT 'Invalid inputs' AS message;
    END IF;
END $$
DELIMITER ;



-- ---------------- FOR allergies -----------------     
-- 1. Create getter function to get key based on diner name and allergy type
DROP FUNCTION IF EXISTS `get_allergy_id`;    
DELIMITER $$
CREATE FUNCTION `get_allergy_id`(dinerName VARCHAR(50), allergyType VARCHAR(50))
RETURNS INT DETERMINISTIC
BEGIN
	DECLARE foundAllergyId INT DEFAULT -1;
    DECLARE foundDinerId INT;
    
    SET foundDinerId = get_diner_id(dinerName);
    
    IF foundDinerId != -1 THEN
		SELECT id INTO foundAllergyId
		FROM allergies
        -- ENUM is internally a string
		WHERE dinerId = foundDinerId AND `type` = allergyType
        LIMIT 1;
    END IF;
	
    RETURN foundAllergyId;
END$$
DELIMITER ;



-- 2. Get allergies table information.
-- Instead of getting the raw dinerId (int)
-- It will present the diner name of dinerId to improve readability
DROP PROCEDURE IF EXISTS `get_all_allergies`;
DELIMITER $$
CREATE PROCEDURE `get_all_allergies`()
BEGIN
	SELECT 
		a.id,
        diner,
        `type`,
        `level`
	FROM 
		allergies a
	JOIN diners d
		ON a.dinerId = d.id
	ORDER BY a.id;
END $$
DELIMITER ;


-- 3. Create procedure to add allergies
DROP PROCEDURE IF EXISTS `add_allergy`;
DELIMITER $$
CREATE PROCEDURE `add_allergy`(IN diner VARCHAR(50), IN allergyType VARCHAR(50), IN allergyLevel VARCHAR(50))
BEGIN
	DECLARE verifyId INT;
    DECLARE verifyDinerId INT;
    
    SET verifyId = get_allergy_id(diner, allergyType);
    SET verifyDinerId = get_diner_id(diner);
    
	-- Check if allergyType and allergy level in the ENUM
    -- In this project, it assumes all diners only have allergic reactions to the listed allergens 
    IF allergyType IN ('Dairy','Shellfish','Nuts','Eggs','Sesame','Wheat','Soy','Other') 
		AND allergyLevel IN ('Sensitive','Mild','Severe') 
        AND verifyId = -1 
        AND verifyDinerId != -1 THEN
		 INSERT INTO allergies(dinerId, `type`, `level`)
         VALUES (verifyDinerId, allergyType, allergyLevel);
         SELECT 'Yes' AS success;
	ELSE
    -- Detailed error signals will be implemented in DAL and BLL  
		SELECT 'Invalid Inputs' AS failure; 
    END IF;	
END $$
DELIMITER ;


-- 4. Create procedure for deleting allergy record
DROP PROCEDURE IF EXISTS `delete_allergy`;
DELIMITER $$
CREATE PROCEDURE `delete_allergy`(IN dinerName VARCHAR(50), IN allergyType VARCHAR(50))
BEGIN
	DECLARE verifyId INT;
	SET verifyId = get_allergy_id(dinerName, allergyType);
    
    IF verifyId != -1 THEN
		DELETE FROM allergies
		WHERE id = verifyId;
    END IF;
    
	-- Indicate successful deletion, it should return -1
	SELECT get_allergy_id(dinerName, allergyType) AS AllergyId;
END $$
DELIMITER ;


-- ---------------- FOR reservations -----------------     
-- 1. Create getter function to check existence based on datetime and room name
DROP FUNCTION IF EXISTS `get_reservation_existence`;    
DELIMITER $$
CREATE FUNCTION `get_reservation_existence`(dtime DATETIME, roomName VARCHAR(50))
RETURNS INT DETERMINISTIC
BEGIN
	DECLARE foundReservation INT;
    -- If found, it will return 1 
	SELECT COUNT(dateAndTime) INTO foundReservation
	FROM reservations
	WHERE dateAndTime = dtime AND room = roomName;
    -- If it is not found, foundReservation is 0 
    IF foundReservation = 0 THEN
		-- Reset foundReservation to align general setting (-1 means not found)
		SET foundReservation = -1;
	END IF;
    RETURN foundReservation;
END$$
DELIMITER ;


-- 2. Get reservation table information.
-- Instead of getting the raw dinerId (int)
-- It will present the diner name of dinerId to improve readability
DROP PROCEDURE IF EXISTS `get_all_reservations`;
DELIMITER $$
CREATE PROCEDURE `get_all_reservations`()
BEGIN
	SELECT 
		dateAndTime,
        room,
        diner,
        totalDiners
	FROM 
		reservations r
	JOIN diners d
		ON r.dinerId = d.id
	ORDER BY 1;
END $$
DELIMITER ;


-- 3. Create procedure to add reservations
DROP PROCEDURE IF EXISTS `add_reservation`;
DELIMITER $$
CREATE PROCEDURE `add_reservation`(IN dtime DATETIME, IN roomName VARCHAR(50), IN dinerName VARCHAR(50), IN totalDiners INT)
BEGIN
	
	DECLARE verifyRoom INT;
    DECLARE verifyDinerId INT;
    
    SET verifyRoom = get_room_existence(roomName);
    SET verifyDinerId = get_diner_id(dinerName);
    
	-- In this setting, only accept reservation that is at least two day prior and booking time must be in hours (17:00 - 21:30)
    -- reference: https://stackoverflow.com/questions/8544438/select-records-from-now-1-day
    IF dtime > NOW() + INTERVAL 2 DAY AND (TIME(dtime) BETWEEN '17:00:00' AND '21:30:00')
		AND verifyRoom = 1 
        AND verifyDinerId != -1 
        AND totalDiners > 0 THEN
		 INSERT INTO reservations(dateAndTime, room, dinerId, totalDiners)
         VALUES (dtime, roomName, verifyDinerId, totalDiners);
         SELECT 'Yes' AS success;
	ELSE
    -- Detailed error types, messages, double-booked will be implemented in DAL and BLL  
		SELECT 'Invalid Inputs' AS failure; 
    END IF;	
END $$
DELIMITER ;


-- 4. Create procedure for deleting reservation record
DROP PROCEDURE IF EXISTS `delete_reservation`;
DELIMITER $$
CREATE PROCEDURE `delete_reservation`(IN dtime DATETIME, IN roomName VARCHAR(50))
BEGIN
	DECLARE verifyExistence INT;
	SET verifyExistence = get_reservation_existence(dtime, roomName);
    
    IF verifyExistence != -1 THEN
		DELETE FROM reservations
		WHERE dateAndTime = dtime AND room = roomName;
    END IF;
    
	-- Indicate successful deletion, it should return -1
	SELECT get_reservation_existence(dtime, roomName) AS existence;
END $$
DELIMITER ;

-- 5. Create event handler to delete expired reservations every hour
SET GLOBAL event_scheduler = ON;
-- In this way, the expired reservations from initial AI-generated data will not appear in the table.
DROP EVENT IF EXISTS `delete_expired_reservations`;
DELIMITER $$
CREATE EVENT `delete_expired_reservations`
ON SCHEDULE EVERY 1 HOUR
STARTS CURRENT_TIMESTAMP
DO 
BEGIN
	DELETE
    FROM reservations
    -- Omakase experience lasts 90 minutes
    WHERE dateAndTime < (NOW() - INTERVAL 90 MINUTE);
END $$
DELIMITER ;
 
-- ---------------- FOR advanced feature -----------------    
-- Create a procedure to export alldetails view into csv
DROP PROCEDURE IF EXISTS `export_details`;
DELIMITER $$
CREATE PROCEDURE `export_details`()
BEGIN
	-- To improve readability, the csv files must include headers.
	-- To add the headers, use UNION ALL to combine these two results
    -- Make sure headers come first, use sorted number 
	SELECT
		dateAndTime, room, diner, phone, class, totalDiners, staff,
		allergy, bill
	FROM
		(
		SELECT 
			'dateAndTime' AS dateAndTime,
			'room' AS room,
			'diner' AS diner,
			'phone' AS phone,
			'class' AS class,
			'totalDiners' AS totalDiners,
			'staff' AS staff,
			'allergy' AS allergy,
			'bill' AS bill,
			1 AS sorted
		UNION ALL
			SELECT
				dateAndTime, room, diner, phone, class, totalDiners,
				staff, allergy, bill, 2 AS sorted
			FROM all_details
		) AS fullLists
    ORDER BY sorted, dateAndTime;
END $$
DELIMITER ;
