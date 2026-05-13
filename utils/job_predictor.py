"""
ResumeIQ - Job Role Prediction Module
Predicts suitable job roles based on detected skills using rule-based matching.
"""


# Job role profiles - mapping roles to required/preferred skills
JOB_PROFILES = {
    'Data Analyst': {
        'required': ['sql', 'excel', 'data analysis'],
        'preferred': ['python', 'power bi', 'tableau', 'r', 'statistical analysis',
                      'pandas', 'data visualization', 'matplotlib'],
        'description': 'Analyze data to help organizations make informed decisions.',
        'avg_salary': '$65,000 - $95,000',
        'demand': 'High'
    },
    'Data Scientist': {
        'required': ['python', 'machine learning', 'sql'],
        'preferred': ['deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
                      'pandas', 'numpy', 'r', 'statistical analysis',
                      'natural language processing', 'data visualization'],
        'description': 'Build predictive models and extract insights from complex datasets.',
        'avg_salary': '$90,000 - $140,000',
        'demand': 'Very High'
    },
    'ML Engineer': {
        'required': ['python', 'machine learning'],
        'preferred': ['deep learning', 'tensorflow', 'pytorch', 'docker',
                      'aws', 'kubernetes', 'mlops', 'scikit-learn',
                      'neural networks', 'computer vision', 'nlp'],
        'description': 'Design and deploy machine learning systems at scale.',
        'avg_salary': '$100,000 - $160,000',
        'demand': 'Very High'
    },
    'Frontend Developer': {
        'required': ['html', 'css', 'javascript'],
        'preferred': ['react', 'angular', 'vue.js', 'typescript', 'next.js',
                      'bootstrap', 'tailwind', 'sass', 'figma', 'webpack',
                      'responsive design', 'ui/ux'],
        'description': 'Create engaging user interfaces and web experiences.',
        'avg_salary': '$70,000 - $120,000',
        'demand': 'High'
    },
    'Backend Developer': {
        'required': ['python', 'sql'],
        'preferred': ['flask', 'django', 'node.js', 'express.js', 'java',
                      'spring boot', 'rest api', 'docker', 'postgresql',
                      'mongodb', 'redis', 'aws', 'microservices'],
        'description': 'Build server-side logic, APIs, and database integrations.',
        'avg_salary': '$80,000 - $130,000',
        'demand': 'High'
    },
    'Full Stack Developer': {
        'required': ['html', 'css', 'javascript'],
        'preferred': ['react', 'node.js', 'python', 'sql', 'mongodb',
                      'express.js', 'flask', 'django', 'docker', 'git',
                      'rest api', 'typescript', 'aws'],
        'description': 'Develop both frontend and backend of web applications.',
        'avg_salary': '$85,000 - $140,000',
        'demand': 'Very High'
    },
    'Python Developer': {
        'required': ['python'],
        'preferred': ['flask', 'django', 'fastapi', 'sql', 'rest api',
                      'docker', 'git', 'postgresql', 'mongodb',
                      'pandas', 'celery', 'redis', 'aws'],
        'description': 'Develop applications and systems using Python.',
        'avg_salary': '$75,000 - $125,000',
        'demand': 'High'
    },
    'Java Developer': {
        'required': ['java'],
        'preferred': ['spring boot', 'spring', 'sql', 'hibernate',
                      'microservices', 'docker', 'aws', 'rest api',
                      'maven', 'jenkins', 'kubernetes', 'oracle'],
        'description': 'Build enterprise applications using Java ecosystem.',
        'avg_salary': '$80,000 - $135,000',
        'demand': 'High'
    },
    'DevOps Engineer': {
        'required': ['linux', 'docker'],
        'preferred': ['kubernetes', 'aws', 'ci/cd', 'jenkins', 'terraform',
                      'ansible', 'python', 'git', 'monitoring',
                      'nginx', 'bash', 'azure', 'google cloud'],
        'description': 'Automate and streamline development and deployment processes.',
        'avg_salary': '$90,000 - $145,000',
        'demand': 'Very High'
    },
    'Cloud Engineer': {
        'required': ['aws'],
        'preferred': ['azure', 'google cloud', 'docker', 'kubernetes',
                      'terraform', 'linux', 'python', 'networking',
                      'security', 'ci/cd', 'serverless'],
        'description': 'Design and manage cloud infrastructure and services.',
        'avg_salary': '$95,000 - $150,000',
        'demand': 'Very High'
    }
}


def predict_jobs(found_skills):
    """
    Predict suitable job roles based on detected skills.
    Returns a ranked list of job matches with match percentages.
    """
    if not found_skills:
        return []

    skills_lower = set(s.lower() for s in found_skills)
    matches = []

    for role, profile in JOB_PROFILES.items():
        required = set(s.lower() for s in profile['required'])
        preferred = set(s.lower() for s in profile['preferred'])
        all_skills = required | preferred

        # Calculate match scores
        required_match = len(required & skills_lower)
        preferred_match = len(preferred & skills_lower)

        # Required skills have higher weight
        if len(required) > 0:
            required_pct = required_match / len(required)
        else:
            required_pct = 0

        if len(preferred) > 0:
            preferred_pct = preferred_match / len(preferred)
        else:
            preferred_pct = 0

        # Overall match: 60% weight on required, 40% on preferred
        match_score = round((required_pct * 0.6 + preferred_pct * 0.4) * 100)

        # Only include if at least one required skill matches
        if required_match > 0 or preferred_match >= 2:
            matched_skills = list((required | preferred) & skills_lower)
            missing_skills = list(required - skills_lower)

            matches.append({
                'role': role,
                'match_score': match_score,
                'matched_skills': matched_skills,
                'missing_required': missing_skills,
                'description': profile['description'],
                'avg_salary': profile['avg_salary'],
                'demand': profile['demand']
            })

    # Sort by match score descending
    matches.sort(key=lambda x: x['match_score'], reverse=True)
    return matches[:6]  # Return top 6 matches
