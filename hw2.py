# Use this file to write your queries. Submit this file to Gradescope after finishing your homework.

# Make sure to test that this script prints out the strings (your SQL queries) correctly.

# To verify your submission is in the correct format: `python3 hw2.py`

# Make sure the program prints out your SQL statements correctly. That means the autograder will read you SQL correctly. Running the Python file will not execute your SQL statements, it simply prints them.

instr = '''Instructions:
	Please put the queries under the corresponding functions below.
	Running this python file will check if the formatting is okay.
	Example:
		def query1():
			return """
				SELECT * FROM agent
			"""
'''

def query1():
	return """
SELECT agent.agent_id, agent.first, agent.last, agent.salary
FROM agent
WHERE salary IN (
(SELECT MIN(salary) FROM agent),
(SELECT MAX(salary) FROM agent)
);
	"""

def query2():
	return """
SELECT team.name, ROUND(AVG(agent.salary), 2) AS team_avg_salary 
FROM teamrel	
JOIN agent ON teamrel.agent_id = agent.agent_id
JOIN team ON teamrel.team_id = team.team_id
GROUP BY teamrel.team_id 
HAVING AVG(agent.salary) < (SELECT AVG(salary) FROM agent)
ORDER BY team_avg_salary ASC;
	"""

def query3():
	return """
SELECT team.name, ROUND(AVG(agent.salary), 2) AS avg_salary, COUNT(agent.agent_id) AS count_agents
FROM teamrel
JOIN agent ON teamrel.agent_id = agent.agent_id
JOIN team ON teamrel.team_id = team.team_id
GROUP BY teamrel.team_id
HAVING COUNT(agent.agent_id) >= 2 
ORDER BY avg_salary DESC
LIMIT 1;
	"""
	
def query4():
	return """
SELECT agent.agent_id, agent.first, agent.last, skill.skill
FROM agent
JOIN skillrel ON skillrel.agent_id = agent.agent_id
JOIN skill ON skill.skill_id = skillrel.skill_id
WHERE skill.skill_id IN (
    SELECT skill_id
    FROM skillrel
    GROUP BY skill_id
    HAVING COUNT(agent_id) <= 5
);
	"""

def query5():
	return """
SELECT affiliation.aff_id, affiliation.title, COUNT(mission.mission_id) AS active_missions
FROM mission
JOIN team ON mission.team_id = team.team_id 
JOIN teamrel ON team.team_id = teamrel.team_id 
JOIN affiliationrel ON teamrel.agent_id = affiliationrel.agent_id 
JOIN affiliation ON affiliationrel.aff_id = affiliation.aff_id
WHERE mission.mission_status = 'ongoing'
GROUP BY affiliation.aff_id
HAVING COUNT(mission.mission_id) = (
    SELECT MAX(mission_count)
    FROM (
        SELECT affiliationrel.aff_id, COUNT(mission.mission_id) AS mission_count
        FROM mission
        JOIN team ON mission.team_id = team.team_id 
        JOIN teamrel ON team.team_id = teamrel.team_id 
        JOIN affiliationrel ON teamrel.agent_id = affiliationrel.agent_id 
        WHERE mission.mission_status = 'ongoing'
        GROUP BY affiliationrel.aff_id
    ) 
)

UNION

SELECT affiliation.aff_id, affiliation.title, COUNT(mission.mission_id) AS active_missions
FROM mission
JOIN team ON mission.team_id = team.team_id 
JOIN teamrel ON team.team_id = teamrel.team_id 
JOIN affiliationrel ON teamrel.agent_id = affiliationrel.agent_id 
JOIN affiliation ON affiliationrel.aff_id = affiliation.aff_id
WHERE mission.mission_status = 'ongoing'
GROUP BY affiliation.aff_id
HAVING COUNT(mission.mission_id) = (
    SELECT MIN(mission_count2)
    FROM (
        SELECT affiliationrel.aff_id, COUNT(mission.mission_id) AS mission_count2
        FROM mission
        JOIN team ON mission.team_id = team.team_id 
        JOIN teamrel ON team.team_id = teamrel.team_id 
        JOIN affiliationrel ON teamrel.agent_id = affiliationrel.agent_id 
        WHERE mission.mission_status = 'ongoing'
        GROUP BY affiliationrel.aff_id
    ) 
)
	"""

