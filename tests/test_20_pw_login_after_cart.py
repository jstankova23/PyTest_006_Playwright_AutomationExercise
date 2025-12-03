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

# 20_TEST CASE: Search Products and Verify Cart After Login
# TEST VYHLEDÁNÍ PRODUKTŮ PODLE KLÍČOVÉHO SLOVA, VLOŽENÍ VŠECH NALEZENÝCH PRODUKTŮ DO KOŠÍKU, SROVNÁNÍ POČTU PRODUKTŮ V KOŠÍKU A PO VYHLEDÁVÁNÍ, LOGIN UŽIVATELE 'Test_20 User'
# A ZÁVĚREČNÉ SROVNÁNÍ POČTU PRODUKTŮ V KOŠÍKU PROTI POČTU PŮVODNĚ NALEZENÝCH PRODUKTŮ
# Test využívá k loginu uživatele 'Test_20 User', kterého pro tento test vytvoří fixture 'test_20_user'.
def test_product_search(page: Page, test_20_user):                  # parametrem je fixture pro vytvoření uživatele 'Test_20 User' pro tento test pro krok 10
    # 1. Launch browser; 
    # 2. Navigate to home url;
    assert page.url == "https://automationexercise.com/"            # ověření, že fixture 'page' otevřela správnou url
    

    # 3. Click on 'Products' button
    products_link = page.get_by_role("link", name=" Products")     # vyhledání linku pro 'Products' stránku
    products_link.click()                                           # kliknutí na link 'Products'
    

    # 4. Verify user is navigated to ALL PRODUCTS page successfully (new page)
    all_products_heading = page.get_by_role("heading", name="All Products")   # lokátor pro nadpis 'ALL PRODUCTS' na nové stránce
    expect(all_products_heading).to_be_visible(timeout=5000) # ověření přesměrování na stránku s daným nadpisem a delší zpomalení (problém s heavy load na stránce)


    # 5. Enter product name (jeans) in search input and click search button
    ### test vyhledání všech produktů s klíčovým slovem 'top' zadaným do vyhledavače
    search_field = page.get_by_role("textbox", name="Search Product")
    searched_value = "jeans"              # s proměnnou 'searched_value' se pracuje v kroku 7
    search_field.fill(searched_value)

    search_btn = page.get_by_role("button", name="")
    search_btn.click()

    # 6. Verify 'SEARCHED PRODUCTS' is visible
    ### ověření, že se zobrazí na stránce nadpis 'SEARCHED PRODUCTS'
    all_products_heading = page.get_by_role("heading", name="Searched Products")   # lokátor pro nadpis 'SEARCHED PRODUCTS' na nové stránce
    expect(all_products_heading).to_be_visible(timeout=1000)       # ověření přesměrování na stránku s daným nadpisem a zpomalení

    # 7. Verify all the products related to search are visible
    ### ověření, že se na stránce s nadpisem 'SEARCHED PRODUCTS' zobrazí všechny produkty obsahující klíčové slovo 'jeans' ve svém názvu
    product_names = page.locator("div.product-information h2") # obecný CSS lokátor pro názvy produktů na stránce SEARCHED PRODUCTS
    
    count = product_names.count()                              # získání počtu nalezených produktů, lokátor.count()
    for i in range(count):                                     # iterace, projít každý nalezený produkt (1. produkt i = 0)
        result_product_name = product_names.nth(i).text_content().strip().lower() # indexovaný lokátor vrátí každý název produktu samostatně; ořez mezer, převod na malá písmena

        # ověření, že vrácený název produktu obsahuje hledané slovo 'jeans' uložené v proměnné 'searched_value';
        # proměnná 'searched_value' byla definovaná v kroku 5 při zadávání kritéria pro vyhledávání
        assert searched_value in result_product_name, f"Produkt '{result_product_name}' neobsahuje hledané slovo '{searched_value}'." # ověření, že název obsahuje hledané slovo 'top'

    
    # 8. Add those products to cart
    ### Seznam nalezených produktů je reprezentován gridem / mřížkou karet produktů
    ### Každý produkt = jedna karta v gridu
    ### Všechny karty mají stejnou třídu <div class="product-image-wrapper">...</div>
    features_container = page.locator("div.features_items")                      # lokátor pro kontejner/sekci features items položek v horní části home page
    features_products = features_container.locator(".product-image-wrapper")     # vnořený lokátor, kolekce všech karet produktů v kontejneru/sekci features items položek
    products_count = features_products.count()                   # zjištění počtu nalezených karet, nutné pro kontrolu počtu produktů v košíku v krocích 9b) a 12

    ### Smyčka pro přidání všech nalezených produktů do košíku
    for i in range(products_count):
        product_card = features_products.nth(i)

        # a) Scroll + hover nad konkrétní kartou produktu (hover je nutný, zobrazí se overlay vrstva s tlačítkem 'Add to Cart')
        ### SCROLL: Pokud je karta produktu mimo viditelnou část stránky, Playwright ji posune do zorného pole, overlay se často aktivuje jen na viditelné kartě
        ### HOVER: Simulace najetí myší na kartu produktu, tím se zobrazí overlay vrstva (.product-overlay) a v ní tlačítko 'Add to cart'
        product_card.scroll_into_view_if_needed() 
        product_card.hover()

        # b) Overlay vrstva: Kliknutí na tlačítko 'Add to Cart'
        add_to_cart_btn = product_card.locator(".overlay-content .btn") # vnořený lokátor pro tlačítko 'Add to Cart' v kartě produktu
        add_to_cart_btn.wait_for(state="visible")                       # vyčkání na zobrazení tlačítka v overlay vrstvě
        add_to_cart_btn.click(force=True)                               # vynucený klik (kvůli překrývání)

        # c) Modální okénko: Kliknutí na 'Continue Shopping' a zavření modalu
        ### Po předchozím kliknutí na tlačítko 'Add to Cart' se objeví modal s tlačítkem 'Continue Shopping' nebo s linkem 'View Cart'
        continue_shop_btn = page.get_by_role("button", name="Continue Shopping")       # lokátor pro tlačítko 'Continue Shopping' v modalu
        continue_shop_btn.wait_for(state="visible")                                    # vyčkání na zobrazení modalového okénka s požadovaným tlačítkem
        continue_shop_btn.click()                                                      # kliknutí na tlačítko
        page.wait_for_selector("button:has-text('Continue Shopping')", state="hidden") # čekání na zavření modalu před dalším krokem / dalším produktem



    # 9. Click 'Cart' button and verify that products are visible in cart
    ### a) Přechod do nákupního košíku přes link 'Cart' v záhlaví stránky
    cart_link = page.get_by_role("link", name=" Cart")                  # lokátor pro link Cart v záhlaví domovské stránky
    cart_link.click()

    ### b) Ověření, že počet produktů v košíku (před loginem) se rovná počtu vyhledaných produktů z kroku 8
    ### tag <tr> = table row, v tomto případě pro řádky v nákupním košíku
    cart_rows = page.locator("tr[id^='product-']") # vyhledání všech řádků produktů (<tr>) v nákupním košíku, jejichž ID atribut začíná řetězcem 'product-'
    expect(cart_rows).to_have_count(products_count) # počet řádků v košíku s daným ID atributu musí odpovídat počtu nalezených produktů se slovem 'jeans' zjištěnému v kroku 8


    # 10. Click 'Signup / Login' button and submit login details
    ### a) Kliknutí na link 'Signup / Login' v záhlaví domovské stránky pro přihlášení uživatele
    login_link = page.get_by_role("link", name=" Signup / Login")   
    login_link.click()

    ### b) Ověření přesměrování na stránku s nadpisem 'Login to your account'
    login_heading = page.get_by_role("heading", name="Login to your account")  
    expect(login_heading).to_be_visible(timeout=2000)  

    ### c) Zadání emailu a hesla uživatele 'Test_20 User', vytvořeného pomocí fixture 'test_20_user' pro tento test
    email = test_20_user["email"]                     
    passwd = test_20_user["password"]                 

    email_input = page.locator("form").filter(has_text="Login").get_by_placeholder("Email Address") 
    password_input = page.get_by_role("textbox", name="Password")                                   

    email_input.fill(email)                    
    password_input.fill(passwd)                 

    ### d) Kliknutí na tlačítko 'Login'
    login_btn = page.get_by_role("button", name="Login")  
    login_btn.click() 

    ### e) Ověření, že se v záhlaví stránky objevil nápis 'Logged in as username' 
    logged_user_info = page.get_by_text(f"Logged in as {test_20_user["name"]}") # vyhledání linku v záhlaví stránky s textem o přihlášeném uživateli
    expect(logged_user_info).to_be_visible()


    # 11. Again, go to Cart page
    cart_link = page.get_by_role("link", name=" Cart")                  # lokátor pro link Cart v záhlaví domovské stránky
    cart_link.click()

    # 12. Verify that those products are visible in cart after login as well
    ### Ověření, že počet produktů v košíku po loginu se rovná počtu vyhledaných produktů z kroku 8
    ### Princip kontroly je stejný jako u kroku 9 b) před loginem
    cart_rows_after_login = page.locator("tr[id^='product-']")
    expect(cart_rows_after_login).to_have_count(products_count)         # proměnná 'product_counts' definovaná v kroku 8



"""
    ### ITERACE JEDNOTLIVÝCH PRVKŮ VE SKUPINĚ - OBECNÉ PRAVIDLO
    count = locator.count()            # počet elementů odpovídajících lokátoru, vrací integer
    for i in range(count):             # for-cyklus procházející všechny elementy podle indexu, generuje indexy od 0 (1. prvek: i = 0)
    result_item = locator.nth(i)       # výsledný element - lokátor na i-tý prvek (umožní pracovat s jedním konkrétním elementem)

"""























