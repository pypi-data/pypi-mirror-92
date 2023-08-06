from goldpot.DefaultConfig import Engines

from goldpot import *

api_key = "<enter you api key>"

def completion_sample(api_key: str):
    cec = CompletionEngineConfig(engine=Engines.DAVINCI_INSTRUCT_BETA, max_tokens=256, temperature=0.0, top_p=0.0, n=1, stream=False,
                                 logprobs=None, echo=False, stop=['####'], presence_penalty=0.0, frequency_penalty=0.0, best_of=1)

    gp = Goldpot(api_key, completion_engine_config=cec)
    # samples = ["Begin: I like\nEnd: beer.", "Begin: I like\nEnd: soccer.", "Begin: I like\nEnd: pizza."]
    samples_ci = SamplesCompletionInput(prompt_config=CompletionPromptConfig().read("conf/sample_prompt_config.yml"),
                                        end="Begin: I like\nEnd:",
                                        max_chars=7500)
    out: CompletionOutput = gp.complete(samples_ci)

    # string_ci = StringCompletionInput(text="Foo Bar!", max_chars=4)
    # out: CompletionOutput = gp.complete(string_ci)

    print(out)


if __name__ == '__main__':
    completion_sample(api_key)

