**1. Purpose **

The purpose of the code is tracking of news appearing on selected websites. These are mainly government websites and websites of agencies responsible for the implementation of European funds in Poland. Most of them do not support accessible channels for tracking news appearing on them (e.g. RSS feeds). After starting the Django server, it retrieves the content of the websites, downloads news from them and presents them in a readable way.

![2023-12-15 (1)](https://github.com/michalpiaszczyk/Sample-news-scrapper-with-beautifulsoap-and-django/assets/112171020/422c058b-e8cd-45fd-9a09-7441cb1dd73d)

![2023-12-15 (2)](https://github.com/michalpiaszczyk/Sample-news-scrapper-with-beautifulsoap-and-django/assets/112171020/96bc1865-bd2e-4ee2-b619-0b29ce8dec08)

![2023-12-15 (3)](https://github.com/michalpiaszczyk/Sample-news-scrapper-with-beautifulsoap-and-django/assets/112171020/0e2b490c-b2a0-49fa-acea-cd3006dcd54f)

You can send chosen news via email

**2. Usage**

To use thise template you need to create django project on your own and use included files.

1. To use About tab you can make "pliki" folder in application folder in your Django project. App will display content of docx and txt file
2. "templates" is folder with .html files for the project. Use it in applicationn folder
3. "config.ini" stores last update date /app folder/
4. "constants.py" is used in filters /app folder/
5. forms.py is used for filters /app folder/



