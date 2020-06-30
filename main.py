import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class IndeedBot:

    def __init__(self):
        """
        Initilializes the Chrome webdriver.
        Sets the job search query string

        self.driver:selenium.webdriver.Chrome
        self.query_string:str
        self.jobs:arr
        self.express_apply_jobs:arr
        """

        self.driver = webdriver.Chrome('./chromedriver')
        self.query_string = "https://www.indeed.fr/jobs?q={job}&l={city}&sort=date"
        self.jobs = []
        self.express_apply_jobs = []


    def nav(self, url):
        """ 
        Navigates to a given url

        Args:
            url:str url chromedriver Chrome instance navigates to.
        """

        self.driver.get(url)
        time.sleep(2) # wait for page load


    def __convert_query(self, job, city):
        """
        Reformats the query for expected syntax of the search
        
        Args:
            job:str: Job type to search for.
            city:str: City location of the job.
        
        Returns:
            job:str
            city:str
        """

        job = '+'.join(job.split(" "))
        city = city.lower()



        return job, city
    

    def query(self, job, city):
        """ 
        Searches indeed for a job in given city

        Args:
            job:str: Job type to search for.
            city:str: City location of the job.
        """

        job, city = self.__convert_query(job, city)

        query = self.query_string.format(job=job, city=city)

        self.nav(query)


    def find_express_jobs(self):
        """"
        Called after chromedriver Chrome instance navigates to job search results.
        Fills list with express jobs in search results.
        """

        self.jobs = self.driver.find_elements_by_class_name("jobsearch-SerpJobCard")

        print(f'Number of jobs {len(self.jobs)}')

        for job in self.jobs:
            try: # Express apply indicator
                job.find_element_by_class_name('jobCardShelfContainer') 
                self.express_apply_jobs.append(job)
            except: # Job is not express apply
                pass
    
    
    def apply_to_express_jobs(self, profile):
        """
        Extracts jobs with express apply.

        Args:
            profile:dict
        """

        print(f'Number of express jobs {len(self.express_apply_jobs)}')

        for job in self.express_apply_jobs:
            self.__process_job(job)
            self.__process_apply_button()
            self.__fill_applicant_form(profile)

            # self.driver.find_element_by_id('form-action-continue').click()


    def __process_apply_button(self):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            apply_button = self.driver.find_element_by_id('indeedApplyButtonContainer')
            apply_button.click()
            time.sleep(2)
    

    def __process_job(self, job):
        """
        Refines url of job posting and navigates to it

        Args:
            job:Selenium.Webdriver.Chrome.WebElement
        """

        job_a_tag = job.find_element_by_tag_name('a')
        job_href = job_a_tag.get_attribute('href')
        # Removing all extraneous indeed url query string parameters
        job_href = job_href.split('&from')[0] 
        self.nav(job_href)


    def __fill_applicant_form(self, profile):
        """
        Finds elements on the applicant form

        Args:
            profile:dict
        """

        actions = ActionChains(self.driver)
        actions.send_keys(profile['name'] + Keys.TAB + \
                          profile['email'] + Keys.TAB + \
                          profile['phone_number'] + Keys.TAB)
        actions.perform()


if __name__ == '__main__':

    profile = {
        'name': "jhon doe",
        'email': "jhon.doe@example.com",
        'phone_number': '0123456789',
        'resume': os.getcwd() + '/resume.txt'
    }
    
    id_bot = IndeedBot()

    # keywords, city
    id_bot.query('alternance python dev', 'paris')

    id_bot.find_express_jobs()
    
    id_bot.apply_to_express_jobs(profile)