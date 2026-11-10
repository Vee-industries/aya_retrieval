"""LongMemEval's own judge prompts, for R-170's judged accuracy (measure 4).

Why: R-170 registered LongMemEval's per-type judge prompts, given to three fresh Claude judges. The
templates below are copied verbatim from ``get_anscheck_prompt`` in LongMemEval's
``src/evaluation/evaluate_qa.py`` (github.com/xiaowu0162/LongMemEval, commit ``d6dc8b5``, 24
November 2024; MIT licence, Copyright (c) 2024 Di Wu, notice in NOTICE). The official judge is
GPT-4o at temperature 0 with 10 new tokens and no system message, and a reply counts as correct
when "yes" appears in it, lower-cased. Here the judges are Claude, so the score is labelled "not
the official score".
"""

from __future__ import annotations

SOURCE = "github.com/xiaowu0162/LongMemEval src/evaluation/evaluate_qa.py @ d6dc8b5"

FACTUAL = (
    "I will give you a question, a correct answer, and a response from a model. Please answer yes"
    " if the response contains the correct answer. Otherwise, answer no. If the response is"
    " equivalent to the correct answer or contains all the intermediate steps to get the correct"
    " answer, you should also answer yes. If the response only contains a subset of the"
    " information required by the answer, answer no. \n\nQuestion: {}\n\nCorrect Answer: {}\n\n"
    "Model Response: {}\n\nIs the model response correct? Answer yes or no only."
)
TEMPORAL = (
    "I will give you a question, a correct answer, and a response from a model. Please answer yes"
    " if the response contains the correct answer. Otherwise, answer no. If the response is"
    " equivalent to the correct answer or contains all the intermediate steps to get the correct"
    " answer, you should also answer yes. If the response only contains a subset of the"
    " information required by the answer, answer no. In addition, do not penalize off-by-one"
    " errors for the number of days. If the question asks for the number of days/weeks/months,"
    " etc., and the model makes off-by-one errors (e.g., predicting 19 days when the answer is"
    " 18), the model's response is still correct. \n\nQuestion: {}\n\nCorrect Answer: {}\n\n"
    "Model Response: {}\n\nIs the model response correct? Answer yes or no only."
)
UPDATE = (
    "I will give you a question, a correct answer, and a response from a model. Please answer yes"
    " if the response contains the correct answer. Otherwise, answer no. If the response contains"
    " some previous information along with an updated answer, the response should be considered"
    " as correct as long as the updated answer is the required answer.\n\nQuestion: {}\n\n"
    "Correct Answer: {}\n\nModel Response: {}\n\nIs the model response correct? Answer yes or no"
    " only."
)
PREFERENCE = (
    "I will give you a question, a rubric for desired personalized response, and a response from"
    " a model. Please answer yes if the response satisfies the desired response. Otherwise,"
    " answer no. The model does not need to reflect all the points in the rubric. The response is"
    " correct as long as it recalls and utilizes the user's personal information correctly.\n\n"
    "Question: {}\n\nRubric: {}\n\nModel Response: {}\n\nIs the model response correct? Answer yes"
    " or no only."
)
ABSTENTION = (
    "I will give you an unanswerable question, an explanation, and a response from a model."
    " Please answer yes if the model correctly identifies the question as unanswerable. The model"
    " could say that the information is incomplete, or some other information is given but the"
    " asked information is not.\n\nQuestion: {}\n\nExplanation: {}\n\nModel Response: {}\n\n"
    "Does the model correctly identify the question as unanswerable? Answer yes or no only."
)
TEMPLATES = {
    "single-session-user": FACTUAL,
    "single-session-assistant": FACTUAL,
    "multi-session": FACTUAL,
    "temporal-reasoning": TEMPORAL,
    "knowledge-update": UPDATE,
    "single-session-preference": PREFERENCE,
}


def judge_prompt(kind: str, question: str, answer: str, response: str, abstention: bool) -> str:
    """Return LongMemEval's judge prompt for one reply, as ``get_anscheck_prompt`` builds it."""
    template = ABSTENTION if abstention else TEMPLATES[kind]
    return template.format(question, answer, response)


def judged_correct(verdict: str) -> bool:
    """Return LongMemEval's reading of a judge's reply: "yes" anywhere in it, lower-cased."""
    return "yes" in verdict.strip().lower()
