# FedspeakGPT
Data and replication package for the analysis of Fed Transcripts and Color Books using Python and GPT API


Soon, I will update the repository with the first draft alongside all related code and data. For now, the repository is used as a small sample of Python code.

A vital component of the project involves preprocessing Bluebooks/Tealbooks, for which 'gen_mentions.py' serves as 1 of >30 .py scripts for this purpose. This task involves extracting information about various alternatives (e.g., Alternative A, Alternative B) from the text. Due to the complex nature of the source material — where a single sentence may omit direct mentions of alternatives, refer to multiple Alternatives, include footnotes, or be interrupted by analytical boxes — this process requires careful analysis. In 'gen_mentions.py,' the code segments the text from each .txt file in the folder into discrete chunks. It then identifies references to any Alternatives, utilizing a dictionary specified in a .xlsx file, and categorizes these references as either direct mentions or comparative mentions.

Consider the sentence: 'Alternative C interprets recent developments even more favorably, stating that downside risks have diminished, as in Alternative B, and adding that “the Committee is becoming more confident that labor market conditions will continue to improve over the medium run.”' In this case, the code identifies "Alternative C," "Alternative B," and "as in Alternative B"; we need to store only "Alternative C" and "as in Alternative B" (since the third one is nested within them). We store "Alternative C" as a direct mention of Alternative C and "as in Alternative B" as a comparative mention of Alternative B.

