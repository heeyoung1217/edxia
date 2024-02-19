import os
import glob

# 대상 디렉토리 설정
directory_path = "data/example_map_1"

# 디렉토리 내의 모든 .txt 파일에 대해 반복 처리하는 코드입니다.
# 주어진 환경에서 실제 파일 시스템에 접근할 수 없으므로, 예시 코드를 제공합니다.

# 예시 코드
for filepath in glob.glob(os.path.join(directory_path, '*.txt')):
    # 파일을 엽니다.
    with open(filepath, 'r') as file:
        # 파일의 내용을 읽습니다.
        content = file.read()

    # 각 행을 분리하고, 각 숫자 사이에 세미콜론을 삽입합니다.
    modified_lines = []
    for line in content.split('\n'):
        modified_line = '; '.join(line.split())
        modified_lines.append(modified_line)

    # 수정된 내용을 다시 하나의 문자열로 결합합니다.
    modified_content = '\n'.join(modified_lines)

    # 변환된 내용을 새 파일에 씁니다. 여기서는 원본 파일명에 "_modified"를 추가합니다.
    new_filepath = filepath.replace('.txt', '_modified.txt')
    with open(new_filepath, 'w') as new_file:
        new_file.write(modified_content)

    print(f"File '{filepath}' has been modified and saved as '{new_filepath}'")