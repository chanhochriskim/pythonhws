# Use this file to write your queries. Submit this file to Gradescope after finishing your homework.

# Make sure to test that this script prints out the strings (your SQL queries) correctly.

# To verify your submission is in the correct format: `python3 hw1.py`

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
	SELECT DISTINCT language
FROM language 
WHERE lang_id IN (
SELECT lang_id
FROM languagerel 
WHERE agent_id IN (
SELECT agent_id
FROM agent
WHERE city = 'Paris'
)
);
	"""
	

def query2():
	return """
	SELECT affiliation.title, agent.agent_id, agent.first, agent.last, agent.city
FROM agent JOIN affiliationrel
ON agent.agent_id = affiliationrel.agent_id JOIN affiliation
ON affiliationrel.aff_id = affiliation.aff_id
WHERE agent.city = 'Seattle' AND affiliation.title = 'FBI';

	"""

def query3():
	return """
	SELECT affiliation.title, agent.agent_id, agent.first, agent.last, language.language
FROM agent 
JOIN affiliationrel ON agent.agent_id = affiliationrel.agent_id 
JOIN affiliation ON affiliationrel.aff_id = affiliation.aff_id 
JOIN languagerel ON agent.agent_id = languagerel.agent_id
JOIN language ON languagerel.lang_id = language.lang_id
WHERE city = 'Seattle' AND affiliation.title = 'FBI';
	"""
	
def query4():
	return """
	SELECT mission.name, team.name, agent.last, language.language, skill.skill 
FROM agent 
JOIN skillrel ON agent.agent_id = skillrel.agent_id
JOIN skill ON skill.skill_id = skillrel.skill_id 
JOIN languagerel ON agent.agent_id = languagerel.agent_id
JOIN language ON language.lang_id = languagerel.lang_id
JOIN teamrel ON agent.agent_id = teamrel.agent_id 
JOIN team ON team.team_id = teamrel.team_id
JOIN mission ON mission.team_id = team.team_id
WHERE skill = 'Kung Fu' AND language = 'English';

	"""

def query5():
	return """
	SELECT agent.agent_id, agent.first, agent.last, affiliation.title
FROM agent
LEFT JOIN affiliationrel ON affiliationrel.agent_id = agent.agent_id
LEFT JOIN affiliation ON affiliation.aff_id = affiliationrel.aff_id
WHERE agent.country = 'Brazil';
	"""

def query6():
	return """
	SELECT agent.agent_id, agent.first, agent.last, language.language, skill.skill
FROM agent
LEFT JOIN skillrel ON agent.agent_id = skillrel.agent_id
LEFT JOIN skill ON skill.skill_id = skillrel.skill_id
JOIN languagerel ON agent.agent_id = languagerel.agent_id 
JOIN language ON language.lang_id = languagerel.lang_id 
WHERE agent.agent_id = 1 OR agent.agent_id = 2 OR agent.agent_id = 3 OR agent.agent_id = 4
ORDER BY agent.agent_id, language.language;
	"""

def query7():
	return """
	SELECT agent.agent_id, agent.first, agent.last, language.language, skill.skill
FROM agent
JOIN skillrel ON agent.agent_id = skillrel.agent_id
JOIN skill ON skill.skill_id = skillrel.skill_id
LEFT JOIN languagerel ON agent.agent_id = languagerel.agent_id 
LEFT JOIN language ON language.lang_id = languagerel.lang_id 
WHERE agent.agent_id = 1 OR agent.agent_id = 2 OR agent.agent_id = 3 OR agent.agent_id = 4
ORDER BY agent.agent_id, language.language;
	"""

def query8():
	return """
	SELECT agent.agent_id, agent.first, agent.last, language.language, skill.skill
FROM agent
JOIN skillrel ON agent.agent_id = skillrel.agent_id
JOIN skill ON skill.skill_id = skillrel.skill_id
JOIN languagerel ON agent.agent_id = languagerel.agent_id 
JOIN language ON language.lang_id = languagerel.lang_id 
WHERE agent.agent_id = 1 OR agent.agent_id = 2 OR agent.agent_id = 3 OR agent.agent_id = 4
ORDER BY agent.agent_id, language.language;
	"""

def query9():
	return """
	SELECT COUNT(DISTINCT language) AS lan_count FROM language;
	"""

def query10():
	return """
	SELECT COUNT(name) AS teams_count FROM team
WHERE team.meeting_frequency = 'weekly';
	"""

def query11():
	return """
	SELECT agent.clearance_id, round(avg(agent.salary), 2) AS average_salary 
FROM agent
WHERE agent.city = 'Miami'
GROUP BY clearance_id
HAVING avg(salary) > 200000;

	"""

def query12():
	return """
	SELECT  skill.skill, COUNT(agent.agent_id) AS cnt
FROM agent
JOIN skillrel ON agent.agent_id = skillrel.agent_id
JOIN skill ON skill.skill_id = skillrel.skill_id
GROUP BY skill.skill
HAVING cnt <= 20;

	"""

def query13():
	return """
	SELECT language.language as "skills and languages"
FROM agent
JOIN languagerel ON agent.agent_id = languagerel.agent_id
JOIN language ON languagerel.lang_id = language.lang_id
WHERE agent.agent_id = 1

UNION 

SELECT skill.skill 
FROM agent
JOIN skillrel ON agent.agent_id = skillrel.agent_id 
JOIN skill ON skillrel.skill_id = skill.skill_id
WHERE agent.agent_id = 1;
	"""

def query14():
	return """
	SELECT 'affiliation: ' || affiliation.title AS aff_city
FROM agent
JOIN affiliationrel ON affiliationrel.agent_id = agent.agent_id
JOIN affiliation ON affiliation.aff_id = affiliationrel.aff_id 
WHERE agent.agent_id IN (
		SELECT agent_id 
		FROM teamrel
		WHERE team_id IN (
		SELECT mission.team_id
		FROM mission
		WHERE name = 'Media Blanket'
)
)

UNION

SELECT 'city: ' || agent.city AS aff_city
FROM agent
WHERE agent.agent_id IN (
		SELECT agent_id 
		FROM teamrel
		WHERE team_id IN (
		SELECT mission.team_id
		FROM mission
		WHERE name = 'Media Blanket'
)
)
	"""

def query15():
	return """
	SELECT DISTINCT team.name AS team_name
FROM team
WHERE team.team_id IN (
SELECT DISTINCT team.team_id
FROM agent
JOIN teamrel ON teamrel.agent_id = agent.agent_id
JOIN team ON teamrel.team_id = team.team_id
JOIN languagerel ON languagerel.agent_id = agent.agent_id
JOIN language ON languagerel.lang_id = language.lang_id
WHERE language.language = 'English'

INTERSECT

SELECT DISTINCT team.team_id
FROM agent
JOIN teamrel ON teamrel.agent_id = agent.agent_id
JOIN team ON teamrel.team_id = team.team_id
JOIN skillrel ON skillrel.agent_id = agent.agent_id
JOIN skill ON skillrel.skill_id = skill.skill_id
WHERE skill.skill = 'Kung Fu'
);
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
