# rasa-llm-challenge
This repository contains a solution for the [Rasa LLM Challenge](https://rasa.com/blog/launching-the-rasa-llm-community-challenge/). The goal of this repo is to create a chatbot that can answer questions about [Rasa documentation](https://rasa.com/docs/rasa/). The solution is based on [OpenAI's GPT-3](https://openai.com/blog/openai-api/) and [GitHub API](https://docs.github.com/en/rest).
## Motivation
**Builder Productivity** is one of the main goals of Rasa.

As Rasa developers, we often find ourselves searching for answers in Rasa docs. We believe it would be great to have a chatbot that can answer questions about Rasa (integrating it on rasa.com might be interesting). This will help developers find answers to their questions faster and easier. 

Moreover, users won't need to know exactly what to search for; they can simply ask a question in natural language and receive an answer. Such a chatbot would save searching time and increase developer productivity. 

One of the advantages of this project compared to ChatGPT is that it can provide answers based on specified versions of Rasa and is not limited by a specific cutoff date.
## Usage
### Watch the demo

https://github.com/CSopiko/rasa-llm-challenge/assets/55315742/9bbff405-84dd-49c1-96bf-7a47701b25f5


### Install dependencies
python version 3.10 is used for this project. 
To install dependencies run the following commands line by line:
```bash
conda create -n llm_doc python=3.10
conda activate llm_doc
pip3 install -r requirements.txt
```
### Set up environment variables
GitHub api token is required to run the script. It can be provided as environment variable `GITHUB_TOKEN`
or as a command line argument `--github_token`.

GitHub api has a rate limit of 60 get requests per hour. If token is exhausted, the script will use stored `all_md_contents.pkl` file to continue the work. If you want updated content from gitub repo you should select `--wait_for_renewal` option `True`, it will take *1 hour* to renew the content.

It is also nacessary to provide OpenAI api key as environment variable `OPENAI_API_KEY` or as a command line argument `--openai_api_key`.

If you do not wish to pass the api keys as command line arguments, you can create `.env` file in the *src directory* of the project with the following content:
```bash
GITHUB_TOKEN=<github_token>
OPENAI_API_KEY=<openai_api_key>
```
And run the script with `--load_from_env` option `True`:
```bash
python main.py --load_from_env True
```
### Run the script
run.sh script can be used to run the script. 
```bash
conda activate llm_doc
cd src
python3 main.py --github_token <github_token> --openai_api_key <openai_api_key> --wait_for_renewal True
```

## Further improvements
As we did not have much time to work on this project, there are many improvements that can be made. Some of them are listed below: 
- [ ] Add support for rasa common errors from stackoverflow
- [ ] Add support for rasa forum questions
