import subprocess

def dumpdata_to_utf8():
    # dumpdata 명령 실행
    result = subprocess.run(
        ["python", "manage.py", "dumpdata", "movies", "--indent", "4"],
        stdout=subprocess.PIPE,  # 표준 출력 캡처
        stderr=subprocess.PIPE,  # 표준 에러 캡처
        text=True,               # 문자열로 출력
        encoding="utf-8"         # 출력 인코딩 설정
    )

    # 명령 실행 결과 확인
    if result.returncode != 0:
        print("Error occurred while running dumpdata:")
        print(result.stderr)  # 에러 메시지 출력
    else:
        # UTF-8로 파일 저장
        with open("movies_fixtures.json", "w", encoding="utf-8") as f:
            f.write(result.stdout)
        print("Fixtures successfully dumped to 'movies_fixtures.json' in UTF-8 encoding.")

# 스크립트 실행
if __name__ == "__main__":
    dumpdata_to_utf8()
