# rasa-llm-challenge
This repository contains a solution for the [Rasa LLM Challenge](https://rasa.com/blog/launching-the-rasa-llm-community-challenge/). The goal of this repo is to create a chatbot that can answer questions about [Rasa documentation](https://rasa.com/docs/rasa/). The solution is based on [OpenAI's GPT-3](https://openai.com/blog/openai-api/) and [GitHub API](https://docs.github.com/en/rest).
## Motivation
**Builder Productivity** is one of the main goals of Rasa. The goal of this project is to create a chatbot that can answer questions about Rasa documentation. This will help Rasa developers to find answers to their questions faster and easier.
## Usage
GitHub api token is required to run the script. It can be provided as environment variable `GITHUB_TOKEN`
or as a command line argument `--github_token`.

GitHub api has a rate limit of 60 get requests per hour. If token is exhausted, the script will use stored `all_md_contents.pkl` file to continue the work. If you want updated content from gitub repo you should select `--wait_for_renewal` option `True`, it will take 1 hour to renew the content.

It is also nacessary to provide OpenAI api key as environment variable `OPENAI_API_KEY` or as a command line argument `--openai_api_key`.

```bash
python3 src/main.py --github_token <github_token> --openai_api_key <openai_api_key>
```

If you do not wish to pass the api keys as command line arguments, you can create `.env` file in the src directory of the project with the following content:
```bash
GITHUB_TOKEN=<github_token>
OPENAI_API_KEY=<openai_api_key>
```


## Further improvements
- [] Add support for nlu data analysis
- [] Add support for generating nlu data