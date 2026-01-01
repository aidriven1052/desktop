"""
네이버 블로그 포스트 생성기
제품 정보를 입력받아 자동으로 블로그 글을 작성합니다.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import random


@dataclass
class Product:
    """제품 정보를 담는 데이터 클래스"""
    name: str
    price: int
    description: str
    images: List[str] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    category: Optional[str] = None
    brand: Optional[str] = None
    rating: Optional[float] = None

    def formatted_price(self) -> str:
        """가격을 포맷팅하여 반환"""
        return f"{self.price:,}원"


class NaverBlogGenerator:
    """네이버 블로그 포스트를 생성하는 클래스"""

    def __init__(self):
        self.templates = {
            'review': self._generate_review,
            'intro': self._generate_intro,
            'comparison': self._generate_comparison,
            'unboxing': self._generate_unboxing
        }

        # 블로그에서 자주 사용하는 표현들
        self.opening_phrases = [
            "안녕하세요! 오늘은",
            "여러분 안녕하세요~",
            "오늘 소개해드릴 제품은",
            "최근에 구매한",
            "요즘 핫한"
        ]

        self.transition_phrases = [
            "그럼 이제",
            "자, 그럼",
            "그래서",
            "본격적으로",
            "이제부터"
        ]

        self.closing_phrases = [
            "지금까지 소개해드렸습니다!",
            "도움이 되셨길 바랍니다 😊",
            "궁금하신 점은 댓글로 남겨주세요!",
            "읽어주셔서 감사합니다!",
            "다음에 더 좋은 정보로 찾아뵙겠습니다!"
        ]

    def generate(self, product: Product, template: str = 'review',
                 output_format: str = 'html') -> str:
        """
        블로그 포스트를 생성합니다.

        Args:
            product: 제품 정보
            template: 템플릿 종류 ('review', 'intro', 'comparison', 'unboxing')
            output_format: 출력 형식 ('html' 또는 'markdown')

        Returns:
            생성된 블로그 포스트 문자열
        """
        if template not in self.templates:
            raise ValueError(f"지원하지 않는 템플릿입니다: {template}")

        # 템플릿에 맞는 콘텐츠 생성
        content = self.templates[template](product)

        # 출력 형식에 맞게 변환
        if output_format == 'html':
            return self._to_html(content, product)
        else:
            return content

    def _generate_review(self, product: Product) -> str:
        """리뷰 형식의 블로그 포스트 생성"""
        opening = random.choice(self.opening_phrases)
        transition = random.choice(self.transition_phrases)
        closing = random.choice(self.closing_phrases)

        content = f"""# {product.name} 솔직 후기! {'⭐' * int(product.rating or 5)}

{opening} {product.name}에 대해 자세히 리뷰해보려고 합니다.

{product.description}

## 📦 제품 정보

- **가격**: {product.formatted_price()}
"""

        if product.brand:
            content += f"- **브랜드**: {product.brand}\n"

        if product.category:
            content += f"- **카테고리**: {product.category}\n"

        if product.rating:
            content += f"- **평점**: {'⭐' * int(product.rating)} ({product.rating}/5.0)\n"

        # 이미지 섹션
        if product.images:
            content += "\n## 📸 제품 사진\n\n"
            for i, img in enumerate(product.images, 1):
                content += f"![{product.name} 이미지 {i}]({img})\n\n"

        # 주요 특징
        if product.features:
            content += "## ✨ 주요 특징\n\n"
            for feature in product.features:
                content += f"- {feature}\n"
            content += "\n"

        # 장점
        if product.pros:
            content += "## 👍 장점\n\n"
            for i, pro in enumerate(product.pros, 1):
                content += f"{i}. **{pro}**\n"
                content += f"   실제로 사용해보니 정말 만족스러운 부분이었습니다.\n\n"

        # 단점
        if product.cons:
            content += "## 👎 아쉬운 점\n\n"
            for i, con in enumerate(product.cons, 1):
                content += f"{i}. {con}\n"
                content += f"   조금 아쉬웠지만 크게 불편한 정도는 아니었어요.\n\n"

        # 총평
        content += f"""## 💭 총평

{transition} 사용해본 소감을 정리해보자면, {product.name}은(는)
{product.formatted_price()}의 가격대를 고려했을 때 충분히 만족스러운 제품이었습니다.

