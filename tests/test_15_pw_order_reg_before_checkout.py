# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures 'page', 'browser_context', 'accept_gdpr' definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect
import uuid                                             # kvůli generování emailu v kroku 9

# 15: Place Order: Register before Checkout
# TEST: OOBJEDNÁVKA 6. A 7. PRODUKTU S REGISTRACÍ UŽIVATELE 'Test_15 User' PŘED VYSTAVENÍM OBJEDNÁVKY, PLATBA A SMAZÁNÍ UŽIVATELE
def test_order_reg_before_checkout(page: Page):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    # 3. Verify that home page is visible successfully
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url
    

    # 4. Click 'Signup / Login' button
    login_link = page.get_by_role("link", name=" Signup / Login")   # vyhledání linku v záhlaví domovské stránky pro přihlášení uživatele
    login_link.click()


    # 5. Fill all details in Signup and create account
    ### Kompletní registrace uživatele 'Test_15 User' určeného pouze pro tento test
    ### Ukládání některých hodnot do proměnných, využijí se v kroku 12 při ověřování adres
    ### a) Ověření přesměrování na stránku s nadpisem 'New User Signup!'
    new_user_heading = page.get_by_role("heading", name="New User Signup!")   # lokátor pro nadpis 'New User Signup!' na nové stránce
    expect(new_user_heading).to_be_visible(timeout=2000)  # ověření s automatizovaným čekáním, že se na stránce objevil cílený nadpis

    ### b) Vytvoření hlavičky uživatele (jméno, email)
    name = "Test_15 User" 
    email = f"test_15_user_{uuid.uuid4().hex[:8]}@example.com" # dynamické vygenerování unikátního emailu

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

    ### e) Vyplnění povinných údajů
    title = page.locator("#id_gender1")                      # gender1 = Mr. / pán
    title.check()                                    

    pswd = "TestPassword123"                                    
    pswd_input = page.get_by_role("textbox", name="Password *") 
    pswd_input.fill(pswd)                                       

    ###### Datum narození: 31. prosince 1974
    page.select_option("#days", "31")        
    page.select_option("#months", "December")      
    page.select_option("#years", "1974")     

    ###### Uložení hodnot do proměnných - dotahují se všechny do adres
    first_name = "Test_15"                  
    last_name = "User"                    
    company = "AutoTest"                    
    address1 = "815 Vine Street"
    address2 = "Apt. 21"
    state = "Ohio"
    city = "Cincinnati"
    zip_code = "45202"
    mobile_num = "+15135550147"
         
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

    ###### Výběr z roletového menu v poli Country - dotahuje se do adres
    country_dropdown = page.get_by_label("Country *")   # lokátor pole Country s roletovým menu
    country_dropdown.select_option("United States")     # výběr konkrétní hodnoty z roletového menu

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
    ### Přidání produktu č. 6 a 7 do nákupního košíku.
    ### Seznam produktů je na stránce reprezentovaný gridem / mřížkou karet produktů;
    ### každý produkt = jedna karta (v gridu / mřížce)
    ### všechny karty mají stejnou třídu <div class="product-image-wrapper">...</div>
    ### 6. karta / produkt: .product-image-wrapper.nth(5)
    ### 7. karta / produkt: .product-image-wrapper.nth(6)

    ### 6. PRODUKT
    ###### a) Vyhledání 6. produktu          
    products = page.locator(".product-image-wrapper")   # CSS lokátor pro seznam všech karet v gridu / mřížce, tzn. karty všech produktů na stránce
    product_6 = products.nth(5)                         # proměnná pro určení pozice karty 6. produktu v mřížce
    product_6.hover()
    
    ###### b) Kliknutí na tlačítko 'Add to Cart'
    add_to_cart_prod6_btn = page. locator(".overlay-content > .btn").nth(5)  # lokátor pro tlačítko 'Add to cart' u 6. produktu s krycí vrstvou
    add_to_cart_prod6_btn.click()                                            # kliknutí na 'Add to cart', tzn. přidání 6. produktu do košíku

    ###### c) Kliknutí na tlačítko 'Continue Shopping'
    continue_shop_btn = page.get_by_role("button", name="Continue Shopping") # lokátor tlačítka 'Continue Shopping'
    continue_shop_btn.click()                                                # kliknutí na tlačítko


    ### 7. PRODUKT
    ###### a) Vyhledání 4. produktu
    product_7 = products.nth(6)                                              # proměnná pro určení pozice karty 7. produktu v mřížce
    product_7.hover()

    ###### b) Kliknutí na tlačítko 'Add to Cart'
    add_to_cart_prod7_btn = page. locator(".overlay-content > .btn").nth(6)  # lokátor pro tlačítko 'Add to cart' u 7. produktu s krycí vrstvou
    add_to_cart_prod7_btn.click()                                            # kliknutí na 'Add to cart', tzn. přidání 7. produktu do košíku

    ###### c) Kliknutí na tlačítko 'Continue Shopping'
    continue_shop_btn = page.get_by_role("button", name="Continue Shopping") # lokátor tlačítka 'Continue Shopping'
    continue_shop_btn.click() 


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


    # 12. Verify Address Details and Review Your Order

    ### a) Kontrola dodací a fakturační adresy
    ### Ověření přesměrování na stránku s nadpisem "Address Details"
    address_details_heading = page.get_by_role("heading", name="Address Details")
    expect(address_details_heading).to_be_visible()

    ### Bloky adres pro dodání zboží a fakturaci
    delivery_block = page.locator("#address_delivery")
    billing_block = page.locator("#address_invoice")

    ### YOUR DELIVERY ADDRESS – ověření dodací adresy
    ### Ověřují se klíčové hodnoty zadané při registraci (ne formát ani pořadí řádků)
    expect(delivery_block).to_contain_text("Mr. Test_15 User")  # oslovení + celé jméno
    expect(delivery_block).to_contain_text(company)
    expect(delivery_block).to_contain_text(address1)
    expect(delivery_block).to_contain_text(address2)
    expect(delivery_block).to_contain_text(city)
    expect(delivery_block).to_contain_text(state)
    expect(delivery_block).to_contain_text(zip_code)
    expect(delivery_block).to_contain_text("United States")
    expect(delivery_block).to_contain_text(mobile_num)

    ### YOUR BILLING ADDRESS – ověření fakturační adresy
    ### Musí obsahovat stejné údaje jako dodací adresa
    expect(billing_block).to_contain_text("Mr. Test_15 User")
    expect(billing_block).to_contain_text(company)
    expect(billing_block).to_contain_text(address1)
    expect(billing_block).to_contain_text(address2)
    expect(billing_block).to_contain_text(city)
    expect(billing_block).to_contain_text(state)
    expect(billing_block).to_contain_text(zip_code)
    expect(billing_block).to_contain_text("United States")
    expect(billing_block).to_contain_text(mobile_num)


    ### b) Kontrola nákupní objednávky
    ### Ověření přesměrování na stránku s nadpisem "Review Your Order"
    ### review_your_order_heading = page.get_by_role("heading", name="Review Your Order")
    ### expect(review_your_order_heading).to_be_visible()
    review_your_order_heading = page.get_by_role("heading", name="Review Your Order")
    expect(review_your_order_heading).to_be_visible()

    ### Kontrola celé tabulky objednávky (sekce obsahující všechny položky objednávky)
    order_table = page.locator("#cart_info")                   
    expect(order_table).to_be_visible()

    ### Kontrola pouze přítomnosti produktů 6 a 7 v objednávce
    ### (bez kontroly množství a cen z důvodu hromadného spuštění testů)
    ### Identifikace konkrétních produktů je provedena jako VNOŘENÝ LOKÁTOR 
    ### Lokátor řádku produktu je definován UVNITŘ lokátoru celé tabulky objednávky
    product_6_row = order_table.locator("tr#product-6")   # lokátor pro řádek produktu 6 vnořený do lokátoru pro tabulku objednávky
    product_7_row = order_table.locator("tr#product-7")   # lokátor pro řádek produktu 7 vnořený do lokátoru pro tabulku objednávky

    ### Ověření, že jsou oba produkty skutečně přítomny v objednávce
    expect(product_6_row).to_be_visible()
    expect(product_7_row).to_be_visible()


    # 13. Enter description in comment text area and click 'Place Order'
    comment_text_area = page.locator("textarea[name=\"message\"]")  # vložení komentáře do boxu s popisem "If you would like to add a comment ..."
    comment_text_area.fill("Test_14 User - test comment.")

    place_order_link = page.get_by_role("link", name="Place Order")
    place_order_link.click()


    # 14. Enter payment details: Name on Card, Card Number, CVC, Expiration date
    ### Uložení hodnot do proměnných
    name_on_card = "Test_14 User"
    card_number = "1111 2222 3333 4444"
    cvc = "777"
    mm = "03"
    yyyy = "2028"

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
    
    
    # 15. Click 'Pay and Confirm Order' button
    pay_and_confirm_btn = page.get_by_role("button", name="Pay and Confirm Order")
    pay_and_confirm_btn.click()


    # 16. Verify success message 'Your order has been placed successfully!'
    success_message = page.get_by_text("Congratulations! Your order")
    expect(success_message).to_be_visible()


    # 17. Click 'Delete Account' button
    delete_acc_link = page.get_by_role("link", name=" Delete Account") # lokátor na link 'Delete Account' v záhlaví stránky
    delete_acc_link.click()                                             # kliknutí na link


    # 18. Verify 'ACCOUNT DELETED!' and click 'Continue' button
    account_deleted_message = page.get_by_text("Account Deleted!")           # vyhledání hlášky 'Account Deleted'
    expect(account_deleted_message).to_be_visible # ověření s automatizovaným čekáním, že se na stránce objevil cílený text

    continue_after_delete_btn = page.get_by_role("link", name="Continue")    # vyhledání linku 'Continue'
    continue_after_delete_btn.click()                                        # kliknutí na link





