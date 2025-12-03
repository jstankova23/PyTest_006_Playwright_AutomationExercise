"""
=============================================================================================================================
CENTRÁLNÍ DEFINICE PYTEST FIXTURES  
PRO UI AUTOMATIZACI DEMO E-SHOPU (PLAYWRIGHT + PYTEST)
=============================================================================================================================

Autor:                      Jana Staňková
Verze projektu:             0.9.5
Datum vytvoření:            11. 11. 2025
Datum poslední aktualizace: 4. 12. 2025

Projekt: UI automatizace demo e-shopu https://automationexercise.com pomocí Playwright (sync API) a PyTest.

----------------------------------------------------------------------------------------------------
ARCHITEKTURA FIXTUR
----------------------------------------------------------------------------------------------------

Architektura fixtur je navržena s důrazem na:
- plnou izolaci jednotlivých testů,
- nulové sdílení cookies, košíku ani přihlášení mezi testy,
- jednotný výchozí stav pomocí uloženého GDPR (`gdpr.json`),
- vysoký výkon díky sdílenému procesu prohlížeče.

Základní stavební pilíře:
- browser        – jeden sdílený proces Chromium pro celou testovací session (session scoped)
- context_gdpr   – nový izolovaný browser context pro každý test se zpracovaným GDPR (function scoped)
- page           – jedna konkrétní stránka (tab) nad daným contextem (function scoped)

# Přehled Fixtures

| **FIXTURE**       | **SCOPE** | **AUTOMATICKÉ SPUŠTĚNÍ** | **VÝSLEDEK** |
|-------------------|-----------|--------------------------|--------------|
| `browser`         | session   | Ne                       | sdílený prohlížeč a kontext pro všechny testy |
| `context_gdpr`    | function  | Ne                       | vlastní browser context pro každý test se zpracovaným GDPR |
| `page`            | function  | Ne                       | nová stránka s domovskou URL pro každý test |
| `session_user`    | session   | Ano                      | uživatel **Session User** pro celou session, smazán na konci všech testů |
| `test_2_user`     | function  | Ne                       | uživatel **Test_2 User** unikátní pro TC02, smazán na konci testu |
| `test_16_user`    | function  | Ne                       | uživatel **Test_16 User** unikátní pro TC16, smazán na konci testu |
| `test_20_user`    | function  | Ne                       | uživatel **Test_20 User** unikátní pro TC20, smazán na konci testu |

----------------------------------------------------------------------------------------------------
SESSION USER
----------------------------------------------------------------------------------------------------

Projekt obsahuje fixture `session_user`, která:
- je spuštěna automaticky (`autouse=True`) před prvním testem,
- vytvoří uživatele **Session User** s dynamickým e-mailem pro celou testovací session,
- je sdílena testy TC04 a TC05,
- po dokončení všech testů uživatele opět přihlásí a smaže.

Protože `context_gdpr` je function-scoped, nemůže být použita v `session_user`.  
`session_user` si proto vytváří **vlastní session-scoped context** pomocí `browser.new_context(storage_state="gdpr.json")`.

----------------------------------------------------------------------------------------------------
OSTATNÍ UŽIVATELÉ
----------------------------------------------------------------------------------------------------

Fixtures `test_2_user`, `test_16_user`, `test_20_user` vytvářejí uživatele:
- vždy unikátní pro konkrétní test,
- s dynamicky generovaným e-mailem,
- s automatickým cleanupem po dokončení testu.

"""

import pytest
import uuid                                             # pro generování dynamických emailů
from playwright.sync_api import sync_playwright, Page, expect

    
# 1) FIXTURE PRO SPUŠTĚNÍ PROHLÍŽEČE – CHROMIUM
# Vytváří jeden sdílený proces prohlížeče pro celou testovací session.
#
# Použité parametry:
# - headless=True  – běh na pozadí,
# - headless=False – viditelné okno při lokálním ladění,
# - slow_mo        – zpomalení akcí pro snadnější sledování průběhu testů.
#
# Fixture je session-scoped z důvodu:
# - výkonu (nevytváří se nový proces pro každý test),
# - existence uživatele 'Session User' po celou testovací session,
# - bezpečného používání storage_state="gdpr.json" v oddělených contexteh.
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        yield browser
        browser.close()


