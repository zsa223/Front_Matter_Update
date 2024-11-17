import os
import yaml
import re
from datetime import datetime

# Markdown 파일의 front matter를 업데이트하는 스크립트
def update_front_matter(directory):
    # 디렉토리 내 모든 파일 검색
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 기존 front matter 추출
                match = re.match(r'---\n(.*?)\n---\n(.*)', content, re.DOTALL)
                if match:
                    front_matter = match.group(1)
                    body = match.group(2)

                    # YAML 파싱
                    front_matter_dict = yaml.safe_load(front_matter)

                    # 필요한 값 업데이트
                    front_matter_dict['tags'] = ['Diary']
                    front_matter_dict['categories'] = ['Diary']
                    front_matter_dict['description'] = "보호된 컨텐츠 입니다."
                    front_matter_dict['render_with_liquid'] = True

                    # title은 그대로 유지, date 필드는 title에서 추출하여 추가
                    if 'date' not in front_matter_dict:
                        title = front_matter_dict.get('title', '')
                        date_match = re.search(r'(\d{4})년 (\d{1,2})월 (\d{1,2})일', title)
                        if date_match:
                            year, month, day = date_match.groups()
                            date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)} 10:00:00 +0200"
                            front_matter_dict['date'] = date_str

                    # 수정된 front matter와 본문을 다시 합침
                    new_front_matter = yaml.dump(front_matter_dict, allow_unicode=True, default_flow_style=False)
                    new_content = f"---\n{new_front_matter}---\n{body}"

                    # 파일에 다시 쓰기
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                    print(f"Updated: {file_path}")

# 스크립트를 실행할 디렉토리 경로를 지정하세요.
directory = "/Users/jaewonkim/Desktop/무제 폴더"  # 원하는 디렉토리 경로로 변경
update_front_matter(directory)
