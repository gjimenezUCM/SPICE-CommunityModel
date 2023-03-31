import requests
import time

def wait(seconds):
    time.sleep(seconds)

def main():

    #--------------------------------------------------------------------------------------------------------------------------
    #    Change server
    #--------------------------------------------------------------------------------------------------------------------------
    
    server = "http://localhost:8080"

    #--------------------------------------------------------------------------------------------------------------------------
    #    Perform GET \communities
    #--------------------------------------------------------------------------------------------------------------------------

    response = requests.get("{}/v2.0/communities".format(server))
    jsonObject = response.json()
    print(response)
    print(jsonObject)
    print("\n")
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    Wait for CM update (if required)
    #--------------------------------------------------------------------------------------------------------------------------
    
    if (response.status_code != 400):
    
        # If the CM has to update (for example, after performing "post.py" since there are new users")
        # It returns a job url to track the update status (class: dict) ( e.g., ({'path': '/jobs/5058'}, <Response [202]>) ) 
        if (isinstance(jsonObject, dict) and 'path' in jsonObject):
            jobId = jsonObject['path'].replace("/v2.0/jobs/","")
            jobStatus = ''

            # When the CM stops updating, the job will change to status (COMPLETED) and include the requested data.
            while jobStatus != 'COMPLETED':
                wait(10)
                
                jobResponse = requests.get("{}/v2.0/jobs/{}".format(server,jobId))
                jobStatus = jobResponse.json()['job']['job-state']

                print("jobStatus: " + str(jobStatus))
                    
            # Retrieve requested data from the job json object
            requestedData = jobResponse.json()['job']['data']

        # If it doesn't need to update, it directly returns the desired result (in this case a list of communities)
        else:
            requestedData = jsonObject
    
        # Print latest result
        print("GET \communities")
        print(requestedData)
    
    
main()