def query6():
	return """
SELECT agent.agent_id, agent.first, agent.last, agent.salary, team.name
FROM agent
JOIN teamrel ON teamrel.agent_id = agent.agent_id
JOIN team ON team.team_id = teamrel.team_id 
WHERE team.name IN ('Oink', 'Wired')
AND agent.salary > (
	SELECT AVG(ag.salary)
	FROM agent ag
	JOIN teamrel trel ON trel.agent_id = ag.agent_id
	JOIN team t ON trel.team_id = t.team_id 
	WHERE team.team_id = t.team_id
);
	"""

def query7():
	return """
SELECT team.name, agent.agent_id, agent.first, agent.last, agent.salary
FROM agent
JOIN teamrel ON teamrel.agent_id = agent.agent_id 
JOIN team ON team.team_id = teamrel.team_id 
WHERE team.name = 'Giraffe' 
AND agent.salary IN (
	(SELECT MIN(salary) FROM agent
	JOIN teamrel ON teamrel.agent_id = agent.agent_id 
	JOIN team ON team.team_id = teamrel.team_id 
	WHERE team.name = 'Giraffe'),
	(SELECT MAX(salary) FROM agent
	JOIN teamrel ON teamrel.agent_id = agent.agent_id 
	JOIN team ON team.team_id = teamrel.team_id 
	WHERE team.name = 'Giraffe')
)

UNION

SELECT team.name, agent.agent_id, agent.first, agent.last, agent.salary
FROM agent
JOIN teamrel ON teamrel.agent_id = agent.agent_id 
JOIN team ON team.team_id = teamrel.team_id 
WHERE team.name = 'Vikings' 
AND agent.salary IN (
	(SELECT MIN(salary) FROM agent
	JOIN teamrel ON teamrel.agent_id = agent.agent_id 
	JOIN team ON team.team_id = teamrel.team_id 
	WHERE team.name = 'Vikings'),
	(SELECT MAX(salary) FROM agent
	JOIN teamrel ON teamrel.agent_id = agent.agent_id 
	JOIN team ON team.team_id = teamrel.team_id 
	WHERE team.name = 'Vikings')
)
	"""

def query8():
	return """
SELECT t1.name AS team1, t2.name AS team2, COUNT(tr1.agent_id) AS agent_count 
FROM teamrel tr1 
JOIN teamrel tr2 ON tr1.agent_id = tr2.agent_id 
JOIN team t1 ON tr1.team_id = t1.team_id 
JOIN team t2 ON tr2.team_id = t2.team_id 
WHERE t1.team_id < t2.team_id 
GROUP BY t1.name, t2.name
HAVING COUNT(tr1.agent_id) > 1;
	"""

def query9():
	return """
SELECT agent.agent_id, agent.first, agent.last, skill.skill
FROM agent
JOIN skillrel ON agent.agent_id = skillrel.agent_id 
JOIN skill ON skill.skill_id = skillrel.skill_id
WHERE skill.skill = 'Meteorology' 
AND agent.agent_id NOT IN (
	-- returns a list of agents who are assigned to ongoing
	SELECT DISTINCT teamrel.agent_id
	FROM mission
	JOIN team ON mission.team_id = team.team_id 
	JOIN teamrel ON team.team_id = teamrel.team_id
	WHERE mission.mission_status = 'ongoing'
)
	"""

def query10():
	return """
SELECT securityclearance.sc_id, securityclearance.sc_level, language.language, COUNT(agent.agent_id) AS agent_count 
FROM securityclearance
JOIN agent ON securityclearance.sc_id = agent.clearance_id
JOIN languagerel ON languagerel.agent_id = agent.agent_id 	
JOIN language ON language.lang_id = languagerel.lang_id
GROUP BY securityclearance.sc_id, securityclearance.sc_level, language.language
HAVING COUNT(agent.agent_id) = (
	SELECT MAX(agent_count)
	FROM (
        SELECT securityclearance.sc_id, language.language, COUNT(agent.agent_id) AS agent_count 
        FROM securityclearance
        JOIN agent ON securityclearance.sc_id = agent.clearance_id
        JOIN languagerel ON languagerel.agent_id = agent.agent_id 
        JOIN language ON language.lang_id = languagerel.lang_id
        GROUP BY securityclearance.sc_id, securityclearance.sc_level, language.language
    ) AS max_counts
    WHERE max_counts.sc_id = securityclearance.sc_id
)
	"""

