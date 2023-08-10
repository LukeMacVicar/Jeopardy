import mysql.connector
import random
import nltk
import nltk.corpus
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk

# Connect to the MySQL database
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sys"
    )

except mysql.connector.Error as e:
    print("Error connecting to MySQL:", e)
    exit(1)
try:
    cursor = conn.cursor()
    cursor.execute("SELECT Category, Question, Answer, Value FROM game_show")
    rows = cursor.fetchall()
except mysql.connector.Error as e:
    print("Error executing the query:", e)
    cursor.close()
    conn.close()
    exit(1)

# Check if there are any questions available
if not rows:
    print("No questions found in the table.")
    cursor.close()
    conn.close()
    exit(1)

# Choose a random index to select a question, answer, and category
random_index = random.randint(0, len(rows) - 1)
category, question, answer, value = rows[random_index]
def next_question():
    # Choose a random index to select a question, answer, and category
    random_index = random.randint(0, len(rows) - 1)
    category, question, answer, value = rows[random_index]

    category_label.config(text=f"{category}\n")
    value_label.config(text=f"{value}\n")
    question_label.config(text=f"{question}\n")
    result_label.config(text="")

def check_answer():
    user_response = answer_entry.get()
    player_answers = [user_response]

    # Sample actual answers
    actual_answers = [answer]

        # Preprocess and tokenize the answers
    stop_words = set(stopwords.words('english'))
    player_tokens = [word_tokenize(answer.lower()) for answer in player_answers]
    actual_tokens = [word_tokenize(answer.lower()) for answer in actual_answers]

    # Combine tokens into sentences for vectorization
    player_sentences = [" ".join(tokens) for tokens in player_tokens]
    actual_sentences = [" ".join(tokens) for tokens in actual_tokens]

    # Vectorize the sentences using TF-IDF
    vectorizer = TfidfVectorizer()
    player_vectors = vectorizer.fit_transform(player_sentences)
    actual_vectors = vectorizer.transform(actual_sentences)

    # Calculate cosine similarity between player answers and actual answers
    for i, player_vector in enumerate(player_vectors):
        similarities = cosine_similarity(player_vector, actual_vectors)
        max_similarity_index = similarities.argmax()
        max_similarity_score = similarities[0][max_similarity_index]
        threshold = 0.8  # Define a threshold to consider an answer correct
        if max_similarity_score >= threshold:
            result_label.config(text=f"Player Answer: {player_answers} - Correct\n")
        else:
            result_label.config(text=f"Corect Answer: {answer} - Incorrect\n", fg="red")
    answer_entry.delete(0,tk.END)

        
# Create the main window
root = tk.Tk()
root.title("Jeopardy Quiz")
root.geometry("800x500")
root.configure(bg="blue")

# Create labels to display the category and question
category_label = tk.Label(root, text=f"Category: {category}", font=("Arial", 14, "bold"))
category_label.pack(pady=10)

value_label = tk.Label(root, text=f"Value: {value}", font=("Arial", 12, "bold"))
value_label.pack(pady=10)

question_label = tk.Label(root, text=f"Question: {question}", font=("Arial", 12))
question_label.pack(pady=10)

check_answer_label = tk.Button(root, text="Check Answer", font=("Arial", 12), command=check_answer)
check_answer_label.pack(pady=10)

# Create an entry widget for the user's answer
answer_entry = tk.Entry(root, font=("Arial", 12))
answer_entry.pack(pady=10)

# Create a button to check the user's answer
next_question_button = tk.Button(root, text="Next Question", font=("Arial", 12), command=next_question)
next_question_button.pack(pady=10) 

root.bind('<Return>', lambda event: check_answer())

# Create a label to display the result (correct/incorrect)
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.pack(pady=10)

# Start the GUI event loop
root.mainloop()

# Close the cursor and connection
cursor.close()
conn.close()

