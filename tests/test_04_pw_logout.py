# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect

# 04_TEST CASE: Logout User
# ODHLÁŠENÍ UŽIVATELE DO DEMO E-SHOP WEBU 'https://automationexercise.com/
# test volá fixture 'session user', která vytváří pro celou testovací session jednoho fixního uživatele a maže ho až po doběhnutí všech testů za celou session
def test_logout(page: Page, session_user):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    # 3. Verify that home page is visible successfully
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url

    # 4. Click on 'Signup / Login' button
    login_link = page.get_by_role("link", name=" Signup / Login")   # vyhledání linku pro přihlášení uživatele
    login_link.click()                                               # kliknutí na link pro přihlášení uživatele

    # 5. Verify 'Login to your account' is visible
    login_heading = page.get_by_role("heading", name="Login to your account")  # lokátor pro nadpis 'Login to your account' na nové stránce
    expect(login_heading).to_be_visible(timeout=2000)  # ověření přesměrování na stránku s daným nadpisem a zpomalení

    # 6. Enter correct email address and password
    email = session_user["email"]                     # uložení uživatelského emailu (z fixture 'session_user') do proměnné
    passwd = session_user["password"]                 # uložení uživatelského hesla (z fixture 'session_user') do proměnné

    email_input = page.locator("form").filter(has_text="Login").get_by_placeholder("Email Address") # lokátor pole "Email Address"
    password_input = page.get_by_role("textbox", name="Password")   # lokátor pole "Password"

    email_input.fill(email)                     # vyplnění pole Email Address
    password_input.fill(passwd)                 # vyplnění pole Password

    # 7. Click 'login' button
    login_btn = page.get_by_role("button", name="Login")  # lokátor tlačítka "Login"
    login_btn.click()                                     # kliknutí na tlačítko "Login"

    # 8. Verify that 'Logged in as username' is visible
    logged_user_info = page.get_by_text(f"Logged in as {session_user["name"]}") # vyhledání linku v záhlaví stránky s textem o přihlášeném uživateli (Logged in as Session User)
    expect(logged_user_info).to_be_visible()

    # 9. Click 'Logout' button
    logout_link = page.get_by_role("link").filter(has_text="Logout") # lokátor pro link v záhlaví stránky pro odhlášení uživatele
    logout_link.click()                                              # kliknutí na link pro odhlášení uživatele

    # 10. Verify that user is navigated to login page
    login_heading = page.get_by_role("heading", name="Login to your account")  # lokátor pro nadpis 'Login to your account' na nové stránce
    expect(login_heading).to_be_visible(timeout=2000)  # ověření přesměrování na stránku s daným nadpisem a zpomalení