# 2) FIXTURE PRO VYTVOŘENÍ IZOLOVANÉHO BROWSER CONTEXTU PRO KAŽDÝ TEST
# Každý test získá vlastní izolovaný browser context (function scoped).
# Používá storage_state="gdpr.json", který obsahuje: odsouhlasené GDPR, cookies, localStorage a sessionStorage.
# 'storage_state' je technický snapshot stavu prohlížeče, který Playwright umí uložit do souboru a znovu načíst.
# Soubor 'gdpr.json' byl vygenerován do kořenového adresáře projektu a obsahuje již zpracované GDPR.
#   Díky tomu:
# - není nutné v jednotlivých testech řešit GDPR,
# - každý test začíná ve stejném výchozím stavu,
# - košík ani přihlášení se mezi testy nesdílejí.
#
# Pokud by byla tato fixture session-scoped, docházelo by ke sdílení košíku mezi testy.
@pytest.fixture
def context_gdpr(browser):
    context = browser.new_context(storage_state="gdpr.json")
    yield context
    context.close()


# 3) FIXTURE PRO VYTVOŘENÍ STRÁNKY (page)
# 3) FIXTURE PRO VYTVOŘENÍ STRÁNKY (page)
# Vytváří novou stránku (tab) nad 'context_gdpr'.
# Automaticky:
# - odstraní reklamní iframe bannery pomocí add_init_script pomocí add_init_script,
# - přejde na domovskou stránku demo e-shopu,
# - po dokončení testu stránku automaticky zavře.
@pytest.fixture
def page(context_gdpr):
    page = context_gdpr.new_page()

    # Odstranění reklamních iframe bannerů (Google Ads)
    # Důležité pouze pro testera/support sledující průběh testu v zobrazeném okně prohlížeče.
    page.add_init_script("""
        setInterval(() => {
            document
                .querySelectorAll("iframe, .google-auto-placed, .adsbygoogle-container")
                .forEach(el => el.remove());
        }, 100);
    """)

    # Přechod na domovskou stránku demo e-shopu
    page.goto("https://automationexercise.com/")
    page.wait_for_load_state("domcontentloaded")

    yield page

    # Zavření stránky po testu
    page.close()



# 4) FIXTURE PRO REGISTRACI UŽIVATELE 'Session User' PRO CELOU TESTOVACÍ SESSION
# Fixture vytvoří uživatele 'Session User' s unikátním dynamickým e-mailem (import uuid).
# Uživatel existuje po celou dobu běhu testovací session (scope="session") a je sdílen pouze mezi testy TC04 a TC05.
# Fixture používá session-scoped fixture 'browser' a vytváří si vlastní browser context, protože function-scoped 
# fixture 'context_gdpr' nelze použít.
# Context je vytvořen se storage_state="gdpr.json", takže GDPR je již odsouhlaseno.
# Fixture vrací slovník s údaji o uživateli.
# Parametr autouse=True zajistí, že se fixture spustí automaticky před prvním testem.
# Na konci celé testovací session se uživatel znovu přihlásí a je smazán (cleanup).

