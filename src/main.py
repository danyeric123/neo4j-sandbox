# pip3 install neo4j-driver
# python3 example.py

from neo4j import GraphDatabase, basic_auth

from dotenv import load_dotenv
import os

load_dotenv()

# ENDPOINT = os.getenv("ENDPOINT")
# AUTH = os.getenv("AUTH")

# driver = GraphDatabase.driver(ENDPOINT, auth=basic_auth("neo4j", AUTH))

# cypher_query = """
# MATCH (movie:Movie {title: $favorite})<-[:ACTED_IN]-(actor)-[:ACTED_IN]->(rec:Movie)<-[:ACTED_IN]-(otherActor)
# RETURN DISTINCT otherActor.name AS actorName, actor.name AS coActor, rec.title AS movie, rec.released AS year
# LIMIT 100
# """
# favorite="The Matrix"
# with driver.session(database="neo4j") as session:
#     results = session.execute_read(
#         lambda tx: tx.run(cypher_query, favorite=favorite).data())
#     for record in results:
#         # print(record["title"])
#         print(f"{record['actorName']} acted with {record['coActor']} from {favorite} in {record['movie']} released in {record['year']}\n")

# driver.close()


driver = GraphDatabase.driver(
  "bolt://54.160.57.27:7687",
  auth=basic_auth("neo4j", "material-railway-island"))

from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config
from random import randint

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


config.DATABASE_URL = f'bolt://{NEO4J_USERNAME}:{NEO4J_PASSWORD}@{NEO4J_URI}'

class Book(StructuredNode):
    title = StringProperty(unique_index=True)
    author = RelationshipTo('Author', 'AUTHOR')
    genre = RelationshipTo('Genre', 'GENRE')

class Author(StructuredNode):
    name = StringProperty(unique_index=True)
    books = RelationshipFrom('Book', 'AUTHOR')

class Genre(StructuredNode):
    name = StringProperty(unique_index=True)
    books = RelationshipFrom('Book', 'GENRE')


genres = ['Fantasy', 'Adventure', 'Thriller', 'Romance', 'Mystery', 'Horror', 'Sci-Fi', 'Dystopian', 'Memoir', 'Cooking', 'Self-help', 'Health', 'Guide', 'Travel', 'Children', 'Religion', 'Spirituality', 'Science', 'History', 'Math', 'Anthology', 'Poetry', 'Encyclopedias', 'Dictionaries', 'Comics', 'Art', 'Journals', 'Biographies', 'Autobiographies', 'Fantasy', 'Adventure', 'Thriller', 'Romance', 'Mystery', 'Horror', 'Sci-Fi', 'Dystopian', 'Memoir', 'Cooking', 'Self-help', 'Health', 'Guide', 'Travel', 'Children', 'Religion', 'Spirituality', 'Science', 'History', 'Math', 'Anthology', 'Poetry', 'Encyclopedias', 'Dictionaries', 'Comics', 'Art', 'Journals', 'Biographies', 'Autobiographies']
authors = [f"Author {i}" for i in range(100)]
books = [f"Book {i}" for i in range(100)]

for genre in genres:
    print(f"Creating genre {genre}")
    Genre(name=genre).save()

for author in authors:
    print(f"Creating author {author}")
    Author(name=author).save()

for book in books:
    print(f"Creating book {book}")
    Book(title=book).save()

for book in Book.nodes:
    print(f"Connecting book {book.title} to author and genre")
    book.author.connect(Author.nodes[randint(0, 99)])
    book.genre.connect(Genre.nodes[randint(0, len(genres) - 1)])
