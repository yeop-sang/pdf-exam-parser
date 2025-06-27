import re
from typing import Dict, Iterator, Any, List
from modules.config_loader import load_config

# Patterns are now loaded from config, so global pre-compilation is removed.

def _parse_explanation(full_explanation: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Parses a full explanation block into a body and structured items using patterns from config."""
    
    exp_patterns = config.get('explanation_patterns', {})
    first_item_delimiter = exp_patterns.get('first_item_delimiter')
    item_split_delimiter = exp_patterns.get('item_split_delimiter')
    sub_item_pattern_str = exp_patterns.get('sub_item')

    if not all([first_item_delimiter, item_split_delimiter, sub_item_pattern_str]):
        # Fallback or error if patterns are missing
        return {'body': full_explanation.strip(), 'explanation_items': []}

    SUB_ITEM_PATTERN = re.compile(sub_item_pattern_str, re.MULTILINE | re.DOTALL)

    # Find the start of the first sub-item to separate body from items
    first_item_match = re.search(first_item_delimiter, full_explanation)
    
    if first_item_match:
        body_end_index = first_item_match.start()
        body = full_explanation[:body_end_index].strip()
        items_text_block = full_explanation[body_end_index:].strip()
    else:
        body = full_explanation.strip()
        items_text_block = ""
        
    explanation_items: List[Dict[str, str]] = []
    if items_text_block:
        # Split the block into individual items based on the start of the next item
        item_texts = re.split(item_split_delimiter, items_text_block)
        for item_text in item_texts:
            if not item_text.strip():
                continue
            
            match = SUB_ITEM_PATTERN.match(item_text.strip())
            if match:
                data = match.groupdict()
                explanation_items.append({
                    'label': data['label'],
                    'text': data['text'].strip()
                })

    return {'body': body, 'explanation_items': explanation_items}


def analyze_text(text_iterator: Iterator[str], config: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
    """
    Analyzes a stream of text page by page using regex patterns from the config.
    Handles items that may span across page breaks in a memory-efficient way.

    Args:
        text_iterator: An iterator that yields text for each page.
        config: A dictionary containing the regex patterns.

    Yields:
        A dictionary for each found item.
    """
    prob_patterns = config.get('problem_patterns', {})
    stream_pattern_str = prob_patterns.get('stream')
    final_pattern_str = prob_patterns.get('final')

    if not stream_pattern_str or not final_pattern_str:
        raise ValueError("Configuration must contain 'stream' and 'final' problem patterns.")

    STREAM_PATTERN = re.compile(stream_pattern_str, re.MULTILINE | re.DOTALL)
    FINAL_PATTERN = re.compile(final_pattern_str, re.MULTILINE | re.DOTALL)
    
    buffer = ""
    for page_text in text_iterator:
        buffer += page_text
        
        last_match_end = 0
        for match in STREAM_PATTERN.finditer(buffer):
            data = match.groupdict()
            parsed_explanation = _parse_explanation(data['explanation'], config)
            
            yield {
                "number": data['number'].strip(),
                "title": data['problem'].strip(),
                "body": parsed_explanation['body'],
                "explanation_items": parsed_explanation['explanation_items']
            }
            last_match_end = match.end()

        if last_match_end > 0:
            buffer = buffer[last_match_end:]

    if buffer:
        for match in FINAL_PATTERN.finditer(buffer):
            data = match.groupdict()
            parsed_explanation = _parse_explanation(data['explanation'], config)

            yield {
                "number": data['number'].strip(),
                "title": data['problem'].strip(),
                "body": parsed_explanation['body'],
                "explanation_items": parsed_explanation['explanation_items']
            }

if __name__ == '__main__':
    # Main block is now for demonstration and requires a config.
    # It will load the default config to run.
    try:
        config = load_config() # Assumes default config is in the correct path
        sample_text = """
01 생물의 특성
석회 동굴에서 발견되는 석순, 석주, 종유석은 탄산 칼슘 성분이
쌓여 만들어진 지형이므로 생물이 아니다.
ㄱ. 물질대사는 생물이 갖는 특성이므로 종유석이 만들어질 때는
물질대사가 일어나지 않는다.
ㄴ. 식물은 빛에너지를 이용한 광합성을 통해 필요한 양분을 만든
다. 따라서 '광합성을 통해 양분을 합성한다.'는 튤립이 갖는 특징
이다.
ㄷ. 튤립의 싹이 자라는 것은 생물의 특성인 생장에 해당하지만,
석순이 자라는 것은 생장에 해당하지 않는다.
02 세균과 바이러스
세균은 스스로 물질대사를 하지만, 바이러스는 독립적으로 물질
대사를 하지 못한다.
ㄱ. 바이러스(X)는 단백질 껍질을 갖는다.
ㄴ. 바이러스(X)는 독립적으로 물질대사를 하지 못하고, 숙주 세
포 내에서만 물질대사를 통해 증식이 가능하다.
ㄷ
.
세균과 바이러스는 모두 유전 물질인 핵산을 가지고 있으므
로, '돌연변이가 일어날 수 있다.'는 세균(A)과 바이러스(X)가 모
두 갖는 특징이다.
03 귀납적 탐구 방법
귀납적 탐구 방법은 자연 현상을 관찰하여 얻은 자료를 종합하고
분석하여 규칙성을 발견하고, 이로부터 일반적인 원리나 법칙을
이끌어내는 탐구 방법이다.
"""
        
        items = analyze_text(iter([sample_text]), config)
        # Iterators are single-use, so convert to list to count and then re-create to print
        items_list = list(items)
        print(f"Found {len(items_list)} items.") 
        
        # To print items, we use the collected list
        for item in items_list:
            print("--- ITEM ---")
            print(f"번호: {item['number']}")
            print(f"문제(제목): {item['title']}")
            print(f"본문:\n{item['body']}\n")
            if item.get('explanation_items'):
                print("해설 항목:")
                for sub_item in item['explanation_items']:
                    print(f"  {sub_item['label']}. {sub_item['text']}")
            print()
            
    except (FileNotFoundError, ValueError) as e:
        print(f"Error for __main__ execution: {e}")
        print("Please ensure 'config/default_config.yaml' exists and is valid.") 