"""

        if product.pros:
            content += f"특히 {product.pros[0]} 부분이 가장 마음에 들었고, "

        content += "전반적으로 추천할 만한 제품이라고 생각합니다!\n\n"

        # 마무리
        content += f"---\n\n{closing}\n"

        return content

    def _generate_intro(self, product: Product) -> str:
        """제품 소개 형식의 블로그 포스트 생성"""
        opening = random.choice(self.opening_phrases)

        content = f"""# {product.name} 완벽 가이드! 📱

{opening} {product.name}에 대해 알아보려고 합니다.

## 🎯 제품 소개

{product.description}

**가격**: {product.formatted_price()}
"""

        if product.brand:
            content += f"**브랜드**: {product.brand}\n"

        # 이미지
        if product.images:
            content += "\n## 📷 제품 갤러리\n\n"
            for img in product.images:
                content += f"![{product.name}]({img})\n\n"

        # 특징
        if product.features:
            content += "## 🌟 이런 특징이 있어요!\n\n"
            for i, feature in enumerate(product.features, 1):
                content += f"### {i}. {feature}\n\n"
                content += f"이 기능 덕분에 더욱 편리하게 사용할 수 있습니다.\n\n"

        # 추천 대상
        content += "## 🎁 이런 분들께 추천합니다\n\n"
        if product.pros:
            for pro in product.pros:
                content += f"- {pro}을(를) 중요하게 생각하시는 분\n"

        content += f"\n## 💰 가격 정보\n\n"
        content += f"현재 {product.formatted_price()}에 만나보실 수 있습니다.\n\n"

        content += "---\n\n"
        content += random.choice(self.closing_phrases) + "\n"

        return content

    def _generate_comparison(self, product: Product) -> str:
        """비교 형식의 블로그 포스트 생성"""
        content = f"""# {product.name} 상세 분석! 🔍

## 제품 개요

{product.description}

**가격**: {product.formatted_price()}

"""

        # 이미지
        if product.images:
            content += "## 제품 이미지\n\n"
            content += f"![{product.name}]({product.images[0]})\n\n"

        # 장단점 비교
        content += "## ⚖️ 장단점 비교\n\n"
        content += "| 장점 ✅ | 단점 ❌ |\n"
        content += "|---------|--------|\n"

        max_len = max(len(product.pros), len(product.cons))
        for i in range(max_len):
            pro = product.pros[i] if i < len(product.pros) else ""
            con = product.cons[i] if i < len(product.cons) else ""
            content += f"| {pro} | {con} |\n"

        content += "\n"

        # 특징 분석
        if product.features:
            content += "## 🔎 세부 특징 분석\n\n"
            for i, feature in enumerate(product.features, 1):
                content += f"### {i}. {feature}\n\n"

        # 가격 대비 가치
        content += f"## 💵 가격 대비 가치\n\n"
        content += f"{product.formatted_price()}라는 가격이 합리적인지 분석해보겠습니다.\n\n"

        if product.rating and product.rating >= 4.0:
            content += "높은 평점과 우수한 기능을 고려하면 가격 대비 만족도가 높은 제품입니다.\n\n"
        else:
            content += "가격대를 고려하여 신중하게 선택하시는 것을 추천드립니다.\n\n"

        content += "---\n\n"
        content += random.choice(self.closing_phrases) + "\n"

        return content

    def _generate_unboxing(self, product: Product) -> str:
        """언박싱 리뷰 형식의 블로그 포스트 생성"""
        content = f"""# {product.name} 언박싱! 📦✨

드디어 기다리던 {product.name}이(가) 도착했습니다!
함께 언박싱해볼까요? 😊

## 📦 택배 도착!

{product.description}

**구매 가격**: {product.formatted_price()}

"""

        # 첫 번째 이미지 (패키지)
        if product.images:
            content += "## 🎁 패키지 첫인상\n\n"
            content += f"![패키지]({product.images[0]})\n\n"
            content += "패키지부터 정말 고급스럽네요! 기대가 됩니다.\n\n"

        # 두 번째 이미지 (개봉)
        if len(product.images) > 1:
            content += "## 📸 개봉 순간!\n\n"
            content += f"![개봉]({product.images[1]})\n\n"
            content += "박스를 열어보니 깔끔하게 포장되어 있습니다.\n\n"

        # 구성품
        content += "## 📋 구성품\n\n"
        if product.features:
            content += "박스 안에는 다음과 같은 것들이 들어있었어요:\n\n"
            for feature in product.features:
                content += f"- {feature}\n"
            content += "\n"

        # 상세 이미지들
        if len(product.images) > 2:
            content += "## 🔍 자세히 살펴보기\n\n"
            for i, img in enumerate(product.images[2:], 1):
                content += f"![상세 이미지 {i}]({img})\n\n"

        # 첫인상
        content += "## 💭 첫인상\n\n"
        if product.pros:
            content += "실제로 받아보니 특히 이런 점들이 좋았어요:\n\n"
            for pro in product.pros:
                content += f"- {pro}\n"
            content += "\n"

        # 마무리
        content += f"""## 🎬 마치며

