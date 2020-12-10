# Design of Skin Dictionary
## How it Came Together
### Inspiration
I decided to create Skin Dictionary because I've always been fascinated by skincare.
There just seems to be an abundance of products, videos, information about everything skincare. 
Yet, the sheer flood of skincare information is actually often overwhelming, confusing, and contradictory. 
I wanted to create a website that serves as the centralized hub of information for all-things skincare.

I've always planned for this website to be a personal project extending beyond CS50 with three main aims:
1. provide information about skin physiology and recent peer-reviewed publications as well as a general-public-friendly, dynamic and exciting "web encyclopedia" on skincare ingredients and conditions.
2. give recommendations to users on the best skin products for their needs
3. serve as a platform for advocacy and information about under-represented groups in skincare.

Within the time constraint of the CS50 Final Project, however, I had to narrow the scope of my project. At the start of my project, I decided that I wanted to focus on my second aim, the treatment recommendation aspect of my website.
Thus, my goal for myself was to create a small version of my website that allows users to get product recommendations tailored to their specific needs and compare products. While there is certainly a lot more that I wish to accomplish with this project, I feel satisfied with the project I have submitted and pushed to Github!

### Back-End
#### Initial Databasing
To begin my project, I needed to have a database from which I could draw suggestions and store all of the information about the various chemicals, products, and symptoms. Using Beautiful Soup, pandas, json, numpy, I scraped information off of Byrdie's A-Z skincare ingredients guide, The Ordinary's catalog on Deciem, and Sephora's catalog from their top 300 best-selling skincare products. I go into great detail about all of my scraping, cleaning and organizing in a python notebook, the SkinDict.ipynb file, which can also be accessed [here](https://colab.research.google.com/drive/1E0CO3DDPxRRiRb2kJ5u-mlCvj6tmMRBN?usp=sharing).

It took a significantly longer time than I had anticipated to gather and clean all of the data so that it would be in format I had wanted. There were many cool features and sources of information I wanted to incorporate but inconsistency in design of websites and pages even within the same catalog made it incredibly difficult to do so. For example, I was really interested in scraping all of the user review data from various websites selling the same products to use NLP to detect the tonality and identify keywords of what functions are associated with each given product or chemical. However, many of the reviews were inaccessible through Beautiful Soup, and only accessible, perhaps, with Selenium. Unfortunately, I was unable to install Selenium and get it to work properly in my Jupyter Notebook. Or, when I wanted to scrape information from Sephora about the compatability of each product with different skin types, I was unable to consistently scrape and separate that information from the 300 product pages because of the lack of a distinct class name for that section of text (it was just text separated with unlabeled html breaks randomly interspersed).

The resulting database structure was as such:
- Main tables:
  - symptoms: **symptoms**
    - containing *symp_name*, *symp_id*
  - chemicals: **chemicals**
    - containing *chem_name*, *chem_id*
  - products: **products**
    - containing: *prod_name*, *prod_brand*, *prod_link*, *prod_price*, *prod_loves*, *prod_price*, *prod_id*
  - users: **users**
    - containing: *user_id*, *username*, *user_name*, *hash*, *user_skintype*, *user_age*, *user_gender*
- Linking tables:
  - symptoms to chemicals: **symp_to_chem**
    - containing *symp_id*, *chem_id*
  - chemicals to products: **chem_to_prod**
    - containing *chem_id*, *prod_id*
  - user requests: **user_requests**
    - containing *req_id*, *user_id*, *symp_id*, *date*
 
 The general flow is that a user makes a request by checking off a number of symptoms, and the symptoms selected and the corresponding user information get logged in **user_requests**. Then, the symptoms get identifed from the *symp_name* to *symp_id*, and then sent to the **symp_to_chem** table where the *chem_id*'s corresponding to the requested *symp_id*'s are collected. Then, the *chem_id*'s are sent to **chem_to_prod**, where the corresponding *prod_id*'s are selected, from which all of the information about the products can be synthesized.

I originally wanted to have the computer discover on its own which chemicals were best-suited to treating what symptoms and making it more specific to the user's particular skin type and the compatabilities of the various chemicals with each other, but due to time constraints and limited experience with neural nets, I ultimately decided to construct my own rules to connect chemicals to symptoms based on what I was able to scrape.

To "automate" the construction of the databases, I created a file, **data_backend.py**, which sets up the entire **skindict.db** database from the csv files of the data.

#### The Flask App
Before the CS50 final project really began, I had intended to review and use full-stack React to develop this webapp or a combination of a Flask backend and React front-end. Unfortunately, due to unforeseen time constraints, I ended up adapting and restructuring the CS50 Finance web application for my final project.

Let us go through the pages and the design choices and considerations that went into each of the eventual layouts/functions:
- **Landing ("~/")**:
  - I wanted my landing page to be engaging and simple, so I didn't really add much functionality to it, besides just having the navigation bar at the top and an option to go to request skincare product recommendations at the bottom-center area of the page.
