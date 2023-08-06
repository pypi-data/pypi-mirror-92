import requests

class KnowBe4:
    def __init__(self, api_key):
        self.api_key = api_key

    """This function builds the API calls for pages that do not support pagation 

    Parameters: api_key: The KnowBe4 API key provided by the user in the creation of the KnowBe4 Object 
                url: The URL to the API end point the data is provided from. This is pre given from the functions below 

    Returns: json data from the API endpoint """    
    def build_non_page_url(api_key, url):
        #Using the requests library to build the API call using the API Ley provided by the user 
        jsondata = requests.get(url, headers = {'Authorization': 'Bearer ' + self.api_key}).json
        #Return the json data from the API call 
        return jsondata
    
    """This function builds the API call for pages that do support pagation
    
    Parameters: api_key: The KnowBe4 API key provided by the user in the creation of the KnowBe4 Object 
                url: The URL to the API end point the data is provided from. This is pre given from the functions below 

    Returns: json data from the API endpoint """ 
    def build_page_url(api_key, url):
        #Create variables 
        page_number = 1
        cont = True
        return_data = []
        #White loop that runs while there are still pages together, Once the API call fails the loop will stop 
        while cont:
            try:
                json_data = requests.get(url, headers = {'Authorization': 'Bearer ' + api_key}, param = {'page' : page_number}).json
            
            except:
                cont = False
            #Adding all the json data together for one return string 
            return_data += json_data
            #Adding one to the page number counter
            page_number += 1

        return return_data

    """Method to return data from the Accounts API endpoint 

    This endpoint retrieves account data from you Knowbe4 account, 
    including your subscription level, number of seats, risk score 
    history, and more.

    Parameters: KnowBe4 Object 
    Returns: Json data"""
    def account(self):
        url = 'https://us.api.knowbe4.com/v1/account'
        return build_non_page_url(self.api_key, url)

    """Method to return data from the Users API endpoint 

    This endpoint retrieves a list of all users in your KnowBe4 account.

    Parameters: KnowBe4 Object 
    Returns: Json data"""
    def users(self):
        url = 'https://us.api.knowbe4.com/v1/users'
        return build_page_url(self.api_key, url)

    """Method to return data from the Groups API endpoint 

    This endpoint retrieves a list of all users who are members of a specific group

    Parameters: KnowBe4 Object 
    Returns: Json data"""        
    def users_in_group(self, group_id):
        url = 'https://us.api.knowbe4.com/v1/groups/' + group_id + '/members'
        return build_non_page_url(self.api_key, url)
    
    """Method to return data from the User API endpoint 

    This endpoint retrieves a specific user based on the provided user identifier This 
    endpoint retrieves a specific group in your KnowBe4 account, based on the provided 
    group identifier (group_id)This endpoint retrieves a specific group in your KnowBe4
     account, based on the provided group identifier (group_id)\(user_id).

    Parameters: KnowBe4 Object 
    Returns: Json data"""
    def user(self, user_id):
        url = 'https://us.api.knowbe4.com/v1/users/' + user_id + ''
        return build_page_url(self.api_key, url)

    """Method to return data from the Groups API endpoint 

    This endpoint retrieves a list of all groups in your KnowBe4 account.

    Parameters: KnowBe4 Object 
    Returns: Json data"""
    def groups(self):
        url = 'https://us.api.knowbe4.com/v1/groups'
        return build_non_page_url(self.api_key, url)

    """Method to return data from the Groups API endpoint 

    This endpoint retrieves a specific group in your KnowBe4 account, based on 
    the provided group identifier (group_id)

    Parameters: KnowBe4 Object 
    Returns: Json data"""         
    def user(self, group_id):
        url = 'https://us.api.knowbe4.com/v1/groups/' + group_id + ''
        return build_non_page_url(self.api_key, url)

    """Method to return data from the Groups API endpoint 

    This endpoint retrieves data from all the phishing campaigns in your account.

    Parameters: KnowBe4 Object 
    Returns: Json data"""  
    def all_phishing_capaigns(self):
        url = 'https://eu.api.knowbe4.com/v1/phishing/campaigns'
        return build_non_page_url(self.api_key, url)
    
    """Method to return data from the Groups API endpoint 

    This endpoint retrieves data from a specific phishing campaign, 
    based on the provided campaign identifier (campaign_id)

    Parameters: KnowBe4 Object 
    Returns: Json data""" 
    def phishing_campaign(self, campaign_id):
        url = 'https://us.api.knowbe4.com/v1/phishing/campaigns/' + campaign_id + ''
        return build_non_page_url(self.api_key, url)
    
    """Method to return data from the Groups API endpoint 

    This endpoint retrieves a list of all phishing security tests in your account.

    Parameters: KnowBe4 Object 
    Returns: Json data""" 
    def all_phishing_security_tests(self):
        url = 'https://us.api.knowbe4.com/v1/phishing/security_tests'  
        return build_non_page_url(self.api_key, url)  
    
    """Method to return data from the Groups API endpoint 

    This endpoint retrieves a list of all phishing security tests from a specific 
    phishing campaign, based on the provided phishing campaign identifier (campaign_id)

    Parameters: KnowBe4 Object 
    Returns: Json data""" 
    def all_phishing_security_test_from_campaign(self, campaign_id):
        url = 'https://us.api.knowbe4.com/v1/phishing/campaigns/' + campaign_id + '/security_tests'
        return build_non_page_url(self.api_key, url)  
    
    """Method to return data from the Groups API endpoint 

    This endpoint retrieves data from a specific phishing security 
    test, based on the provided phishing security test identifier (pst_id).

    Parameters: KnowBe4 Object 
    Returns: Json data""" 
    def phishing_security_test(self, pst_id):
        url = 'https://us.api.knowbe4.com/v1/phishing/security_tests/' + pst_id + ''
        return build_non_page_url(self.api_key, url) 

    """Method to return data from the Groups API endpoint 

    This endpoint retrieves a list of all the recipients (users) that were part of a specific 
    phishing security test, based on the provided phishing security test identifier (pst_id)

    Parameters: KnowBe4 Object 
    Returns: Json data"""    
    def security_test_results(self, pst_id):
        url = 'https://us.api.knowbe4.com/v1/phishing/security_tests/' + pst_id + '/recipients'
        return build_non_page_url(self.api_key, url) 
    
    """Method to return data from the Groups API endpoint 

    This endpoint retrieves details about a specific user's phishing security test results, based on 
    the provided phishing security test identifier (pst_id) and recipient identifier (recipient_id)

    Parameters: KnowBe4 Object 
    Returns: Json data""" 
    def user_security_test_results(self, pst_id, recipient_id):
        url = 'https://us.api.knowbe4.com/v1/phishing/security_tests/' + pst_id + '/recipients/' + recipient_id + ''
        return build_non_page_url(self.api_key, url) 