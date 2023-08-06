# Goldpot

## Introduction
Goldpot is a thin convenience layer on top of OpenAI's [GPT-3](https://openai.com/blog/openai-api/) Python [library](https://github.com/openai/openai-python). The name was proposed by GPT-3 itself as an answer to the question: "How to name a GPT-3 Python software library?" (well, at least it was one of the first meaningful proposals :smile:)

### Configuration:
```python
from goldpot import *

gp = Goldpot("<enter you api key here>")
```

The (data-)class Goldpot accepts two additional configuration parameters: `completion_engine_config` and `search_engine_config`.

These parameters can be used to override the default values (which are the same values as given below) by either specifying them programmatically or in the case of the completion engine config also by reading in a config file:
```python
# Completion: Programmatically
completion_engine_config = CompletionEngineConfig(engine=Engines.ADA, max_tokens=128, temperature=0.0, top_p=1.0, n=1, stream=False, logprobs=None, echo=False, stop=['####', '----', '————', '____'], presence_penalty=0.0, frequency_penalty=0.0, best_of=1)

# Completion: From config file 
completion_engine_config = CompletionEnginesConfigReader().read("conf/sample_engines_config.yml").get("TST")

# Search: Programmatically
search_engine_config = Engines.ADA
```
(See [sample_engines_config.yml](conf/sample_engines_config.yml) for a sample completion engine config file.)

### Completion:
After configuration, `Goldpot.complete()` can be used to request a completion from the GPT-3 API. It accepts a `CompletionInput` instance, which main purpose is to split long input texts in multiple input prompts i.e. you may also get multiple responses back. Goldpot takes care of this. 


All `CompletionInput` instances offer a `get_prompts()` method that splits the input into (potentially) multiple prompts. This method is mostly used internally but can be optionally called for checking the split before submitting the request (e.g. for debugging purposes). 

Currenlty two instantiable subclasses exist: 
- **StringCompletionInput:** Creates a completion input simply from a string, optionally a max length parameter (to override the default) can be passed:  
```python
ci = StringCompletionInput(text="Foo Bar!", max_chars=4)
print(ci.get_prompt())  # ['Foo ', 'Bar!']
```
- **SamplesCompletionInput:** Uses a list of samples plus initial and final part to build a completion input. They can be passed programmatically or read from a file:

```python
# Programmatically
samples = ["Begin: I like\nEnd: beer.", "Begin: I like\nEnd: soccer.", "Begin: I like\nEnd: pizza."]
ci = SamplesCompletionInput(start="Complete the following sentences:", 
                        samples=samples,
                        end="Begin: I like\nEnd:",
                        max_chars=7500)

# Reading from file
ci = SamplesCompletionInput(prompt_config=CompletionPromptConfig().read("conf/sample_prompt_config.yml"),
                             end="Begin: I like\nEnd:",
                             max_chars=7500)
```
(See [sample_prompt_config.yml](conf/sample_prompt_config.yml) for a sample completion engine config file.)

A `CompletionInput` instance can then be used in the following way:
```python
out: CompletionOutput = gp.complete(ci)
print(out.completions[0])  # first completion result
# print(out)  # complete response object
```
The response object consists of the following components:
- **completions: List[str]** -> GPT-3 completions (one per prompt)
- **completion: str** -> Concatenated completions
- **results: List[CompletionResult]** -> Class instance representation of out.output
- **prompts: List[str]** -> The prompts generated from the input
- **output: List[OpenAIObject]** -> GPT-3 raw response

### Search:
Similar to completion, `Goldpot.search()` accepts a `SearchInput` instance, again, which splits the input documents (accordingly to the provided `max_chars` and the GPT-3's 200 document limitation.)
```python
docs = ['I like pizza.', 'Python is a scripting language.', 'Socrates is an ancient philosopher.']
si = SearchInput(query="I like beer.", docs=docs, max_chars=8000)
out: SearchOutput = gp.search(si)

print(out.scores)
# {'I like pizza.': (284.211, 0.94737), 'Python is a scripting language.': (-9.132, 0.0), 'Socrates is an ancient philosopher.': (-25.988, 0.0)}

print(out.scores_sorted)
#[('I like pizza.', (284.211, 0.94737)), ('Python is a scripting language.', (-9.132, 0.0)), ('Socrates is an ancient philosopher.', (-25.988, 0.0))]
```
The response object consists of the following components:
- **scores: List[Tuple(str, Tuple[float, float])]** -> Each document is associated with two float score values: the first one is the raw GPT-3 score (from -infinity to +infinity) and a second normalized one (between 0 to 1, calculated as score.clip(0, 300)/300, as 0 and 300 are the typical low/high values for semantical dissimlar/similar query/document matches as per GPT-3 documentation.)
- **scores_sorted** -> Same as scores but sorted by GPT-3 scores
- **docs: List[str]** -> Documents used as input
- **output: List[OpenAIObject]** -> GPT-3's raw response

## Installation

```bash
$ pip install goldpot
```

## Roadmap
- More splitting/ chaining options
- Multi threading
- Monad support
- OpenAI's [DALL-E](https://openai.com/blog/dall-e/) integration
