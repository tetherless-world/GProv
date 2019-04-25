#from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
from flask import Flask, render_template
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, term
from rdflib.namespace import FOAF, DC
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd



foaf = Graph()



def plot_stats():
    # Data to plot
    labels = 'Python', 'C++', 'Ruby', 'Java'
    sizes = [215, 130, 245, 210]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    #explode = (0, 0, 0, 0.1)  # explode 1st slice
     
    # Plot
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
     
    plt.axis('equal')
    plt.show()

def provenance_Information(drug, therapy):
    foaf.parse("gprov/static/rdf/guidelineInstance.owl")
    
    query1 = '''
    PREFIX bibo: <http://bibliontology.com/index.html#>
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX gprov: <https://idea.tw.rpi.edu/projects/heals/gprov/>
    PREFIX prov: <https://www.w3.org/ns/prov#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xml: <http://www.w3.org/XML/1998/namespace>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    SELECT DISTINCT ?recommendationText ?evidenceText ?citation ?articleTitle
    WHERE{{
          ?rule rdf:type gprov:FormalRule .
          ?rule prov:wasDerivedFrom ?recommendation .
          ?recommendation rdf:type gprov:Recommendation .
          ?recommendation gprov:hasValue ?recommendationText . 
          ?recommendation prov:wasGeneratedBy ?evidenceSentence .
          ?evidenceSentence rdf:type gprov:EvidenceSentence .
          ?evidenceSentence gprov:hasValue ?evidenceText .
          ?evidenceSentence prov:hadPrimarySource ?citation .
          ?citation dct:title ?articleTitle .
         FILTER (regex(str(?recommendationText), "{0}") || regex(str(?evidenceText), "{1}") ) .
        }}
    '''
    query = query1.format(drug, therapy)
    res = foaf.query(query)

    return list(res)[0]

def patient_query(lastName):
    foaf = Graph()
    foaf.parse("gprov/static/rdf/patients.ttl", format="turtle")   
    
    query1 = """
    PREFIX dmto: <https://bioportal.bioontology.org/ontologies/DMTO.owl/>
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX person: <http://idea.rpi.edu/ont/person#>
    PREFIX sio: <http://semanticscience.org/resource/>
    PREFIX snomed: <http://purl.bioontology.org/ontology/SNOMEDCT/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xml: <http://www.w3.org/XML/1998/namespace>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    SELECT DISTINCT ?FName ?LName ?race ?sex ?drug ?age ?drugsubplan
    WHERE{{
          ?p rdf:type sio:Patient .
          ?p sio:hasAttribute ?a .
          ?a rdf:type sio:FirstName .
          ?a sio:hasValue ?FName .
          ?p sio:hasAttribute ?b .
          ?b rdf:type sio:LastName .
          ?b sio:hasValue ?LName .
          ?p sio:hasAttribute ?c .
          ?c rdf:type sio:Race .
          ?c sio:hasValue ?race .
          ?p sio:hasAttribute ?d .
          ?d rdf:type sio:BiologicalSex .
          ?d sio:hasValue ?sex .
          ?p sio:hasAttribute ?e .
          ?e rdf:type sio:Drug .
          ?e sio:hasValue ?drug .
          ?p sio:hasAttribute ?g .
          ?g rdf:type sio:Age .
          ?g sio:hasValue ?age .
          ?p sio:hasAttribute ?f .
          ?f rdf:type dmto:DrugSubplan .
          ?f sio:hasValue ?drugsubplan .
          FILTER (regex(str(?LName), \"{0}\") ) .
        }}
    """
    
    query = query1.format(lastName)
    res = foaf.query(query)
    return res
#    print(list(res))


    
def annotation(data):
    g= Graph()

    gprov = Namespace("https://purl.org/heals/gprov/")
    prov = Namespace("https://www.w3.org/ns/prov#")
    sio = Namespace("http://semanticscience.org/resource/")
    bibo = Namespace("http://purl.org/ontology/bibo/")
    
    rule = data.iloc[0]['rule']
    recommendation = data.iloc[0]['recommendation']
    recommendation_text = data.iloc[0]['recommendation_text']
    influencer = data.iloc[0]['influencer']
    grade_value = data.iloc[0]['grade_value']
    generated_by = data.iloc[0]['generated_by']
    evidence_sentence = data.iloc[0]['evidence_sentence']
    primary_source = data.iloc[0]['primary_source']
    
    guideline = data.iloc[0]['guideline']
    guideline_volume = data.iloc[0]['guideline_volume']
    guideline_date = data.iloc[0]['guideline_date']
    guideline_title = data.iloc[0]['guideline_title']
    filename = rule.replace('_','')
    
    formal_rule = term.URIRef('gprov:{}'.format(rule))
    rec = term.URIRef('gprov:{}'.format(recommendation))
    g.add((formal_rule, RDF.type, gprov.FormalRule))
    g.add((formal_rule, prov.wasDerievedFrom, rec))
    
    g.add((rec, RDF.type, gprov.Recommendation))
    g.add((rec, DC.isPartOf, term.URIRef('gprov:{}'.format(guideline))))
    g.add((rec, sio.SIO_000300, Literal(recommendation_text)))
    g.add((rec, prov.wasGeneratedBy, term.URIRef('gprov:{}'.format(generated_by))))
    g.add((rec, prov.hadPrimarySource, term.URIRef('gprov:{}'.format(guideline))))
    g.add((rec, prov.wasInfluencedBy, term.URIRef('gprov:{}'.format(influencer))))
    
    g.add((term.URIRef('gprov:{}'.format(generated_by)), RDF.type, gprov.EvidenceSentence))
    g.add((term.URIRef('gprov:{}'.format(generated_by)), prov.hadPrimarySource, term.URIRef('gprov:{}'.format(primary_source))))
    g.add((term.URIRef('gprov:{}'.format(generated_by)), sio.SIO_000300, Literal(evidence_sentence)))
    
    g.add((term.URIRef('gprov:{}'.format(influencer)), RDF.type, gprov.Grade))
    g.add((term.URIRef('gprov:{}'.format(influencer)), prov.hadPrimarySource, term.URIRef('gprov:{}'.format(primary_source))))
    g.add((term.URIRef('gprov:{}'.format(influencer)), sio.SIO_000300, Literal(grade_value)))
    
    g.add((term.URIRef('gprov:{}'.format(guideline)), RDF.type, gprov.Guideline))
    g.add((term.URIRef('gprov:{}'.format(guideline)), bibo.volume, Literal(guideline_volume)))
    g.add((term.URIRef('gprov:{}'.format(guideline)), DC.date, Literal(guideline_date)))
    g.add((term.URIRef('gprov:{}'.format(guideline)), DC.title, Literal(guideline_title)))
    


    g.bind('DC', URIRef('http://purl.org/dc/elements/1.1/'))
    g.bind('gprov', URIRef('https://purl.org/heals/gprov/'))
    g.bind('prov', URIRef('https://www.w3.org/ns/prov#'))
    g.bind('sio', URIRef('http://semanticscience.org/resource/'))
    g.bind('bibo', URIRef('http://purl.org/ontology/bibo/'))
    g.serialize(destination='gprov/static/rdf/kgs/{}'.format(filename), format='ttl')

	
def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()

def date():
    return datetime.now().strftime('%Y-%m-%d')


