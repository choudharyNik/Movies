from django.http import JsonResponse
from movies.models import Movie, MovieCast, Genre
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def list_or_create_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        overview = request.POST.get('overview')
        tagline = request.POST.get('tagline')
        release_date = request.POST.get('release date')
        vote_average = request.POST.get('average vote')
        vote_count = request.POST.get('vote count')

        movie = Movie.objects.get_or_create(title = title, overview = overview, tagline = tagline,
                                    release_date = release_date, 
                                    vote_average = vote_average, vote_count = vote_count)[0]
        
        genrelist = request.POST.getlist('genre[]')
        genres = []
        for name in genrelist:
            genre = Genre.objects.get_or_create(name = name)[0]
            dic = {'id':genre.id, 'genre':name}
            genres.append(dic)
            movie.genres.add(genre)
            

        #give cast in format -> charactername - castname
        castlist = request.POST.getlist('cast[]')
        movie_id = movie.id
        created_movie_cast = []
        for name in castlist:
            cast_name = name.split(' - ')[0]
            character_name = name.split(' - ')[1]
            MovieCast.objects.get_or_create(cast_name = cast_name, 
                                            character_name = character_name, 
                                            movie_id = movie_id)
            cast = {'character_name': character_name, 'cast_name': cast_name, 'movie_id': movie_id}
            created_movie_cast.append(cast)

        
        created_movie = {'movie_id':movie.id, 'title':title, 'overview':overview, 
                        'tagline':tagline, 'release_date': release_date, 
                        'vote_average': vote_average, 'vote_count': vote_count}
        
                
        return JsonResponse({'data': {**created_movie, 'genres':genres, 'MovieCast': created_movie_cast}})
    elif request.method == 'GET':
        movies = Movie.objects.all()
       
        movies_list = {'title': [], 'overview': [], 
                        'tagline': [], 'release_date': [], 
                        'vote_average': [], 'vote_count': []}
        
        for movie in movies:
            movies_list['title'].append(movie.title)
            movies_list['overview'].append(movie.overview) 
            movies_list['tagline'].append(movie.tagline)
            movies_list['release_date'].append(movie.release_date) 
            movies_list['vote_average'].append(movie.vote_average)
            movies_list['vote_count'].append(movie.vote_count)

        return JsonResponse({'data': {**movies_list}})



@csrf_exempt
def retrieve_update_delete_movie(request, id):
    movie = Movie.objects.get(id = id)
    movie_casts = movie.moviecast_set.all()
    genres = movie.genres.all()
    
    if request.method == "GET":
        
        details = {'title': movie.title, 'overview': movie.overview, 'tagline': movie.tagline,
                'release_date': movie.release_date, 'vote_average': movie.vote_average, 
                'vote_count': movie.vote_count}
        
        casts_list = []
        for cast in movie_casts:
            casts_list.append({'cast_name': cast.cast_name, 'character_name': cast.character_name})

        genreslist = []
        for genre in genres:
            genreslist.append({'genre_name': genre.name})

        return JsonResponse({'data': {**details, 'casts_list': casts_list, 
                                    'genres_list': genreslist}})


    elif request.method == 'PUT':
        body = json.loads(request.body.decode('utf-8'))
        movie = Movie.objects.filter(id=body['id']).update(**body)
        
        return JsonResponse({'data':'Data updated successfully!!'})

    elif request.method == 'DELETE':
        body = json.loads(request.body.decode('utf-8'))
        movie = Movie.objects.filter(id = body['id']).delete()

        return JsonResponse({'data': 'Data deleted successfully!!'})























# def index(request):
#     return render (request, 'DisplayApp/index.html')

# def displaylist(request):
#     csvfile_data = pd.read_csv(r'C:\Users\pjhaj\Desktop\Django_Projects_new\Movies_List\movies.csv')

#     if request.method == "POST":
#         for i in range(len(csvfile_data.index)):
#             row = csvfile_data.loc[i]

#             title = row.title
#             genres = row.genres
#             character_name_and_cast = row.character_name_and_cast
#             overview = row.overview
#             release_date = parse(row.release_date, dayfirst=True)
#             tagline = row.tagline
#             avg_vote = row.vote_average
#             vote_count = row.vote_count

#             movies_instance = Movies(title = title, overview = overview, 
#                                      release_date = release_date, tagline = tagline, 
#                                      vote_avg = avg_vote, vote_count = vote_count)
#             movies_instance.save()
            
#             genreslist = genres.split(', ')
#             for k in range(len(genreslist)):
#                 genre = genreslist[k]
#                 # genres_instance = Genres(genre = genre)
#                 # genres_instance.save()
#                 genres_instance = Genres.objects.get_or_create(genre=genre)[0]
#                 movies_instance.genres.add(genres_instance)


            

#             charactercastlist = character_name_and_cast.split(', ')
#             for j in range(len(charactercastlist)):
#                 furthersplit = charactercastlist[j].split(' - ')
#                 char_name = furthersplit[0]
#                 cast_name = furthersplit[1]
#                 mcast_instance = Mcast(char_name = char_name, cast_name = cast_name, movie= movies_instance)
#                 mcast_instance.save()

            

#         return render (request, 'DisplayApp/index.html')


#     return render (request, 'DisplayApp/savedata.html')

# def moviedetails(request):
#     movie = Movies.objects.all()
#     p = Paginator(movie, 10)
#     page_number = request.GET.get('page')
#     page_obj = p.get_page(page_number)
#     return render (request, 'DisplayApp/displaylist.html', 
#                    {'page_obj':page_obj})

# def details(request, id):
#     movie = Movies.objects.get(id = id)
#     charsndcasts = Mcast.objects.filter(movie_id = id)

#     return render (request, 'DisplayApp/details.html', {'movie':movie,
#                                                         'charsandcasts':charsndcasts})
