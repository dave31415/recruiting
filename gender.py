#gender
import subprocess
import csv
import math

executable ="/Users/davej/Downloads/names/0717-182/gender"
parameters="-get_gender"
name_file="/Users/davej/JC-names-big.csv"

def get_gender(first_name):
    if first_name.__class__ == list:
        #a list of names
        length=len(first_name)
        output=[get_gender(name) for name in first_name]
        return output
    #just one name
    proc=subprocess.Popen([executable,parameters,first_name],stdout=subprocess.PIPE)
    stdout=proc.stdout.readline()
    if "name not found" in stdout or "error in name" in stdout: return "?" 
    gender=stdout.split(":")[1].strip()
    #print stdout, gender
    gender=gender.split('is')[1]
    #remove the quote
    gender=gender.replace("'","").strip()
    if gender == 'un': gender="unisex"
    return gender
    
def read_names():
    names=list(csv.DictReader(open(name_file,'rU')))
    return names

def force_decision(genders,strict=True):
    if genders.__class__ == str : genders=[genders]

    male_fem=[]
    if strict :
        fem_list=["female"]
        male_list=["male"]
    else :
        fem_list=["female","mostly female"]
        male_list=["male","mostly male"]
    for gen in genders:
        sex='?'
        if gen in fem_list: sex = "F"
        if gen in male_list: sex = "M"
        male_fem.append(sex)
    return male_fem

def mf_stats(names=None,strict=True):
    if names== None : names=read_names()
    Males_hired=0
    Males_rejected=0
    Females_hired=0
    Females_rejected=0
    n_people=len(names)

    for person in names:
        first_name=person["First name"]
        result=person["Job Step"]
        gen=get_gender(first_name)
        sex=force_decision(gen,strict=strict)[0]
        if sex == "M":
            if result == "Hired": 
                Males_hired+=1
            if result == "Rejected":
                Males_rejected+=1
        if sex == "F":
            if result == "Hired":
                Females_hired+=1
            if result == "Rejected":
                Females_rejected+=1

    male_rate=float(Males_hired)/(Males_hired+ Males_rejected)*100
    female_rate=float(Females_hired)/(Females_hired+ Females_rejected)*100

    male_error_percent=1.0/math.sqrt(Males_hired)
    female_error_percent=1.0/math.sqrt(Females_hired)

    male_rate_err=male_rate*male_error_percent
    female_rate_err=female_rate*female_error_percent

    n_male = Males_hired+Males_rejected
    n_female = Females_hired+Females_rejected
    n_both=n_male+n_female

    sflag="Not-strict"
    if strict : sflag= "Strict"

    line='----------------------------'

    print line
    print "Gender decision : %s"%sflag
    print line
    print "Percent of applicants Female: %.1f"%(100.0*n_female/float(n_female+n_male)),"%"
    print "Number of people total",n_people
    print "Number with identifiable gender: %s %.2f"%(n_both,100.0*n_both/n_people),"%"

    print "Males Hired", Males_hired
    print "Males Rejected", Males_rejected
    print "Females Hired", Females_hired
    print "Females Rejected", Females_rejected

    
    print "Male hire rate: %.2f +/- %.2f"%(male_rate,male_rate_err)
    print "Female hire rate: %.2f +/- %.2f"%(female_rate,female_rate_err)
    