def query11():
	return """
SELECT team.team_id, team.name, COUNT(distinct_agent.agent_id) AS cnt 
FROM team
JOIN (
	SELECT teamrel.team_id, languagerel.agent_id
	FROM teamrel 
	JOIN languagerel ON teamrel.agent_id = languagerel.agent_id
	WHERE teamrel.team_id BETWEEN 1 AND 10
	GROUP BY teamrel.team_id, languagerel.lang_id 
	HAVING COUNT(languagerel.agent_id) = 1
) AS distinct_agent 
ON team.team_id = distinct_agent.team_id 
GROUP BY team.team_id, team.name 
	"""

def query12():
	return """
SELECT 
    agent.agent_id, 
    agent.first, 
    agent.last, 
    COALESCE(affiliation.title, '') AS affiliation_title, 
    ROUND(COALESCE(salary_info.avg_salary, 0),2) AS avg_salary,  
    COALESCE(salary_info.max_salary, 0) AS max_salary  
FROM agent
LEFT JOIN affiliationrel ON affiliationrel.agent_id = agent.agent_id
LEFT JOIN affiliation ON affiliation.aff_id = affiliationrel.aff_id
LEFT JOIN (
    SELECT affiliationrel.aff_id, 
           AVG(agent.salary) AS avg_salary, 
           MAX(agent.salary) AS max_salary
    FROM agent
    LEFT JOIN affiliationrel ON affiliationrel.agent_id = agent.agent_id
    GROUP BY affiliationrel.aff_id
) salary_info 
ON affiliation.aff_id = salary_info.aff_id
WHERE agent.country = 'Brazil'
GROUP BY agent.agent_id, agent.first, agent.last, COALESCE(affiliation.title, '')

	"""

def query13():
	return """
SELECT affiliation.aff_id, affiliation.title, SUM(mission.mission_status = 'success') AS successful_missions, SUM(mission.mission_status = 'failed') AS failed_missions
FROM affiliation
JOIN affiliationrel ON affiliation.aff_id = affiliationrel.aff_id
JOIN teamrel ON affiliationrel.agent_id = teamrel.agent_id
JOIN team ON teamrel.team_id = team.team_id
JOIN mission ON team.team_id = mission.team_id
GROUP BY affiliation.aff_id, affiliation.title
	"""

def query14():
	return """
SELECT agent.agent_id, agent.first, agent.last, agent.country, affiliation.title
FROM agent
JOIN affiliationrel ON agent.agent_id = affiliationrel.agent_id 
JOIN affiliation ON affiliationrel.aff_id = affiliation.aff_id 
WHERE agent.country = 'Japan'
AND agent.agent_id IN (
    SELECT affiliationrel.agent_id
    FROM affiliationrel
    JOIN agent ON agent.agent_id = affiliationrel.agent_id
    WHERE agent.country = 'Japan'
    GROUP BY affiliationrel.agent_id
    HAVING COUNT(affiliationrel.aff_id) > 1
)
ORDER BY agent.agent_id 
	"""

def query15():
	return """
SELECT 
    affiliation.title AS affiliation,
    COALESCE(SUM(agent.country = 'USA'), 0) AS USA,
	COALESCE(SUM(agent.country = 'Poland'), 0) AS Poland,
	COALESCE(SUM(agent.country = 'Austrailia'), 0) AS Austrailia
FROM agent
JOIN affiliationrel ON agent.agent_id = affiliationrel.agent_id 
JOIN affiliation ON affiliationrel.aff_id = affiliation.aff_id 
WHERE affiliation.title IN ('MI6', 'KGB', 'Interpol', 'CIA', 'FBI')
GROUP BY affiliation.title
ORDER BY affiliation.aff_id
	"""

# Do not edit below

if __name__ == "__main__":
	try:
		if all(type(eval(f'print(t:=query{f+1}()),t')[1])==str for f in range(15)):
			print(f'Your submission is valid.')
		else:
			raise TypeError('Invalid Return Types.')
	except Exception as e:
		print(f'Your submission is invalid.\n{instr}\n{e}')
