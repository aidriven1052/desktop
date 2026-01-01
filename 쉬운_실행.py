#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버 블로그 포스트 생성기 - 초보자용 대화형 프로그램
코딩을 모르는 사람도 쉽게 사용할 수 있습니다!
"""

from naver_blog_generator import NaverBlogGenerator, Product
import os


def print_line():
    """구분선 출력"""
    print("=" * 70)


def print_title(title):
    """제목 출력"""
    print_line()
    print(f"  {title}")
    print_line()


def ask_question(question, default=""):
    """질문하고 답변 받기"""
    if default:
        answer = input(f"{question} (기본값: {default}): ").strip()
        return answer if answer else default
    else:
        answer = input(f"{question}: ").strip()
        return answer


def ask_yes_no(question):
    """예/아니오 질문"""
    while True:
        answer = input(f"{question} (예/아니오): ").strip().lower()
        if answer in ['예', 'y', 'yes', '네']:
            return True
        elif answer in ['아니오', 'n', 'no', '아니요']:
            return False
        else:
            print("'예' 또는 '아니오'로 답해주세요.")


def ask_number(question, default=0):
    """숫자 입력받기"""
    while True:
        try:
            answer = input(f"{question} (기본값: {default}): ").strip()
            if not answer:
                return default
            return int(answer)
        except ValueError:
            print("❌ 숫자만 입력해주세요!")


def ask_rating(question):
    """평점 입력받기 (0-5)"""
    while True:
        try:
            answer = input(f"{question} (0-5 사이 숫자): ").strip()
            if not answer:
                return None
            rating = float(answer)
            if 0 <= rating <= 5:
                return rating
            else:
                print("❌ 0에서 5 사이의 숫자를 입력해주세요!")
        except ValueError:
            print("❌ 숫자만 입력해주세요!")


def ask_list(question, example=""):
    """리스트 항목 입력받기"""
    print(f"\n{question}")
    if example:
        print(f"예시: {example}")
    print("항목을 하나씩 입력하세요. 완료하면 빈칸에서 엔터를 누르세요.")

    items = []
    count = 1
    while True:
        item = input(f"  {count}. ").strip()
        if not item:
            break
        items.append(item)
        count += 1

    return items


def main():
    """메인 프로그램"""
    os.system('clear' if os.name == 'posix' else 'cls')

    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║          🎨 네이버 블로그 포스트 생성기 🎨                ║
    ║                                                            ║
    ║              초보자도 쉽게 사용할 수 있어요!              ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """)

    print("\n환영합니다! 👋")
    print("몇 가지 질문에 답하시면 멋진 블로그 글이 자동으로 만들어집니다.\n")

    input("준비되셨으면 엔터를 눌러주세요...")

    # 1. 기본 정보
    print_title("1️⃣  제품 기본 정보")

    name = ask_question("제품 이름을 입력하세요", "샘플 제품")
    price = ask_number("가격을 입력하세요 (숫자만)", 100000)
    description = ask_question("제품을 한 줄로 설명해주세요", "멋진 제품입니다")

    # 2. 추가 정보
    print("\n" + "="*70)
    print("추가 정보를 입력하시겠어요? (선택사항)")
    print("="*70)

    brand = None
    category = None
    rating = None

    if ask_yes_no("브랜드 이름을 입력하시겠어요?"):
        brand = ask_question("브랜드 이름")

    if ask_yes_no("카테고리를 입력하시겠어요?"):
        category = ask_question("카테고리 (예: 전자제품, 의류, 화장품)")

    if ask_yes_no("평점을 입력하시겠어요?"):
        rating = ask_rating("평점")

    # 3. 이미지
    print_title("2️⃣  제품 이미지")

    images = []
    if ask_yes_no("이미지 URL을 추가하시겠어요?"):
        images = ask_list("이미지 URL을 입력하세요", "https://example.com/image.jpg")

    # 4. 특징
    print_title("3️⃣  제품 특징")

    features = []
    if ask_yes_no("제품 특징을 추가하시겠어요?"):
        features = ask_list("제품의 특징을 입력하세요", "빠른 배송, 좋은 품질")

    # 5. 장점
    print_title("4️⃣  제품 장점")

    pros = []
    if ask_yes_no("제품 장점을 추가하시겠어요?"):
        pros = ask_list("제품의 장점을 입력하세요", "가성비가 좋음, 디자인이 예쁨")

    # 6. 단점
    print_title("5️⃣  제품 단점")

    cons = []
    if ask_yes_no("제품 단점을 추가하시겠어요?"):
        cons = ask_list("제품의 단점을 입력하세요", "가격이 비쌈, 무거움")

    # 7. 템플릿 선택
    print_title("6️⃣  블로그 글 스타일 선택")

    print("\n어떤 스타일의 글을 만들까요?\n")
    print("1. 리뷰 (제품 사용 후기)")
    print("2. 소개 (제품 소개글)")
    print("3. 비교 (장단점 비교)")
    print("4. 언박싱 (개봉 후기)")

    while True:
        template_choice = input("\n선택하세요 (1-4): ").strip()
        if template_choice == '1':
            template = 'review'
            template_name = '리뷰'
            break
        elif template_choice == '2':
            template = 'intro'
            template_name = '소개'
            break
        elif template_choice == '3':
            template = 'comparison'
            template_name = '비교'
            break
        elif template_choice == '4':
            template = 'unboxing'
            template_name = '언박싱'
            break
        else:
            print("❌ 1, 2, 3, 4 중에서 선택해주세요!")

    # 8. 출력 형식 선택
    print("\n" + "="*70)
    print("어떤 형식으로 저장할까요?")
    print("="*70)
    print("\n1. HTML (브라우저에서 볼 수 있는 형식)")
    print("2. 마크다운 (텍스트 파일)")

    while True:
        format_choice = input("\n선택하세요 (1-2): ").strip()
        if format_choice == '1':
            output_format = 'html'
            extension = '.html'
            break
        elif format_choice == '2':
            output_format = 'markdown'
            extension = '.md'
            break
        else:
            print("❌ 1 또는 2를 선택해주세요!")

    # 9. 파일 이름
    print_title("7️⃣  파일 이름")

    filename = ask_question(
        "저장할 파일 이름을 입력하세요 (확장자 제외)",
        f"{name}_블로그글"
    )
    filename = filename + extension

    # 10. 제품 정보 요약
    print_title("📋 입력하신 정보 확인")

    print(f"\n제품명: {name}")
    print(f"가격: {price:,}원")
    print(f"설명: {description}")
    if brand:
        print(f"브랜드: {brand}")
    if category:
        print(f"카테고리: {category}")
    if rating:
        print(f"평점: {rating}/5.0")
    if images:
        print(f"이미지: {len(images)}개")
    if features:
        print(f"특징: {len(features)}개")
    if pros:
        print(f"장점: {len(pros)}개")
    if cons:
        print(f"단점: {len(cons)}개")
    print(f"\n글 스타일: {template_name}")
    print(f"저장 형식: {output_format}")
    print(f"파일 이름: {filename}")

    print("\n" + "="*70)
    if not ask_yes_no("\n이 정보로 블로그 글을 만들까요?"):
        print("\n취소되었습니다. 처음부터 다시 시작해주세요.")
        return

    # 11. 블로그 글 생성
    print_title("🎨 블로그 글 생성 중...")

    try:
        # Product 객체 생성
        product = Product(
            name=name,
            price=price,
            description=description,
            images=images,
            features=features,
            pros=pros,
            cons=cons,
            brand=brand,
            category=category,
            rating=rating
        )

        # 블로그 글 생성
        generator = NaverBlogGenerator()
        post = generator.generate(
            product,
            template=template,
            output_format=output_format
        )

        # 파일 저장
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(post)

        # 완료!
        print_title("✅ 완료!")

        print(f"\n블로그 글이 성공적으로 만들어졌습니다!")
        print(f"파일 이름: {filename}")
        print(f"파일 위치: {os.path.abspath(filename)}")

        if output_format == 'html':
            print(f"\n📝 사용 방법:")
            print(f"1. '{filename}' 파일을 더블클릭하여 브라우저에서 열기")
            print(f"2. 내용을 복사해서 네이버 블로그에 붙여넣기")
        else:
            print(f"\n📝 사용 방법:")
            print(f"1. '{filename}' 파일을 메모장으로 열기")
            print(f"2. 내용을 복사해서 네이버 블로그에 붙여넣기")

        print("\n" + "="*70)
        print("🎉 수고하셨습니다! 멋진 블로그 글이 완성되었어요!")
        print("="*70)

    except Exception as e:
        print(f"\n❌ 오류가 발생했습니다: {e}")
        print("다시 시도해주세요.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 프로그램을 종료합니다. 안녕히 가세요!")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        print("프로그램 개발자에게 문의해주세요.")
