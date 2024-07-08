from promptic import llm
from pydantic import ValidationError
from tenacity import retry, retry_if_exception_type
from interfaces import DialogueGenerator, Dialogue


class ResearchPaperGenerator(DialogueGenerator):
    def __init__(self, gemini_api_key):
        self.gemini_api_key = gemini_api_key

    @retry(retry=retry_if_exception_type(ValidationError))
    @llm(model="gemini/gemini-1.5-flash", max_tokens=8192)
    def generate_dialogue(self, text: str) -> Dialogue:
        """
        Your task is to transform the input text into a detailed, in-depth podcast dialogue. The input text is likely from a research paper. Your goal is to create a dialogue that thoroughly covers all aspects of the paper, providing listeners with a deep understanding equivalent to having read and analyzed the paper themselves.

        <input_text>
        {text}
        </input_text>

        Carefully analyze the input text, identifying:
        1. Research question/hypothesis
        2. Methodology
        3. Key findings and results
        4. Theoretical framework
        5. Implications and conclusions
        6. Limitations and future research
        7. Novel concepts or techniques
        8. Statistical analyses
        9. Figures and tables
        10. Key citations

        <scratchpad>
        Outline a structure for the podcast that covers all these elements in depth. Consider how to explain complex concepts, address potential questions, and relate the research to broader contexts. Plan to use analogies, examples, or scenarios to illustrate difficult ideas.

        Develop three personas for the dialogue:
        1. Host: Knowledgeable moderator
        2. Lead Researcher: Expert on the paper
        3. Field Expert: Authority providing broader context

        Sketch out key discussion points and how each persona will contribute to a comprehensive exploration of the paper.
        </scratchpad>

        Now, write the podcast dialogue. Aim for a natural, conversational flow that delves deep into the paper's content. Explain technical terms and complex ideas thoroughly. The dialogue should be extensive, using your full output capacity to create a detailed discussion that leaves listeners with little need to read the original paper.

        <podcast_dialogue>
        Write your in-depth podcast dialogue here. Use real names for the host and guests, not placeholders. Structure the conversation to cover:
        1. Introduction and context
        2. Detailed exploration of methodology
        3. Comprehensive discussion of results and their implications
        4. Critical examination of limitations and future directions
        5. Broader impact and conclusions

        Ensure the host asks probing questions, the Lead Researcher provides detailed explanations, and the Field Expert offers critique and context. Anticipate and address potential listener questions throughout.

        End with a natural summary of the main insights, reinforcing key points without making it sound like an obvious recap.

        Remember, the goal is to create a dialogue so comprehensive that listeners gain a deep understanding of the paper, equivalent to having read and analyzed it themselves.
        </podcast_dialogue>
        """
