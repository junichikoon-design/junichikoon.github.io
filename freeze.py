# freeze.py
from main import app
from flask_frozen import Freezer

freezer = Freezer(app)

# GitHub Pages로 내보낼 "키워드 목록"
KEYWORDS = ["python"]  # 필요하면 여기에 더 추가

@freezer.register_generator
def static_berlin_result():
    for kw in KEYWORDS:
        yield 'static_berlin_result', {'keyword': kw}

@freezer.register_generator
def static_web3_result():
    for kw in KEYWORDS:
        yield 'static_web3_result', {'keyword': kw}

@freezer.register_generator
def static_wework_result():
    for kw in KEYWORDS:
        yield 'static_wework_result', {'keyword': kw}

@freezer.register_generator
def home():
    yield 'home'

if __name__ == "__main__":
    freezer.freeze()  # build/ 폴더에 정적 파일 생성