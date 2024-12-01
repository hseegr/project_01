import requests
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre, Actor
from django.conf import settings

API_KEY = settings.TMDB_API_KEY
BASE_URL = "https://api.themoviedb.org/3"

def fetch_movies(page=1):
    """Fetch popular movies excluding 19세 관람가."""
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "language": "ko-KR",
        "sort_by": "popularity.desc",  # 인기 순 정렬
        "page": page,
        "certification_country": "KR",  # 한국 기준
        "certification.lte": "18",  # 19세 관람가 제외
    }
    response = requests.get(url, params=params)
    return response.json().get("results", []) if response.status_code == 200 else []

def fetch_movie_credits(movie_id):
    """Fetch credits (cast and crew) for a specific movie."""
    url = f"{BASE_URL}/movie/{movie_id}/credits"
    response = requests.get(url, params={"api_key": API_KEY})
    return response.json() if response.status_code == 200 else None

def fetch_movie_details(movie_id):
    """Fetch detailed information for a specific movie."""
    url = f"{BASE_URL}/movie/{movie_id}"
    response = requests.get(url, params={"api_key": API_KEY, "language": "ko-KR", "append_to_response": "release_dates"})
    if response.status_code == 200:
        details = response.json()
        print(details.get("release_dates"))  # API 응답 디버깅
        return details
    return None

def save_movie(movie_data, credits_data):
    """Save movie details to the database, excluding movies without posters."""
    # 영화 상세 정보 가져오기
    movie_details = fetch_movie_details(movie_data["id"])
    if not movie_details:
        print(f"Skipping movie '{movie_data['title']}' (No detailed info available)")
        return

    # 포스터가 없는 영화 제외
    if not movie_data.get("poster_path"):
        print(f"Skipping movie '{movie_data['title']}' (No poster available)")
        return

    # 연령등급 가져오기
    age_rating = None
    release_dates = movie_details.get("release_dates", {}).get("results", [])
    for country_data in release_dates:
        if country_data["iso_3166_1"] == "KR":  # 한국 기준
            for release_date in country_data.get("release_dates", []):
                age_rating = release_date.get("certification")
                if age_rating:
                    break
        if age_rating:
            break

    # 영화 저장
    movie, created = Movie.objects.get_or_create(
        title=movie_data["title"],
        release_date=movie_data["release_date"],
        runtime=movie_details.get("runtime"),
        overview=movie_data.get("overview"),
        poster_path=movie_data["poster_path"],
        director=next(
            (crew["name"] for crew in credits_data["crew"] if crew["job"] == "Director"), None
        ),
    )

    # 연령등급 저장
    movie.age_rating = age_rating or "정보 없음"  # 값이 없으면 기본값 설정

    # 장르 저장
    for genre_data in movie_details.get("genres", []):
        genre, _ = Genre.objects.get_or_create(
            tmdb_id=genre_data["id"],
            defaults={"name": genre_data["name"]},
        )
        movie.genres.add(genre)

    # 배우 저장 (최대 5명)
    for actor_data in credits_data.get("cast", [])[:5]:
        actor, _ = Actor.objects.get_or_create(
            name=actor_data["name"],
            character=actor_data.get("character"),
            profile_path=actor_data.get("profile_path"),
        )
        movie.actors.add(actor)

    movie.save()
    print(f"Saved movie '{movie.title}' with age rating: {movie.age_rating}")


class Command(BaseCommand):
    help = "Fetch popular movies excluding 19세 관람가 and save them to the database"

    def handle(self, *args, **kwargs):
        total_movies = 0
        max_movies = 100  # 총 100개의 영화 저장
        for page in range(1, 6):  # 최대 5페이지 순회
            movies = fetch_movies(page)
            for movie_data in movies:
                if total_movies >= max_movies:
                    print("Collected 100 movies. Stopping further requests.")
                    return  # 100개 저장 후 종료

                # 영화 크레딧 데이터 가져오기
                credits_data = fetch_movie_credits(movie_data["id"])
                if credits_data:
                    save_movie(movie_data, credits_data)
                    total_movies += 1
                    print(f"Saved {total_movies}/100 movies")

        print(f"Movies fetched and saved successfully. Total: {total_movies}")