@pytest.fixture(scope="session", autouse=True)
def session_user(browser):                                  # využívá fixture 'browser' (session scoped)
    context = browser.new_context(storage_state="gdpr.json") # vytváří si svůj kontext se zpracovaným GDPR 
    page = context.new_page()

    name = "Session User"
    email = f"session_user_{uuid.uuid4().hex[:8]}@example.com"  # dynamické vygenerování unikátního emailu
    password = "TestPassword123"

    # Vytvoření uživatelského jména a emailové adresy (dynamické)
    page.goto("https://automationexercise.com/")
    page.get_by_role("link", name=" Signup / Login").click()

    page.get_by_role("textbox", name="Name").fill(name)
    page.locator("form").filter(has_text="Signup").get_by_placeholder("Email Address").fill(email)
    page.get_by_role("button", name="Signup").click()

    # Vypsání chybové hlášky v případě pokusu založení uživatele s již existujícím emailem (účtem)
    duplicate_email_error = page.get_by_text("Email Address already exist!")

    if duplicate_email_error.is_visible():
        raise AssertionError(
            f"Registrace uživatele {name} selhala – v systému již existuje email: {email}"
        )

    # V případě úspěšného přihlášení uživatele čekání na stránku s textem "Enter Account Information"
    expect(page.get_by_text("Enter Account Information")).to_be_visible()

    # Vyplnění povinných údajů
    ### Oslovení a heslo                          
    title_input = page.locator("#id_gender1")   # oslovení Mr. / pan
    title = "Mrs."
    title_input.check()

    page.fill("#password", password)

    ### Datum narození: 23. listopadu 1979
    page.select_option("#days", "23")
    page.select_option("#months", "11")
    page.select_option("#years", "1979")

    ### Adresa dodání (kopíruje se v objednávce i do adresy pro fakturaci)
    ###### a) Uložení hodnot do proměnných - dotahují se do adres
    first_name = "Session"                  
    last_name = "User"                    
    # pole 'Company' prázdné (nepovinné)                 
    address1 = "123 Test Street"      
    # pole 'Address2' prázdné (nepovinné)   
    state = "Florida"                       
    city = "Sarasota"                       
    zip_code = "34201"                      
    mobile_num ="+19415550123"    

    ###### b) Lokátory
    first_name_input = page.get_by_role("textbox", name="First name *")                    
    last_name_input = page.get_by_role("textbox", name="Last name *")                  
    address1_input = page.get_by_role("textbox", name="Address * (Street address, P.")    
    state_input = page.get_by_role("textbox", name="State *")                      
    city_input = page.get_by_role("textbox", name="City * Zipcode *")                       
    zip_code_input = page.locator("#zipcode")                      
    mobile_num_input = page.get_by_role("textbox", name="Mobile Number *")     

    ###### c) Vyplnění polí
    first_name_input.fill(first_name)                    
    last_name_input.fill(last_name)                
    address1_input.fill(address1)  
    state_input.fill(state)                     
    city_input.fill(city)                      
    zip_code_input.fill(zip_code)                     
    mobile_num_input.fill(mobile_num)

    ###### Výběr z roletového menu v poli Country
    country = "United States"                           
    country_dropdown = page.get_by_label("Country *")   
    country_dropdown.select_option(country)             
    
    ### Dokončení registrace
    page.get_by_role("button", name="Create Account").click()
    expect(page.get_by_text("Account Created!")).to_be_visible()   # Vyčkání na potvrzení o úspěšně vytvořeném uživateli
    page.get_by_role("link", name="Continue").click()

    ### Odhlášení uživatele – v případě, že je stále přihlášen; testy provádí přihlášení samy
    logout_link = page.get_by_role("link").filter(has_text="Logout")
    if logout_link.is_visible():
        logout_link.click()
    
    ### Vrácení stránky do defaultního stavu
    page.goto("https://automationexercise.com/")

    ### Vrácení údajů testům
    ### Fixture vrací slovník s klíči: 'email', 'password', 'name', 'title', 'first_name', 'last_name' a všemi řádky adresy
    yield {
        "email": email,            # použito pro login
        "password": password,      # použito pro login
        "name": name,              # použito pro ověření textu „Logged in as username“ v záhlaví
        "title": title,
        "first_name": first_name,
        "last_name": last_name, 
        "address1": address1,                 
        "state": state,
        "city": city,
        "zip_code": zip_code,
        "mobile_num": mobile_num,
        "country": country,                
    }

    ### Cleanup – smazání uživatele po doběhnutí všech testů v session
    page.goto("https://automationexercise.com/login")

    ### Přihlášení před mazáním
    page.locator("form").filter(has_text="Login").get_by_placeholder("Email Address").fill(email)
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Login").click()

    expect(page.get_by_text(f"Logged in as {name}")).to_be_visible() # čekání, dokud se v záhlaví stránky neobjeví text "Logged in as Session User"

    ### Smazání uživatele
    page.goto("https://automationexercise.com/delete_account")
    expect(page.get_by_text("Account Deleted!")).to_be_visible()
    page.get_by_role("link", name="Continue").click()

    ### Zavření contextu
    page.close()
    context.close()




