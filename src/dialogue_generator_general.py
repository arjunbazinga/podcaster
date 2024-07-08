from promptic import llm
from pydantic import ValidationError
from tenacity import retry, retry_if_exception_type
from interfaces import DialogueGenerator, Dialogue


class GeminiDialogueGenerator(DialogueGenerator):
    def __init__(self, gemini_api_key):
        self.gemini_api_key = gemini_api_key

    @retry(retry=retry_if_exception_type(ValidationError))
    @llm(model="gemini/gemini-1.5-flash", max_tokens=8192)
    def generate_dialogue(self, text: str) -> Dialogue:
        """
        Your task is to take the input text provided and turn it into an engaging, informative podcast dialogue. The input text may be messy or unstructured, as it could come from a variety of sources like PDFs or web pages. Don't worry about the formatting issues or any irrelevant information; your goal is to extract the key points and interesting facts that could be discussed in a podcast.

        Here is the input text you will be working with:

        <input_text>
        {text}
        </input_text>

        First, carefully read through the input text and identify the main topics, key points, and any interesting facts or anecdotes. Think about how you could present this information in a fun, engaging way that would be suitable for an audio podcast.

        <scratchpad>
        Brainstorm creative ways to discuss the main topics and key points you identified in the input text. Consider using analogies, storytelling techniques, or hypothetical scenarios to make the content more relatable and engaging for listeners.

        Keep in mind that your podcast should be accessible to a technical audience, who is interested but not necessarily extremely knowledgeable in the topic, so avoid using too much jargon or assuming extremely specific knowledge of the topic. If necessary, think of ways to briefly explain any complex concepts in simple terms.

        Use your imagination to fill in any gaps in the input text or to come up with thought-provoking questions that could be explored in the podcast. The goal is to create an informative and entertaining dialogue, so feel free to be creative in your approach.

        Write your brainstorming ideas and a rough outline for the podcast dialogue here. Be sure to note the key insights and takeaways you want to reiterate at the end.
        </scratchpad>

        Now that you have brainstormed ideas and created a rough outline, it's time to write the actual podcast dialogue. Aim for a natural, conversational flow between the host and any guest speakers. Incorporate the best ideas from your brainstorming session and make sure to explain any complex topics in an easy-to-understand way.

        <podcast_dialogue>
        Write your engaging, informative podcast dialogue here, based on the key points and creative ideas you came up with during the brainstorming session. Use a conversational tone and include any necessary context or explanations to make the content accessible to a general audience. Use made-up names for the hosts and guests to create a more engaging and immersive experience for listeners. Do not include any bracketed placeholders like [Host] or [Guest]. Design your output to be read aloud -- it will be directly converted into audio.

        Make the dialogue as long and detailed as possible, while still staying on topic and maintaining an engaging flow. Aim to use your full output capacity to create the longest podcast episode you can, while still communicating the key information from the input text in an entertaining way.

        At the end of the dialogue, have the host and guest speakers naturally summarize the main insights and takeaways from their discussion. This should flow organically from the conversation, reiterating the key points in a casual, conversational manner. Avoid making it sound like an obvious recap - the goal is to reinforce the central ideas one last time before signing off.
        </podcast_dialogue>
        """