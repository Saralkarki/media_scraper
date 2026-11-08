-- Total count of the data
SELECT count(*) as total_count_of_scraped_urls FROM url_list; -- 2744 items

-- Total run time 
SELECT date(max(fetched_at)) to_date, date(min(fetched_at)) from_date FROM url_list; -- From 2025 September 16th to 2026 July 16th

-- Count total number of days the engine has been working
SELECT ROUND(julianday(max(fetched_at)),0) - ROUND(julianday(min(fetched_at)),0) AS total_days FROM url_list; -- 303 days

-- Count actual days of working
SELECT count(DISTINCT date(fetched_at)) extraction_days FROM url_list; -- 177 Working days in total where urls were stored

-- Check the response code counts (First data filteration)
SELECT response_code,label,count(*) as total_response_code_counts
FROM url_list  ul
JOIN lkp_response_code lrc  ON ul.response_code  = lrc.code
GROUP BY response_code;  -- 1977 Good ones

-- How many failed
SELECT count(response_code)  as failure_response_codes_count
FROM url_list 
WHERE response_code != 200; --767 items that were filtered out because the response code were not 200 (Filteration)



-- sanity check
WITH successful_code AS (
SELECT count(response_code) ok_count FROM url_list WHERE response_code = 200),
unsuccessful_code AS(
SELECT count (response_code) bad_count FROM url_list WHERE response_code != 200)
SELECT ok_count, bad_count, ok_count + bad_count total_count 
FROM successful_code, unsuccessful_code; -- 2744 total articles


-- Check the Parsed Newspaper (Second data filteration before LLM model runs) - for all OK Counts (1977)
SELECT parsed_newspaper3k, count(*),label 
FROM url_list ul
JOIN lkp_parsed_newspaper3k lkp 
	ON ul.parsed_newspaper3k =  lkp.code
GROUP BY parsed_newspaper3k; -- 1 (succesfully extracted): 1364, 
-- Behind paywall(2) 251 , Manual intervention required(3) - 227, Extraction failed (0) - 135. 

-- Total count of unsuccessful
SELECT count(parsed_newspaper3k) total_count_failed_items FROM url_list where parsed_newspaper3k != 1; 

-- Sanity check total count of unparsed articles by newspaper 3k
WITH successful_code AS (
SELECT count(parsed_newspaper3k) good_count 
FROM url_list WHERE parsed_newspaper3k = 1),
unsuccessful_code AS (
SELECT count(parsed_newspaper3k) bad_count
FROM url_list WHERE parsed_newspaper3k !=1)
SELECT good_count, bad_count, good_count + bad_count total_count
FROM successful_code , unsuccessful_code ; -- 1364 articles parsed for the LLM to be able to run, 613 rejected by NEWSpaper 3k for reasons


-- Total LLM Parsed should run for 1364 articles
SELECT count(llm_parsed) FROM url_list; -- Out of 1364 parsed_newspaper3k content, 1362 have been processed by the LLM , 2 remain in pipeline

-- How many LLM parsed out of the 1364 that have extracted content or parsed_newspaper3k = 1 ;
SELECT llm_parsed,label, count(*) total_count
FROM url_list ul
LEFT JOIN lkp_llm_parsed llm
	ON ul.llm_parsed = llm.code
GROUP BY llm_parsed   ;
-- 1384 NULL (text not yet extracted by pipeline or where extraction has failed and so LLM won't run),  -1 : 221 failed, 
-- 1 : 36 made it to the final table, 2 : 1105 LLM flagged as unrelated (So this tell me we can still optimize our search maybe . Either way 
-- LLM is flagging them.

-- Month wise scraping of wheat data to see a pattern. I expect to find more data in November, December, January, Feb, March,April,May
select strftime('%Y-%m', fetched_at) as month, count(*) as monthly_data_extraction
from url_list 
WHERE response_code = 200
group by 1 
order by 1;

-- Month wise data for the classification
SELECT strftime('%Y-%m', date) AS month,
	   news_type,
       count(*)                AS events
FROM wheat_disease
WHERE date > '2024-12-12'
GROUP BY month,news_type
ORDER BY month;

SELECT url from wheat_disease where news_type = 'sighting';

SELECT country, count(*) FROM wheat_disease 
WHERE news_type is NOT NULL
GROUP BY country 
ORDER BY 2 DESC ;

SELECT count(*) AS district_rows,
       count(DISTINCT url) AS unique_articles
FROM wheat_disease
WHERE news_type is NOT NULL;

SELECT districts FROM wheat_disease ; -- Total 172 articles
