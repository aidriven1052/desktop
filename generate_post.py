#!/usr/bin/env python3
"""
커맨드라인에서 네이버 블로그 포스트를 생성하는 스크립트
"""

import argparse
import json
import sys
from pathlib import Path
from naver_blog_generator import NaverBlogGenerator, Product


def load_product_from_json(json_file: str) -> Product:
    """JSON 파일에서 제품 정보를 로드합니다."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return Product(
            name=data.get('name', ''),
            price=data.get('price', 0),
            description=data.get('description', ''),
            images=data.get('images', []),
            features=data.get('features', []),
            pros=data.get('pros', []),
            cons=data.get('cons', []),
            category=data.get('category'),
            brand=data.get('brand'),
            rating=data.get('rating')
        )
    except FileNotFoundError:
        print(f"오류: '{json_file}' 파일을 찾을 수 없습니다.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"오류: JSON 파싱 실패 - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='네이버 블로그 포스트 생성기',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  %(prog)s --product-file product.json --template review
  %(prog)s --product-file product.json --template intro --output post.html
  %(prog)s --product-file product.json --template unboxing --format markdown

템플릿 종류:
  review      - 제품 리뷰 형식
  intro       - 제품 소개 형식
  comparison  - 제품 비교 형식
  unboxing    - 언박싱 리뷰 형식
        """
    )

    parser.add_argument(
        '--product-file', '-p',
        required=True,
        help='제품 정보가 담긴 JSON 파일 경로'
    )

    parser.add_argument(
        '--template', '-t',
        choices=['review', 'intro', 'comparison', 'unboxing'],
        default='review',
        help='블로그 포스트 템플릿 (기본값: review)'
    )

    parser.add_argument(
        '--format', '-f',
        choices=['html', 'markdown'],
        default='html',
        help='출력 형식 (기본값: html)'
    )

    parser.add_argument(
        '--output', '-o',
        help='출력 파일 경로 (지정하지 않으면 표준 출력)'
    )

    args = parser.parse_args()

    # 제품 정보 로드
    product = load_product_from_json(args.product_file)

    # 블로그 포스트 생성
    generator = NaverBlogGenerator()
    post = generator.generate(
        product,
        template=args.template,
        output_format=args.format
    )

    # 출력
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(post, encoding='utf-8')
        print(f"✅ 블로그 포스트가 '{args.output}' 파일로 저장되었습니다.")
    else:
        print(post)


if __name__ == '__main__':
    main()
