"""
ResumeIQ - Skill Detection Engine
Detects technical and soft skills from resume text using pattern matching.
"""
import re

# Comprehensive skill database organized by category
SKILL_DATABASE = {
    'Programming Languages': [
        'Python', 'Java', 'C++', 'C#', 'C', 'JavaScript', 'TypeScript',
        'Ruby', 'PHP', 'Swift', 'Kotlin', 'Go', 'Rust', 'Scala',
        'R', 'MATLAB', 'Perl', 'Dart', 'Lua', 'Assembly'
    ],
    'Web Technologies': [
        'HTML', 'CSS', 'JavaScript', 'TypeScript', 'React', 'Angular',
        'Vue.js', 'Next.js', 'Node.js', 'Express.js', 'jQuery',
        'Bootstrap', 'Tailwind', 'SASS', 'LESS', 'Webpack',
        'REST API', 'GraphQL', 'WebSocket', 'Ajax'
    ],
    'Frameworks & Libraries': [
        'Flask', 'Django', 'FastAPI', 'Spring Boot', 'Spring',
        'React', 'Angular', 'Vue.js', 'Next.js', 'Express.js',
        'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn',
        'Pandas', 'NumPy', 'Matplotlib', 'Seaborn',
        'React Native', 'Flutter', 'Electron',
        '.NET', 'ASP.NET', 'Laravel', 'Ruby on Rails'
    ],
    'Data Science & ML': [
        'Machine Learning', 'Deep Learning', 'Data Analysis',
        'Data Science', 'Natural Language Processing', 'NLP',
        'Computer Vision', 'Neural Networks', 'Random Forest',
        'Decision Tree', 'Regression', 'Classification',
        'Clustering', 'Reinforcement Learning', 'Transfer Learning',
        'Feature Engineering', 'Data Mining', 'Big Data',
        'Statistical Analysis', 'A/B Testing', 'Data Visualization',
        'Predictive Modeling', 'Time Series'
    ],
    'Databases': [
        'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'SQLite',
        'Oracle', 'Redis', 'Cassandra', 'DynamoDB',
        'Elasticsearch', 'Firebase', 'MariaDB',
        'Microsoft SQL Server', 'Neo4j'
    ],
    'Cloud & DevOps': [
        'AWS', 'Azure', 'Google Cloud', 'GCP', 'Docker',
        'Kubernetes', 'Jenkins', 'CI/CD', 'Terraform',
        'Ansible', 'Linux', 'Unix', 'Nginx', 'Apache',
        'Heroku', 'Vercel', 'Netlify', 'DigitalOcean'
    ],
    'Tools & Platforms': [
        'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Jira',
        'Confluence', 'Slack', 'VS Code', 'IntelliJ',
        'Eclipse', 'Postman', 'Swagger', 'Figma',
        'Adobe XD', 'Photoshop', 'Illustrator',
        'Excel', 'Power BI', 'Tableau', 'Looker',
        'Jupyter', 'Google Colab', 'Anaconda'
    ],
    'Soft Skills': [
        'Leadership', 'Communication', 'Teamwork', 'Problem Solving',
        'Critical Thinking', 'Time Management', 'Adaptability',
        'Creativity', 'Project Management', 'Agile', 'Scrum',
        'Public Speaking', 'Negotiation', 'Mentoring',
        'Collaboration', 'Analytical Thinking'
    ]
}

# All unique skills flattened
ALL_SKILLS = set()
for category_skills in SKILL_DATABASE.values():
    ALL_SKILLS.update(category_skills)


def detect_skills(text):
    """
    Detect skills present in the resume text.
    Returns found skills, missing common skills, and suggested skills.
    """
    if not text:
        return {'found': [], 'missing': [], 'suggested': [], 'by_category': {}}

    text_lower = text.lower()
    found_skills = []
    found_by_category = {}

    for category, skills in SKILL_DATABASE.items():
        found_in_category = []
        for skill in skills:
            # Create regex pattern for whole-word matching
            # Handle special characters in skill names
            escaped_skill = re.escape(skill)
            pattern = r'(?i)\b' + escaped_skill + r'\b'
            # Special handling for short skill names to avoid false matches
            if len(skill) <= 2:
                pattern = r'(?i)(?<![a-zA-Z])' + escaped_skill + r'(?![a-zA-Z])'
            if re.search(pattern, text):
                if skill not in found_skills:
                    found_skills.append(skill)
                    found_in_category.append(skill)
        if found_in_category:
            found_by_category[category] = found_in_category

    # Determine missing common/important skills
    common_skills = [
        'Python', 'Java', 'JavaScript', 'SQL', 'HTML', 'CSS',
        'Git', 'React', 'Node.js', 'Docker', 'AWS',
        'Machine Learning', 'Data Analysis', 'Excel',
        'Linux', 'Agile', 'REST API'
    ]
    missing_skills = [s for s in common_skills if s not in found_skills]

    # Suggest skills based on what's found
    suggested_skills = _suggest_skills(found_skills)

    return {
        'found': found_skills,
        'missing': missing_skills,
        'suggested': suggested_skills,
        'by_category': found_by_category
    }


def _suggest_skills(found_skills):
    """Suggest complementary skills based on detected skills."""
    suggestions = []
    found_set = set(s.lower() for s in found_skills)

    # Skill suggestion rules
    suggestion_rules = {
        'python': ['Flask', 'Django', 'FastAPI', 'Pandas', 'NumPy'],
        'java': ['Spring Boot', 'Maven', 'Hibernate', 'JUnit'],
        'javascript': ['React', 'Node.js', 'TypeScript', 'Next.js'],
        'react': ['Redux', 'TypeScript', 'Next.js', 'Jest'],
        'machine learning': ['TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas'],
        'data analysis': ['Pandas', 'Excel', 'Power BI', 'Tableau', 'SQL'],
        'sql': ['PostgreSQL', 'MongoDB', 'Redis', 'Database Design'],
        'docker': ['Kubernetes', 'CI/CD', 'Jenkins', 'AWS'],
        'aws': ['Docker', 'Terraform', 'Lambda', 'S3'],
        'html': ['CSS', 'JavaScript', 'Bootstrap', 'React'],
        'flask': ['SQLAlchemy', 'REST API', 'Jinja2', 'PostgreSQL'],
        'node.js': ['Express.js', 'MongoDB', 'REST API', 'Socket.io'],
    }

    for skill in found_skills:
        skill_lower = skill.lower()
        if skill_lower in suggestion_rules:
            for suggested in suggestion_rules[skill_lower]:
                if suggested.lower() not in found_set and suggested not in suggestions:
                    suggestions.append(suggested)

    return suggestions[:10]  # Return top 10 suggestions


def get_skill_categories():
    """Return the skill database categories."""
    return SKILL_DATABASE
