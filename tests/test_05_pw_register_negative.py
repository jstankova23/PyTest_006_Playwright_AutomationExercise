# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures 'page', 'browser_context', 'accept_gdpr' definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect

# 05_TEST CASE: Register user with existing email - Negative Test
# TEST NEŮSPĚŠENÉHO POKUSU O REGISTRACI UŽIVATELE S JIŽ EXISTUJÍCÍM EMAILEM V DEMO E-SHOP WEBU 'https://automationexercise.com/'
# test využívá email uživatele 'Session User', kterého na začátku testovací session vytváří fixture 'session_user' a předává data uživatele SessionUser testům;
# takto je zajištěno, že test použije email již existujícího uživatele pro danou testovací session, a tím pádem se nepodaří tomuto testu založit dalšího uživatele;
# očekávaný výsledek: aplikace nedovolí zaregistrovat uživatele 'Test Email Duplicity', zobrazí chybovou hlášku, že uvedený email už v databázi uživatelů existuje
def test_registration_negative(page: Page, session_user):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    # 3. Verify that home page is visible successfully
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url
    
    # 4. Click on 'Signup / Login' button
    login_link = page.get_by_role("link", name=" Signup / Login")   # vyhledání linku pro přihlášení uživatele
    login_link.click()                                               # kliknutí na link pro přihlášení uživatele
    
    # 5. Verify 'New User Signup!' is visible (new page)
    new_user_heading = page.get_by_role("heading", name="New User Signup!")   # lokátor pro nadpis 'New User Signup!' na nové stránce
    expect(new_user_heading).to_be_visible(timeout=2000)  # ověření přesměrování na stránku s daným nadpisem a zpomalení

    # 6. Enter name and already registered email address
    name = "Test Email Duplicity"                 # uložení uživatelského jména do proměnné
    email = session_user["email"]                 # uložení uživatelského hesla (z fixture 'session_user') do proměnné - KLÍČOVÉ PRO TENTO TEST

    name_input = page.get_by_role("textbox", name="Name")                                            # lokátor pole "Name"
    email_input = page.locator("form").filter(has_text="Signup").get_by_placeholder("Email Address") # lokátor pole "Email"

    name_input.fill(name)                       # vyplnění pole Name
    email_input.fill(email)                     # vyplnění pole Email
 
    # 7. Click 'Signup' button
    signup_btn = page.get_by_role("button", name="Signup")  # lokátor tlačítka "Signup"
    signup_btn.click()                                      # kliknutí na tlačítko "Signup"

    # 8. Verify error 'Email Address already exist!' is visible
    error = page.get_by_text("Email Address already exist!") # lokátor pro chybovou hlášku 'Email Address already exist!'
    assert error.is_visible(timeout=500)         # ověření zobrazení očekávané chybové hlášky, mírná časová rezerva pro zobrazení hlášky
    


























