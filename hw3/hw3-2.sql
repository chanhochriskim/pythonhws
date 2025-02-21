
DELIMITER $$ 
CREATE PROCEDURE `running_avg1`(IN agent_X_id integer) 
BEGIN  
-- Start your code here
DELETE FROM sp1_result;

INSERT INTO sp1_result (agent_Y_id)
SELECT agent_Y_id
FROM (
    -- Common languages subquery
    SELECT * FROM (
        SELECT l1.agent_id AS agent_Y_id, COUNT(*) AS total
        FROM languagerel l1
        JOIN languagerel l2 
            ON l1.lang_id = l2.lang_id
        WHERE l2.agent_id = agent_X_id 
            AND l1.agent_id <> agent_X_id
        GROUP BY l1.agent_id
    ) AS comm_language 

    UNION ALL

    -- Common skills subquery
    SELECT * FROM (
        SELECT s1.agent_id AS agent_Y_id, COUNT(*) AS total
        FROM skillrel s1
        JOIN skillrel s2 
            ON s1.skill_id = s2.skill_id
        WHERE s2.agent_id = agent_X_id 
            AND s1.agent_id <> agent_X_id
        GROUP BY s1.agent_id
    ) AS comm_skill 
) AS combined_similarity  

GROUP BY agent_Y_id
ORDER BY SUM(total) DESC, agent_Y_id ASC
LIMIT 1;
-- End your code here
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE running_avg2()
BEGIN
-- Start your code here
    DECLARE loop_end_flag INT DEFAULT FALSE; -- flag when we reach the last row of cursor
    -- variables to store agent data while iterating through cursor 
    DECLARE var_agent_id INT;
    DECLARE var_first TEXT;
    DECLARE var_last TEXT;
    DECLARE var_salary INT;
    DECLARE var_country TEXT;

    -- agent cursor (one by one thru row in a loop)
    DECLARE cursor_agent CURSOR FOR 
        SELECT agent_id, first, last, salary, country
        FROM agent
        ORDER BY salary DESC, agent_id ASC;

    -- no more rows left detecting (if true, set loop_end_flag flag to be 1)
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET loop_end_flag = 1;

    -- clearing previous results... DELETE FROM sp2_result WHERE agent_id IS NOT NULL;
    
    -- temporary tables to track down each
    -- 1. selected agents: top 10 2. used countries: uniqueness 3. used languages: at least 1 new language.
    CREATE TEMPORARY TABLE IF NOT EXISTS top10_agents (
        agent_id INT PRIMARY KEY, first TEXT, last TEXT, salary INT, country VARCHAR(255)
    );

    -- already used country 
    CREATE TEMPORARY TABLE IF NOT EXISTS country_tracker (
        country VARCHAR(255) UNIQUE
    );

    -- already spoken language 
    CREATE TEMPORARY TABLE IF NOT EXISTS lang_tracker (
        lang_id INT UNIQUE 
    );
    
    -- opening cursor to read agents one by one & loop through agents until 10 agents are met. 
    OPEN cursor_agent;

    looping: LOOP
        FETCH cursor_agent INTO var_agent_id, var_first, var_last, var_salary, var_country;

        IF loop_end_flag THEN
            LEAVE looping;
        END IF; 

        -- checking if agent's country is used already
        IF NOT EXISTS (SELECT 1 FROM country_tracker WHERE country = var_country) THEN 
            -- if not, checking if agent has a new language
            IF EXISTS (
                SELECT 1 
                FROM languagerel lr
                WHERE lr.agent_id = var_agent_id AND NOT EXISTS (
                    SELECT 1 FROM lang_tracker
                    WHERE lang_tracker.lang_id = lr.lang_id
                )
            ) THEN
                -- insert the agent into the table. 
                INSERT INTO top10_agents (agent_id, first, last, salary, country)
                VALUES (var_agent_id, var_first, var_last, var_salary, var_country);
                -- update the country tracker
                INSERT IGNORE INTO country_tracker (country) VALUES (var_country);
                -- also update the lang tracker. 
                INSERT IGNORE INTO lang_tracker (lang_id)
                SELECT lang_id 
                FROM languagerel
                WHERE agent_id = var_agent_id;
            END IF; 
        END IF;

        -- stop if 10 agents are met.
        IF (SELECT COUNT(agent_id) FROM top10_agents) = 10 THEN  
            LEAVE looping;
        END IF; 
    END LOOP;

    INSERT INTO sp2_result (agent_id, first, last, salary, country)
    SELECT agent_id, first, last, salary, country FROM top10_agents;

    DROP TEMPORARY TABLE IF EXISTS top10_agents;
    DROP TEMPORARY TABLE IF EXISTS country_tracker;
    DROP TEMPORARY TABLE IF EXISTS lang_tracker;
-- End your code here
END $$
DELIMITER ;
