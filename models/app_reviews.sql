{{ config(materialized='view', alias='app_reviews') }}

SELECT *
FROM {{ source('app_reviews', 'app_reviews') }}
WHERE review_text IS NOT NULL
  AND review_text != ''
