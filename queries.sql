-- 1. Average rent and number of listings by city (aggregation)
SELECT city, COUNT(*) AS listings, ROUND(AVG(rent), 0) AS avg_rent
FROM listings
GROUP BY city
ORDER BY avg_rent DESC;

-- 2. Average rent by city and number of bedrooms (aggregation, two columns)
SELECT city, bhk, COUNT(*) AS listings, ROUND(AVG(rent), 0) AS avg_rent
FROM listings
GROUP BY city, bhk
ORDER BY city, bhk;

-- 3. Average rent per square foot by city (calculated column)
SELECT city, ROUND(AVG(rent_per_sqft), 2) AS avg_rent_per_sqft
FROM listings
GROUP BY city
ORDER BY avg_rent_per_sqft;

-- 4. How furnishing status changes average rent in each city
SELECT city, furnishing_status, ROUND(AVG(rent), 0) AS avg_rent
FROM listings
GROUP BY city, furnishing_status
ORDER BY city, avg_rent;

-- 5. Top 3 most expensive localities in each city (window function)
--    Only localities with at least 5 listings, so one big listing cannot skew the ranking.
SELECT city, area_locality, listings, avg_rent
FROM (
    SELECT city,
           area_locality,
           COUNT(*) AS listings,
           ROUND(AVG(rent), 0) AS avg_rent,
           RANK() OVER (PARTITION BY city ORDER BY AVG(rent) DESC) AS rnk
    FROM listings
    GROUP BY city, area_locality
    HAVING COUNT(*) >= 5
)
WHERE rnk <= 3
ORDER BY city, rnk;

-- 6. Average rent by region (join with the regions table)
SELECT r.region, COUNT(*) AS listings, ROUND(AVG(l.rent), 0) AS avg_rent
FROM listings AS l
JOIN regions AS r ON l.city = r.city
GROUP BY r.region
ORDER BY avg_rent DESC;

-- 7. Median rent by city (SQLite has no MEDIAN function, so use a window function)
SELECT city, ROUND(AVG(rent), 0) AS median_rent
FROM (
    SELECT city, rent,
           ROW_NUMBER() OVER (PARTITION BY city ORDER BY rent) AS rn,
           COUNT(*) OVER (PARTITION BY city) AS cnt
    FROM listings
)
WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
GROUP BY city
ORDER BY median_rent;
