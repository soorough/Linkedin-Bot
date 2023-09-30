from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import os

class LinkedinBot:

    def __init__(self, data):
        # Parameter initialization
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']

        # Set the system PATH to include the directory of chromedriver
        chromedriver_path = data['driver_path']
        os.environ['PATH'] += os.pathsep + chromedriver_path

        self.driver = webdriver.Chrome()

    def login_linkedin(self):
        # This function logs into your personal LinkedIn profile

        # go to the LinkedIn login url
        self.driver.get("https://www.linkedin.com/login")

        # introduce email and password and hit enter
        login_email = self.driver.find_element(By.NAME, 'session_key')
        login_email.clear()
        login_email.send_keys(self.email)
        login_pass = self.driver.find_element(By.NAME, 'session_password')
        login_pass.clear()
        login_pass.send_keys(self.password)
        login_pass.send_keys(Keys.RETURN)
        
        time.sleep(15)

    def job_search(self):
        # This function goes to the 'Jobs' section and looks for all the jobs that match the keywords and location

        # go to Jobs
        jobs_link = self.driver.find_element(By.XPATH, "//span[text()='Jobs']")
        jobs_link.click()
        time.sleep(2)
        # search based on keywords and location and hit enter
        search_keywords = self.driver.find_element(By.XPATH, "//input[starts-with(@id, 'jobs-search-box-keyword')]")

        # search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        time.sleep(1)

        search_location = self.driver.find_element(By.XPATH, "//input[starts-with(@id, 'jobs-search-box-location')]")
        search_location.clear()
        search_location.send_keys(self.location)
        time.sleep(2)
        search_location.send_keys(Keys.RETURN)

    def filter(self):
        # This function filters all the job results by 'Easy Apply'

        # Wait for the "Easy Apply" button to be clickable
        easy_apply_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Easy Apply filter.']"))
        )

        # Click the "Easy Apply" button
        easy_apply_button.click()
    
    def find_offers(self): #This function finds all the offers through all the pages result of the search and filter

        # find the total amount of results (if the results are above 24-more than one page-, we will scroll trhough all available pages)
        total_results = self.driver.find_element(By.CLASS_NAME, "display-flex.t-normal.t-12.t-black--light.jobs-search-results-list__text")
        total_results_int = int(total_results.text.split(' ', 1)[0].replace(",", "")) #"1,234 results" converted to 1234
        print(total_results_int)

        time.sleep(2)
        # get results for the first page
        current_page = self.driver.current_url
        results = self.driver.find_elements(By.CSS_SELECTOR, "li.ember-view.jobs-search-results__list-item.occludable-update.p0.relative.scaffold-layout__list-item")


        # for each job add, submits application if no questions asked
        for result in results:
            hover = ActionChains(self.driver).move_to_element(result)
            hover.perform()
            titles = result.find_elements(By.CSS_SELECTOR, "a.job-card-container__link.job-card-list__title")
            for title in titles:
                self.submit_apply(title)
        
        # if there is more than one page, find the pages and apply to the results of each page
        if total_results_int > 24:
            time.sleep(2)

            # Find the last page and construct the URL of each page based on the total number of pages
            find_pages = self.driver.find_elements(By.CSS_SELECTOR, "ul.artdeco-pagination__pages.artdeco-pagination__pages--number li")
            # Get the total number of pages from the last page element
            total_pages_element = find_pages[-1]  # The last page number is the second-last element in the list


            # Extract the numeric part from the total pages using regular expression
            total_pages_int = int(total_pages_element.text.strip())
            print(total_pages_int)

            get_last_page = self.driver.find_element(By.XPATH, "//button[@aria-label='Page "+str(total_pages_int)+"']")
            get_last_page.send_keys(Keys.RETURN)

            time.sleep(2)

            last_page = self.driver.current_url
            # Get the total number of jobs from the current URL
            total_jobs = int(self.driver.current_url.split('start=')[1])
            print(total_jobs)


            # go through all available pages and job offers and apply
            for page_number in range(25,total_jobs+25,25):
                self.driver.get(current_page+'&start='+str(page_number))
                time.sleep(2)
                results_ext = self.driver.find_elements(By.CSS_SELECTOR, "li.ember-view.jobs-search-results__list-item.occludable-update.p0.relative.scaffold-layout__list-item")
                for result_ext in results_ext:
                    hover_ext = ActionChains(self.driver).move_to_element(result_ext)
                    hover_ext.perform()
                    titles_ext = result_ext.find_elements(By.CSS_SELECTOR, "a.job-card-container__link.job-card-list__title")
                    for title_ext in titles_ext:
                        self.submit_apply(title_ext)
        else:
            self.close_session()




    def submit_apply(self, job_add):
        #This function submits the application for the job add found

        print('You are applying to the position of: ', job_add.text)
        job_add.click()
        time.sleep(3)

        # click on the easy apply button, skip if already applied to the position
        try:
            apply_button = self.driver.find_element(By.CSS_SELECTOR, "button.jobs-apply-button.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view")
            apply_button.click()
        except NoSuchElementException:
            print('You already applied to this job, go to the next...')
            pass
        time.sleep(1)

                # try to submit if submit application is available...
        try:
            try:
                submit = self.driver.find_element(By.XPATH, "//button[@aria-label='Submit application']")
                submit.send_keys(Keys.RETURN)
                time.sleep(3)
                dismiss = self.driver.find_element(By.XPATH, "//button[@data-test-modal-close-btn]")
                dismiss.click()
                time.sleep(3)
            except NoSuchElementException:
                count = 0
                while count<5:
                    print(count)
                    if "Continue to next step" in self.driver.page_source:
                        next = self.driver.find_element(By.XPATH, "//button[@aria-label='Continue to next step']")
                        next.send_keys(Keys.RETURN)
                        time.sleep(2)
                        count+=1
                        continue
                    
                    
                    elif "Review your application" in self.driver.page_source:
                        review = self.driver.find_element(By.XPATH, "//button[@aria-label='Review your application']")
                        review.send_keys(Keys.RETURN)
                        time.sleep(2)
                    
                        if count>=4:  # Checkt for presence of element
                            break
                        else:
                            submit = self.driver.find_element(By.XPATH, "//button[@aria-label='Submit application']")
                            submit.send_keys(Keys.RETURN)
                            time.sleep(3)
                            dismiss = self.driver.find_element(By.XPATH, "//button[@data-test-modal-close-btn]")
                            dismiss.click()
                            time.sleep(3)
                            break
                    # try:
                    #     check1 = WebDriverWait(self.driver, 5).until(
                    #     EC.presence_of_element_located((By.XPATH, '//div[contains(@aria-invalid, "true")]'))
                    #     )
                    #     print(check1)
                    # except Exception as e:
                    #     print("Element not found or other error:", e)
                    # if check1 is not None:  # Check for presence of element
                    #     break
                print('Not a direct application, going to the next...')
                try:
                    discard = self.driver.find_element(By.XPATH, "//button[@data-test-modal-close-btn]")
                    discard.click()
                    time.sleep(1)
                    discard_confirm = self.driver.find_element(By.XPATH, "//button[@data-test-dialog-secondary-btn and @data-control-name='discard_application_confirm_btn']")
                    discard_confirm.click()
                    time.sleep(1)
                except NoSuchElementException:
                    pass
                

        # ... if not available, discard application and go to the next
        except NoSuchElementException:
            print('Not a direct application, going to the next...')
            try:
                discard = self.driver.find_element(By.XPATH, "//button[@data-test-modal-close-btn]")
                discard.click()
                time.sleep(1)
                discard_confirm = self.driver.find_element(By.XPATH, "//button[@data-test-dialog-secondary-btn and @data-control-name='discard_application_confirm_btn']")
                discard_confirm.click()
                time.sleep(1)
            except NoSuchElementException:
                pass

        time.sleep(1)

    def close_session(self):
        #This function closes the actual session

        print('End of the session, see you later!')
        self.driver.close()

    def apply(self):
        #Apply to job offers

        self.driver.maximize_window()
        self.login_linkedin()
        time.sleep(2)
        self.job_search()
        time.sleep(2)
        self.filter()
        time.sleep(2)
        self.find_offers()
        time.sleep(2)
        self.close_session()

if __name__ == '__main__':
    with open('config.json') as config_file:
        data = json.load(config_file)

    bot = LinkedinBot(data)
    bot.apply()
