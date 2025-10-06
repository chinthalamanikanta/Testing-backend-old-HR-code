import pytest
from selenium import webdriver
from datetime import date, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import random
import time

@pytest.fixture
def driver():
    service = EdgeService(r"C:\Users\MTL1026\Downloads\edgedriver_win64\msedgedriver.exe")
    driver = webdriver.Edge(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_register_and_login(driver):
    driver.get("http://localhost:3000/register")

    # Generate unique email and company name
    random_suffix = random.randint(1000, 9999)
    random_email = f"testuser{random_suffix}@middlewaretalents.com"
    random_company = f"company{random_suffix}"
    random_employeId = random.randint(1000, 1030)
    random_personalemployeId =f"MTL{random_employeId}"

    # Fill registration form
    driver.find_element(By.NAME,"firstname").send_keys("testuser")
    driver.find_element(By.NAME,"lastname").send_keys("testlast")
    driver.find_element(By.NAME, "email").send_keys(random_email)
    driver.find_element(By.NAME,"company").send_keys(random_company)
    driver.find_element(By.NAME, "password").send_keys("Password@123")
    driver.find_element(By.NAME, "confirmPassword").send_keys("Password@123")

    # Submit form
    driver.find_element(By.ID, "registerBtn").click()
    
    #  Wait up to 10s for redirection to /login (company prefix doesn’t matter)
    try:
        WebDriverWait(driver, 10).until(EC.url_contains("/login"))
    except:
        # Debug output if redirect didn't happen
        print(" Registration failed. Current URL:", driver.current_url)
        print("Page content:\n", driver.page_source[:1000])  # show first 1000 chars
        raise

     # 🔑 Enter login credentials
    driver.find_element(By.NAME, "email").send_keys(random_email)
    driver.find_element(By.NAME, "password").send_keys("Password@123")
    driver.find_element(By.ID, "loginBtn").click()
    

    WebDriverWait(driver, 5).until(EC.url_contains("/employee"))


    driver.get("http://localhost:3000/employee")
    time.sleep(2)
    driver.find_element(By.ID, "pencilBtn").click()
    time.sleep(2)

    driver.find_element(By.NAME, "firstName").send_keys("")
    time.sleep(2)
    driver.find_element(By.NAME, "lastName").send_keys("")
    time.sleep(2)

    driver.find_element(By.NAME, "dateOfBirth").send_keys("09-08-2025")

    # # Street address
    driver.find_element(By.NAME, "streetAddress").send_keys("123 Main Street")

    # # City
    driver.find_element(By.NAME, "city").send_keys("Hyderabad")

    # # State / Province
    driver.find_element(By.NAME, "region").send_keys("Telangana")

    # # ZIP / Postal code
    driver.find_element(By.NAME, "postalCode").send_keys("500001")
    
    ####
    
    # Locate dropdown element
    dropdown_element = driver.find_element(By.NAME, "country")

    # Step 1: Click to open dropdown
    dropdown_element.click()
    time.sleep(1)

    # Step 2: Wrap with Select
    country_dropdown = Select(dropdown_element)

    # Get all options except the first one (placeholder "Select a country")
    options = country_dropdown.options[1:]

    # Pick a random country
    random_country = random.choice(options)
    print(f"Selecting random country: {random_country.text}")

    # Select the random option
    country_dropdown.select_by_visible_text(random_country.text)
    time.sleep(2)



    driver.find_element(By.NAME, "nextBtn").click()
    time.sleep(2)
     
    #testing for working professional Email case 
        # Locate dropdown element
    dropdown_element_current = driver.find_element(By.NAME, "workingCountry")

    # Step 1: Click to open dropdown
    dropdown_element_current.click()
    time.sleep(1)

    # Step 2: Wrap with Select
    country_dropdown2 = Select(dropdown_element_current)

    # Get all options except the first one (placeholder "Select a country")
    options2 = country_dropdown2.options[1:]

    # Pick a random country
    random_country2 = random.choice(options2)
    print(f"Selecting random country: {random_country2.text}")

    # Select the random option
    country_dropdown2.select_by_visible_text(random_country2.text)
    time.sleep(2)


    # Test Case employee ID
    driver.find_element(By.NAME, "employeeId").send_keys(random_personalemployeId)
    time.sleep(2)


    #selecting JOB ROLES
    dropdown_element_job = driver.find_element(By.NAME, "jobRole")

    # Step 1: Click to open dropdown
    dropdown_element_job.click()
    time.sleep(1)

    # Step 2: Wrap with Select
    job_role_dropdown3 = Select(dropdown_element_job)

    # Get all options except the first one (placeholder "Select a country")
    options3 = job_role_dropdown3.options[1:]

    # Pick a random country
    random_job_role = random.choice(options3)
    print(f"Selecting random country: {random_job_role.text}")

    # Select the random option
    job_role_dropdown3.select_by_visible_text(random_job_role.text)
    time.sleep(2)

    ##empolyeStatus
    dropdown_element_empolyeStatus = driver.find_element(By.NAME, "statusEmployee")

    # Step 1: Click to open dropdown
    dropdown_element_empolyeStatus.click()
    time.sleep(1)

    # Step 2: Wrap with Select
    employmentStatus_dropdown4 = Select(dropdown_element_empolyeStatus)

    # Get all options except the first one (placeholder "Select a country")
    options4 = employmentStatus_dropdown4.options[1:]

    # Pick a random country
    random_employeStatus4 = random.choice(options4)
    print(f"Selecting random country: {random_employeStatus4.text}")

    # Select the random option
    employmentStatus_dropdown4.select_by_visible_text(random_employeStatus4.text)
    time.sleep(2)

    # Collect all role inputs (admin, manager, employee)
    roles = driver.find_elements(By.XPATH, "//input[@id ='rolemail']")

    # Randomly select one
    random_role = random.choice(roles)
    random_role.click()
    random_role_selected = random_role.get_attribute("value")
    time.sleep(2)


    if random_role_selected == "employee":
        checkboxes = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//input[@type='checkbox']"))
        )
        
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                driver.execute_script("arguments[0].click();", checkbox)  # JS click avoids overlay issues
        time.sleep(1)

    driver.find_element(By.NAME, "submitForm").click()
    time.sleep(2)

    # Wait for the logo to be visible
    logo = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "profileLogo"))
    )

    # Option 1: Use ActionChains to move and click
    actions = ActionChains(driver)
    actions.move_to_element(logo).click().perform()
    time.sleep(2)

    driver.find_element(By.NAME, "signOut").click()
    time.sleep(3)

    driver.get(f"http://localhost:3000/{random_company}/login")
    time.sleep(3)

    driver.find_element(By.NAME, "email").send_keys(random_email)
    driver.find_element(By.NAME, "password").send_keys("Password@123")
    driver.find_element(By.ID, "loginBtn").click()
    time.sleep(3)

    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    # Verify employee page is reached
    current_url = driver.current_url.lower()
    assert "/dashboard" in current_url, f"Expected /dashboard, but got {current_url}"
    print("✅ Successfully registered, logged in, redirected to /dashboard, and navigated to /employee")
    
    ##posting News
    # Step 1: Click "Post news" (default visible)
    if (random_role_selected == "admin"):
        post_news_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "postnewsBtn"))
        )
        post_news_btn.click()
        time.sleep(5)

        driver.find_element(By.NAME, "postHeading").send_keys("Modi Open the Metro")
        time.sleep(2)
        driver.find_element(By.NAME, "detailNews").send_keys("After long time Modi visit to Bangalore for opening Metro")
        time.sleep(4)
        
        driver.find_element(By.NAME, "postBtn").click()
        # ✅ Wait for the alert popup
        WebDriverWait(driver, 5).until(EC.alert_is_present())

        # ✅ Switch to the alert
        alert = driver.switch_to.alert

        # ✅ (Optional) check the alert text
        assert "News posted successfully" in alert.text
        print("Alert text:", alert.text)

        # ✅ Accept the alert
        alert.accept()

        time.sleep(2)

        ##Post Holiday
        post_holiday = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "postHoliday")))
        post_holiday.click()
        time.sleep(2)
        driver.find_element(By.NAME, "postHolidaypurpose").send_keys("Happy New Year 2026")
        time.sleep(2)
        driver.find_element(By.NAME, "holidayDate").send_keys("08/09/2025")
        time.sleep(2)
        driver.find_element(By.NAME, "postHolidaydate").click()
        time.sleep(2)
        # # driver.find_element(By.NAME, "viewHolidaylist").click()
        # # time.sleep(5)
        
    #add job roles
    driver.get(f"http://localhost:3000/employee")
    time.sleep(5)

    driver.find_element(By.NAME, "addJobRoles").click()
    time.sleep(2)

    driver.find_element(By.NAME, "enterJobRole").send_keys("Full-stact Developer")
    driver.find_element(By.NAME, "submitRole").click()
    time.sleep(2)
    driver.find_element(By.NAME, "closeJobroletab").click()
    time.sleep(2)

    # #add employee into HR app
    driver.find_element(By.NAME, "addEmployees").click()
    time.sleep(2)

    driver.find_element(By.NAME, "firstName").send_keys("naveen")
    driver.find_element(By.NAME, "lastName").send_keys("kumar")
    

    driver.find_element(By.NAME, "dateOfBirth").send_keys("09/08/2002")

    # # Street address
    driver.find_element(By.NAME, "streetAddress").send_keys("123 Main sd Street")

    # # City
    city_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "city"))
    )
    city_input.clear()
    city_input.send_keys("Bangalore")

    # # State / Province
    region_input = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "region")))
    region_input.clear()
    region_input.send_keys("Karnataka")
   
    # # ZIP / Postal code
    driver.find_element(By.NAME, "postalCode").send_keys("560100")
    
    # ####
    
    # Locate dropdown element
    dropdown_element = driver.find_element(By.NAME, "country")

    # Step 1: Click to open dropdown
    dropdown_element.click()
    time.sleep(1)

    # Step 2: Wrap with Select
    country_dropdown = Select(dropdown_element)

    # Get all options except the first one (placeholder "Select a country")
    options = country_dropdown.options[1:]

    # Pick a random country
    random_country = random.choice(options)
    print(f"Selecting random country: {random_country.text}")

    # Select the random option
    country_dropdown.select_by_visible_text(random_country.text)
    time.sleep(2)



    driver.find_element(By.NAME, "nextBtn2").click()
    time.sleep(2)
     
    #testing for working professional Email case 
        # Locate dropdown element
    dropdown_element_current = driver.find_element(By.NAME, "workingCountry")
    time.sleep(2)

    # Step 1: Click to open dropdown
    dropdown_element_current.click()
    time.sleep(1)

    # Step 2: Wrap with Select
    country_dropdown2 = Select(dropdown_element_current)

    # Get all options except the first one (placeholder "Select a country")
    options2 = country_dropdown2.options[1:]

    # Pick a random country
    random_country2 = random.choice(options2)
    print(f"Selecting random country: {random_country2.text}")

    # Select the random option
    country_dropdown2.select_by_visible_text(random_country2.text)
    time.sleep(2)


    # Test Case employee ID
    driver.find_element(By.NAME, "employeeId").send_keys("MTL1087")
    time.sleep(2)
    
    #date of joining employee
    # Pick random date between 2015 and today
    # start_date = date(2015, 1, 1)
    # end_date = date.today()
    # random_days = random.randint(0, (end_date - start_date).days)
    # random_date = start_date + timedelta(days=random_days)

    # # Select the input and send date
    # date_input = driver.find_element(By.ID, "date-of-joining")
    # date_input.clear()
    # date_input.send_keys(random_date.strftime("%Y-%m-%d"))

    # print(f"✅ Selected random joining date: {random_date}")
    # time.sleep(2)


    driver.find_element(By.NAME, "corporateEmail").send_keys("Yaswanth@middlewaretalents.com")
    time.sleep(2)

    #selecting JOB ROLES
    dropdown_element_job = driver.find_element(By.NAME, "jobRole")

    # Step 1: Click to open dropdown
    dropdown_element_job.click()
    time.sleep(1)

    # Step 2: Wrap with Select
    job_role_dropdown3 = Select(dropdown_element_job)

    # Get all options except the first one (placeholder "Select a country")
    options3 = job_role_dropdown3.options[1:]

    # Pick a random country
    random_job_role = random.choice(options3)
    print(f"Selecting random country: {random_job_role.text}")

    # Select the random option
    job_role_dropdown3.select_by_visible_text(random_job_role.text)
    time.sleep(2)

    ##empolyeStatus
    dropdown_element_empolyeStatus = driver.find_element(By.NAME, "employmentStatus")

    # Step 1: Click to open dropdown
    dropdown_element_empolyeStatus.click()
    time.sleep(1)

    # Step 2: Wrap with Select
    employmentStatus_dropdown5 = Select(dropdown_element_empolyeStatus)

    # Get all options except the first one (placeholder "Select a country")
    options5 = employmentStatus_dropdown5.options[1:]

    # Pick a random country
    random_employeStatus5 = random.choice(options5)

    # Select the random option
    employmentStatus_dropdown5.select_by_visible_text(random_employeStatus5.text)
    time.sleep(2)

    
    reporting_to_person = driver.find_element(By.NAME, "reportingTo")
    reporting_to_person.click()
    time.sleep(1)
    selecting_person = Select(reporting_to_person)
    options6 = selecting_person.options[1:]
    random_selecting = random.choice(options6)
    selecting_person.select_by_visible_text(random_selecting.text)
    time.sleep(2)

    #nationalCardNum
    driver.find_element(By.NAME, "nationalInsuranceNumber").send_keys("1234567")

    # Collect all role inputs (admin, manager, employee)
    roles = driver.find_elements(By.XPATH, "//input[@id='role-employee']")

    # Randomly select one
    random_role = random.choice(roles)
    random_role.click()
    random_role_selected = random_role.get_attribute("value")
    time.sleep(2)


    if random_role_selected == "employee":
        checkboxes = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//input[@type='checkbox']"))
        )
        
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                driver.execute_script("arguments[0].click();", checkbox)  # JS click avoids overlay issues
        time.sleep(1)


    driver.find_element(By.NAME, "professional-submit").click()
    time.sleep(4)

    # folder_upload = driver.find_element(By.ID, "fileUpload")
    # time.sleep(4)
    # folder_upload.send_keys(r"C:\Users\MTL1026\Pictures\Screenshots\Screenshot 2025-09-08 131252.png")
    # time.sleep(2)
    # print("✅ File uploaded successfully")
    
    # Absolute path of the file you want to upload
    # file_path = os.path.abspath("C:\Users\MTL1026\Pictures\Screenshots\Screenshot 2025-09-08 131252.png")

    # Wait for the hidden input
    file_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "identityCard"))
    )

    # Upload the file
    file_input.send_keys(r"C:\Users\MTL1026\Pictures\Screenshots\Screenshot 2025-09-08 131252.png")

    print(f"✅ File uploaded: {file_input}")

    driver.find_element(By.NAME, "fileSubmitted").click()
    time.sleep(5)

    # Capture credentials using IDs
    corporate_email = driver.find_element(By.ID, "corporateEmail").text.replace("Corporate Email:", "").strip()
    password = driver.find_element(By.ID, "corporatePassword").text.replace("Password:", "").strip()

    print("Email:", corporate_email)
    print("Password:", password)

    time.sleep(3)
    driver.find_element(By.NAME, "closeCredentials").click()
    time.sleep(2)

    # # STEP 3: Open new tab
    # driver.execute_script("window.open('');")
    # driver.switch_to.window(driver.window_handles[1])  # Switch to new tab

    # # STEP 4: Go to login page
    # # driver.get("http://192.168.100.203:3000/login")
    # driver.get(f"http://192.168.100.203:3000/{random_company}/login")

    # time.sleep(2)

    # # STEP 5: Fill in login form
    # driver.find_element(By.NAME, "email").send_keys(corporate_email)  # Adjust locator
    # driver.find_element(By.NAME, "password").send_keys(password)  # Adjust locator
    # driver.find_element(By.ID, "loginBtn").click()  # Adjust locator

    # time.sleep(5)

    driver.get(f"http://localhost:3000/MyTeam")
    time.sleep(4)

    driver.get(f"http://localhost:3000/tasks")
    time.sleep(3)

    driver.find_element(By.NAME, "createTask").click()
    WebDriverWait(driver, 10).until(EC.url_contains("/CreateTask"))
    driver.find_element(By.NAME, "assignTask").click()
    time.sleep(2)

    driver.find_element(By.NAME ,"taskTitle").send_keys("Updated HR portal within two days")
    time.sleep(3)
    driver.find_element(By.NAME, "taskDetails").send_keys("Updated HR Timesheet module quickly and pull the code in github quickly")
    time.sleep(3)
    driver.find_element(By.NAME, "addTasksto").click()
    time.sleep(3)
    
    driver.find_element(By.NAME, "backToTasks").click()
    time.sleep(4)
    driver.find_element(By.NAME, "updateTask").click()
    time.sleep(4)
    task_completed = driver.find_element(By.ID, "completed")
    time.sleep(2)
    # If not already selected, click it
    if not task_completed.is_selected():
        task_completed.click()
    print("✅ Checkbox selected successfully")

    time.sleep(2)
    driver.find_element(By.NAME, "updatedTaskComplete").click()

    time.sleep(3)
    driver.find_element(By.NAME, "receivedTask").click()
    time.sleep(2)
    driver.get(f"http://localhost:3000/OrgChart")
    time.sleep(3)
    # driver.get(f"http://localhost:3000/TimesheetManage")
    # time.sleep(3)
    # driver.find_element(By.NAME , "timesheetForm").click()
    # driver.find_element(By.NAME, "startDate").send_keys("19/09/2025")
    # driver.find_element(By.NAME, "endDate").send_keys("24/09/2025")
    # driver.find_element(By.NAME, "numberOfHours").send_keys("12")
    # driver.find_element(By.NAME, "clientName").send_keys("Yash")
    # driver.find_element(By.NAME, "projectName").send_keys("HR app Project")

    #  # Locate dropdown element
    # dropdown_element = driver.find_element(By.NAME, "taskType")

    # # Step 1: Click to open dropdown
    # dropdown_element.click()
    # time.sleep(1)

    # # Step 2: Wrap with Select
    # country_dropdown = Select(dropdown_element)

    # # Get all options except the first one (placeholder "Select a country")
    # options = country_dropdown.options[1:]

    # # Pick a random country
    # random_task = random.choice(options)
    # print(f"Selecting random task: {random_task.text}")

    # # Select the random option
    # country_dropdown.select_by_visible_text(random_task.text)
    # time.sleep(2)

    # #workLocation
    # present_workLocation = driver.find_element(By.NAME ,"workLocation")
    # present_workLocation.click()
    # time.sleep(2)
    # random_workplace = Select(present_workLocation)
    # options_workplace = random_workplace.options[1:]
    # selecting_choice = random.choice(options_workplace)
    # random_workplace.select_by_visible_text(selecting_choice.text)
    # time.sleep(3)
    
    # oncallSupport = driver.find_element(By.NAME, "onCallSupport")
    # oncallSupport.click()
    # time.sleep(3)
    # whetherSupport = Select(oncallSupport)
    # optionsTocall = whetherSupport.options[1:]
    # callSupport = random.choice(optionsTocall)
    # whetherSupport.select_by_visible_text(callSupport.text)
    # time.sleep(4)

    # driver.find_element(By.NAME, "submitTimesheet").click()
    # time.sleep(2)

     # STEP 3: Open new tab
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])  # Switch to new tab

    # STEP 4: Go to login page
    # driver.get("http://192.168.100.203:3000/login")
    driver.get(f"http://192.168.100.203:3000/{random_company}/login")

    time.sleep(2)

    # STEP 5: Fill in login form
    driver.find_element(By.NAME, "email").send_keys(corporate_email)  # Adjust locator
    driver.find_element(By.NAME, "password").send_keys(password)  # Adjust locator
    driver.find_element(By.ID, "loginBtn").click()  # Adjust locator

    time.sleep(4)

    driver.get(f"http://localhost:3000/MyColleague")
    time.sleep(4)

    driver.get(f"http://localhost:3000/tasks")
    time.sleep(3)

    driver.find_element(By.NAME, "receivedTask").click()
    time.sleep(2)