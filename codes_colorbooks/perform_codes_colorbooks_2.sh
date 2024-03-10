#!/bin/bash
echo We use DOCxs in ../Data/bluebook_prepare/docx_files
echo Transcribe docx to txt
python docx_to_txt.py
echo Delete strikethrough text (used to show changes from the last Meeting)
python no_strikethrough.py
echo Manually delete missed strikethrough text, so the next code runs using no_strikethrough_manual folder
echo Concatenate footnote paragraphs (paragraphs after the footnote symbol now contain the whole footnote text)
python concatenate_pars_footnotes.py
echo Move footnotes to correct positions in the text
python move_footnotes.py
echo Drop empty paragraphs and drop footnote symbols
python empty_pars_and_footnotes.py
echo Move insets/analytical boxes (paragraphs/pages) to the end of the text
python move_inserted_pages.py
echo Add ':' after titles
python change_titles.py
echo Concatenate paragraphs, if they dont end with '.' or '."' to form correct paragraphs
python concatenate_pars.py
echo Add tags for different Alternatives mentions to every sentence
python listing_phrases.py
echo Recognize if the text 'as in Alternative X' points out or compares
python work_with_as_in.py
echo Translate the tag into the letter indicating the Alternative
python gen_mentions.py
echo Drop sentences with mentions of different Alternatives within a sentence that do not contain any info about the Alternatives
python split_sentences.py
echo Split sentences with different Alternatives mentions via GPT API, preserving the original wording
python split_with_gpt.py
echo Split the text based on Alternatives mentions
python append_mentions.py
echo Delete the text not relied to the Alternative within each stored chunk using GPT API
python cut_mentions.py
echo Store the text of different Alternatives mentions in separate files
python store_alternatives.py
echo Append drafts of Alternatives
python final_alternatives.py
