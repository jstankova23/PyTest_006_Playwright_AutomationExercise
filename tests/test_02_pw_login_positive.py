# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect

# 02_TEST CASE: Login User with correct email and password - Positive Test
# PŘIHLÁŠENÍ UŽIVATELE DO DEMO E-SHOP WEBU 'https://automationexercise.com/'
# Test vyžaduje existenci uživatele, proto volá fixture 'test_2_user', která mu zaregistruje nového uživatele.
# Test volá fixture 'test_2_user', která nejdříve vytvoří unikátního dočasného uživatele výhradně pro tento test. 
# Uživatel 'Test_2 User' je specifický pouze pro tento test.
# Na konci testu je uživatel 'Test_2 User' vymazán samotným testem, v případě selhání, výmaz uživatele zajišťuje fixture.
def test_login_positive(page: Page, test_2_user):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    # 3. Verify that home page is visible successfully
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url

    # 4. Click on 'Signup / Login' button
    login_link = page.get_by_role("link", name=" Signup / Login")   # vyhledání linku pro přihlášení uživatele
    login_link.click()                                               # kliknutí na link pro přihlášení uživatele

    # 5. Verify 'Login to your account' is visible
    login_heading = page.get_by_role("heading", name="Login to your account")  # lokátor pro nadpis 'Login to your account' na nové stránce
    expect(login_heading).to_be_visible(timeout=2000)                          # ověření přesměrování na stránku s daným nadpisem a zpomalení

    # 6. Enter correct email address and password
    email = test_2_user["email"]      # uložení uživatelského emailu do proměnné (z fixture 'test_2_user'z conftest.py), slovník test_2_user, klíč email
    passwd = test_2_user["password"]  # uložení uživatelského hesla do proměnné (z fixture 'test_2_user'z conftest.py), slovník test_2_user, klíč email

    email_input = page.locator("form").filter(has_text="Login").get_by_placeholder("Email Address") # lokátor pole "Email Address"
    password_input = page.get_by_role("textbox", name="Password")   # lokátor pole "Password"

    email_input.fill(email)                     # vyplnění pole Email Address
    password_input.fill(passwd)                 # vyplnění pole Password

    # 7. Click 'login' button
    login_btn = page.get_by_role("button", name="Login")  # lokátor tlačítka "Login"
    login_btn.click()                                     # kliknutí na tlačítko "Login"

    # 8. Verify that 'Logged in as username' is visible
    logged_user_info = page.get_by_text(f"Logged in as {test_2_user["name"]}") # vyhledání linku v záhlaví stránky s textem o přihlášeném uživateli
    expect(logged_user_info).to_be_visible()

    # 9. Click 'Delete Account' button
    delete_link = page.get_by_role("link", name=" Delete Account") # lokátor pro link v záhlaví stránky pro vymazání uživatele
    delete_link.click()                                             # kliknutí na link pro vymazání uživatele

    # 10. Verify that 'ACCOUNT DELETED!' is visible
    new_delete_heading = page.get_by_text("Account Deleted!") # lokátor pro nadpis 'Account Deleted!' na nové stránce
    expect(new_delete_heading).to_be_visible(timeout=2000)    # ověření přesměrování na stránku s daným nadpisem a zpomalení
