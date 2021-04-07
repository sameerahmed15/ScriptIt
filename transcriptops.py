import json


def transcript_parser(transcript_path):
    result = None
    with open(transcript_path, 'r') as content:
        result = json.load(content)

    result_word_alts = result['word_alternatives']
    result_length = len(result_word_alts)
    dom_elements = ''
    transcript_text = []

    for word_obj in result_word_alts:
        word_time = word_obj['start_time']
        best_word = word_obj['alternatives'][0]['word']
        best_word = best_word.replace('<', '')
        transcript_text.append(best_word)
        dom_elements += (f'<button class="transcript-btns" '
                         f'onclick=seekVideo({word_time})>'
                         f'{best_word}</button>\n')

    # Append entire transcript text based on word_alternatives
    result['transcript'] = ' '.join(transcript_text)
    with open(transcript_path, 'w', encoding='utf-8') as out:
        json.dump(result, out, ensure_ascii=False, indent=4)

    dom_elements += (f'\n<button class="button1" '
                     f'onclick="editTranscript()">Edit</button>')

    return dom_elements


def transcript_edit(transcript_path):
    result = None
    with open(transcript_path, 'r') as content:
        result = json.load(content)

    result_word_alts = result['word_alternatives']
    dom_elements = ''

    for word_obj in result_word_alts:
        word_time = word_obj['start_time']
        alt_words = word_obj['alternatives']
        num_alts = len(alt_words)
        dom_elements += f'\n<div id={word_time}>'

        if num_alts > 1:
            dom_elements += (f'\n<select name={word_time} '
                             f'onchange="editCustom(this.name, this.value)">'
                             f'\n')

            alt_words_set = set([alt_words[k]['word'] for k in range(num_alts)])

            for j in range(len(alt_words_set)):
                alt_word = alt_words[j]['word']
                if '<' in alt_word:
                    alt_word = alt_word.replace('<', '')
                dom_elements += (f'<option value="{alt_word}">'
                                 f'{alt_word}</option>\n')

            dom_elements += f'<option value="CUSTOM412">CUSTOM...</option>\n'
            dom_elements += f'</select>\n'

        elif num_alts == 1:
            input_word = alt_words[0]['word']
            dom_elements += (f'\n<input type="text" name="{word_time}" '
                             f'value="{input_word}" '
                             f'onchange="editCustom(this.name, this.value)">'
                             f'\n')

        dom_elements += f'</div>\n'

    dom_elements += (f'\n<button class="button1" '
                     f'onclick="exitEditTranscript()">Exit</button>')

    return dom_elements


def transcript_modify(transcript_path, timestamp, new_word):
    result = None
    with open(transcript_path, 'r') as content:
        result = json.load(content)

    result_word_alts = result['word_alternatives']

    for word_obj in result_word_alts:
        if timestamp == word_obj['start_time']:
            old_word = word_obj['alternatives'][0]['word']
            old_word_obj = {'word': f'{old_word}', 'confidence': 0.0}
            new_word_obj = {'word': f'{new_word}', 'confidence': 1}
            word_obj['alternatives'][0] = new_word_obj
            word_obj['alternatives'].append(old_word_obj)

    with open(transcript_path, 'w', encoding='utf-8') as out:
        json.dump(result, out, ensure_ascii=False, indent=4)

    print(f'Updated Transcript! New word: {new_word}')
    return True