- **Login/Logout ("~/login")**:
  - Logging in and out was also quite standard. I used similar features as those in CS50 Finance. The one difference is that my login page also included a link to the register page in case users wanted to register as a new user.
- **Register ("~/register")**:
  - In the registration process, I asked for a few extra inputs beyond just username and password because I had intended to use those metrics to help further tailor the recommendations to the particular user. However, due to trouble actually scraping for which skin types various products were compatible with, I ended up not really using or storing that information in my databases.
- **Request ("~/request")**:
  - This page was really the heart of my project. In the request page, I created a small checkbox form for users to select which symptoms they wanted product recommendations for. From what got submitted to the form, my function would then go through the databases in the flow described previously to extract up to two products per price category (there were three price categories: $0 - $15, $15 - $35, $35 and up) per symptom selected ordered by popularity. I had thought about using a text input and natural language processing to filter out extra filler words and identify keywords to then query my database for, but I quickly realized that that approach may not be as efficacious as literally providing options for users to choose from. 
    - I noticed that several websites, including Sephora, had options where you could take a "skincare quiz" and get recommendations for skincare routines. However, these alternatives would often only let people choose one symptom/area of concern to focus on. I wanted to let people choose all of the skin concerns they wanted treatments for. Additionally, most of these were only based on what the products were marketed towards, while my query would look for chemicals known for treating those areas of concern and then recommending products containing those chemicals in their active ingredient lists.
  - Instead of redirecting to another page and storing the user's requests and recommendations in a database, I decided to render a different template with a table containing all of the products. My reasoning for doing so is that I didn't believe that users would really feel a need to save their recommendations when they could enter the same query again and get similar/the same results.
    - One area I would definitely like to improve in the future is to make the table more dynamic, perhaps when I finally move this over to React, and allow the table to refresh according to more user specifications, like what price ranges and how many products to show, and whether or not to order by popularity of product or some other factor.
- **Compare ("~/compare")**:
  - I decided to add a compare function after realizing that my website was quite one-dimensional.
  - In this page, I basically let users choose up to four products that they want to compare side-by-side and then display a page with information about the product's brand, name, popularity, and key ingredients (basically the chemicals from my 101 chemical table) that were found as ingredients for this product. This page only really required usage of the same tables and databases I had already created.

### Front-End
#### Design Process
I spent a rather significant amount of time thinking about how I wanted the website to look and be structured. To help with the thinking process, I eventually created a mock-up in Figma of a design system and overall page layout with quite a few of the pages in high-fidelity form. The mock-up, including the favicon and logo I designed (with aid from Icons8, freepik, and Adobe Illustrator), can be found [here](https://www.figma.com/file/EhC7RGB9d2B37BCWMmGgVC/Skin-Dictionary?node-id=2%3A3).

I ended up creating an entire design system, complete with fonts, headings, primary colors, text colors, a component, logo, and favicon. I also built out most of the pages on Figma and used the Inspect property in Figma to help with the eventual CSS formatting.

#### Implementation
Implementing the design was rather straightforward for the most part. There were two main limitations that I haven't yet been able to figure out.
1. This typing animation that worked well when I was designing a homepage website for myself just would not work properly in this Flask application. I'm not sure if it was something wrong with the way I embedded the source code into **layout.html** and then tried to use as a block in my **index.html**, but it was not rendering as I had intended.
2. Framing was not as responsive as it should have been. Thus, the website is best used with iPad, iPad Pro, or larger displays like laptops and desktops as opposed to phones. I figure that if I were to alter the declarations of the fonts to make them more scalable, perhaps that could help with how the text would often overflow the containers in smaller, narrower displays. 

### Contact
If you have any further questions, concerns, suggestions, please reach out! You can contact me at cindywang@college.harvard.edu or by phone/Zoom at 845-743-6807. Any help is much appreciated :)

## Built With
- Google Colab (Jupyter Notebooks)
  - various python packages including but not limited to: Beautiful Soup, json, pandas, numpy, re, requests, csv
- CS50 IDE
- VS Code
- Figma
- Adobe Illustrator
- Bootstrap

## References + Resources
- [Byrdie's Skincare Ingredients A-Z](https://www.byrdie.com/skincare-ingredients-glossary-4800556)
- [The Ordinary's Catalog](https://theordinary.deciem.com/)
- [Sephora's Best-Selling Skincare Catalog](https://www.sephora.com/shop/skin-care-solutions?pageSize=300)
- [HODP's Guide to Web Scraping](https://docs.hodp.org/docs/scraping)
- [W3 Schools](https://www.w3schools.com/)
- [GoTrained Python Tutorials](https://python.gotrained.com/beautifulsoup-extracting-urls/)
- [Python Spot](https://pythonspot.com/extract-links-from-webpage-beautifulsoup/)
- [Kite](https://www.kite.com/python/examples/1730/beautifulsoup-find-the-next-sibling-of-a-tag)
- [Crummy](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-the-tree)
- [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html)
- [Link Gopher](https://sites.google.com/site/linkgopher/)
