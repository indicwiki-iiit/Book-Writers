#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from writers_genxml import tewiki, writePage


# import deeptranslit
# from deeptranslit import DeepTranslit


# to get writer personal data
def getWriterData(row):
    title = str(str(row['పేరు']))
    writer_data = {
        'name': str(row['పేరు']),
        'late': str(row['కీర్తిశేషులు?']),
        'first_story_date': str(row['తొలికథ తేదీ']),
        'current_status': str(row['ప్రస్తుతం']),
        'birth': str(row['జననం']),
        'birth_place': str(row['పుట్టిన ఊరు']),
        'birth_district': str(row['పుట్టిన జిల్లా']),
        'address': str(row['చిరునామా']),
        'usage_name': str(row['వాడుకనామం']),
        'studies': str(row['చదువు']),  
        'occupation': str(row['వృత్తి']),
        'place_of_work': str(row['ఉద్యోగపు ఊళ్లు']),
        'phone_number': str(row['ఫోన్‌']), 
        'place_of_study': str(row['చదివిన ఊళ్లు']),
        'awards': str(row['పురస్కారాలు']),
        'well_known_writings': str(row['ప్రసిద్ధ రచనలు']),
        'mail_id': str(row['ఈ-మెయిల్‌']),
        'district_of_study': str(row['చదివిన జిల్లా']),
        'death': str(row['మరణం']),
    }
    return writer_data


# to get writer book data	
def getWriterBookData(row):
    title = str(str(row['పేరు']))
    writer_books_data = {
        'name': str(row['పేరు']),
        'book_name': str(row['పుస్తకం']),
        'type_of_book': str(row['రకం']),
        'book_publishing_date': str(row['ప్రచురణ తేది']),
    }
    return writer_books_data


def getWriterBookData(author_name, df):
    sdf = df[df['పేరు'] == author_name]
    sdf = sdf.drop(['పేరు', "Unnamed: 0"], axis=1)
    sdf = sdf.rename(columns={'పేరు': "name", 'పుస్తకం': 'book', 'రకం': 'type','ప్రచురణ తేది': 'publishing_date'})
    return sdf.to_dict('records')


# # to get writer stories data	
# def getWriterStoriesData(row):
# 	title = str(str(row['పేరు']))
# 	writer_stories_data = {
#         'name': str(row['పేరు']), 
#         'story': str(row['కథ']),
#         'paper':str(row['పత్రిక']),
#         'paper_duration':str(row['పత్రిక అవధి']),
#         'publishing_date': str(row['ప్రచురణ తేది']),
#         'volume': str(row['volume']),
# 	}
# 	return writer_stories_data

def getWriterStoriesData(author_name, df):
    sdf = df[df['పేరు'] == author_name]
    sdf = sdf.drop(['పేరు', "Unnamed: 0", "సంపుటి"], axis=1)
    sdf = sdf.rename(columns={'పేరు': "name", 'కథ': 'story', 'పత్రిక': 'paper', 'పత్రిక అవధి': "paper_duration",
                              'ప్రచురణ తేది': 'publishing_date'})
    # writer_stories_data = {
    #       'name': str(row['పేరు']),
    #       'story': str(row['కథ']),
    #       'paper':str(row['పత్రిక']),
    #       'paper_duration':str(row['పత్రిక అవధి']),
    #       'publishing_date': str(row['ప్రచురణ తేది']),
    #       'volume': str(row['volume']),
    # }
    return sdf.to_dict('records')


