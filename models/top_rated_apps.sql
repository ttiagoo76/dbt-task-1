SELECT 
    app_name,
    app_category,
    COUNT(*) as total_reviews,
    ROUND(AVG(rating::numeric), 2) as average_rating,
    MIN(rating) as min_rating,
    MAX(rating) as max_rating
FROM {{ source('app_reviews', 'app_reviews') }}
WHERE app_name IS NOT NULL
  AND rating IS NOT NULL
GROUP BY app_name, app_category
ORDER BY average_rating DESC, total_reviews DESC
LIMIT 3
