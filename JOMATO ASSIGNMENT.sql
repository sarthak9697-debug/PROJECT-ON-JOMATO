SELECT * FROM [dbo].[Jomato$]

                                            --ASSIGNMENT 2 JOMATO--
--CREATE A USER-DEFINED FUNCTION TO STUFF THE WORD “CHICKEN” INTO ‘QUICK BITES’

CREATE FUNCTION dbo.fn_StuffChicken (@input VARCHAR(100))
RETURNS VARCHAR(100)
AS
BEGIN
    RETURN STUFF(@input, 7, 0, 'Chicken ')
END;
SELECT 
    RestaurantName,
    RestaurantType,
    dbo.fn_StuffChicken(RestaurantType) AS StuffedType
FROM Jomato$;


 -- CREATE A RATING STATUS COLUMN BASED ON RATING CONDITIONS
 SELECT *,
    CASE
        WHEN Rating > 4 THEN 'Excellent'
        WHEN Rating > 3.5 THEN 'Good'
        WHEN Rating > 3 THEN 'Average'
        ELSE 'Bad'
    END AS RatingStatus
FROM Jomato$;

-- FIND CEIL, FLOOR, AND ABS VALUES OF RATING; DISPLAY CURRENT DATE, YEAR, MONTH, DAY
SELECT 
    RestaurantName,
    Rating,
    CEILING(Rating) AS CeilRating,
    FLOOR(Rating) AS FloorRating,
    ABS(Rating) AS AbsoluteRating,
    GETDATE() AS CurrentDate,
    YEAR(GETDATE()) AS Year,
    DATENAME(MONTH, GETDATE()) AS Month_Name,
    DAY(GETDATE()) AS Day
FROM Jomato$;

--DISPLAY RESTAURANT TYPE AND TOTAL AVERAGE COST USING ROLLUP
SELECT 
    RestaurantType,
    SUM(AverageCost) AS TotalAvgCost
FROM Jomato$
GROUP BY ROLLUP(RestaurantType);

-- USE THE FUNCTION TO DISPLAY THE RESTAURANT NAME AND CUISINE TYPE WHICH HAS THE MAXIMUM NUMBER OF RATINGS
SELECT TOP 1 
    RestaurantName, 
    CuisinesType, 
    [no#of#rating]
FROM Jomato$
ORDER BY [no#of#rating] DESC;
