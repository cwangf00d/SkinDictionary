# Skin Dictionary

Welcome to Skin Dictionary! This website and web application works to take user input on a select number of skin conditions and provide product recommendations at varying price levels using a SQL database as well as provide a mechanism for users to compare various skin products.

Much of the initial scraping and cleaning of data was done in a Python notebook, which can be found attached in the .ipynb file.

## Getting Started
### Pre-requisites
This web app was made with Python, Jinja, Flask, HTML, CSS, JavaScript for use on computer and mobile.

### Accessing
Access the completed web application at:

### Installing
1. Upload the files downloaded from Gradescope in the CS50 IDE or your preferred development environment or clone this github repository at https://github.com/cwangf00d/SkinDictionary.
2. Use the command line and enter the main directory of the root folder of the project, "cd skindictionary".
3. Use "flask run" to view a local version of the file.

## The Directory
### Data directory
- **chem_full.csv**: Scraped from Byrdie's "Skincare Ingredients A-Z" guide using Beautiful Soup. It contains information about 101 chemicals commonly found in skincare products along with information about its functions and compatibility with other chemicals.
- **chem_to_prod.csv**: Created with Numpy and Pandas packages. A compiled table linking 101 chemicals to the 55 products from The Ordinary that the chemicals are found in.
- **chem_to_sephora_prod.csv**: Created with Numpy and Pandas packages. A compiled table linking 101 chemicals to 300 products from Sephora's best-selling skincare products that the chemicals are found in.
- **prod_ordinary_full.csv**: Scraped from Deciem's online store for The Ordinary using Beautiful Soup. It contains information about 55 products from The Ordinary's catalogue including their name, url, ingredients, and price.
- **prod_sephora_full.csv**: Scraped from Sephora's online store for bestselling skincare products using Beautiful Soup. It contains information about 300 of Sephora's best-selling skincare products, including their name, brand, popularity (loves), url, price, and ingredients.
- **SkinDict.ipynb**: Python notebook, created from Google Colab, used Numpy, Pandas, Beautiful Soup, Re, Requests, JSON, etc. Contains very detailed documentation and run-through of how all of the other tables in this directory were created.
- **SkinDict.py**: Python file version of SkinDict.ipynb.
- **symp_to_chem_names.csv**: Created with Numpy and Pandas packages. A compiled table linking 13 common skin conditions/symptoms/needs with the 101 chemicals associated with treating said conditions.
  - list of symptoms used: 
      - uneven skin tone
      - redness
      - dullness
      - dryness
      - acne
      - exfoliator/cleanser
      - aging
      - itchiness
      - general discomfort
      - sun damage
      - wound
      - oiliness
      - rough 
  
### Static directory
- **favicon.ico**: I created the favicon using Adobe Illustrator, Figma, Favicon.io and icons from Icons8.
- **logo.png**: I created the logo from a frame vector from Freepik, Adobe Illustrator and Figma.
- **styles.css**: Main styling document for website, I created a high-fidelity mock-up of website, including design guide and page layouts, which can be found in this Figma file: https://www.figma.com/file/EhC7RGB9d2B37BCWMmGgVC/Skin-Dictionary?node-id=2%3A3.

### Templates directory
This directory contains the HTML templates used to set up the framework of the pages of the website.
- **apology.html**: Display page for whatever error the user may run into.
- **compare.html**: Form to allow submission of up to four skincare products from catalog of 300 Sephora products to compare.
- **comparison.html**: Display page of cards representing the skincare products the user chose to compare, provides information about the name, brand, popularity, price, and ingredients for each product.
- **index.html**: Landing page, links users to other pages and log in.
- **layout.html**: Base HTML for use as a block for rest of website.
- **login.html**: Log in page for user authentication.
- **recs.html**: Display page of table featuring skincare product recommendations for users based on specific request.
- **register.html**: Registration page for new users.
- **request.html**: Form to allow submission of specific skincare treatment recommendation request.

### Root directory
- **.~c9_invoke_E9InGo.py**: Do not edit. Taken from CS50 Finance application.
- **application.py**: Main file with routes to all pages that can be found in the web application.
- **data_backend.py**: Setup for SQL database to be used in the web application. Contains all necessary commands to extract information from csvs provided in the "/data" directory.
- **helpers.py**: Helper python file with methods used in application.py such as the apology function, user recognition, and Jinja currency formatting. 
- **requirements.txt**: Text file with program needs.
- **skindict.db**: SQLite database containing multiple tables from which the main functionality of the app draws from.
- **TODO**: MAKE changes to skindict removing things I don't use.

