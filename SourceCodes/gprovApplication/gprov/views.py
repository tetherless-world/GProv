from .models import provenance_Information, annotation, patient_query
from flask import Flask, request, session, redirect, url_for, render_template, flash
import pandas as pd

#import wtforms

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    lastName = "Smith"
    patientList = ["Select patient from the list", "John Smith", "Samantha Brown"]
    res = patient_query(lastName)
    res2 = list(patient_query(lastName))[0]

    for rows in res:
            drug = str(rows.drug.toPython())
            drugTherapy = str(rows.drugsubplan.toPython())
        
    prov = provenance_Information(drug, drugTherapy)
    

    return render_template('physician.html',patient=patientList, row=prov, me=res2)

@app.route('/patient', methods=['GET', 'POST'])
def patient():
    lastName = "Smith"
    patientList = ["Select patient from the list", "John Smith", "Samantha Brown"]
    res2 = list(patient_query(lastName))[0]
    
    if request.method == 'POST':
        myPatient = request.form['patient']
#        print(lastName)
        lastName = myPatient.split()[1]
        print(lastName)
        res = patient_query(lastName)
        for rows in res:
            drug = str(rows.drug.toPython())
            dt = str(rows.drugsubplan.toPython())
            drugTherapy = dt.lower()
        
        prov = provenance_Information(drug, drugTherapy)
        res2 = list(patient_query(lastName))[0]
        return render_template('physician.html',patient=patientList, row=prov, me=res2)
    
    res = patient_query(lastName)
    for rows in res:
            drug = str(rows.drug.toPython())
            drugTherapy = str(rows.drugsubplan.toPython())
        
    prov = provenance_Information(drug, drugTherapy)
    
    return render_template('physician.html',patient=patientList, row=prov, me=res2)


@app.route('/CMView', methods=['GET','POST'])
def forms():
    
    if request.method == 'POST':
        rule = request.form['FormalRule']
        recommendation = request.form['RecommendationID']
        recommendation_text = request.form['RecommendationText']
        influencer = recommendation + '_grade'
        grade_value = request.form['RecommendationGrade']
        generated_by = recommendation + '_evidence'
        evidence_sentence = request.form['RecommendationES']
        primary_source = request.form['citationID']
        
        guideline = "ADA_Guidelines"
        guideline_volume = request.form['Volume']
        guideline_date = request.form['GuidelineDate']
        guideline_title = request.form['GuidelineTitle']
        guideline_publisher = request.form['Publisher']
        disease_name = request.form['DiseaseName']
        
        data = pd.DataFrame({'rule':rule,'recommendation':recommendation, 'recommendation_text':recommendation_text, 'influencer':influencer, 'grade_value':grade_value, 'generated_by':generated_by, 'evidence_sentence':evidence_sentence, 'primary_source':primary_source, 'guideline':guideline, 'guideline_volume':guideline_volume, 'guideline_date':guideline_date, 'guideline_title':guideline_title}, index=[0])
        annotation(data)
        
        return render_template('forms.html')

    return render_template('forms.html')

@app.route('/CMView', methods=['GET','POST'])
def annotations():
    if request.method == 'POST':
        rule = request.form['FormalRule']
        recommendation = request.form['RecommendationID']
        recommendation_text = request.form['RecommendationText']
        influencer = recommendation + '_grade'
        grade_value = request.form['RecommendationGrade']
        generated_by = recommendation + '_evidence'
        evidence_sentence = request.form['RecommendationES']
        primary_source = request.form['citationID']
        
        guideline = "ADA_Guidelines"
        guideline_volume = request.form['Volume']
        guideline_date = request.form['GuidelineDate']
        guideline_title = request.form['GuidelineTitle']
        guideline_publisher = request.form['Publisher']
        disease_name = request.form['DiseaseName']
        
        data = pd.DataFrame({'rule':rule,'recommendation':recommendation, 'recommendation_text':recommendation_text, 'influencer':influencer, 'grade_value':grade_value, 'generated_by':generated_by, 'evidence_sentence':evidence_sentence, 'primary_source':primary_source, 'guideline':guideline, 'guideline_volume':guideline_volume, 'guideline_date':guideline_date, 'guideline_title':guideline_title}, index=[0])
        annotation(data)
    return render_template('forms.html')

@app.route('/phmview', methods=['GET','POST'])
def phmView():
    return render_template('stats.html')
    