언박싱을 해보니 {product.formatted_price()}의 가치가 충분히 느껴지는 제품이네요!
앞으로 사용하면서 더 자세한 리뷰로 찾아뵙겠습니다.

---

"""
        content += random.choice(self.closing_phrases) + "\n"

        return content

    def _to_html(self, markdown_content: str, product: Product) -> str:
        """마크다운을 HTML로 변환"""
        import re

        html = markdown_content

        # 제목 변환
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)

        # 굵은 글씨
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

        # 이미지
        html = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)',
                     r'<img src="\2" alt="\1" style="max-width: 100%; height: auto; margin: 20px 0;">',
                     html)

        # 리스트 항목
        html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)

        # 번호 리스트
        html = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)

        # 수평선
        html = re.sub(r'^---$', r'<hr>', html, flags=re.MULTILINE)

        # 단락
        html = re.sub(r'\n\n', r'</p><p>', html)
        html = f'<p>{html}</p>'

        # 테이블 변환
        html = re.sub(r'\|(.+)\|', lambda m: '<tr>' + ''.join(f'<td>{cell.strip()}</td>'
                                                                for cell in m.group(1).split('|')) + '</tr>',
                     html)
        html = re.sub(r'(<tr>.*</tr>)', r'<table style="width:100%; border-collapse: collapse;">\1</table>',
                     html, flags=re.DOTALL)

        # 전체 HTML 구조
        full_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product.name} - 네이버 블로그</title>
    <style>
        body {{
            font-family: 'Malgun Gothic', '맑은 고딕', sans-serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #03C75A;
            border-bottom: 3px solid #03C75A;
            padding-bottom: 10px;
            font-size: 28px;
        }}
        h2 {{
            color: #1EC800;
            margin-top: 30px;
            font-size: 22px;
        }}
        h3 {{
            color: #555;
            margin-top: 20px;
            font-size: 18px;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}
        ul, ol {{
            padding-left: 25px;
        }}
        li {{
            margin: 8px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        td, th {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        hr {{
            border: none;
            border-top: 2px solid #eee;
            margin: 30px 0;
        }}
        strong {{
            color: #03C75A;
        }}
    </style>
</head>
<body>
    {html}
</body>
</html>"""

        return full_html


def main():
    """메인 함수 - 사용 예시"""
    # 샘플 제품 데이터
    product = Product(
        name="삼성 갤럭시 버즈2 프로",
        price=229000,
        brand="삼성전자",
        category="무선 이어폰",
        rating=4.5,
        description="뛰어난 노이즈 캔슬링 기능을 갖춘 프리미엄 무선 이어폰",
        images=[
            "https://images.samsung.com/kdp/goods/2022/08/10/a1659960000001l.jpg",
            "https://images.samsung.com/kdp/goods/2022/08/10/a1659960000002l.jpg",
            "https://images.samsung.com/kdp/goods/2022/08/10/a1659960000003l.jpg"
        ],
        features=[
            "지능형 ANC (Active Noise Cancellation)",
            "최대 29시간 재생 (케이스 포함)",
            "360도 오디오 지원",
            "IPX7 방수 등급",
            "고해상도 코덱 지원"
        ],
        pros=[
            "탁월한 음질과 노이즈 캔슬링",
            "편안한 착용감",
            "긴 배터리 수명",
            "프리미엄 디자인"
        ],
        cons=[
            "가격이 다소 높은 편",
            "케이스가 약간 큰 편",
            "일부 안드로이드 기기에서만 전체 기능 사용 가능"
        ]
    )

    # 블로그 생성기 초기화
    generator = NaverBlogGenerator()

    # 다양한 템플릿으로 생성
    print("=" * 80)
    print("리뷰 형식 블로그 포스트")
    print("=" * 80)
    review_post = generator.generate(product, template='review', output_format='markdown')
    print(review_post)

    print("\n\n" + "=" * 80)
    print("HTML 출력 샘플")
    print("=" * 80)
    html_post = generator.generate(product, template='review', output_format='html')

    # HTML 파일로 저장
    with open('sample_blog_post.html', 'w', encoding='utf-8') as f:
        f.write(html_post)
    print("HTML 파일이 'sample_blog_post.html'로 저장되었습니다.")


if __name__ == '__main__':
    main()