# 5) FIXTURE PRO REGISTRACI UŽIVATELE 'Test_2 User' pro TC02
# Fixture vytvoří dočasného uživatele 'Test_2 User' s dynamickým e-mailem (import uuid).
# Fixture vrací slovník s údaji o uživateli.
# Uživatelský účet je určen výhradně pro konkrétní test (TC02).
# Po dokončení testu je uživatel automaticky smazán.
@pytest.fixture
def test_2_user(page: Page):
    name = "Test_2 User"
    email = f"test_2_user_{uuid.uuid4().hex[:8]}@example.com" # dynamické vygenerování unikátního emailu
    password = "TestPassword123"

    # Vytvoření uživatelského jména a emailové adresy (dynamické)
    page.goto("https://automationexercise.com/")
    page.get_by_role("link", name=" Signup / Login").click()

    page.get_by_role("textbox", name="Name").fill(name)
    page.locator("form").filter(has_text="Signup").get_by_placeholder("Email Address").fill(email)
    page.get_by_role("button", name="Signup").click()

    # Vypsání chybové hlášky v případě pokusu založení uživatele s již existujícím emailem (účtem)
    duplicate_email_error = page.get_by_text("Email Address already exist!")

    if duplicate_email_error.is_visible():
        raise AssertionError(
            f"Registrace uživatele {name} selhala – v systému již existuje email: {email}"
        )

    # V případě úspěšného přihlášení uživatele čekání na stránku s textem "Enter Account Information"
    expect(page.get_by_text("Enter Account Information")).to_be_visible()

    # Vyplnění povinných údajů
    ### Oslovení a heslo                          
    title_input = page.locator("#id_gender2")   # Mrs. / paní
    title = "Mrs."
    title_input.check()

    page.fill("#password", password)

    ### Datum narození: 10. května 1990
    page.select_option("#days", "10")
    page.select_option("#months", "5")
    page.select_option("#years", "1990")

    ### Adresa dodání (kopíruje se v objednávce i do adresy pro fakturaci)
    ###### a) Uložení hodnot do proměnných - dotahují se do adres
    first_name = "Test_2"                  
    last_name = "User"                    
    # pole 'Company' prázdné (nepovinné)                  
    address1 = "78 Harbour View Road"
    # pole 'Address2' prázdné (nepovinné)          
    state = "New South Wales"
    city = "Sydney"
    zip_code = "2000"
    mobile_num = "+61 412 345 678"

    ###### b) Lokátory
    first_name_input = page.get_by_role("textbox", name="First name *")                    
    last_name_input = page.get_by_role("textbox", name="Last name *")                  
    address1_input = page.get_by_role("textbox", name="Address * (Street address, P.")    
    state_input = page.get_by_role("textbox", name="State *")                      
    city_input = page.get_by_role("textbox", name="City * Zipcode *")                       
    zip_code_input = page.locator("#zipcode")                      
    mobile_num_input = page.get_by_role("textbox", name="Mobile Number *")     

    ###### c) Vyplnění polí adresy
    first_name_input.fill(first_name)                    
    last_name_input.fill(last_name)                
    address1_input.fill(address1)  
    state_input.fill(state)                     
    city_input.fill(city)                      
    zip_code_input.fill(zip_code)                     
    mobile_num_input.fill(mobile_num)

    ###### d) Výběr hodnoty Country z roletového menu
    country = "Australia"                           # hodnota, která se dotahuje do adres
    country_dropdown = page.get_by_label("Country *")   
    country_dropdown.select_option(country)             

    ### Dokončení registrace
    page.get_by_role("button", name="Create Account").click()
    expect(page.get_by_text("Account Created!")).to_be_visible()   # Vyčkání na potvrzení o úspěšně vytvořeném uživateli
    page.get_by_role("link", name="Continue").click()

    ### Odhlášení (logout) uživatele - testy si samy provádějí přihlášení
    logout_link = page.get_by_role("link").filter(has_text="Logout")
    if logout_link.is_visible():
        logout_link.click()

    ### Vrácení stránky do defaultního stavu
    page.goto("https://automationexercise.com/")

    ### Vrácení údajů testům
    ### Fixture vrací slovník s klíči: 'email', 'password', 'name', 'title', 'first_name', 'last_name' a všemi řádky adresy
    yield {
        "email": email,            # použito pro login
        "password": password,      # použito pro login
        "name": name,              # použito pro ověření textu „Logged in as username“ v záhlaví
        "title": title,
        "first_name": first_name,
        "last_name": last_name, 
        "address1": address1,                 
        "state": state,
        "city": city,
        "zip_code": zip_code,
        "mobile_num": mobile_num,
        "country": country,                
    }

    ### Cleanup – pokud test nezmazal uživatele, smaže ho fixture, mazání dočasného uživatele po každém testu
    page.goto("https://automationexercise.com/delete_account")

    ### Někdy se zobrazí potvrzovací stránka
    if page.get_by_text("Account Deleted!").is_visible():
        page.get_by_role("link", name="Continue").click()



