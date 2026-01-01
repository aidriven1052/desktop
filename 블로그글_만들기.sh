#!/bin/bash

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║          🎨 네이버 블로그 포스트 생성기 🎨                ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "블로그 글 생성 프로그램을 시작합니다..."
echo ""

# Python 버전 확인
if command -v python3 &> /dev/null; then
    python3 쉬운_실행.py
elif command -v python &> /dev/null; then
    python 쉬운_실행.py
else
    echo "❌ Python이 설치되어 있지 않습니다."
    echo "Python을 먼저 설치해주세요: https://www.python.org"
fi

echo ""
read -p "종료하려면 엔터를 누르세요..."
