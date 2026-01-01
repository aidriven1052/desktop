#!/usr/bin/env python3
"""
네이버 블로그 포스트 생성기 사용 예시
다양한 방법으로 블로그 포스트를 생성하는 방법을 보여줍니다.
"""

from naver_blog_generator import NaverBlogGenerator, Product


def example_1_simple_review():
    """예시 1: 간단한 제품 리뷰 생성"""
    print("\n" + "="*80)
    print("예시 1: 간단한 제품 리뷰 생성")
    print("="*80 + "\n")

    product = Product(
        name="애플 에어팟 프로 2세대",
        price=359000,
        description="애플의 프리미엄 노이즈 캔슬링 무선 이어폰"
    )

    generator = NaverBlogGenerator()
    post = generator.generate(product, template='review', output_format='markdown')
    print(post)


def example_2_detailed_product():
    """예시 2: 상세한 제품 정보로 소개글 생성"""
    print("\n" + "="*80)
    print("예시 2: 상세한 제품 정보로 소개글 생성")
    print("="*80 + "\n")

    product = Product(
        name="다이슨 V15 무선청소기",
        price=899000,
        brand="다이슨",
        category="무선청소기",
        rating=4.7,
        description="레이저로 먼지를 보여주는 차세대 무선청소기",
        images=[
            "https://example.com/dyson-v15-main.jpg",
            "https://example.com/dyson-v15-laser.jpg",
            "https://example.com/dyson-v15-use.jpg"
        ],
        features=[
            "레이저 먼지 감지 기술",
            "최대 60분 강력한 흡입력",
            "LCD 스크린으로 실시간 먼지 크기 표시",
            "HEPA 필터레이션",
            "5단계 필터링 시스템"
        ],
        pros=[
            "강력한 흡입력",
            "레이저로 먼지가 눈에 보임",
            "다양한 헤드 구성",
            "긴 사용 시간"
        ],
        cons=[
            "무게가 다소 무거움",
            "높은 가격",
            "소음이 있는 편"
        ]
    )

    generator = NaverBlogGenerator()
    post = generator.generate(product, template='intro', output_format='markdown')
    print(post)


def example_3_comparison():
    """예시 3: 비교 분석형 포스트 생성"""
    print("\n" + "="*80)
    print("예시 3: 비교 분석형 포스트 생성")
    print("="*80 + "\n")

    product = Product(
        name="소니 WH-1000XM5",
        price=449000,
        brand="소니",
        category="헤드폰",
        rating=4.9,
        description="업계 최고의 노이즈 캔슬링 헤드폰",
        features=[
            "업계 최고 수준의 노이즈 캔슬링",
            "30시간 연속 재생",
            "LDAC 고음질 코덱 지원",
            "멀티포인트 연결",
            "터치 컨트롤"
        ],
        pros=[
            "최상급 노이즈 캔슬링",
            "뛰어난 음질",
            "편안한 착용감",
            "긴 배터리 수명"
        ],
        cons=[
            "높은 가격",
            "접이식 구조가 아님",
            "방수 기능 없음"
        ]
    )

    generator = NaverBlogGenerator()
    post = generator.generate(product, template='comparison', output_format='markdown')
    print(post)


def example_4_unboxing():
    """예시 4: 언박싱 리뷰 생성"""
    print("\n" + "="*80)
    print("예시 4: 언박싱 리뷰 생성")
    print("="*80 + "\n")

    product = Product(
        name="아이패드 프로 12.9인치 M2",
        price=1799000,
        brand="애플",
        category="태블릿",
        rating=5.0,
        description="애플의 최고급 프로 태블릿",
        images=[
            "https://example.com/ipad-box.jpg",
            "https://example.com/ipad-unbox.jpg",
            "https://example.com/ipad-screen.jpg",
            "https://example.com/ipad-pencil.jpg"
        ],
        features=[
            "12.9인치 Liquid Retina XDR 디스플레이",
            "M2 칩 탑재",
            "128GB / 256GB / 512GB / 1TB / 2TB 저장공간",
            "Apple Pencil 2세대 지원",
            "Magic Keyboard 호환",
            "Thunderbolt / USB 4 지원"
        ],
        pros=[
            "맥북에 버금가는 강력한 성능",
            "아름다운 디스플레이",
            "Apple Pencil 활용도",
            "iPadOS의 생산성 기능"
        ],
        cons=[
            "매우 높은 가격",
            "무게가 무거운 편",
            "앱 생태계가 맥OS보다 제한적"
        ]
    )

    generator = NaverBlogGenerator()
    post = generator.generate(product, template='unboxing', output_format='markdown')
    print(post)


