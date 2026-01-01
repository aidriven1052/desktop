# 네이버 블로그 포스트 생성기

제품 정보를 입력하면 자동으로 네이버 블로그 형식의 글을 작성해주는 프로그램입니다.

## 🚀 빠른 시작 (코딩 초보자용)

**가장 쉬운 방법:**

1. **Windows**: `블로그글_만들기.bat` 파일을 더블클릭
2. **Mac/Linux**: `블로그글_만들기.sh` 파일을 더블클릭
3. 질문에 답하면 자동으로 블로그 글이 생성됩니다!

📖 더 자세한 설명이 필요하다면:
- **초보자**: `초보자_가이드.md` 파일 읽기 (초등학생도 이해 가능!)
- **빠른 시작**: `빠른_시작_가이드.md` 파일 읽기 (3분이면 완성!)

## 기능

- 제품명, 가격, 이미지, 설명 등의 정보를 입력받아 블로그 포스트 생성
- 다양한 템플릿 지원 (리뷰형, 소개형, 비교형)
- 자연스러운 한국어 블로그 글 생성
- HTML 및 마크다운 형식 출력

## 설치 방법

```bash
pip install -r requirements.txt
```

## 사용 방법

### 방법 1. 대화형 프로그램 (가장 쉬움! ⭐ 추천)

```bash
# Windows
블로그글_만들기.bat 더블클릭

# Mac/Linux
./블로그글_만들기.sh
# 또는
python3 쉬운_실행.py
```

질문에 답하기만 하면 끝!

### 방법 2. 커맨드 라인으로 사용

```bash
python generate_post.py --product-file product.json --template review --output post.html
```

### 방법 3. Python 모듈로 사용

```python
from naver_blog_generator import NaverBlogGenerator, Product

# 제품 정보 설정
product = Product(
    name="삼성 갤럭시 버즈2 프로",
    price=229000,
    images=[
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg"
    ],
    description="뛰어난 노이즈 캔슬링 기능을 갖춘 무선 이어폰",
    features=[
        "지능형 ANC (Active Noise Cancellation)",
        "최대 29시간 재생 (케이스 포함)",
        "360도 오디오",
        "IPX7 방수"
    ],
    pros=[
        "탁월한 음질",
        "편안한 착용감",
        "긴 배터리 수명"
    ],
    cons=[
        "가격이 다소 높음",
        "케이스가 약간 큼"
    ]
)

# 블로그 포스트 생성
generator = NaverBlogGenerator()
post = generator.generate(product, template="review")

print(post)
```

### 방법 4. 다양한 예시 보기

```bash
python3 example_usage.py
```

## 파일 설명

| 파일 | 설명 | 대상 |
|------|------|------|
| `쉬운_실행.py` | 대화형 프로그램 (질문에 답하면 자동 생성) | ⭐ 초보자 추천 |
| `블로그글_만들기.bat` | Windows용 실행 파일 | Windows 사용자 |
| `블로그글_만들기.sh` | Mac/Linux용 실행 파일 | Mac/Linux 사용자 |
| `generate_post.py` | 커맨드라인 도구 | 개발자 |
| `naver_blog_generator.py` | 핵심 라이브러리 | 개발자 |
| `example_usage.py` | 다양한 사용 예시 | 학습용 |
| `초보자_가이드.md` | 초보자용 상세 가이드 | 코딩 초보자 |
| `빠른_시작_가이드.md` | 3분 빠른 시작 | 바쁜 사람 |

## 템플릿 종류

- **review**: 제품 리뷰 형식
- **intro**: 제품 소개 형식
- **comparison**: 제품 비교 형식
- **unboxing**: 언박싱 리뷰 형식

## 예시

입력한 제품 정보를 바탕으로 아래와 같은 블로그 포스트가 생성됩니다:

```
# 삼성 갤럭시 버즈2 프로 솔직 후기! 🎧

안녕하세요! 오늘은 최근에 구매한 삼성 갤럭시 버즈2 프로에 대해
자세히 리뷰해보려고 합니다.

## 제품 정보
- 가격: 229,000원
- 주요 특징: 뛰어난 노이즈 캔슬링 기능을 갖춘 무선 이어폰

...
```

## 라이선스

MIT License
