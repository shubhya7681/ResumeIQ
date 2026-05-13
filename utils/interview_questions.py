"""
ResumeIQ - Interview Question Generator
Generates skill-based interview questions for detected skills.
"""

# Curated interview questions database organized by skill
INTERVIEW_QUESTIONS = {
    'Python': [
        {'question': 'What is list comprehension in Python?', 'difficulty': 'Easy'},
        {'question': 'Explain the difference between list and tuple.', 'difficulty': 'Easy'},
        {'question': 'What are decorators in Python?', 'difficulty': 'Medium'},
        {'question': 'Explain the GIL (Global Interpreter Lock).', 'difficulty': 'Hard'},
        {'question': 'What is the difference between deep copy and shallow copy?', 'difficulty': 'Medium'},
        {'question': 'How does memory management work in Python?', 'difficulty': 'Hard'},
        {'question': 'What are generators and how do they differ from iterators?', 'difficulty': 'Medium'},
        {'question': 'Explain *args and **kwargs.', 'difficulty': 'Easy'},
    ],
    'Java': [
        {'question': 'What is the difference between JDK, JRE, and JVM?', 'difficulty': 'Easy'},
        {'question': 'Explain OOP concepts in Java.', 'difficulty': 'Easy'},
        {'question': 'What is the difference between HashMap and HashTable?', 'difficulty': 'Medium'},
        {'question': 'Explain multithreading in Java.', 'difficulty': 'Hard'},
        {'question': 'What is the Java Memory Model?', 'difficulty': 'Hard'},
        {'question': 'Explain the SOLID principles.', 'difficulty': 'Medium'},
    ],
    'JavaScript': [
        {'question': 'What is the difference between let, var, and const?', 'difficulty': 'Easy'},
        {'question': 'Explain closures in JavaScript.', 'difficulty': 'Medium'},
        {'question': 'What is the event loop?', 'difficulty': 'Hard'},
        {'question': 'Explain prototypal inheritance.', 'difficulty': 'Medium'},
        {'question': 'What are Promises and async/await?', 'difficulty': 'Medium'},
        {'question': 'What is hoisting in JavaScript?', 'difficulty': 'Easy'},
    ],
    'SQL': [
        {'question': 'What is a JOIN? Explain different types.', 'difficulty': 'Easy'},
        {'question': 'What is the difference between WHERE and HAVING?', 'difficulty': 'Easy'},
        {'question': 'Explain normalization and its forms.', 'difficulty': 'Medium'},
        {'question': 'What are indexes and how do they improve performance?', 'difficulty': 'Medium'},
        {'question': 'Write a query to find the second highest salary.', 'difficulty': 'Medium'},
        {'question': 'What is a subquery vs a CTE?', 'difficulty': 'Medium'},
    ],
    'React': [
        {'question': 'What is the Virtual DOM?', 'difficulty': 'Easy'},
        {'question': 'Explain the component lifecycle.', 'difficulty': 'Medium'},
        {'question': 'What are React Hooks? Explain useState and useEffect.', 'difficulty': 'Medium'},
        {'question': 'What is the difference between state and props?', 'difficulty': 'Easy'},
        {'question': 'How does React reconciliation work?', 'difficulty': 'Hard'},
        {'question': 'What is Redux and when would you use it?', 'difficulty': 'Medium'},
    ],
    'Node.js': [
        {'question': 'What is Node.js and how does it work?', 'difficulty': 'Easy'},
        {'question': 'Explain the event-driven architecture.', 'difficulty': 'Medium'},
        {'question': 'What is middleware in Express.js?', 'difficulty': 'Easy'},
        {'question': 'How does Node.js handle concurrency?', 'difficulty': 'Hard'},
        {'question': 'What is the difference between process.nextTick() and setImmediate()?', 'difficulty': 'Hard'},
    ],
    'Machine Learning': [
        {'question': 'What is the bias-variance tradeoff?', 'difficulty': 'Medium'},
        {'question': 'Explain the difference between supervised and unsupervised learning.', 'difficulty': 'Easy'},
        {'question': 'What is overfitting and how do you prevent it?', 'difficulty': 'Medium'},
        {'question': 'Explain cross-validation.', 'difficulty': 'Medium'},
        {'question': 'What is gradient descent?', 'difficulty': 'Medium'},
        {'question': 'What are precision, recall, and F1 score?', 'difficulty': 'Medium'},
        {'question': 'Explain the Random Forest algorithm.', 'difficulty': 'Medium'},
    ],
    'Deep Learning': [
        {'question': 'What is a neural network?', 'difficulty': 'Easy'},
        {'question': 'Explain backpropagation.', 'difficulty': 'Hard'},
        {'question': 'What are CNNs and where are they used?', 'difficulty': 'Medium'},
        {'question': 'What is the vanishing gradient problem?', 'difficulty': 'Hard'},
        {'question': 'Explain the difference between RNN, LSTM, and GRU.', 'difficulty': 'Hard'},
        {'question': 'What are transformers in deep learning?', 'difficulty': 'Hard'},
    ],
    'Data Analysis': [
        {'question': 'What is exploratory data analysis (EDA)?', 'difficulty': 'Easy'},
        {'question': 'How do you handle missing data?', 'difficulty': 'Medium'},
        {'question': 'What is the difference between correlation and causation?', 'difficulty': 'Easy'},
        {'question': 'Explain common data visualization techniques.', 'difficulty': 'Easy'},
        {'question': 'What is A/B testing?', 'difficulty': 'Medium'},
    ],
    'Flask': [
        {'question': 'What is Flask and how does it differ from Django?', 'difficulty': 'Easy'},
        {'question': 'Explain Flask routing and decorators.', 'difficulty': 'Easy'},
        {'question': 'How do you handle forms in Flask?', 'difficulty': 'Medium'},
        {'question': 'What is Jinja2 templating?', 'difficulty': 'Easy'},
        {'question': 'How do you implement authentication in Flask?', 'difficulty': 'Medium'},
    ],
    'Django': [
        {'question': 'What is the Django MTV architecture?', 'difficulty': 'Easy'},
        {'question': 'Explain Django ORM.', 'difficulty': 'Medium'},
        {'question': 'What is Django middleware?', 'difficulty': 'Medium'},
        {'question': 'How does Django handle security?', 'difficulty': 'Medium'},
        {'question': 'What are Django signals?', 'difficulty': 'Hard'},
    ],
    'Docker': [
        {'question': 'What is Docker and why is it used?', 'difficulty': 'Easy'},
        {'question': 'What is the difference between an image and a container?', 'difficulty': 'Easy'},
        {'question': 'Explain Docker Compose.', 'difficulty': 'Medium'},
        {'question': 'What is a Dockerfile and its key instructions?', 'difficulty': 'Medium'},
        {'question': 'How does Docker networking work?', 'difficulty': 'Hard'},
    ],
    'AWS': [
        {'question': 'What are the core AWS services?', 'difficulty': 'Easy'},
        {'question': 'Explain EC2 instance types.', 'difficulty': 'Medium'},
        {'question': 'What is S3 and its storage classes?', 'difficulty': 'Medium'},
        {'question': 'Explain IAM roles and policies.', 'difficulty': 'Medium'},
        {'question': 'What is a VPC?', 'difficulty': 'Hard'},
    ],
    'Git': [
        {'question': 'What is the difference between git merge and git rebase?', 'difficulty': 'Medium'},
        {'question': 'Explain the Git branching strategy.', 'difficulty': 'Medium'},
        {'question': 'What is a pull request?', 'difficulty': 'Easy'},
        {'question': 'How do you resolve merge conflicts?', 'difficulty': 'Medium'},
    ],
    'HTML': [
        {'question': 'What are semantic HTML elements?', 'difficulty': 'Easy'},
        {'question': 'Explain the difference between block and inline elements.', 'difficulty': 'Easy'},
        {'question': 'What is the DOM?', 'difficulty': 'Easy'},
        {'question': 'What are HTML5 APIs?', 'difficulty': 'Medium'},
    ],
    'CSS': [
        {'question': 'What is the CSS box model?', 'difficulty': 'Easy'},
        {'question': 'Explain Flexbox and Grid layout.', 'difficulty': 'Medium'},
        {'question': 'What is the difference between position absolute, relative, and fixed?', 'difficulty': 'Easy'},
        {'question': 'Explain CSS specificity.', 'difficulty': 'Medium'},
    ],
    'C++': [
        {'question': 'What is the difference between C and C++?', 'difficulty': 'Easy'},
        {'question': 'Explain pointers and references.', 'difficulty': 'Medium'},
        {'question': 'What are virtual functions?', 'difficulty': 'Medium'},
        {'question': 'Explain RAII (Resource Acquisition Is Initialization).', 'difficulty': 'Hard'},
    ],
    'MongoDB': [
        {'question': 'What is a NoSQL database?', 'difficulty': 'Easy'},
        {'question': 'Explain the difference between SQL and MongoDB.', 'difficulty': 'Easy'},
        {'question': 'What is sharding in MongoDB?', 'difficulty': 'Hard'},
        {'question': 'Explain aggregation pipeline.', 'difficulty': 'Medium'},
    ],
    'Excel': [
        {'question': 'What is the difference between VLOOKUP and HLOOKUP?', 'difficulty': 'Easy'},
        {'question': 'Explain pivot tables.', 'difficulty': 'Easy'},
        {'question': 'What are macros in Excel?', 'difficulty': 'Medium'},
        {'question': 'Explain INDEX-MATCH vs VLOOKUP.', 'difficulty': 'Medium'},
    ],
    'Power BI': [
        {'question': 'What is Power BI and its components?', 'difficulty': 'Easy'},
        {'question': 'What is DAX?', 'difficulty': 'Medium'},
        {'question': 'Explain data modeling in Power BI.', 'difficulty': 'Medium'},
        {'question': 'How do you create calculated columns vs measures?', 'difficulty': 'Medium'},
    ],
    'Tableau': [
        {'question': 'What are the different types of charts in Tableau?', 'difficulty': 'Easy'},
        {'question': 'What is a calculated field?', 'difficulty': 'Easy'},
        {'question': 'Explain LOD expressions.', 'difficulty': 'Hard'},
        {'question': 'What is the difference between Tableau Desktop and Server?', 'difficulty': 'Medium'},
    ],
}


def generate_questions(found_skills, max_per_skill=4):
    """
    Generate interview questions based on detected skills.
    Returns a dictionary mapping skill names to their questions.
    """
    if not found_skills:
        return {}

    result = {}
    for skill in found_skills:
        # Normalize skill name for lookup
        skill_key = skill.strip()
        # Try exact match first, then case-insensitive
        questions = INTERVIEW_QUESTIONS.get(skill_key)
        if not questions:
            for key in INTERVIEW_QUESTIONS:
                if key.lower() == skill_key.lower():
                    questions = INTERVIEW_QUESTIONS[key]
                    skill_key = key
                    break

        if questions:
            result[skill_key] = questions[:max_per_skill]

    return result


def get_all_question_categories():
    """Return all available question categories."""
    return list(INTERVIEW_QUESTIONS.keys())
