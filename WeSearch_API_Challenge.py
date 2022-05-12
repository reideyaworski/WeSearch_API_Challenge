#WESEARCH API CHALLENGE (START 8:30am EST)

#Import Libraries and Modules
import requests
import random 
import os 


#Create a credentials (user:pass) class
class Credentials:
    def __init__(self,email,password):
        self.email = email
        self.password = password

def main():
    ### DATA PREPARATION ###
    filenamesClean = [] #etsablish empty list for later use
    documents = [] #establish empty list for file upload
    
    path = input("Please enter the data path: ") #request user input to locate data directory 
    filenames = os.listdir(path=path) #identify filenames in directory 

    #Create for loop to store data-only files in directory 
    for i in filenames:
        if i.endswith("-main"):
            filenamesClean.append(i)      
   
    #print(filenamesClean) #UNCOMMENT TO VIEW RESULTS
   
   
    #Create a random selection of 1000 opinion files
    randomOpinions = random.sample(filenamesClean, k=1000)
    randomOpinions.sort() #Sort this list alphanumerically 
    
    #print(randomOpinions) #UNCOMMENT TO VIEW RESULTS
   
    #If you would like to view the text contents of randomOpinions, run the following for loop
    #for i in randomOpinions:
        #print(open(i,"r", encoding='utf-8').read())
        
    for i in randomOpinions:
        documents.append(open(i,"r", encoding='utf-8').read())
    
    documents = [sub.replace('\n', '') for sub in documents]

    
    ### ACCESS WESEARCH API ###
    
    #Create a while loop to retrieve user credentials
    while True:
        response = input("Type 'start' to begin: ")
        if response == 'start':
            email = input("Enter email: ")
            password = input("Enter password: ")
            credentials = Credentials(email,password)
            print("Thank you!")
            break
        else:
            print("Please try again...")
            print('\n')
    
    
    #AUTHENTICATION REQUEST
    headers = {'Content-Type': 'application/json',}
    data = '{"email":"' + credentials.email + '",' + '"password":"' + credentials.password +'"}'
    r = requests.post('https://project-apollo-api.stg.gc.casetext.com/v0/auth/login', headers=headers, data=data)
    token = r.json()['token'] #retrieve and store authorization token
    
    
    #CREATE A COLLECTION (Using lawbert model)
    headers = {'Authorization': 'Bearer ' + token,'Content-Type': 'application/json',}
    data = '{ "model": "lawbert" }'
    rCollection = requests.post('https://project-apollo-api.stg.gc.casetext.com/v0/supreme-court-opinions/create', headers=headers,data=data)
    #print(rCollection.status_code)
    
    #Check to see if collection has been created
    if rCollection.status_code == 201:
        print('STATUS: Collection Created!')
    else:
        print('STATUS: Error! HTTP Status Code ' + str(rCollection.status_code))
    
    
    #Add US Supreme Court Opinions documents to collection
    headers = {'Authorization': 'Bearer ' + token,'Content-Type': 'text/plain',}
    for i in range(len(documents)):
        r.addDocuments = requests.post('https://project-apollo-api.stg.gc.casetext.com/v0/supreme-court-opinions', headers=headers, data=documents[i].encode('utf-8'))
    
    #Check to see if documents have been uploaded
    if r.addDocuments.status_code == 201:
        print('STATUS: Documents Uploaded.')
    else:
        print('STATUS: Error! HTTP Status Code ' + str(r.addDocuments.status_code))
    
    print('\n')
    print("Thank you for using WeSearch!")
    
if __name__ == "__main__":
    main()