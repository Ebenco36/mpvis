from src.Feedbacks.services import FeedbackService
from src.Training.models import Question, Category, Answer
from database.db import db
from src.User.service import UserService

def addDefaultAdmin():
    UserService.create_user(
        "Admin admin", 
        "08299938839", 
        "Admin1", 
        "admin01@gmail.com", 
        "password", 
        True, 
        True
    )
    print("Admin User has been created.")

def addFeedbackQuestions():
    data = [
        {
            "question_text": "The interface made a positive first impression on me.",
            "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
        },
        {
            "question_text": "I found it easy to navigate and find what I was looking for.",
            "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
        },
        {
            "question_text": "The layout and organization of elements are intuitive.",
            "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
        },
        {
            "question_text": "The colors and fonts are visually appealing and easy to read.",
            "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
        },
        {
            "question_text": "The interface responds well on different devices.",
            "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
        },
        {
            "question_text": "Interactive elements (buttons, forms, etc.) are easy to use.",
            "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
        },
        {
            "question_text": "The interface has acceptable loading times.",
            "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
        },
        {
            "question_text": "The content is clear and easy to understand.",
            "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
        },
        {
            "question_text": "The calls-to-action are clear and compelling.",
            "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
        },
        {
            "question_text": "Error messages are clear and helpful.",
            "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
        },
        {
            "question_text": "The interface is accessible for users with disabilities.",
            "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
        },
        {
            "question_text": "The interface provides a personalized experience.",
            "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
        },
        {
            "question_text": "The feedback system is helpful.",
            "options": ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
        },
        {
            "question_text": "On a scale of 1 to 10, how satisfied are you with the overall user experience?",
            "options": [str(i) for i in range(1, 11)]
        },
        {
            "question_text": "What specific suggestions do you have for improving the UI/UX?",
            "options": []  # Open-ended question, no predefined options
        }
    ]

    results = FeedbackService.update_or_create_questions(data)
    

