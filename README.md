# Book-Writers
The repository "Book-Writers" contains all the information related to "https://kathanilayam.com/". Using the data from the website, we automatically created the writer's wiki pages.

Data files: 
1) books_data_final: list of books for each writer/author
2) stories_data_final: list of stories for each writer/author
3) writers_data_final: personal data about the writer

Data is read from all three files to write a template for each writer. 

male_template_v3: jinja template for the wiki article

The XML file is large and unable to upload the file. If anyone wants the file, they can download it from the below link:
[writers_articles.xml](https://iiitaphyd-my.sharepoint.com/:u:/g/personal/mounika_marreddy_research_iiit_ac_in/Ec0gkgJM3_5Nt6REltRFmdkBGipr0ZBZa0irpvb20ksoJA?e=9KX8AW) 

new_writers_render_v2.py file is used to merge the three data files and generate the XML file.


Future Scope:
If the content is increased in the "kathanilayam" website, scrape the three data files from the website.
Then no need to change the remaining files, pass the three files to the "new_writers_render_v2.py" file, and an XML file will be created.