def main():
    file_loader = FileSystemLoader('')
    env = Environment(loader=file_loader, newline_sequence='\n', keep_trailing_newline=True)
    # doing for male authors
    template = env.get_template('male_template_v3.j2')

    df_writerinfo = pd.read_csv('writers_data_final.csv', encoding='utf-8')
    # print("shape is ", df_writerinfo.shape)
    df_booksinfo = pd.read_csv('books_data_final.csv', encoding='utf-8')
    # print("books shape is", df_booksinfo.shape)
    # df_booksinfo = pd.read_csv('/home/mounika/Desktop/IIITH/Wikipedia/csv_files/books_data_final.csv', encoding='utf-8')
    df_storiesinfo = pd.read_csv('stories_data_final.csv', encoding='utf-8')
    # print("stories shape is", df_storiesinfo.shape)
    # df_storiesinfo = pd.read_csv('/home/mounika/Desktop/IIITH/Wikipedia/csv_files/stories_data_final.csv', encoding='utf-8')

    # fobj = open('asteroids_articles_100.xml', 'w')
    fobj = open('new_writers_articles.xml', 'w', encoding="utf-8")
    fobj.write(tewiki + '\n')

    # writer info
    count = 0
    for index, row in df_writerinfo.iterrows():
        # print("head")
        # print(df.head)
        # print("columns = ", df.columns)
        # print("index = ", index)
        # print("ROW = ",row)
        title = ''
        # print(row['పేరు'], type(row['పేరు']))
        if isinstance(row['పేరు'], str):
            title = row['పేరు']
        else:
            title = str(row['పేరు'])
        # print("title = ", title)
        writers_data = getWriterData(row)
        # print("\n")
        stories_data = getWriterStoriesData(title, df_storiesinfo)
        books_data = getWriterBookData(title, df_booksinfo)
        # print(stories_data)
        writers_data.update({"stories_list": stories_data})
        writers_data.update({"stories_count": len(stories_data)})
        writers_data.update({"books_list": books_data})
        writers_data.update({"books_count": len(books_data)})
        # print(writers_data)
        text = template.render(writers_data)
        #     # print(text)
        writePage(title, text, fobj)
        #     print('\n', index, title)
        count += 1
        if count%100 == 0:
            print("count = ", count)
        # if count == 3:
        #     break

    # fobj.write('</mediawiki>')
    # fobj.close()


if __name__ == '__main__':
    main()

# {{ booksTable( items) }}
# {{ StoriesTable(items) }}
# | పేరు = {{name}}
# | వాడుకనామం = {{usage_name}}
# | ప్రస్తుతం = {{current_status}}
# | జననం = {{birth}}
# | కీర్తిశేషులు? = {{late}}
# | మరణం  = {{death}}
# | తొలికథ తేదీ  = {{first_story_date}}
# | పుట్టిన ఊరు	= {{birth_place	}}
# | పుట్టిన జిల్లా	              = {{birth_district	}}
# | చదువు            = {{studies}}
# | చదివిన జిల్లా        = {{district_of_study}}
# | చదివిన ఊళ్లు   = {{place_of_study}}
# | వృత్తి	       = {{occupation	}}
# | ఉద్యోగపు ఊళ్లు         = {{place_of_work}}
# | పురస్కారాలు        = {{awards}}
# | ప్రసిద్ధ రచనలు       = {{ well_known_writings }}
# | చిరునామా        = {{address}}
# | ఫోన్‌	      = {{phone_number	}}
# |ఈ-మెయిల్‌  = {{ mail_id }}

        # | other_names = {{usage_name}}
        # | birth_place = {{birth_place}}
        # | death_date  = {{death}}
        # | birth_date  = {{birth}}
        # | education   = {{studies}}
        # | occupation  = {{occupation}}
        # | awards      = {{awards}}
        # | notable_works  = {{well_known_writings}}

# <table  class = "wikitable" >
# <tr>
#     <th>Story</th>
#     <th>Paper</th>
#     <th>Paper Duration</th>
#     <th>Publishing Data</th>
# </tr>
# {% for item in items %}
# <TR>
#    <TD class="c1">{{item.story}}</TD>
#    <TD class="c2">{{item.paper}}</TD>
#    <TD class="c3">{{item.paper_duration}}</TD>
#    <TD class="c4">{{item.publishing_date}}</TD>
# </TR>
# {% endfor %}
# </table>