# 6) FIXTURE PRO REGISTRACI UŽIVATELE 'Test_16 User' pro TC16
# Fixture vytvoří dočasného uživatele 'Test_16 User' s dynamickým e-mailem (import uuid).
# Fixture vrací slovník s údaji o uživateli.
# Uživatelský účet je určen výhradně pro konkrétní test (TC16).
# Po dokončení testu je uživatel automaticky smazán.
@pytest.fixture
def test_16_user(page: Page):
    name = "Test_16 User"
    email = f"test_16_user_{uuid.uuid4().hex[:8]}@example.com" # dynamické vygenerování unikátního emailu
    password = "TestPassword123"

    # Vytvoření uživatelského jména a emailové adresy (dynamické)
    page.goto("https://automationexercise.com/")
    page.get_by_role("link", name=" Signup / Login").click()

    page.get_by_role("textbox", name="Name").fill(name)
    page.locator("form").filter(has_text="Signup").get_by_placeholder("Email Address").fill(email)
    page.get_by_role("button", name="Signup").click()

    # Vypsání chybové hlášky v případě pokusu založení uživatele s již existujícím emailem (účtem)
    duplicate_email_error = page.get_by_text("Email Address already exist!")

    if duplicate_email_error.is_visible():
        raise AssertionError(
            f"Registrace uživatele {name} selhala – v systému již existuje email: {email}"
        )

    # V případě úspěšného přihlášení uživatele čekání na stránku s textem "Enter Account Information"
    expect(page.get_by_text("Enter Account Information")).to_be_visible()

    # Vyplnění povinných údajů
    ### Oslovení a heslo                          
    title_input = page.locator("#id_gender2")   # Mr. / pan
    title = "Mrs."
    title_input.check()

    page.fill("#password", password)

    ### Datum narození: 17. října 2001
    page.select_option("#days", "17")
    page.select_option("#months", "10")
    page.select_option("#years", "2001")

    ### Adresa dodání (kopíruje se v objednávce i do adresy pro fakturaci)
    ###### a) Uložení hodnot do proměnných - dotahují se do adres
    first_name = "Test_16"                  
    last_name = "User"                    
    # pole 'Company' prázdné (nepovinné)                  
    address1 = "15 Rothschild Boulevard"
    address2 = "Apartment 12"
    state = "Tel Aviv District"
    city = "Tel Aviv"
    zip_code = "6688101"
    mobile_num = "+972 52 345 6789"

    ###### b) Lokátory
    first_name_input = page.get_by_role("textbox", name="First name *")                    
    last_name_input = page.get_by_role("textbox", name="Last name *")                  
    address1_input = page.get_by_role("textbox", name="Address * (Street address, P.")    
    state_input = page.get_by_role("textbox", name="State *")                      
    city_input = page.get_by_role("textbox", name="City * Zipcode *")                       
    zip_code_input = page.locator("#zipcode")                      
    mobile_num_input = page.get_by_role("textbox", name="Mobile Number *")     

    ###### c) Vyplnění polí adresy
    first_name_input.fill(first_name)                    
    last_name_input.fill(last_name)                
    address1_input.fill(address1)  
    state_input.fill(state)                     
    city_input.fill(city)                      
    zip_code_input.fill(zip_code)                     
    mobile_num_input.fill(mobile_num)

    ###### d) Výběr hodnoty Country z roletového menu
    country = "Israel"                           # hodnota, která se dotahuje do adres
    country_dropdown = page.get_by_label("Country *")   
    country_dropdown.select_option(country)             

    ### Dokončení registrace
    page.get_by_role("button", name="Create Account").click()
    expect(page.get_by_text("Account Created!")).to_be_visible()   # Vyčkání na potvrzení o úspěšně vytvořeném uživateli
    page.get_by_role("link", name="Continue").click()

    ### Odhlášení (logout) uživatele - testy si samy provádějí přihlášení
    logout_link = page.get_by_role("link").filter(has_text="Logout")
    if logout_link.is_visible():
        logout_link.click()

    ### Vrácení stránky do defaultního stavu
    page.goto("https://automationexercise.com/")

    ### Vrácení údajů testům
    ### Fixture vrací slovník s klíči: 'email', 'password', 'name', 'title', 'first_name', 'last_name' a všemi řádky adresy
    yield {
        "email": email,            # použito pro login
        "password": password,      # použito pro login
        "name": name,              # použito pro ověření textu „Logged in as username“ v záhlaví
        "title": title,
        "first_name": first_name,
        "last_name": last_name, 
        "address1": address1,                 
        "state": state,
        "city": city,
        "zip_code": zip_code,
        "mobile_num": mobile_num,
        "country": country,                
    }

    ### Cleanup – pokud test nezmazal uživatele, smaže ho fixture, mazání dočasného uživatele po každém testu
    page.goto("https://automationexercise.com/delete_account")

    ### Někdy se zobrazí potvrzovací stránka
    if page.get_by_text("Account Deleted!").is_visible():
        page.get_by_role("link", name="Continue").click()




