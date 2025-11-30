# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures 'page', 'browser_context', 'accept_gdpr' definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect

# 16: Place Order: Login before Checkout
# TEST: LOGIN UŽIVATELE 'TEMP USER', OBJEDNÁNÍ 8., 9. A 10. PRODUKTU, PLATBA A SMAZÁNÍ UŽIVATELE
### Fixture 'temp_user' vytvoří dočasného uživatele s dynamickou adresou pouze pro tento test a i když tento test uživatele maže, 
### fixture zajišťuje jeho výmaz pro případ, kdyby tento test nedoběhl do konce.
def test_order_login_before_checkout(page: Page, temp_user): # fixture 'temp_user' vytvoří dočasného uživatele pouze pro tento test
    # 1. Launch browser; 
    # 2. Navigate to home url;
    # 3. Verify that home page is visible successfully
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url
    

    # 4. Click 'Signup / Login' button
    # kliknutí na link 'Signup / Login' v záhlaví domovské stránky pro přihlášení uživatele
    login_link = page.get_by_role("link", name=" Signup / Login")   
    login_link.click()


    # 5. Fill email, password and click 'Login' button
    ### Ověření přesměrování na stránku s nadpisem 'Login to your account'
    login_heading = page.get_by_role("heading", name="Login to your account")  
    expect(login_heading).to_be_visible(timeout=2000)  

    ### Zadání emailu a hesla uživatele 'Temp User', vytvořeného pomocí fixture 'temp_user' pro tento test
    email = temp_user["email"]                     
    passwd = temp_user["password"]                 

    email_input = page.locator("form").filter(has_text="Login").get_by_placeholder("Email Address") 
    password_input = page.get_by_role("textbox", name="Password")                                   

    email_input.fill(email)                    
    password_input.fill(passwd)                 

    ### Kliknutí na tlačítko 'Login'
    login_btn = page.get_by_role("button", name="Login")  
    login_btn.click()                                     


    # 6. Verify ' Logged in as username' at top
    logged_user_info = page.get_by_text(f"Logged in as {temp_user["name"]}") # vyhledání linku v záhlaví stránky s textem o přihlášeném uživateli
    expect(logged_user_info).to_be_visible()


    # 7. Add products to cart
    ### Přidání 8., 9. a 10. produktu dle pořadí zobrazení na stránce do košíku, identifikace konkrétních produktů probíhá ale podle jejich ID v DOM (ID neodpovídá vždy pořadí na stránce).
    ### Seznam produktů je na stránce reprezentovaný gridem / mřížkou karet produktů;
    ### každý produkt = jedna karta (v gridu / mřížce)
    ### všechny karty mají stejnou třídu <div class="product-image-wrapper">...</div>
    products = page.locator(".product-image-wrapper")   # CSS lokátor pro seznam všech karet v gridu / mřížce, tzn. karty všech produktů na stránce


    ### Přidání 8. produktu do košíku
    ###### a) Vyhledání 8. produktu dle ID přes href v mřížce a hover
    product_8 = products.filter(has=page.locator("a[data-product-id='8']")).first # vyhledání první karty produktu z mřížky (products), která obsahuje odkaz na detail produktu s daným ID
    product_8.scroll_into_view_if_needed() # pokud je karta produktu mimo viditelnou část stránky, Playwright ji posune do zorného pole, overlay se často aktivuje jen na viditelné kartě
    product_8.hover()                      # simulace najetí myší na kartu produktu, tím se zobrazí overlay vrstva (.product-overlay) a v ní tlačítko 'Add to cart'

    ###### b) Kliknutí na tlačítko 'Add to Cart'
    add_to_cart_prod8_btn = product_8.locator(".overlay-content .btn") # vyhledání tlačítka 'Add to Cart' v overlay vrstvě (vnořený lokátor) UVNITŘ TÉTO KONKRÉTNÍ KARTY produktu 
    add_to_cart_prod8_btn.wait_for(state="visible") # vyčkání, až se overlay vrstva skutečně ukáže
    add_to_cart_prod8_btn.click(force=True)         # kliknutí na tlačítko 'Add to Cart', i když ho dočasně něco překrývá, klik i při krátkém překrytí karty produktu

    ###### c) Kliknutí na tlačítko 'Continue Shopping' v modalu (popup / vyskakovací okno s tlačítkem 'Continue Shopping')
    continue_shop_btn = page.get_by_role("button", name="Continue Shopping") # lokátor pro tlačítko 'Continue Shopping'
    continue_shop_btn.wait_for(state="visible")                              # vyčkání na plné zobrazení modalu 
    continue_shop_btn.click()                                                # kliknutí na tlačítko 'Continue Shopping' v modalu
    page.wait_for_selector("button:has-text('Continue Shopping')", state="hidden")  # vyčkání na zavření modalu (skrytý stav modalu / tlačítka), pak teprve přejít na další produkt


    ### Přidání 9. produktu do košíku
    ###### a) Vyhledání 9. produktu dle ID přes href v gridu a hover
    product_9 = products.filter(has=page.locator("a[href='/product_details/11']")).first  # POZOR: ID produktu je jiné než jeho pořadové číslo na stránce
    product_9.scroll_into_view_if_needed()  
    product_9.hover()

    ###### b) Kliknutí na tlačítko 'Add to Cart'
    add_to_cart_prod9_btn = product_9.locator(".overlay-content .btn")
    add_to_cart_prod9_btn.wait_for(state="visible") 
    add_to_cart_prod9_btn.click(force=True)

    ###### c) Kliknutí na tlačítko 'Continue Shopping'
    continue_shop_btn = page.get_by_role("button", name="Continue Shopping")
    continue_shop_btn.wait_for(state="visible") 
    continue_shop_btn.click()
    page.wait_for_selector("button:has-text('Continue Shopping')", state="hidden")


    ### Přidání 10. produktu do košíku
    ###### a) Vyhledání 10. produktu dle ID přes href v gridu a hover
    product_10 = products.filter(has=page.locator("a[href='/product_details/12']")).first  # POZOR: ID produktu je jiné než jeho pořadové číslo na stránce
    product_10.scroll_into_view_if_needed() 
    product_10.hover()

    ###### b) Kliknutí na tlačítko 'Add to Cart'
    add_to_cart_prod10_btn = product_10.locator(".overlay-content .btn")
    add_to_cart_prod10_btn.wait_for(state="visible")
    add_to_cart_prod10_btn.click(force=True)

    ###### c) Kliknutí na tlačítko 'Continue Shopping'
    continue_shop_btn = page.get_by_role("button", name="Continue Shopping")
    continue_shop_btn.wait_for(state="visible")
    continue_shop_btn.click()
    page.wait_for_selector("button:has-text('Continue Shopping')", state="hidden")



    # 8. Click 'Cart' button
    cart_link = page.get_by_role("link", name=" Cart")                      # lokátor pro link Cart v záhlaví domovské stránky
    cart_link.click()


    # 9. Verify that cart page is displayed
    ### a) Technické ověření přesměrování na stránku košíku (kontrola URL)
    expect(page).to_have_url("https://automationexercise.com/view_cart")     
    
    ### b) Uživatelské ověření, že je skutečně zobrazen obsah nákupního košíku
    shopping_cart_heading = page.get_by_text("Shopping Cart") 
    expect(shopping_cart_heading).to_be_visible()                                      
    

    # 10. Click Proceed To Checkout
    proceed_to_checkout_link = page.get_by_text("Proceed To Checkout")          
    proceed_to_checkout_link.click()                                           


    # 11. Verify Address Details and Review Your Order
    ### a) Kontrola dodací a fakturační adresy
    ##### Porovnávají se údaje z registrace uživatele 'Temp User' (fixture 'temp_user') proti údajům zobrazeným v adresách objednávky v UI.
    ##### Demo aplikace aktuálně neumožňuje zadat rozdílnou dodací a fakturační adresu, proto jsou v tuto chvíli obě adresy vždy shodné.
    ##### Přesto se obě adresy vždy porovnávají proti registračním údajům daného uživatele.
    ##### Porovnání adres pracuje i s prázdnými hodnotami – validují se pouze vyplněná pole.
    
    ##### Ověření přesměrování na stránku s nadpisem "Address Details"
    address_details_heading = page.get_by_role("heading", name="Address Details")
    expect(address_details_heading).to_be_visible()

    ##### UI - INFO Z OBJEDNÁVKY

    ######## Bloky adres pro dodání zboží a fakturaci
    delivery_block = page.locator("#address_delivery")
    billing_block = page.locator("#address_invoice")

    ######## Společný seznam polí pro dodací i fakturační adresu
    ######## Obsahuje všechna pole, která mohou (ale nemusí) být u uživatele vyplněna
    ######## Definice klíčů, která pole se mají porovnávat (JEN NÁZVY POLÍ, ne jejich hodnoty)
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

    ##### POROVNÁNÍ ÚDAJŮ Z REGISTRACE UŽIVATELE 'Temp User' VS. UI (INFO Z OBJEDNÁVKY)

    ######## YOUR DELIVERY ADDRESS – ověření dodací adresy
    ######## Ověřují se klíčové hodnoty zadané při registraci uživatele 'Temp User' (ne formát ani pořadí řádků)
    title_full_name = f'{temp_user["title"]} {temp_user["first_name"]} {temp_user["last_name"]}' # 1.řádek adresy: oslovení (Mr./Mrs.) + celé jméno, proměnnou využívají obě adresy
    expect(delivery_block).to_contain_text(title_full_name)     # ověření, zda text složený z oslovení a celého jména existuje někde v bloku s dodací adresou

    ##### For cyklus projde všechna definiovaná pole adresy a ověří jejich přítomnost pouze v případě, že má uživatel dané pole skutečně vyplněno
    for field in address_fields:                              # Cyklus prochází seznam klíčů (address_fields),
        value = temp_user.get(field)                          # pro každý klíč si vezme hodnotu z fixture 'temp_user' pro registraci uživatele 'Temp User',
        if value:                                             # pokud hodnota ve fixture existuje,
            assert value in delivery_block.inner_text(), f"Delivery address validation failed for field '{field}': '{value}' not found in delivery address."  
            # ověří, že se hodnota nachází v UI - v objednávce v textu bloku pro dodací adresu, jinak test spadne s popisem pole

    ######## YOUR BILLING ADDRESS – ověření fakturační adresy
    ######## Stejné ověření a postup jako u dodací adresy, porovnávají se údaje z registrace uživatele z fixture proti hodnotám v UI (v objednávce).
    expect(billing_block).to_contain_text(title_full_name)

    for field in address_fields:
        value = temp_user.get(field)
        if value:
            assert value in billing_block.inner_text(), f"Billing address validation failed for field '{field}': '{value}' not found in billing address."  



    ### b) Kontrola nákupní objednávky
    ##### Ověření přesměrování na stránku s nadpisem "Review Your Order"
    review_your_order_heading = page.get_by_role("heading", name="Review Your Order")
    expect(review_your_order_heading).to_be_visible()

    ##### Kontrola celé tabulky objednávky (sekce obsahující všechny položky objednávky)
    order_table = page.locator("#cart_info")                   
    expect(order_table).to_be_visible()
    page.wait_for_timeout(500) # čekání, aby se tabulka skutečně naplnila (doplněno)

    ##### Kontrola pouze přítomnosti produktů 8, 9 a 10 v objednávce
    ##### (bez kontroly množství a cen z důvodu hromadného spuštění testů)
    ##### Identifikace konkrétních produktů je provedena jako VNOŘENÝ LOKÁTOR 
    ##### Lokátor řádku produktu je definován UVNITŘ lokátoru celé tabulky objednávky
    product_8_row = order_table.locator("tr#product-8")
    product_9_row = order_table.locator("tr#product-11")  # POZOR: ID neodpovídá pořadovému číslu produktu na obrazovce
    product_10_row = order_table.locator("tr#product-12") # POZOR: ID neodpovídá pořadovému číslu produktu na obrazovce

    ##### Ověření, že jsou všechny tři produkty skutečně přítomny v objednávce
    expect(product_8_row).to_be_visible()
    expect(product_9_row).to_be_visible()
    expect(product_10_row).to_be_visible()


    # 12. Enter description in comment text area and click 'Place Order'
    ### Vložení komentáře do boxu s popisem "If you would like to add a comment ..."
    comment_text_area = page.locator("textarea[name=\"message\"]")  
    comment_text_area.fill("Test_16 User - test comment.")

    place_order_link = page.get_by_role("link", name="Place Order")
    place_order_link.click()


    # 13. Enter payment details: Name on Card, Card Number, CVC, Expiration date
    ### Uložení hodnot do proměnných
    name_on_card = "Test_16 User"
    card_number = "9999 1111 2222 3333"
    cvc = "123"
    mm = "11"
    yyyy = "2029"

    ### Lokátory
    name_on_card_input = page.locator("input[name=\"name_on_card\"]")
    card_number_input = page.locator("input[name=\"card_number\"]")
    cvc_input = page.get_by_role("textbox", name="ex.")
    mm_input = page.get_by_role("textbox", name="MM")
    yyyy_input = page.get_by_role("textbox", name="YYYY")

    ### Vyplnění polí
    name_on_card_input.fill(name_on_card)
    card_number_input.fill(card_number)
    cvc_input.fill(cvc)
    mm_input.fill(mm)
    yyyy_input.fill(yyyy)
    
    
    # 14. Click 'Pay and Confirm Order' button
    pay_and_confirm_btn = page.get_by_role("button", name="Pay and Confirm Order")
    pay_and_confirm_btn.click()


    # 15. Verify success message 'Your order has been placed successfully!'
    success_message = page.get_by_text("Congratulations! Your order")
    expect(success_message).to_be_visible()


    # 16. Click 'Delete Account' button
    delete_acc_link = page.get_by_role("link", name=" Delete Account") # lokátor na link 'Delete Account' v záhlaví stránky
    delete_acc_link.click()                                             # kliknutí na link


    # 17. Verify 'ACCOUNT DELETED!' and click 'Continue' button
    account_deleted_message = page.get_by_text("Account Deleted!")           # vyhledání hlášky 'Account Deleted'
    expect(account_deleted_message).to_be_visible # ověření s automatizovaným čekáním, že se na stránce objevil cílený text

    continue_after_delete_btn = page.get_by_role("link", name="Continue")    # vyhledání linku 'Continue'
    continue_after_delete_btn.click()                                        # kliknutí na link





