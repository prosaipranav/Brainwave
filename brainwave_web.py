import streamlit as st 


# to config the page layout 

st.set_page_config(page_title="BrainWave", page_icon=":sparkles:", layout="wide")

st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 2rem;   # this is to remove that blank space on top of the title 
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .center-title {
        font-size: 75px;
        font-weight: bold;
        text-align: center;
        color: #FFFFFF;
    }
    </style>
    <h1 class="center-title">✨ BrainWave ✨</h1>
    """, 
    unsafe_allow_html=True
)


def main1():
    st.divider()
    
    choices = ["Home", "Source Code", "MySQL Command", "Chatbot"]
    choice = st.sidebar.selectbox("Menu", choices)

    # Conditional rendering based on selected menu item
    if choice == "Home":
        st.header("About Us :wave:")
        st.write("""
            :red[Welcome to the Quiz Application!] Our platform provides an engaging and interactive environment for creating, managing, and playing quizzes.
            Whether you're an educator or a knowledge enthusiast, this platform offers tools to suit your needs.
            
            ### Key Features
            **Create Quizzes** - Customization and ease of use for tailored quizzes.
            
            **Manage Quizzes** - Access, view, and delete quizzes as needed.
            
            **Play Quizzes** - Immediate feedback and interactive experience.
            
            ### Our Mission
            To deliver an accessible platform for learning, training, and fun through versatile quizzes.
        """)

    elif choice == "Source Code":
        st.code("""
import streamlit as st
import mysql.connector as mysql_conn
import time as t
import ollama 
from streamlit_option_menu import option_menu

# to config the page layout 

st.set_page_config(page_title="BrainWave", page_icon=":sparkles:", layout="wide")

st.markdown(""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 2rem;   # this is to remove that blank space on top of the title 
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        "", unsafe_allow_html=True)

hide_st_style = ""
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            ""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown(
    ""
    <style>
    .center-title {
        font-size: 75px;
        font-weight: bold;
        text-align: center;
        color: #31333F;
    }
    </style>
    <h1 class="center-title">✨ BrainWave ✨</h1>
    "", 
    unsafe_allow_html=True
)

def chatbot():
    # Initialize message history if not already done
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    st.chat_message("assistant").markdown("I'm your BrainWave AI! I'm here to help you with your daily brainwave exercises!")

    # Function to generate responses from the model
    def model_res_generator():
        try:
            stream = ollama.chat(
                model="llama3",
                messages=st.session_state["messages"],
                stream=True,
            )
            for chunk in stream:
                yield chunk["message"]["content"]
        except Exception as e:
            st.error("Error generating response. Please try again.")

    # Display chat messages from history on app rerun
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything..."):
        # Add latest message to history in format {role, content}
        st.session_state["messages"].append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Show a "thinking" message while generating response
        with st.chat_message("assistant"):
            thinking_placeholder = st.empty()
            thinking_placeholder.markdown("_I'm thinking..._")

            # Generate the response
            message = ""
            for chunk in model_res_generator():
                message += chunk
                thinking_placeholder.markdown(message)  # Update with each chunk

            # Replace "thinking" message with the full response
            st.session_state["messages"].append({"role": "assistant", "content": message})


def change_color():
    st.markdown(""
    <style>
    .stProgress .st-bo {
        background-color: lightgreen;
    }
    </style>
    "", unsafe_allow_html=True)


def get_db_connection():
    return mysql_conn.connect(
        host='localhost',
        user='root',
        password='1234',
        database='quiz_project'
    )

def fetch_all_quizzes():
    mydb = get_db_connection()
    curs = mydb.cursor()
    query = "SELECT id, quiz_name FROM quiz_names"
    curs.execute(query)
    quizzes = curs.fetchall()
    curs.close()
    mydb.close()
    return quizzes

def fetch_quiz_details(quiz_id):
    mydb = get_db_connection()
    curs = mydb.cursor(dictionary=True)

    query = "SELECT qq.q_no, qq.question, qo.option_no, qo.options_ FROM quiz_questions qq " \
            "JOIN quiz_options qo ON qq.id = qo.id AND qq.q_no = qo.q_no " \
            "WHERE qq.id = %s"
    curs.execute(query, (quiz_id,))
    questions = {}
    for row in curs.fetchall():
        q_no = row['q_no']
        if q_no not in questions:
            questions[q_no] = {
                'question': row['question'],
                'options': {}
            }
        questions[q_no]['options'][row['option_no']] = row['options_']

    query = "SELECT q_no, option_no FROM quiz_answers WHERE id = %s"
    curs.execute(query, (quiz_id,))
    correct_answers = {row['q_no']: row['option_no'] for row in curs.fetchall()}

    curs.close()
    mydb.close()

    return questions, correct_answers

