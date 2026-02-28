I found a way to use the access tokens and authentication from gemini CLI to get free inference using google's internal v1 API, only requiring a google cloud account.

First, go into C:\Users*Your Username*\AppData\Roaming\npm\node_modules@google\gemini-cli\node_modules@google\gemini-cli-core\dist\src\code_assist, and open oauth2.js. There, you will find your client id and client secret.

Then, go to C:\Users\*Your Username*.gemini, then open oauth_creds.json to find your refresh token.

Put all of that into your .env using the example.

Do python -m pip install -r requirements.txt, then run python main.py.

From here, you can use this to get free inference with good rate limits to do whatever your heart desires!