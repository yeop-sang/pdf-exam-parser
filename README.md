# PDF 문제집 텍스트 추출 및 CSV 변환 도구

이 프로젝트는 PDF 형식의 문제집 파일에서 문제와 해설 텍스트를 지능적으로 추출하여, 구조화된 CSV 파일로 변환하는 Python 기반의 커맨드 라인 도구입니다.

## 주요 기능

- **PDF 텍스트 추출**: `PyMuPDF` 라이브러리를 사용하여 PDF에서 페이지별로 텍스트를 효율적으로 추출합니다.
- **지능형 텍스트 분석**: 정규식을 기반으로 문제 번호, 제목, 본문, 그리고 하위 항목(ㄱ, ㄴ, ㄷ)이 포함된 해설을 자동으로 인식하고 분리합니다.
- **스트리밍 처리**: 대용량 PDF 파일도 메모리 문제 없이 처리할 수 있도록 페이지 스트림 기반으로 설계되었습니다.
- **CSV 변환**: 추출하고 분석한 데이터를 체계적인 CSV 파일로 저장하여 다른 데이터 분석 도구에서 쉽게 활용할 수 있습니다.
- **유연한 설정 관리**: 정규식 패턴을 외부 YAML 설정 파일(`config/default_config.yaml`)에서 관리하므로, 다양한 문제집 레이아웃에 맞게 쉽게 수정하고 확장할 수 있습니다.
- **텍스트 전처리**: 텍스트 정제(합자 변환, 공백 정규화 등) 옵션을 제공하여 분석 정확도를 높일 수 있습니다.

## 설치 및 의존성

이 프로젝트는 Python 3.10 이상 및 `uv` 가상 환경 관리 도구가 필요합니다.

1.  **프로젝트 클론:**
    ```bash
    git clone <repository_url>
    cd pdf_crawler
    ```

2.  **가상 환경 생성 및 활성화:**
    ```bash
    uv venv
    source .venv/bin/activate
    ```

3.  **의존성 설치:**
    ```bash
    uv pip install -r requirements.txt
    ```

## 사용법

`extract_tool.py` 스크립트를 사용하여 PDF 파일을 변환할 수 있습니다.

**기본 사용법:**

```bash
python extract_tool.py <입력_PDF_경로> <출력_CSV_경로>
```

**예시:**

```bash
python extract_tool.py documents/sample.pdf results/output.csv
```

### 옵션

-   `--preprocess`: 텍스트 정제 및 전처리 기능을 활성화합니다.
    ```bash
    python extract_tool.py sample.pdf output.csv --preprocess
    ```

-   `--config <경로>`: 커스텀 설정 파일(`*.yaml`)의 경로를 지정합니다.
    ```bash
    python extract_tool.py sample.pdf output.csv --config my_custom_config.yaml
    ```

## 설정 파일

핵심적인 텍스트 분석 로직(문제 및 해설 인식)은 YAML 설정 파일에 의해 제어됩니다. 기본 설정은 `config/default_config.yaml`에 정의되어 있습니다.

필요에 따라 이 파일을 복사하여 자신만의 커스텀 설정 파일을 만들고, `--config` 옵션을 통해 사용할 수 있습니다. 이를 통해 다양한 형태의 PDF 레이아웃에 유연하게 대응할 수 있습니다.

```yaml
# config/default_config.yaml 예시

problem_patterns:
  # 다음 문제 번호가 나오기 전까지의 블록을 찾는 정규식
  stream: '^(?P<number>\d+)\s+(?P<problem>.*?)\n(?P<explanation>.*?)(?=\n\d+\s)'
  # 문서의 가장 마지막 문제를 찾는 정규식
  final: '^(?P<number>\d+)\s+(?P<problem>.*?)\n(?P<explanation>.*?)(?=\n\d+\s|\Z)'

explanation_patterns:
  # 해설 내의 ㄱ, ㄴ, ㄷ 과 같은 하위 항목을 찾는 정규식
  sub_item: '^(?P<label>[ㄱ-ㅎ])\s*\.\s*(?P<text>.*)'
  # ...
``` 