def reference():
    # Display input field for reference link
    reference_link = st.text_input("Please provide the reference link :point_down:(optional)")

    # Store values in session state when provided
    if reference_link:
        st.session_state.reference_link = reference_link

def display_reference(quiz_id):
    mydb = get_db_connection()
    curs = mydb.cursor()
    
    query = "SELECT reference_link FROM quiz_names WHERE id = %s"
    curs.execute(query, (quiz_id,))
    
    result = curs.fetchone()  # Fetch the result
    curs.close()
    mydb.close()

    if result is not None and result[0]:  # Check if result exists and has a value for reference_link
        reference_link = result[0]
        st.info(f"Here is a reference link for further study: :red[[Reference Link]({reference_link})]")
    else:
        st.info("No reference link provided.")

def create_quiz(quiz_name, questions):
    try:
        mydb = get_db_connection()
        curs = mydb.cursor()

        # Check if the quiz name already exists
        check_query = "SELECT id FROM quiz_names WHERE quiz_name = %s"
        curs.execute(check_query, (quiz_name,))
        existing_quiz = curs.fetchone()

        if existing_quiz:
            st.warning("Quiz name already exists. Please provide another quiz name.")
        else:
            # Insert the quiz name, MySQL will automatically assign the id
            insert_query = "INSERT INTO quiz_names(quiz_name, reference_link) VALUES (%s, %s)"
            curs.execute(insert_query, (quiz_name, st.session_state.reference_link if 'reference_link' in st.session_state else None))
            mydb.commit()

            # Fetch the last inserted quiz_id
            quiz_id = curs.lastrowid
            
            st.success("Quiz name is available.")

            # Insert the questions and their options
            for i, (question, options, correct) in enumerate(questions, start=1):
                query2 = "INSERT INTO quiz_questions (id, q_no, question) VALUES (%s, %s, %s)"
                curs.execute(query2, (quiz_id, i, question))

                for j, option in enumerate(options, start=1):
                    query3 = "INSERT INTO quiz_options (id, q_no, option_no, options_) VALUES (%s, %s, %s, %s)"
                    curs.execute(query3, (quiz_id, i, j, option))

                query4 = "INSERT INTO quiz_answers (id, q_no, option_no) VALUES (%s, %s, %s)"
                curs.execute(query4, (quiz_id, i, correct))

            mydb.commit()
            st.success("Congratulations!! Your quiz has been successfully created!!")
            
    except mysql_conn.Error as err:
        st.error(f"Error: {err}")
    finally:
        curs.close()
        mydb.close()


def delete_quiz(quiz_id):
    try:
        mydb = get_db_connection()
        curs = mydb.cursor()

        delete_answers_query = "DELETE FROM quiz_answers WHERE id = %s"
        delete_options_query = "DELETE FROM quiz_options WHERE id = %s"
        delete_questions_query = "DELETE FROM quiz_questions WHERE id = %s"
        delete_quiz_query = "DELETE FROM quiz_names WHERE id = %s"

        curs.execute(delete_answers_query, (quiz_id,))
        curs.execute(delete_options_query, (quiz_id,))
        curs.execute(delete_questions_query, (quiz_id,))
        curs.execute(delete_quiz_query, (quiz_id,))

        mydb.commit()
        st.success(f"Quiz with ID {quiz_id} has been deleted.")
    except mysql_conn.Error as err:
        st.error(f"Error: {err}")
    finally:
        curs.close()
        mydb.close()


