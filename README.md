# Amazon_Scraping_with_BeautifulSoup
Scraping Amazon products data in 'csv' files using BeautifulSoup.

----------------------------------------------------------------------------------------------------------------------

After executing 'main.py' file:-

1) Firstly, It generates a 'product_list.csv' file inside 'Product_List' directory.
   
   This file contains [product_url, product_name, product_price, product_rating, product_reviews] in order in each row for a product.

2) Secondly, It generates a 'products.csv' file inside 'Information_of_Products' directory.
   
   For each 'product_url' in 'product_list.csv', it generates a row with fields [product_title, product_ASIN, product_Manufacturer, product_desc].

----------------------------------------------------------------------------------------------------------------------
