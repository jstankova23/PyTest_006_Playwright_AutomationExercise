# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

"""

VÝZNAM:       kontejner                                > kolekce karet                            > produkt
PROMĚNNÁ:     features_container/recommended_cotainer  > features_products/recommended_products   > product_XX (XX - pořadové číslo na stránce pro uživatele)
CSS SELEKTOR: div.features_items/div.recommended_items > .product-image-wrapper                   > a[data-product-id="YY"]
                                                                                                    product_id = "YY" (YY - ID productu v DOM)

Kontejner pro FEATURES ITEMS:
features_container = page.locator("div.features_items")                  # kontejner
features_products = features_container.locator(".product-image-wrapper") # kolekce karet
product_id = "YY"                                                        # ID produktu (pořadové číslo produktu z aplikace neodpovídá vždy ID produktu)                           
product_XX = features_products.filter(has=page.locator(f'a[data-product-id="{product_id}"]') # produkt 

"""

from playwright.sync_api import Page, expect
import uuid                                             # kvůli generování emailu v kroku 5 b)

# 23: Verify address details in checkout page
# TEST: REGISTRACE NOVÉHO UŽIVATELE, VLOŽENÍ 13. A 14. PRODUKTU DO KOŠÍKU Z HOME PAGE, KONTROLA ADRES, SMAZÁNÍ UŽIVATELE (BEZ PLATBY)
# Test stejný jako TC15: 'test_order_reg_before_checkout' v souboru 'test_15_pw_order_reg_before_checkout.py', kde je navíc i platba.
# Tento test TC23 by měl správně porovnávat dodací adresu (Delivery Address) a adresu pro fakturaci (Billing Address) a zaměřit se na kontrolu jejich odlišných hodnot. 
# Aktuálně ale demo e-shop umožňuje při registraci uživatele zadat jen jednu adresu. Tato adresa z registrace uživatele se dotahuje do nákupní objednávky do obou adres 
# (Delivery Address, Billing Address), které jsou v objednávce chráněny proti zápisu, tzn. není možné adresy jakkoliv měnit.
# Delivery Address a Billing Address jsou tak vždy shodné a obě se dotahují z jedné stejné adresy zadané při registraci uživatele. Test adres byl již proveden
# v předcházejících testech (TC15, TC16). Aktuálně tento test TC23 je tedy duplicití. Odpovídá testu TC15, kde je navíc i platba.
def test_order_reg_verify_address(page: Page):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    # 3. Verify that home page is visible successfully
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url
    

    # 4. Click 'Signup / Login' button
    login_link = page.get_by_role("link", name=" Signup / Login")   # vyhledání linku v záhlaví domovské stránky pro přihlášení uživatele
    login_link.click()


    # 5. Fill all details in Signup and create account
    ### Kompletní registrace uživatele 'Test_23 User' určeného pouze pro tento test
    ### Ukládání některých hodnot do proměnných, využijí se při ověřování adres
    ### a) Ověření přesměrování na stránku s nadpisem 'New User Signup!'
    new_user_heading = page.get_by_role("heading", name="New User Signup!")   # lokátor pro nadpis 'New User Signup!' na nové stránce
    expect(new_user_heading).to_be_visible(timeout=2000)  # ověření s automatizovaným čekáním, že se na stránce objevil cílený nadpis

    ### b) Vytvoření hlavičky uživatele (jméno, email)
    name = "Test_23 User" 
    email = f"test_23_user_{uuid.uuid4().hex[:8]}@example.com" # dynamické vygenerování unikátního emailu

    name_input = page.get_by_role("textbox", name="Name")
    name_input.fill(name)

    email_input = page.locator("form").filter(has_text="Signup").get_by_placeholder("Email Address")
    email_input.fill(email)

    page.get_by_role("button", name="Signup").click()

    ### c) Vypsání chybové hlášky v případě pokusu založení uživatele s již existujícím emailem (účtem)
    duplicate_email_error = page.get_by_text("Email Address already exist!")

    if duplicate_email_error.is_visible():
        raise AssertionError(
            f"Registrace uživatele {name} selhala – v systému již existuje email: {email}"
        )

    ### d) V případě úspěšného přihlášení uživatele čekání na stránku s textem "Enter Account Information"
    expect(page.get_by_text("Enter Account Information")).to_be_visible()

    ### e) Vyplnění dalších údajů o dodavateli
    ###### Oslovení (nepovinné)  - vytvoření proměnné, dotahuje se do 1. řádku adres
    ###### - Lokátory s proměnnými  
    mr_radio = page.locator("#id_gender1")      # id_gender1 = Mr. / pan
    mrs_radio = page.locator("#id_gender2")     # id_gender2 = Mrs. / paní
    ###### - Zaškrtnutí pole dle volby proměnné
    mr_radio.check()                            # zaškrtnutí pole Mr. / pan
    ###### - Dotažení hodnoty do proměnné 'title' podle skutečného stavu (zaškrtnutého pole Mr. nebo Mrs.)
    title = None
    if mr_radio.is_checked():
        title = "Mr."
    elif mrs_radio.is_checked():
        title = "Mrs."
    else:
        print("INFO: Title was not checked.") # pokud není zaškrtnuté žádné pole, jen tisk hlášky, pole není povinné, žádná výjimka
                     
    ###### Heslo (povinné)
    pswd = "TestPassword123"                                    
    pswd_input = page.get_by_role("textbox", name="Password *") 
    pswd_input.fill(pswd)                                       

    ###### Datum narození: 7. září 1987 (nepovinné)
    page.select_option("#days", "7")        
    page.select_option("#months", "September")      
    page.select_option("#years", "1987")     

    ###### Uložení hodnot do proměnných - dotahují se všechny do adres
    first_name = "Test_23"                  
    last_name = "User"                    
    company = "AutoTest"            # nepovinné
    address1 = "27 MG Road"
    address2 = "Flat 5B"            # nepovinné
    state = "Maharashtra"
    city = "Mumbai"
    zip_code = "400001"
    mobile_num = "+91 98765 43210"
               
    ###### Lokátory
    first_name_input = page.get_by_role("textbox", name="First name *")                    
    last_name_input = page.get_by_role("textbox", name="Last name *")                  
    company_input = page.get_by_role("textbox", name="Company", exact=True)                      
    address1_input = page.get_by_role("textbox", name="Address * (Street address, P.")    
    address2_input = page.get_by_role("textbox", name="Address 2")         
    state_input = page.get_by_role("textbox", name="State *")                      
    city_input = page.get_by_role("textbox", name="City * Zipcode *")                       
    zip_code_input = page.locator("#zipcode")                      
    mobile_num_input = page.get_by_role("textbox", name="Mobile Number *")     

    ###### Vyplnění polí
    first_name_input.fill(first_name)                    
    last_name_input.fill(last_name)                
    company_input.fill(company)                      
    address1_input.fill(address1)  
    address2_input.fill(address2)    
    state_input.fill(state)                     
    city_input.fill(city)                      
    zip_code_input.fill(zip_code)                     
    mobile_num_input.fill(mobile_num)

    ###### Výběr z roletového menu v poli Country
    country = "India"                                   # hodnota, která se dotahuje do adres
    country_dropdown = page.get_by_label("Country *")   # lokátor pole Country s roletovým menu
    country_dropdown.select_option(country)             # výběr konkrétní hodnoty z roletového menu

    ### f) Dokončení registrace
    page.get_by_role("button", name="Create Account").click()
  

    # 6. Verify 'ACCOUNT CREATED!' and click 'Continue' button
    ### Ověření, že se zobrazil nadpis 'ACCOUNT CREATED!'
    expect(page.get_by_text("Account Created!")).to_be_visible()   # ověření s automatizovaným čekáním, že se na stránce objevil cílený nadpis
    page.get_by_role("link", name="Continue").click()              # kliknutí na link 'Continue'

   
    # 7. Verify ' Logged in as username' at top
    logged_user_info = page.get_by_text(f"Logged in as {name}") # vyhledání linku v záhlaví stránky s textem o přihlášeném uživateli (proměnná 'name' z kroku 5 b)
    expect(logged_user_info).to_be_visible()


    # 8. Add products to cart
    ### Přidání 13. a 14. produktu dle pořadí zobrazení na stránce do košíku, identifikace konkrétních produktů probíhá ale podle jejich ID v DOM (ID neodpovídá vždy pořadí na stránce).   
    ### Seznam produktů je v horní části home page v sekci FEATURES ITEMS reprezentovaný gridem / mřížkou karet produktů;
    ### Každý produkt = jedna karta (v gridu / mřížce)
    ### Všechny karty mají stejnou třídu <div class="product-image-wrapper">...</div>
    features_container = page.locator("div.features_items")                      # lokátor pro kontejner/sekci features items položek v horní části home page
    features_products = features_container.locator(".product-image-wrapper")     # vnořený lokátor, kolekce všech karet produktů v kontejneru/sekci features items položek
    
    ### Přidání 13. produktu do košíku
    ###### a) Vyhledání 6. produktu dle ID přes href v mřížce a hover
    product_id = "15"                       # POZOR: pořadové číslo produktu viditelné z aplikace neodpovídá ID produktu v DOM
    product_13 = features_products.filter(has=page.locator(f"a[data-product-id='{product_id}']")).first # vyhledání první karty produktu z mřížky (products), která obsahuje odkaz na detail produktu s daným ID
    product_13.scroll_into_view_if_needed() # pokud je karta produktu mimo viditelnou část stránky, Playwright ji posune do zorného pole, overlay se často aktivuje jen na viditelné kartě
    product_13.hover()                      # simulace najetí myší na kartu produktu, tím se zobrazí overlay vrstva (.product-overlay) a v ní tlačítko 'Add to cart'

    ###### b) Overlay vrstva: Kliknutí na tlačítko 'Add to Cart'
    add_to_cart_prod13_btn = product_13.locator(".overlay-content .btn") # vyhledání tlačítka 'Add to Cart' v overlay vrstvě (vnořený lokátor) UVNITŘ TÉTO KONKRÉTNÍ KARTY produktu 
    add_to_cart_prod13_btn.wait_for(state="visible") # vyčkání, až se overlay vrstva skutečně ukáže
    add_to_cart_prod13_btn.click(force=True)         # kliknutí na tlačítko 'Add to Cart', i když ho dočasně něco překrývá, klik i při krátkém překrytí karty produktu

    ###### c) Modal: Kliknutí na tlačítko 'Continue Shopping' v modalu (popup / vyskakovací okno s tlačítkem 'Continue Shopping')
    continue_shop_btn = page.get_by_role("button", name="Continue Shopping") # lokátor pro tlačítko 'Continue Shopping'
    continue_shop_btn.wait_for(state="visible")                              # vyčkání na plné zobrazení modalu 
    continue_shop_btn.click()                                                # kliknutí na tlačítko 'Continue Shopping' v modalu
    page.wait_for_selector("button:has-text('Continue Shopping')", state="hidden")  # vyčkání na zavření modalu (skrytý stav modalu / tlačítka), pak teprve přejít na další produkt


    ### Přidání 14. produktu do košíku
    ###### a) Vyhledání 7. produktu dle ID přes href v gridu a hover
    product_id = "16"                       # POZOR: pořadové číslo produktu viditelné z aplikace neodpovídá ID produktu v DOM
    product_14 = features_products.filter(has=page.locator(f"a[data-product-id='{product_id}']")).first
    product_14.scroll_into_view_if_needed()  
    product_14.hover()

    ###### b) Overlay vrstva: Kliknutí na tlačítko 'Add to Cart'
    add_to_cart_prod14_btn = product_14.locator(".overlay-content .btn")
    add_to_cart_prod14_btn.wait_for(state="visible") 
    add_to_cart_prod14_btn.click(force=True)

    ###### c) Modal: Kliknutí na tlačítko 'Continue Shopping'
    continue_shop_btn = page.get_by_role("button", name="Continue Shopping")
    continue_shop_btn.wait_for(state="visible") 
    continue_shop_btn.click()
    page.wait_for_selector("button:has-text('Continue Shopping')", state="hidden")


    # 9. Click 'Cart' button
    cart_link = page.get_by_role("link", name=" Cart")                      # lokátor pro link Cart v záhlaví domovské stránky
    cart_link.click()


    # 10. Verify that cart page is displayed
    ### a) Technické ověření přesměrování na stránku košíku (kontrola URL)
    expect(page).to_have_url("https://automationexercise.com/view_cart")     
    
    ### b) Uživatelské ověření, že je skutečně zobrazen obsah nákupního košíku
    shopping_cart_heading = page.get_by_text("Shopping Cart") 
    expect(shopping_cart_heading).to_be_visible()                                      
    

    # 11. Click Proceed To Checkout
    proceed_to_checkout_link = page.get_by_text("Proceed To Checkout")          # lokátor na link 'Proceed to Checkout'
    proceed_to_checkout_link.click()                                            # kliknutí na link


    # 12. Verify that the delivery address is same address filled at the time registration of account
    # 13. Verify that the billing address is same address filled at the time registration of account
    # OBA ÚKOLY JSOU SHODNÉ, AKTUÁLNĚ APLIKACE UMOŽŇUJE ZADAT JEN JEDNU ADRESU PŘI REGISTRACI UŽIVATELE A V NÁKUPNÍ OBJEDNÁVCE SE DANÁ ADRESA Z REGISTRACE DOTAHUJE
    # DO DODACÍ ADRESY A DO ADRESY PRO FAKTURACI A APLIKACE AKTUÁLNĚ NEUMOŽŇUJE TYTO ADRESY JAKKOLIV MĚNIT (POLE JSOU CHRÁNĚNA PROTI ZÁPISU)
    ### a) Kontrola dodací a fakturační adresy
    ##### Porovnávají se údaje zadané při registraci uživatele 'Test_15 User' (proměnné definované přímo v tomto testu) proti údajům zobrazeným v adresách objednávky v UI.
    ##### Demo aplikace aktuálně neumožňuje zadat rozdílnou dodací a fakturační adresu, proto jsou v tuto chvíli obě adresy shodné.
    ##### Přesto se obě vždy porovnávají proti registračním údajům daného uživatele.
    ##### Porovnání adres pracuje i s prázdnými hodnotami – validují se pouze vyplněná pole.

    ##### Ověření přesměrování na stránku s nadpisem "Address Details"
    address_details_heading = page.get_by_role("heading", name="Address Details")
    expect(address_details_heading).to_be_visible()

    ##### Bloky adres pro dodání zboží a fakturaci
    delivery_block = page.locator("#address_delivery")
    billing_block = page.locator("#address_invoice")

    ##### Společný seznam polí pro dodací i fakturační adresu
    ##### Definice klíčů, která pole se mají porovnávat (JEN NÁZVY POLÍ, ne jejich hodnoty)
    address_fields = [
        "company",
        "address1",
        "address2",
        "city",
        "state",
        "zip_code",
        "country",
        "mobile_num"
    ]

    ##### Sestavení dat uživatele z proměnných definovaných v testu
    ##### Definice slovníku s hodnotami, jaké konkrétní HODNOTY má každý klíč v tomto testu
    ##### Slovnik - ruční mapování mezi názvy polí a skutečnými hodnotami uloženými v proměnných, aby mohl fungovat for cyklus
    ##### V testech, kde je uživatel vytvořen pomocí fixture mi tento slovník vrací přímo sama fixture (yield) a není nutný pak tento krok v testu
    test_user_data = {
        "company": company,
        "address1": address1,
        "address2": address2,
        "city": city,
        "state": state,
        "zip_code": zip_code,
        "country": country,          
        "mobile_num": mobile_num
    }

    ### YOUR DELIVERY ADDRESS – ověření dodací adresy
    ##### Ověřují se klíčové hodnoty zadané při registraci (ne formát ani pořadí řádků)

    ##### - První řádek adresy
    ##### Nepovinné oslovení (Mr./Mrs.) + povinné celé jméno - STEJNÉ PRO OBĚ ADRESY
    ##### Checkbox 'title' (Mr./Mrs.) není povinný, pole pro obě pohlaví mohou být prázdný; IF ošetří, aby se v oslovení nebojevilo 'None'
    if title:      
        title_full_name = f"{title} {first_name} {last_name}"
    else:
        title_full_name = f"{first_name} {last_name}" 

    ##### - Ověření výsledné sloučené hodnoty pro 1. řádek dodací adresy
    expect(delivery_block).to_contain_text(title_full_name)

    ##### - Ověření ostatních řádků dodací adresy
    ##### For cyklus projde všechna definovaná pole adresy a ověří jejich přítomnost pouze v případě, že má uživatel dané pole skutečně vyplněno
    for field in address_fields:
        value = test_user_data.get(field)     # hodnota z registrace uživatele v rámci tohoto testu
        if value:                             # pokud hodnota existuje
            assert value in delivery_block.inner_text(), \
                f"Delivery address validation failed for field '{field}': '{value}' not found in delivery address."


    ### YOUR BILLING ADDRESS – ověření adresy pro fakturaci
    ##### - Ověření výsledné sloučené hodnoty pro 1. řádek adresy pro fakturaci (aktuálně demo web má vždy obě adresy shodné)
    expect(billing_block).to_contain_text(title_full_name)

    ##### - Ověření ostatních řádků adresy pro fakturaci
    for field in address_fields:
        value = test_user_data.get(field)
        if value:
            assert value in billing_block.inner_text(), \
                f"Billing address validation failed for field '{field}': '{value}' not found in billing address."



    ### b) Kontrola nákupní objednávky
    ### Ověření přesměrování na stránku s nadpisem "Review Your Order"
    review_your_order_heading = page.get_by_role("heading", name="Review Your Order")
    expect(review_your_order_heading).to_be_visible()

    ### Kontrola celé tabulky objednávky (sekce obsahující všechny položky objednávky)
    order_table = page.locator("#cart_info")                   
    expect(order_table).to_be_visible()

    ### Kontrola pouze přítomnosti produktů 13 a 14 v objednávce
    ### (bez kontroly množství a cen z důvodu hromadného spuštění testů)
    ### Identifikace konkrétních produktů je provedena jako VNOŘENÝ LOKÁTOR 
    ### Lokátor řádku produktu je definován UVNITŘ lokátoru celé tabulky objednávky
    product_13_row = order_table.locator("tr#product-15")   # lokátor pro řádek produktu 6 vnořený do lokátoru pro tabulku objednávky, POZOR: ID neodpovídá pořadovému čislu v UI
    product_14_row = order_table.locator("tr#product-16")   # lokátor pro řádek produktu 7 vnořený do lokátoru pro tabulku objednávky, POZOR: ID neodpovídá pořadovému čislu v UI

    ### Ověření, že jsou oba produkty skutečně přítomny v objednávce
    expect(product_13_row).to_be_visible()
    expect(product_14_row).to_be_visible()


    # 14. Click 'Delete Account' button
    delete_acc_link = page.get_by_role("link", name=" Delete Account") # lokátor na link 'Delete Account' v záhlaví stránky
    delete_acc_link.click()                                             # kliknutí na link


    # 15. Verify 'ACCOUNT DELETED!' and click 'Continue' button
    account_deleted_message = page.get_by_text("Account Deleted!")           # vyhledání hlášky 'Account Deleted'
    expect(account_deleted_message).to_be_visible # ověření s automatizovaným čekáním, že se na stránce objevil cílený text

    continue_after_delete_btn = page.get_by_role("link", name="Continue")    # vyhledání linku 'Continue'
    continue_after_delete_btn.click()                                        # kliknutí na link