def play_quiz(quiz_id):
    # Initialize session state for the current quiz session
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 1
        st.session_state.selected_options = {}
        st.session_state.score = 0
        st.session_state.answered_questions = set()  # Track answered questions to prevent multiple submissions
        st.session_state.progress = 0  # Initialize progress to 0

    # Fetch quiz details
    questions, correct_answers = fetch_quiz_details(quiz_id)
    total_questions = len(questions)

    current_question = st.session_state.current_question
    question_data = questions[current_question]

    # Progress bar logic
    if 'progress_value' not in st.session_state:
        st.session_state.progress_value = 0  # Initialize progress value in session state

    # Display progress bar
    progress = st.progress(st.session_state.progress_value)  # Use the progress value from session state

    # Display the current question and options
    st.write(f"**Question {current_question}:** {question_data['question']}")
    options = question_data['options']
    selected_option = st.radio("Select an option", list(options.values()), key=f"option_{current_question}")

    # Only show the Submit button if the current question hasn't been answered yet
    if current_question not in st.session_state.answered_questions:
        if st.button("Submit", key=f"submit_{current_question}"):
            correct_option = options[correct_answers[current_question]]

            # Check if the selected option is correct
            if selected_option == correct_option:
                st.success("Correct! :tada:")
                st.balloons()
                st.session_state.score += 1
            else:
                st.error(f"Incorrect! The correct answer was: {correct_option}")

            # Store the selected option for the current question and mark it as answered
            st.session_state.selected_options[current_question] = selected_option
            st.session_state.answered_questions.add(current_question)  # Mark the question as answered

            # Update the progress bar after answering
            st.session_state.progress_value = current_question / total_questions  # Calculate progress
            progress.progress(st.session_state.progress_value)  # Update the progress bar

            if current_question == total_questions:
                change_color()
    else:
        # Display a warning or info message when the user tries to submit the answer again
        st.warning("You have already submitted your answer for this question. Please proceed to the next one.")

    # Display "Next Question" button if there are more questions
    if current_question < total_questions:
        if st.button("Next Question", key=f"next_{current_question}"):
            st.session_state.current_question += 1
            st.session_state.progress_value = current_question / total_questions  # Update progress for next question
            st.rerun()  # Refresh the app to load the next question

    # Display "Finish Quiz" button after the last question
    else:
        if st.button("Finish Quiz", key=f"finish_{quiz_id}"):
            with st.spinner("Please wait.. untill we process the results :memo: of the quiz"):
                t.sleep(4)
            st.info(f":blue-background[Your Final Score: {st.session_state.score}/{total_questions}]")

            # Show reference link if the user scored less than full marks
            if st.session_state.score < total_questions:
                display_reference(quiz_id)

            # Reset the quiz session state after finishing
            st.session_state.current_question = 1
            st.session_state.selected_options = {}
            st.session_state.score = 0
            st.session_state.answered_questions = set()  # Reset answered questions
            st.session_state.progress_value = 0  # Reset progress bar to 0


if 'quizzes' not in st.session_state:
    st.session_state.quizzes = fetch_all_quizzes()

def view_quiz():
    st.write("**View Quiz Questions**")
    st.write(" ")
    st.write(" ")
    # Fetch all quizzes and store in session state if not already done
    if 'quizzes' not in st.session_state:
        st.session_state.quizzes = fetch_all_quizzes()

    quizzes = st.session_state.quizzes

    if quizzes:
        # Create a dictionary with quiz names and corresponding quiz IDs
        quiz_names = {quiz[1]: quiz[0] for quiz in quizzes}

        # Selectbox to choose a quiz by name
        selected_quiz_name = st.selectbox("Select Quiz to View Questions", list(quiz_names.keys()))

        # Show the "Show Questions" button after a quiz is selected
        if st.button("Show Questions", key=f"show_{selected_quiz_name}"):
            quiz_id = quiz_names[selected_quiz_name]
            show_questions(quiz_id)  # Display questions for the selected quiz
        st.write(" ")
    else:
        st.write("No quizzes available to view.")


def show_questions(quiz_id):
    # Fetch the questions for the selected quiz
    questions, _ = fetch_quiz_details(quiz_id)

    # Display the questions without showing the options
    for q_no, q_data in questions.items():
        
        st.info(f"**Question {q_no}:** {q_data['question']}")
        

