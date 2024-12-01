import openai
from decouple import config
openai.api_key=config('OPENAI_API_KEY')
response = openai.ChatCompletion.create(
    model="gpt-4o-mini", 
    messages=[
        {"role": "user", "content":
            "현재 닐씨 추천을 하기 위해서는 현재 위치한 도시명을 입력해야해. 하지만 현재 도시명의 입력 형식은 영어의 형태를 가지고 있어. 예시로 서울은 Seoul, 수원은 Suwon의 형태아."+
            "주요 사용자들이 한국인인만큼 영어로 입력하는 방식은 불편함을 가지고 있어. 때문에 입력하는 방식을 한글로도 가능하게 하고 싶어."+
            "구글에 검색해본 결과 OPENWEATHERMAP API는 Geocoding API를 사용해서 위도와 경도 데이터를 사용하면 한글명으로 입력해도 될 거 같아. Geocoding API는 한글 입력도 지원하고 있으니 이 방식을 사용해보면 좋을 것 같아."+
            "현재 내가 사용하는 코드는 다음과 같으니까 이걸 참고해봐"+
            "def get_weather_data(city):"+
            "api_key = settings.OPENWEATHERMAP_API_KEY"+
            "encoded_city = quote(city)"+
            "url = f'http://api.openweathermap.org/data/2.5/weather?q={encoded_city}&appid={api_key}&units=metric&l'"+
            "response = requests.get(url)"+
            "if response.status_code == 200:"+
            "return response.json()"+
            "return None"+
            "get_weather_data 하나의 함수로 동작하도록 작성해줘"
        }
    ],
    max_tokens=1000
)

print(response['choices'][0]['message']['content'].strip())  # 'message'로 수정