### Other resources
- **DESIGN.md**: Contains detailed information about each of the functions and the overall setup of the entire application!

## Using the Website
### Registering
Upon opening the website for the first time, the user will see a landing page. There are two ways to navigate to registration.
1. The user can click on the highlighted box around "awaits" in "beautiful skin awaits" at the bottom of the landing page. Clicking on this box will take the user to the log in page, where they can find a redirect link to the registration page if they are a new user.
2. The user can click on "REGISTER" in the navigation bar located to the top right of the webpage.

To officially register, the user must input their name, age, gender, skin type (if known), username, password, and confirm their password (the inputs must match).
On clicking "Sign up", the user will be redirected to the log in page, where they can then log in with their username and password they just created.

### Logging In
Upon opening the website, the user can log in via two different methods.
1. The user can click on the highlighted box around "awaits" in "beautiful skin awaits" at the bottom of the landing page to be taken to the login screen.
2. The user can click on "LOGIN" in the navigation bar located on the top right of the website.

To log in, the user can use the username and password they created or my sample login (username: cwang; password: hihi).
Upon clicking "log in" and submitting, the user will be redirected to the landing page.

### Making a Request
To make a request, the user must be logged in. Follow the instructions under registering (if a new user) and logging in (if an existing user or using sample user authentication information).

To navigate to the request page, the user must click on "REQUEST" in the navigation bar to the top right or navigate to "/request" in the URL bar.
Then, the user can select by clicking on the checkbox by whichever skin condition/need they wish to get a recommendation for and then pressing "Request".

Upon submitting their request, users will be shown a table displaying their recommendations specific to their requests. This table contains information about the product name as a hyperlink connecting it to the Sephora page where the product can be purchased, brand, price, price range category, and popularity (loves). 
For each symptom selected from the form, 6 products will be recommended, two from each price range. Thus, if the user were to select "dullness" and "dryness" they would receive up to 12 distinct product recommendations.

### Comparing Products
Users can also compare up to four skincare products from Sephora's top 300 best-selling skincare products.
[NOTE] Users do **not** have to be logged in to access this feature.
From the navigation bar on the top right of the webpage, users can use this feature by clicking on "COMPARE", this will redirect the user to a form.

In the form, users can enter a number, 1-4, of how many products they would like to compare. Then, in the four dropdown select options below, they can select whichever product(s) they want to compare. The products are organized in lexicographical order. If the user wishes to compare less than four products, they can just leave the unused dropdown options unselected.
To submit their comparison request, the user can press "Compare". A number and products to compare must be provided. A known "error" is that the webapp will not check to see if the number you picked matches the number of products selected in the dropdowns. This is to be more flexible in case the user suddenly decides to compare more than what they had indicated.
If the user accidentally selects the same treatment in multiple dropdowns, only one version of that product will be displayed in the resulting page.

Upon submission of the compare request, users will be provided a display of cards representing each of the products. Each card contains information about the name of the product, the brand, price, popularity, and chemicals from the 101 commonly used skincare ingredients list from Byrdie's skincare guide.

### Logging Out
To log out of the website, the user can click on "LOGOUT" on the navigation bar in the top right.

## Screenshots
Screenshots of the webapp's UI are below. To see a high-fidelity mockup of the website, including the fonts, colors, components, logo, favicon, and overall page layout, visit the [Figma](https://www.figma.com/file/EhC7RGB9d2B37BCWMmGgVC/Skin-Dictionary?node-id=2%3A3) file I created. 
For more information on how the website was put together, visit the DESIGN.md file in the Implementation directory.

## Built With
- Google Colab
- CS50 IDE
- Figma

## References
- [Byrdie Skincare Ingredients A-Z](https://www.byrdie.com/skincare-ingredients-glossary-4800556)
- [Sephora Skincare Catalog](https://www.sephora.com/shop/skin-care-gift-sets?icid2=homepage_slideshow_multi-world_slotting_hotholidaygifts_cyoa_01_skincare_us_desktop_hotspot_120620)