def main():
    st.divider()
    # Initialize active choice index only once
    if "active_index" not in st.session_state:
        st.session_state.active_index = 0  # Set "Home" as default initially

    # Define choices and their respective indices
    choices = ["Home", "Create Quiz", "View Quizzes", "Delete Quiz", "Play Quiz", "Doubt"]
    choice_index_map = {choice: idx for idx, choice in enumerate(choices)}

    # Get the selected menu option and index
    choice = option_menu(
        menu_title=None,
        options=choices,
        icons=["house", "tools", "archive", "trash3", "collection play", "robot"],
        orientation="horizontal",
        key="menu_bar",
        default_index=st.session_state.active_index
    )

    # Update the active index in session state
    st.session_state.active_index = choice_index_map[choice]

    # Conditional rendering based on selected menu item
    if choice == "Home":
        st.header("About Us :wave:")
        st.write("
            :red[Welcome to the Quiz Application!] Our platform provides an engaging and interactive environment for creating, managing, and playing quizzes.
            Whether you're an educator or a knowledge enthusiast, this platform offers tools to suit your needs.
            
            ### Key Features
            **Create Quizzes** - Customization and ease of use for tailored quizzes.
            
            **Manage Quizzes** - Access, view, and delete quizzes as needed.
            
            **Play Quizzes** - Immediate feedback and interactive experience.
            
            ### Our Mission
            To deliver an accessible platform for learning, training, and fun through versatile quizzes.")
    elif choice == "Create Quiz":
        st.header("Create a New Quiz")
        quiz_name = st.text_input("Enter Name of Quiz")
        st.write("---")
        reference()
        st.write("---")
        if quiz_name:
            n = st.number_input("Total Number of Questions", min_value=1, step=1, format="%d")
            questions = []
            for i in range(1, n + 1):
                st.write("---")
                question = st.text_area(f"Enter question number {i}")
                options = []
                for j in range(1, 4 + 1):
                    option = st.text_input(f"Enter option {j} for question {i}")
                    options.append(option)
                correct_option = st.number_input(f"Enter correct option number for question {i}", min_value=1, max_value=4, format="%d")
                questions.append((question, options, correct_option))

            if st.button("Create Quiz"):
                create_quiz(quiz_name, questions)

    elif choice == "View Quizzes":
        view_quiz()
        
    elif choice == "Delete Quiz":
        st.header("Delete a Quiz")
        if st.session_state.quizzes:
            for quiz in st.session_state.quizzes:
                st.info(f"Quiz Name: :red[{quiz[1]}]")
                if st.button(f"Delete Quiz {quiz[0]}", key=f"delete_{quiz[0]}"):
                    delete_quiz(quiz[0])
                    st.session_state.quizzes = fetch_all_quizzes()  # Refresh the list of quizzes
                    st.rerun()  # Refresh the app
        else:
            st.write("No quizzes found.")

    elif choice == "Play Quiz":
        st.header("Play a Quiz")
        quizzes = st.session_state.quizzes
        if quizzes:
            quiz_names = {quiz[1]: quiz[0] for quiz in quizzes}
            quiz_name = st.selectbox("Select Quiz to Play", list(quiz_names.keys()))
            quiz_id = quiz_names[quiz_name]

            if 'start_quiz' not in st.session_state:
                st.session_state.start_quiz = False

            if not st.session_state.start_quiz:
                if st.button("Start Quiz"):
                    st.session_state.start_quiz = True
                    st.rerun()  # Refresh the app to start the quiz
            else:
                play_quiz(quiz_id)
        else:
            st.write("No quizzes available.")
    elif choice == "Doubt":
        st.session_state.active_index = 5
        st.header("Ask Questions:question: to the Chatbot :robot_face:", divider=True)
        chatbot()

# Run the main function
if __name__ == '__main__':
    main()
""")
        st.warning(""" in the st.markdown functions in the program please replace the double ' " ' with triple ' " ' """)

    elif choice == "MySQL Command":
        st.code("""
CREATE TABLE quiz_names (
    id INT AUTO_INCREMENT PRIMARY KEY,
    quiz_name VARCHAR(255) UNIQUE NOT NULL,
    reference_link TEXT
);

CREATE TABLE quiz_questions (
    id INT,
    q_no INT,
    question TEXT,
    PRIMARY KEY (id, q_no),
    FOREIGN KEY (id) REFERENCES quiz_names(id)
    ON DELETE CASCADE
);

CREATE TABLE quiz_options (
    id INT,
    q_no INT,
    option_no INT,
    options_ TEXT,
    PRIMARY KEY (id, q_no, option_no),
    FOREIGN KEY (id, q_no) REFERENCES quiz_questions(id, q_no)
    ON DELETE CASCADE
);

CREATE TABLE quiz_answers (
    id INT,
    q_no INT,
    option_no INT,
    PRIMARY KEY (id, q_no),
    FOREIGN KEY (id, q_no, option_no) REFERENCES quiz_options(id, q_no, option_no)
    ON DELETE CASCADE
);
""")
    elif choice == "Chatbot":
        st.write("in order to the chatbot you should download ollama locally in your computer. ")
        reference_link = "https://ollama.com/"
        st.info(f"Download ollama:   :red[[click here]({reference_link})] ")
        reference_link1= "https://youtu.be/d0o89z134CQ?si=jGUaRKWjIpF05cn8"
        st.info(f"Watch this video:   :red[[click here]({reference_link1})] ")
        reference_link2= "https://youtu.be/ZHZKPmzlBUY?si=UZ7vBlndv03PZStk"
        st.info(f"Watch this video:   :red[[click here]({reference_link2})] ")

# Run the main function

if __name__ == '__main__':
    main1()