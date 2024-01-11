import json
import nltk
import random
from TimaChatBot.random_responses import random_string
from TimaChatBot.getUserInput import getUserInput
from nltk.tokenize import word_tokenize
from TimaChatBot.Matching_utils import lemmatizer, lemmatize_input, enhance_required_words_matching


if not nltk.data.find('tokenizers/punkt'):
    nltk.download('punkt')

# Load JSON data
def load_conversation_data(file):
    with open(file) as BotAnswers:
        print(f"successfully Loaded '{file}'!")
        return json.load(BotAnswers)

# Store JSON data
response_data = load_conversation_data("TimaChatBot/Training.json")

# Initialize WordNet Lemmatizer

def Tokenize__input(input_string):
    return word_tokenize(input_string)

last_selected_response = None

def generate_response(user_input):

    global last_selected_response

    split_query = Tokenize__input(user_input.lower())
    matching_scores = []

    # Check if input is empty
    if user_input == "":
        return "Please say something so we can chat :("
    
    # Check if the input is very short
    if len(split_query) < 3:
        for response in response_data:
            if any(word in split_query for word in response["user_input"]):
                list_count = len(response["user_input"])
                random_item = random.randrange(list_count)
                if response["bot_response"][random_item] != last_selected_response:
                    last_selected_response = response["bot_response"][random_item]
                    return last_selected_response

        # If no direct match found, return a generic response for short input
        return "I'm not sure what to make of such a short input. Can you provide more details?"

    for response in response_data:
        response_matching = 0
        required_matching = enhance_required_words_matching(user_input, response["required_words"])

        # Amount of required words should match the required score
        if required_matching > 0:
            # Check each word the user has typed
            for word in split_query:
                # If the word is in the response, add to the score
                if word in response["user_input"]:
                    response_matching += 1
            
            # Normalize the response matching score by dividing by the length of user input
            if split_query:
                response_matching /= len(split_query)

        # Add score to list
        matching_scores.append(response_matching)

    # Find the best response and return it if they're not all 0
    best_response = max(matching_scores)
    response_index = matching_scores.index(best_response)

    if best_response != 0:
        selected_response = response_data[response_index]
        bot_responses = selected_response["bot_response"]
        list_count = len(bot_responses)
        random_item = random.randrange(list_count)
        if bot_responses[random_item] != last_selected_response:
            last_selected_response = bot_responses[random_item]
            return last_selected_response

    # If there is no good response, return a random one.
    return random_string()

while True:
    user_input = getUserInput()
    print("You:", user_input)
    print("Bot:", generate_response(user_input))
