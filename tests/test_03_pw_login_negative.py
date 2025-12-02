# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect

# 03_TEST CASE: Login User with correct email and password - Negative Test
# POKUS O PŘIHLÁŠENÍ UŽIVATELE DO DEMO E-SHOP WEBU 'https://automationexercise.com/' S CHYBNÝM EMAILEM A HESLEM
# test nevolá fixture pro dočasného uživatele ani pro fixního uživatele
def test_login_negative(page: Page):
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

    # 6. Enter incorrect email address and password
    email = "invalid_email@error.com"           # uložení neexistujícího emailu do proměnné
    passwd = "InvalidPassword"                  # uložení neplatného hesla do proměnné

    email_input = page.locator("form").filter(has_text="Login").get_by_placeholder("Email Address") # lokátor pole "Email Address"
    password_input = page.get_by_role("textbox", name="Password")   # lokátor pole "Password"

    email_input.fill(email)                     # vyplnění pole Email Address
    password_input.fill(passwd)                 # vyplnění pole Password

    # 7. Click 'login' button
    login_btn = page.get_by_role("button", name="Login")  # lokátor tlačítka "Login"
    login_btn.click()                                     # kliknutí na tlačítko "Login"

    # 8. Verify error 'Your email or password is incorrect!' is visible
    new_incorrect_heading = page.get_by_text("incorrect")     # lokátor pro nadpis obsahující slovo 'incorrect' na nové stránce
    expect(new_incorrect_heading).to_be_visible(timeout=2000)    # ověření přesměrování na stránku s daným nadpisem a zpomalení
