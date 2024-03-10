import os
import re

# Author: Oleg Telegin

# Get the number of Alternatives for the dictionary
def check_for_specific_phrases(content, phrases_list):
    condition1_met = False
    condition2_met = False
    for phrase in phrases_list:
        # Create a flexible regex for the phrase to ignore spaces and newlines
        flexible_regex = create_flexible_regex(phrase)
        if re.search(flexible_regex, content, re.IGNORECASE | re.DOTALL):
            condition1_met = True
    dop_phrase = "Alternative D"
    dop_regex = create_flexible_regex(dop_phrase)
    if re.search(dop_regex, content, re.DOTALL):
        condition2_met = True

    # Both conditions must be met to return "four"
    if condition1_met and condition2_met:
        return "four"
    else:
        return "three"

# Create a regex pattern that matches the phrase with any amount of whitespace (including none)
# between each character of the phrase.
def create_flexible_regex(phrase):
    return r'\s*'.join(re.escape(char) for char in phrase) + r'\s*'

# Get phrases from txt file
def read_phrases(phrases_file_path):
    with open(phrases_file_path, 'r', encoding='utf-8') as file:
        phrases = [line.strip() for line in file.readlines()]
    return phrases

# Split the text into chunks
def split_into_chunks_and_sentences(content, phrases, alternatives_indicator):
    delimiter_pattern = r'(\(Font Size: [^\)]+\)\s)'
    chunks = re.split(delimiter_pattern, content)[1:]
    processed_text = ""
    exclusion_pattern = re.compile(r'^\{' + alternatives_indicator + ',(not)?first\}(?:\s+\d+\.)?$')

    for i, chunk in enumerate(chunks):
        if i % 2 == 0:
            continue  # Skip delimiters
        sentences = re.split(r'(?<=\.)\s|(?<=\.")\s|(?<=\.”)\s|(?<=\.)\n|(?<=\.")\n|(?<=\.”)\n', chunk)  # Splitting by '.' or '."'

        for j, sentence in enumerate(sentences):
            if j == 0:
                tags = ["first"]
            else:
                # Check if the previous sentence ends with "number."
                if re.match(r'\d+\.$', sentences[j - 1].strip()):
                    tags = ["first"]
                else:
                    tags = ["notfirst"]
            for phrase_index, phrase in enumerate(phrases, start=1):
                flexible_regex = create_flexible_regex(phrase)
                for match in re.finditer(flexible_regex, sentence):
                    tags.append(str(phrase_index))
            tag_string = "{" + alternatives_indicator + "," + ",".join(tags) + "} " + sentence + "\n"
            if not exclusion_pattern.match(tag_string.strip()):
                processed_text += tag_string
    return processed_text

# Process all files in a folder
def process_folder(input_folder, output_folder, phrases_file_a, phrases_file_b, specific_phrases):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)

            with open(input_file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            alternatives_indicator = check_for_specific_phrases(content, specific_phrases)
            phrases_file_path = phrases_file_a if alternatives_indicator == "four" else phrases_file_b
            phrases = read_phrases(phrases_file_path)
            processed_text = split_into_chunks_and_sentences(content, phrases, alternatives_indicator)

            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(processed_text)
            print(f"Processed {filename}")

# Paths and function call
input_folder = '../Data/bluebook_prepare/concatenate_pars'
output_folder = '../Data/bluebook_prepare/listing_phrases'
phrases_file_a = '../Data/bluebook_prepare/list_of_phrases_for_four_alternatives.txt'
phrases_file_b = '../Data/bluebook_prepare/list_of_phrases_for_three_alternatives.txt'
specific_phrases = ["four alternatives", "four policy alternatives", "four main policy alternatives"]

process_folder(input_folder, output_folder, phrases_file_a, phrases_file_b, specific_phrases)