def example_5_html_output():
    """예시 5: HTML 파일로 저장"""
    print("\n" + "="*80)
    print("예시 5: HTML 파일로 저장")
    print("="*80 + "\n")

    product = Product(
        name="닌텐도 스위치 OLED",
        price=429000,
        brand="닌텐도",
        category="게임기",
        rating=4.6,
        description="더 커지고 선명해진 OLED 화면의 닌텐도 스위치",
        features=[
            "7인치 OLED 디스플레이",
            "64GB 내장 메모리",
            "향상된 오디오",
            "유선 LAN 포트 내장 독",
            "넓어진 킥스탠드"
        ],
        pros=[
            "선명하고 아름다운 OLED 화면",
            "다양한 게임 라이브러리",
            "휴대 및 거치 모드",
            "가족 모두 즐길 수 있음"
        ],
        cons=[
            "성능 향상은 없음",
            "Joy-Con 드리프트 문제",
            "비싼 게임 가격"
        ]
    )

    generator = NaverBlogGenerator()
    html_post = generator.generate(product, template='review', output_format='html')

    # HTML 파일로 저장
    filename = 'nintendo_switch_review.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_post)

    print(f"✅ HTML 파일이 '{filename}'로 저장되었습니다.")
    print(f"   브라우저에서 열어보세요!")


def example_6_multiple_templates():
    """예시 6: 하나의 제품으로 여러 템플릿 생성"""
    print("\n" + "="*80)
    print("예시 6: 하나의 제품으로 여러 템플릿 생성")
    print("="*80 + "\n")

    product = Product(
        name="테슬라 모델 Y",
        price=56990000,
        brand="테슬라",
        category="전기차",
        rating=4.5,
        description="가족을 위한 완벽한 전기 SUV",
        features=[
            "1회 충전 주행거리 최대 511km",
            "0-100km/h 가속 3.7초",
            "7인승 구성 가능",
            "오토파일럿 기본 탑재",
            "파노라믹 글래스 루프"
        ],
        pros=[
            "뛰어난 주행 성능",
            "넓은 실내 공간",
            "첨단 자율주행 기능",
            "낮은 유지비용"
        ],
        cons=[
            "높은 초기 구매 비용",
            "충전 인프라 필요",
            "실내 마감 품질 편차"
        ]
    )

    generator = NaverBlogGenerator()

    templates = ['review', 'intro', 'comparison']

    for template in templates:
        print(f"\n{'='*60}")
        print(f"템플릿: {template.upper()}")
        print('='*60 + "\n")

        post = generator.generate(product, template=template, output_format='markdown')
        print(post[:500] + "...\n")  # 처음 500자만 출력


def main():
    """모든 예시 실행"""
    print("\n" + "🎨 "*20)
    print("네이버 블로그 포스트 생성기 - 사용 예시")
    print("🎨 "*20)

    examples = [
        ("간단한 리뷰", example_1_simple_review),
        ("상세 소개글", example_2_detailed_product),
        ("비교 분석", example_3_comparison),
        ("언박싱 리뷰", example_4_unboxing),
        ("HTML 저장", example_5_html_output),
        ("다중 템플릿", example_6_multiple_templates)
    ]

    print("\n실행할 예시를 선택하세요:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print(f"  {len(examples) + 1}. 모두 실행")
    print("  0. 종료")

    try:
        choice = input("\n선택 (0-7): ").strip()

        if choice == '0':
            print("\n👋 프로그램을 종료합니다.")
            return

        if choice == str(len(examples) + 1):
            for name, func in examples:
                func()
        elif choice.isdigit() and 1 <= int(choice) <= len(examples):
            examples[int(choice) - 1][1]()
        else:
            print("\n❌ 올바른 번호를 입력하세요.")

    except KeyboardInterrupt:
        print("\n\n👋 프로그램을 종료합니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")


if __name__ == '__main__':
    main()
