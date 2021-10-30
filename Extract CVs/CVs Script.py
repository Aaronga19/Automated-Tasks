import spacy
import pdfminer
import re
import os 
import pandas as pd
import pdf2txt


def convert_pdf(file):
    output_filename = os.path.basename(os.path.splitext(file)[0]) + ".txt"
    output_filepath = os.path.join("Extract CVs/output/txt/", output_filename)
    pdf2txt.main(args=[file, "--outfile", output_filepath])
    print(output_filepath + " saved succesfully!!!")
    return open(output_filepath, encoding='utf8').read()



# Loading the language model

nlp = spacy.load("en_core_web_sm") # english = en_core_web_sm; spanish = es_core_news_sm


result_dict = {'name': [], 'phone': [], 'email': [], 'skills': []}
names = []
phones = []
emails = []
skills = []



# phone_num = https://stackoverflow.com/a/3868861
def parse_content(text):
    skillset = re.compile("python|java|sql|hadoop|tableau")
    phone_num = re.compile(
        "(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
    )
    doc = nlp(text)    
    name = [entity.text for entity in doc.ents if entity.label_ is "PERSON"][3]
    print(name)
    email = [word for word in doc if word.like_email == True]
    print(email)
    phone = str(re.findall(phone_num, text.lower()))
    skills_list = re.findall(skillset,text.lower())
    unique_skills_list = str(set(skills_list))
    names.append(name)
    emails.append(email)
    phones.append(phone)
    skills.append(unique_skills_list)
    print("Extraction completed successfully!!!")


for file in os.listdir('Extract CVs/resumes/'):
    if file.endswith('.pdf'):
        print('Reading....' + file)
        txt = convert_pdf(os.path.join('Extract CVs/resumes/', file))
        parse_content(txt)


result_dict['name'] = names
result_dict['phone']= phones
result_dict['email']= emails
result_dict['skills']= skills

# Convert the dict to a Data Frame
result_df = pd.DataFrame(result_dict)
# Convert data frame to csv
result_df.to_csv('Extract CVs/output/csv/parsed_resume.csv')
print('Files converted to csv and saved')



