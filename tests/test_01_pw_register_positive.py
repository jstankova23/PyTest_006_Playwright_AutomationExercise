# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures 'page', 'browser_context', 'accept_gdpr' definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect
import uuid                                             # kvůli generování emailu v kroku 9

# 01_TEST CASE: Register User - Positive Test
# REGISTRACE UŽIVATELE DO DEMO E-SHOP WEBU 'https://automationexercise.com/' 
# vytvořený uživatel 'Test_1 User' s dynamickým emailem je v závěru tohoto testu vymazán
def test_registration_positive(page: Page):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    # 3. Verify that home page is visible successfully
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url
    
    # 4. Click on 'Signup / Login' button
    login_link = page.get_by_role("link", name=" Signup / Login")   # vyhledání linku v záhlaví domovské stránky pro přihlášení uživatele
    login_link.click()                                               # kliknutí na link pro přihlášení uživatele
    
    # 5. Verify 'New User Signup!' is visible (new page)
    new_user_heading = page.get_by_role("heading", name="New User Signup!")   # lokátor pro nadpis 'New User Signup!' na nové stránce
    expect(new_user_heading).to_be_visible(timeout=2000)  # ověření s automatizovaným čekáním, že se na stránce objevil cílený nadpis

    # 6. Enter name and email address
    ### Uložení hodnot do proměnných
    name = "Test_1 User"               
    email = f"test_1_user_{uuid.uuid4().hex[:8]}@example.com"      # dynamický email

    ### Lokátory
    name_input = page.get_by_role("textbox", name="Name")                                            
    email_input = page.locator("form").filter(has_text="Signup").get_by_placeholder("Email Address") 

    ### Vyplnění polí hodnotami proměnných
    name_input.fill(name)                       
    email_input.fill(email)                     
    
    # 7. Click 'Signup' button
    signup_btn = page.get_by_role("button", name="Signup")  # lokátor tlačítka "Signup"
    signup_btn.click()                                      # kliknutí na tlačítko "Signup"

    ### Chybová hláška v případě pokusu založení uživatele s již existujícím emailem (účtem)
    duplicate_email_error = page.get_by_text("Email Address already exist!")   # lokátor chybové hlášky

    if duplicate_email_error.is_visible():
        raise AssertionError(
            f"Registrace uživatele {name} selhala – v systému již existuje email: {email}"
        )

    # 8. Verify that 'ENTER ACCOUNT INFORMATION' is visible (new page)
    new_page_heading = page.get_by_text("Enter Account Information") # lokátor pro nadpis 'Enter Account Information' na nové stránce
    expect(new_page_heading).to_be_visible(timeout=2000)  # ověření s automatizovaným čekáním, že se na stránce objevil cílený nadpis

    # 9. Fill details: Title, Name, Email, Password, Date of birth
    title = page.locator("#id_gender2")                      # gender2 = Mrs. / paní 
    title.check()  

    pswd = "TestPassword123"                                    # uložení hesla do proměnné
    pswd_input = page.get_by_role("textbox", name="Password *") # lokátor pole Password
    pswd_input.fill(pswd)                                       # vyplnění pole Password

    ### datum narození: 1. ledna 2000
    page.select_option("#days", "1")        
    page.select_option("#months", "January")      
    page.select_option("#years", "2000")     

    # 10. Select checkbox 'Sign up for our newsletter!'
    newsletter = page.get_by_text("Sign up for our newsletter!")  # lokátor zaškrtávacího pole pro odběr novinek
    newsletter.check()                                            # zaškrtnutí pole pro odběr novinek
    
    # 11. Select checkbox 'Receive special offers from our partners!'
    offers = page.get_by_text("Receive special offers from")      # lokátor zaškrtávacího pole pro speicální nabídky
    offers.check()                                                # zaškrtnutí pole pro speicální nabídky

    # 12. Fill details: First name, Last name, Company, Address, Address2, Country, State, City, Zipcode, Mobile Number (Address Information section)
    ### Uložení hodnot pro adresu a telefon uživatele do proměnných
    first_name = "Test_1"                     
    last_name = "User"                  
    company = "AutoTest"                    
    address1 = "4520 Palm Breeze Lane"      
    address2 = "Apt. 12B"         
    state = "Florida"                       
    city = "Sarasota"                       
    zip_code = "34232"                      
    mobile_num ="(941) 555-4827"            

    ### Lokátory 
    first_name_input = page.get_by_role("textbox", name="First name *")                    
    last_name_input = page.get_by_role("textbox", name="Last name *")                  
    company_input = page.get_by_role("textbox", name="Company", exact=True)                      
    address1_input = page.get_by_role("textbox", name="Address * (Street address, P.")    
    address2_input = page.get_by_role("textbox", name="Address 2")         
    state_input = page.get_by_role("textbox", name="State *")                      
    city_input = page.get_by_role("textbox", name="City * Zipcode *")                       
    zip_code_input = page.locator("#zipcode")                      
    mobile_num_input = page.get_by_role("textbox", name="Mobile Number *")     

    ### Vyplnění polí
    first_name_input.fill(first_name)                    
    last_name_input.fill(last_name)                
    company_input.fill(company)                      
    address1_input.fill(address1)  
    address2_input.fill(address2)    
    state_input.fill(state)                     
    city_input.fill(city)                      
    zip_code_input.fill(zip_code)                     
    mobile_num_input.fill(mobile_num)
    
    ### Výběr z roletového menu v poli Country
    country_dropdown = page.get_by_label("Country *")   # lokátor pole Country s roletovým menu
    country_dropdown.select_option("United States")     # výběr konkrétní hodnoty z roletového menu

    # 13. Click 'Create Account button'
    create_acc_btn = page.get_by_role("button", name="Create Account")
    create_acc_btn.click()
    
    # 14. Verify that 'ACCOUNT CREATED!' is visible
    new_acc_page_heading = page.get_by_text("Account Created!") # lokátor pro nadpis 'Account Created!' na nové stránce
    expect(new_acc_page_heading).to_be_visible(timeout=5000)    # ověření přesměrování na stránku s daným nadpisem a zpomalení

    # 15. Click 'Continue' button
    continue_after_create = page.get_by_role("link", name="Continue")   # vyhledání tlačítka (link) pro pokračování
    continue_after_create.click()                                       # kliknutí na tlačítko (link) pro pokračování

    # 16. Verify that 'Logged in as username' is visible
    logged_user_info = page.get_by_text(f"Logged in as {name}") # vyhledání linku v záhlaví stránky s textem o přihlášeném uživateli (proměnná 'name' z kroku 6)
    expect(logged_user_info).to_be_visible()

    # 17. Click 'Delete Account' button
    delete_link = page.get_by_role("link", name=" Delete Account") # lokátor pro link v záhlaví stránky pro vymazání uživatele
    delete_link.click()                                             # kliknutí na link pro vymazání uživatele

    # 18. Verify that 'ACCOUNT DELETED!' is visible and click 'Continue' button
    new_delete_heading = page.get_by_text("Account Deleted!") # lokátor pro nadpis 'Account Deleted!' na nové stránce
    expect(new_delete_heading).to_be_visible(timeout=2000)    # ověření přesměrování na stránku s daným nadpisem a zpomalení

    continue_after_delete = page.get_by_role("link", name="Continue")   # vyhledání tlačítka (link) pro pokračování
    continue_after_delete.click()                                       # kliknutí na tlačítko (link) pro pokračování
























