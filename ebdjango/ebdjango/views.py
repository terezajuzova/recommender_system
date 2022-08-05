from django.http import HttpResponse
from django.template import loader

from .models import books, book_ratings
from django.shortcuts import render,get_object_or_404
from django.db.models import Q

import pandas as pd
import json


def book_list(request):
  template = loader.get_template('book_list.html')
  return HttpResponse(template.render())


# Define function to search book

def search(request):

    results = []

    if request.method == "GET":

        search_input = request.GET.get('search')

        if search_input == '':
            search_input = 'None'

        books_list = books.objects.values('book_title', 'book_isbn')
        ratings = book_ratings.objects.values('user_id', 'book_isbn', 'book_rating')
        recommended_books = get_recommended_books(books_list, ratings, search_input)

    return render(request, 'search.html', {'search_input': search_input, 'results': recommended_books})


def get_recommended_books(books_list, ratings, search_input):

    list_of_books = list(books_list)
    list_of_ratings = list(ratings)

    df_books = pd.DataFrame(list_of_books)
    df_ratings = pd.DataFrame(list_of_ratings)


    # Merge ratings and books datasets
    df = pd.merge(df_ratings, df_books, on='book_isbn', how='inner')

    # Aggregate by book
    agg_ratings = df.groupby('book_title')['book_rating'].agg([('mean_rating','mean'), ('number_of_ratings','count')]).reset_index()

    # Keep the books with over 100 ratings
    agg_ratings_100 = agg_ratings[agg_ratings['number_of_ratings'] > 100]
    df_100 = pd.merge(df, agg_ratings_100[['book_title']], on='book_title', how='inner')

    # Create user-item matrix
    matrix = df_100.pivot_table(index='user_id', columns='book_title', values='book_rating')

    # Now one book is chosen
    books_ratings = matrix[search_input]

    # Correlations between the others books
    similar_books_ratings = matrix.corrwith(books_ratings)

    correlation = pd.DataFrame(similar_books_ratings, columns=['Correlation'])
    correlation.dropna(inplace=True)

    # Result dataframe
    result_dataframe = correlation.sort_values('Correlation', ascending=False).head(10)
    result_json = result_dataframe.reset_index().to_json(orient='records')

    return json.loads(result_json)