# 7) FIXTURE PRO REGISTRACI UŽIVATELE 'Test_20 User' pro TC20
# Fixture vytvoří dočasného uživatele 'Test_20 User' s dynamickým e-mailem (import uuid).
# Fixture vrací slovník s údaji o uživateli.
# Uživatelský účet je určen výhradně pro konkrétní test (TC20).
# Po dokončení testu je uživatel automaticky smazán.
@pytest.fixture
def test_20_user(page: Page):
    name = "Test_20 User"
    email = f"test_20_user_{uuid.uuid4().hex[:8]}@example.com" # dynamické vygenerování unikátního emailu
    password = "TestPassword123"

    # Vytvoření uživatelského jména a emailové adresy (dynamické)
    page.goto("https://automationexercise.com/")
    page.get_by_role("link", name=" Signup / Login").click()

    page.get_by_role("textbox", name="Name").fill(name)
    page.locator("form").filter(has_text="Signup").get_by_placeholder("Email Address").fill(email)
    page.get_by_role("button", name="Signup").click()

    # Vypsání chybové hlášky v případě pokusu založení uživatele s již existujícím emailem (účtem)
    duplicate_email_error = page.get_by_text("Email Address already exist!")

    if duplicate_email_error.is_visible():
        raise AssertionError(
            f"Registrace uživatele {name} selhala – v systému již existuje email: {email}"
        )

    # V případě úspěšného přihlášení uživatele čekání na stránku s textem "Enter Account Information"
    expect(page.get_by_text("Enter Account Information")).to_be_visible()

    # Vyplnění povinných údajů
    ### Oslovení a heslo                          
    title_input = page.locator("#id_gender2")   # Mrs. / paní
    title = "Mrs."
    title_input.check()

    page.fill("#password", password)

    ### Datum narození: 3. dubna 1989
    page.select_option("#days", "3")
    page.select_option("#months", "4")
    page.select_option("#years", "1989")

    ### Adresa dodání (kopíruje se v objednávce i do adresy pro fakturaci)
    ###### a) Uložení hodnot do proměnných - dotahují se do adres
    first_name = "Test_20"                  
    last_name = "User"                    
    # pole 'Company' prázdné (nepovinné)                  
    address1 = "120 Orchard Road"
    address2 = "Unit 18-05"
    state = "Central Region"
    city = "Singapore"
    zip_code = "238865"
    mobile_num = "+65 9123 4567"

    ###### b) Lokátory
    first_name_input = page.get_by_role("textbox", name="First name *")                    
    last_name_input = page.get_by_role("textbox", name="Last name *")                  
    address1_input = page.get_by_role("textbox", name="Address * (Street address, P.")    
    state_input = page.get_by_role("textbox", name="State *")                      
    city_input = page.get_by_role("textbox", name="City * Zipcode *")                       
    zip_code_input = page.locator("#zipcode")                      
    mobile_num_input = page.get_by_role("textbox", name="Mobile Number *")     

    ###### c) Vyplnění polí adresy
    first_name_input.fill(first_name)                    
    last_name_input.fill(last_name)                
    address1_input.fill(address1)  
    state_input.fill(state)                     
    city_input.fill(city)                      
    zip_code_input.fill(zip_code)                     
    mobile_num_input.fill(mobile_num)

    ###### d) Výběr hodnoty Country z roletového menu
    country = "Singapore"                             # hodnota, která se dotahuje do adres
    country_dropdown = page.get_by_label("Country *")   
    country_dropdown.select_option(country)             

    ### Dokončení registrace
    page.get_by_role("button", name="Create Account").click()
    expect(page.get_by_text("Account Created!")).to_be_visible()   # Vyčkání na potvrzení o úspěšně vytvořeném uživateli
    page.get_by_role("link", name="Continue").click()

    ### Odhlášení (logout) uživatele - testy si samy provádějí přihlášení
    logout_link = page.get_by_role("link").filter(has_text="Logout")
    if logout_link.is_visible():
        logout_link.click()

    ### Vrácení stránky do defaultního stavu
    page.goto("https://automationexercise.com/")

    ### Vrácení údajů testům
    ### Fixture vrací slovník s klíči: 'email', 'password', 'name', 'title', 'first_name', 'last_name' a všemi řádky adresy
    yield {
        "email": email,            # použito pro login
        "password": password,      # použito pro login
        "name": name,              # použito pro ověření textu „Logged in as username“ v záhlaví
        "title": title,
        "first_name": first_name,
        "last_name": last_name, 
        "address1": address1,                 
        "state": state,
        "city": city,
        "zip_code": zip_code,
        "mobile_num": mobile_num,
        "country": country,                
    }

    ### Cleanup – pokud test nezmazal uživatele, smaže ho fixture, mazání dočasného uživatele po každém testu
    page.goto("https://automationexercise.com/delete_account")

    ### Někdy se zobrazí potvrzovací stránka
    if page.get_by_text("Account Deleted!").is_visible():
        page.get_by_role("link", name="Continue").click()