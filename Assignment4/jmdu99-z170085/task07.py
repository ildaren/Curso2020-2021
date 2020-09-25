# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tV5j-DRcpPtoJGoMj8v2DSqR_9wyXeiE

**Task 07: Querying RDF(s)**
"""

# !pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/resources/example6.rdf", format="xml")
'''
# Para ver el grafo inicialmente
print("\nGrafo completo")
for s, p, o in g:
  print(s,p,o)
  '''
from rdflib.plugins.sparql import prepareQuery

ns = Namespace("http://somewhere#")
subclasses=[]

# **TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**

print("\nTASK 7.1: List all subclasses of Person")

q1 = prepareQuery('''
  SELECT 
    ?Subject ?Subject2
  WHERE { 
    ?Subject rdfs:subClassOf ns:Person
    {?Subject2 rdfs:subClassOf ?Subject}
  }
  ''',
  initNs = { "ns": ns, "rdfs": RDFS}
  )
for r in g.query(q1):
  uri1= r.Subject
  uri2= r.Subject2
  subclasses.append(uri1)
  subclasses.append(uri2)
  print(uri1)
  print(uri2)

  
# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

print("\nTASK 7.2: List all individuals of Person")

q2 = prepareQuery('''
  SELECT 
    ?Subject
  WHERE { 
    {?Subject rdf:type ns:Person} 
    UNION
    {?Subject rdf:type ?Researcher}
    UNION
    { ?Subject rdf:type ?PhDstudent}
  }
  ''',
  initNs = { "ns": ns, "rdf": RDF}
  )
for r in g.query(q2,initBindings = {'?Researcher' : subclasses[0], '?PhDstudent' : subclasses[1]}):
  print(r.Subject.toPython())


# **TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**
print("\nTASK 7.3: List all individuals of Person and all their properties including their class")

q3 = prepareQuery('''
  SELECT 
    ?Subject ?Predicate ?Object
  WHERE {
      {
    {?Subject rdf:type ns:Person} 
    UNION
    { ?Subject rdf:type ?Researcher }
    UNION
    { ?Subject rdf:type ?PhDstudent}
    }.
    {?Subject ?Predicate ?Object} 
  }
  ''',
  initNs = { "ns": ns, "rdf": RDF}
  )
contador=0
for r in g.query(q3,initBindings = {'?Researcher' : subclasses[0], '?PhDstudent' : subclasses[1]}):
  print("Row "+str(contador) +"\n")
  print(r)
  print("\n")
  contador+=1