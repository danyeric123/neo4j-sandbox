# pip3 install neo4j-driver
# python3 example.py

from neo4j import GraphDatabase, basic_auth

from dotenv import load_dotenv
import os

load_dotenv()

ENDPOINT = os.getenv("ENDPOINT")
AUTH = os.getenv("AUTH")

driver = GraphDatabase.driver(ENDPOINT, auth=basic_auth("neo4j", AUTH))

cypher_query = """
MATCH (movie:Movie {title: $favorite})<-[:ACTED_IN]-(actor)-[:ACTED_IN]->(rec:Movie)<-[:ACTED_IN]-(otherActor)
RETURN DISTINCT otherActor.name AS actorName, actor.name AS coActor, rec.title AS movie, rec.released AS year
LIMIT 100
"""
favorite="The Matrix"
with driver.session(database="neo4j") as session:
    results = session.execute_read(
        lambda tx: tx.run(cypher_query, favorite=favorite).data())
    for record in results:
        # print(record["title"])
        print(f"{record['actorName']} acted with {record['coActor']} from {favorite} in {record['movie']} released in {record['year']}\n")

driver.close()