def addQuestion():
    questions_data = [
        {
            "category": "Introduction",
            "title": "Understanding the Basics",
            "image": "cell_membrane_image.jpg",
            "questions": [
                {
                    "text": "What role does the cell membrane play in maintaining the stability and functionality of a cell?",
                    "options": [
                        {"text": "A. Structural support.", "is_correct": False},
                        {"text": "B. Energy production.", "is_correct": False},
                        {"text": "C. Waste elimination.", "is_correct": False},
                        {"text": "D. All of the above.", "is_correct": True},
                    ]
                },
                {
                    "text": "How do membrane proteins contribute to the overall function of the cell membrane?",
                    "options": [
                        {"text": "A. Facilitate cell communication.", "is_correct": False},
                        {"text": "B. Aid in nutrient transport.", "is_correct": False},
                        {"text": "C. Contribute to cell structure.", "is_correct": False},
                        {"text": "D. All of the above.", "is_correct": True},
                    ]
                },
                {
                    "text": "Why might studying enriched membrane proteins be significant in understanding cellular processes?",
                    "options": [
                        {"text": "A. Higher abundance.", "is_correct": False},
                        {"text": "B. Unique functions.", "is_correct": False},
                        {"text": "C. Associated with diseases.", "is_correct": False},
                        {"text": "D. All of the above.", "is_correct": True},
                    ]
                },
                {
                    "text": "What distinguishes 'enriched' membrane proteins from others in terms of their roles and significance?",
                    "options": [
                        {"text": "A. Higher abundance.", "is_correct": False},
                        {"text": "B. Unique functions.", "is_correct": False},
                        {"text": "C. Associated with diseases.", "is_correct": False},
                        {"text": "D. All of the above.", "is_correct": True},
                    ]
                },
            ]
        },
        {
            "category": "Understanding Data",
            "title": "Data Collection",
            "image": "protein_data_points.jpg",
            "questions": [
                {
                    "text": "What characteristics of enriched membrane proteins should be considered during the data collection process?",
                    "options": [
                        {"text": "A. Structural information.", "is_correct": False},
                        {"text": "B. Experimental results.", "is_correct": False},
                        {"text": "C. Various characteristics.", "is_correct": False},
                        {"text": "D. All of the above.", "is_correct": True},
                    ]
                },
                {
                    "text": "In the dataset, what specific details about enriched membrane proteins can be extracted from individual columns?",
                    "options": [
                        {"text": "A. Structural information.", "is_correct": False},
                        {"text": "B. Experimental results.", "is_correct": False},
                        {"text": "C. Various characteristics.", "is_correct": False},
                        {"text": "D. All of the above.", "is_correct": True},
                    ]
                },
                {
                    "text": "How might experimental data contribute to a comprehensive understanding of enriched membrane proteins?",
                    "options": [
                        {"text": "A. Providing insights into protein structure.", "is_correct": False},
                        {"text": "B. Revealing functional roles.", "is_correct": False},
                        {"text": "C. Both A and B.", "is_correct": True},
                        {"text": "D. Neither A nor B.", "is_correct": False},
                    ]
                },
                {
                    "text": "Why is it crucial to consider both structural and functional aspects of enriched membrane proteins in the dataset?",
                    "options": [
                        {"text": "A. To ensure data completeness.", "is_correct": False},
                        {"text": "B. To gain a holistic understanding.", "is_correct": True},
                        {"text": "C. Because it's a common practice.", "is_correct": False},
                        {"text": "D. There's no need to consider both aspects.", "is_correct": False},
                    ]
                },
            ]
        },
        {
            "category": "Introducing Machine Learning",
            "title": "Training the Model",
            "image": "training_flowchart.jpg",
            "questions": [
                {
                    "text": "How can machine learning models be trained to recognize important patterns in enriched membrane proteins?",
                    "options": [
                        {"text": "A. Provide examples of important proteins.", "is_correct": True},
                        {"text": "B. Let the computer decide on its own.", "is_correct": False},
                        {"text": "C. Skip the training process.", "is_correct": False},
                    ]
                },
                {
                    "text": "Why is it necessary to use data from both MPstruct and PDB in training the machine learning model?",
                    "options": [
                        {"text": "A. To increase computational complexity.", "is_correct": False},
                        {"text": "B. To introduce redundancy.", "is_correct": False},
                        {"text": "C. To capture a diverse range of information.", "is_correct": True},
                        {"text": "D. Both A and B.", "is_correct": False},
                    ]
                },
                {
                    "text": "What challenges might arise in training a machine learning model with enriched membrane protein data, and how can they be addressed?",
                    "options": [
                        {"text": "A. Overfitting due to limited data.", "is_correct": True},
                        {"text": "B. Lack of computational resources.", "is_correct": False},
                        {"text": "C. No challenges; it's a straightforward process.", "is_correct": False},
                        {"text": "D. Both A and B.", "is_correct": False},
                    ]
                },
                {
                    "text": "How does the inclusion of data from both MPstruct and PDB enhance the model's ability to recognize significant patterns?",
                    "options": [
                        {"text": "A. By introducing noise in the data.", "is_correct": False},
                        {"text": "B. By providing complementary information.", "is_correct": True},
                        {"text": "C. There's no impact on the model's performance.", "is_correct": False},
                        {"text": "D. Both A and C.", "is_correct": False},
                    ]
                },
            ]
        },
        {
            "category": "Introducing Machine Learning",
            "title": "Predictions",
            "image": "prediction_scenario.jpg",
            "questions": [
                {
                    "text": "Once our machine learning model 'learns,' how can it predict interactions or functions of enriched membrane proteins?",
                    "options": [
                        {"text": "A. Guessing randomly.", "is_correct": False},
                        {"text": "B. Relying only on protein names.", "is_correct": False},
                        {"text": "C. Leveraging learned patterns from training data.", "is_correct": True},
                        {"text": "D. Ignoring predictions altogether.", "is_correct": False},
                    ]
                },
                {
                    "text": "In what scenarios could the predictive ability of our machine learning model be valuable in studying enriched membrane proteins?",
                    "options": [
                        {"text": "A. Identifying potential drug targets.", "is_correct": True},
                        {"text": "B. Naming proteins accurately.", "is_correct": False},
                        {"text": "C. Creating random predictions.", "is_correct": False},
                        {"text": "D. Ignoring predictions altogether.", "is_correct": False},
                    ]
                },
                {
                    "text": "How can the predictions made by the model guide further experiments or investigations in the field of enriched membrane proteins?",
                    "options": [
                        {"text": "A. By providing new research directions.", "is_correct": True},
                        {"text": "B. By limiting further experiments.", "is_correct": False},
                        {"text": "C. Predictions have no impact on experiments.", "is_correct": False},
                        {"text": "D. Ignoring predictions altogether.", "is_correct": False},
                    ]
                },
                {
                    "text": "What steps can be taken to validate and refine the predictions made by the machine learning model?",
                    "options": [
                        {"text": "A. Conducting experimental validations.", "is_correct": True},
                        {"text": "B. Ignoring predictions altogether.", "is_correct": False},
                        {"text": "C. Relying solely on predictions without validation.", "is_correct": False},
                        {"text": "D. Both A and C.", "is_correct": False},
                    ]
                },
            ]
        },
        {
            "category": "Evaluation and Improvement",
            "title": "Model Accuracy",
            "image": "confusion_matrix.jpg",
            "questions": [
                {
                    "text": "After the model makes predictions, how do we assess its accuracy?",
                    "options": [
                        {"text": "A. Ignoring accuracy assessment.", "is_correct": False},
                        {"text": "B. Using metrics like confusion matrix.", "is_correct": True},
                        {"text": "C. Asking random people for feedback.", "is_correct": False},
                        {"text": "D. Both A and C.", "is_correct": False},
                    ]
                },
                {
                    "text": "Why is it important to continually evaluate and improve the model's performance?",
                    "options": [
                        {"text": "A. Models are perfect from the beginning.", "is_correct": False},
                        {"text": "B. To adapt to changes in data patterns.", "is_correct": True},
                        {"text": "C. Ignoring model performance is acceptable.", "is_correct": False},
                        {"text": "D. Both A and C.", "is_correct": False},
                    ]
                },
                {
                    "text": "What measures can be taken to enhance the model's accuracy, especially when dealing with enriched membrane proteins?",
                    "options": [
                        {"text": "A. Increasing data quality and quantity.", "is_correct": True},
                        {"text": "B. Decreasing computational complexity.", "is_correct": False},
                        {"text": "C. Ignoring data quality.", "is_correct": False},
                        {"text": "D. Both B and C.", "is_correct": False},
                    ]
                },
                {
                    "text": "How does feedback received during the evaluation process contribute to model improvement?",
                    "options": [
                        {"text": "A. By reinforcing incorrect predictions.", "is_correct": False},
                        {"text": "B. By guiding adjustments to the model.", "is_correct": True},
                        {"text": "C. Ignoring feedback has no impact.", "is_correct": False},
                        {"text": "D. Both A and C.", "is_correct": False},
                    ]
                },
            ]
        },
        {
            "category": "Real-World Application",
            "title": "Applying Insights",
            "image": "biological_process.jpg",
            "questions": [
                {
                    "text": "Now that we have insights from our model, how can it aid in understanding diseases related to enriched membrane proteins?",
                    "options": [
                        {"text": "A. Insights have no relevance to diseases.", "is_correct": False},
                        {"text": "B. By identifying potential disease markers.", "is_correct": True},
                        {"text": "C. Ignoring disease-related applications.", "is_correct": False},
                        {"text": "D. Both A and C.", "is_correct": False},
                    ]
                },
                {
                    "text": "In drug development, how might the insights gained from analyzing enriched membrane proteins contribute?",
                    "options": [
                        {"text": "A. By slowing down the drug development process.", "is_correct": False},
                        {"text": "B. By identifying potential drug targets.", "is_correct": True},
                        {"text": "C. Ignoring drug development applications.", "is_correct": False},
                        {"text": "D. Both A and C.", "is_correct": False},
                    ]
                },
                {
                    "text": "What ethical considerations should be kept in mind when applying machine learning insights to biological research?",
                    "options": [
                        {"text": "A. Ignoring ethical considerations is acceptable.", "is_correct": False},
                        {"text": "B. Ensuring privacy of patient data.", "is_correct": True},
                        {"text": "C. Disregarding fair representation of diverse populations.", "is_correct": False},
                        {"text": "D. Both A and C.", "is_correct": False},
                    ]
                },
                {
                    "text": "How can the application of machine learning insights contribute to advancing our overall knowledge of enriched membrane proteins?",
                    "options": [
                        {"text": "A. By hindering scientific progress.", "is_correct": False},
                        {"text": "B. By providing new avenues for research.", "is_correct": True},
                        {"text": "C. Ignoring contributions to scientific knowledge.", "is_correct": False},
                        {"text": "D. Both A and C.", "is_correct": False},
                    ]
                },
            ]
        },
    ]
    try:
        # Begin a transaction
        with db.session.begin(subtransactions=True):
            # Add questions to the database
            for category_data in questions_data:
                category_name = category_data['category']
                category_desc = category_data['title']

                # Check if the category already exists
                existing_category = Category.query.filter_by(name=category_name).first()
                if existing_category:
                    print(f"Category '{category_name}' already exists. Skipping insertion.")
                    continue

                category = Category(name=category_name, description=category_desc)
                db.session.add(category)
                db.session.flush()  # Ensure that the category gets an ID before associating questions

                title = category_data['title']
                image = category_data['image']
                questions = category_data['questions']

                for question_data in questions:
                    text = question_data['text']

                    # Check if the question text already exists
                    existing_question = Question.query.filter_by(text=text).first()
                    if existing_question:
                        print(f"Question with text '{text}' already exists. Skipping insertion.")
                        continue

                    # Add the main question to the database and associate it with the category
                    main_question = Question(category=category, text=text)
                    db.session.add(main_question)
                    db.session.flush()  # Ensure that the main question gets an ID before associating options

                    # Add options to the database and associate them with the main question
                    for option_data in question_data['options']:
                        option_is_correct = option_data['is_correct']
                        option_text = option_data['text']
                        option = Answer(question=main_question, text=option_text, is_correct=option_is_correct)
                        db.session.add(option)
                        db.session.flush() 

        # Commit the transaction
        db.session.commit()
        print("Transaction committed successfully")
        # Close the database connection
        db.session.close()
    except Exception as e:
        # Rollback the transaction in case of any exception
        db.session.rollback()
        print(f"An error occurred: {str(e)}")