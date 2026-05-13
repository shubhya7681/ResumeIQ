"""
ResumeIQ - Career Roadmap Module
Provides structured learning roadmaps for different career paths.
"""

CAREER_ROADMAPS = {
    'Data Analyst': {
        'icon': 'fas fa-chart-bar',
        'color': '#6C63FF',
        'steps': [
            {
                'phase': 'Phase 1: Foundation',
                'duration': '1-2 Months',
                'tasks': [
                    'Learn Excel & Google Sheets (Pivot tables, VLOOKUP, charts)',
                    'Learn SQL fundamentals (SELECT, JOIN, GROUP BY, subqueries)',
                    'Understand basic statistics (mean, median, mode, standard deviation)',
                    'Learn data types and data cleaning concepts'
                ]
            },
            {
                'phase': 'Phase 2: Python for Data',
                'duration': '2-3 Months',
                'tasks': [
                    'Learn Python basics (variables, loops, functions, OOP)',
                    'Master Pandas for data manipulation',
                    'Learn NumPy for numerical computing',
                    'Practice data cleaning and preprocessing'
                ]
            },
            {
                'phase': 'Phase 3: Visualization',
                'duration': '1-2 Months',
                'tasks': [
                    'Learn Matplotlib and Seaborn for Python visualizations',
                    'Master Power BI or Tableau for business dashboards',
                    'Create compelling data stories',
                    'Build portfolio with 3-5 analysis projects'
                ]
            },
            {
                'phase': 'Phase 4: Advanced & Job Ready',
                'duration': '2-3 Months',
                'tasks': [
                    'Learn advanced SQL (window functions, CTEs, optimization)',
                    'Study A/B testing and hypothesis testing',
                    'Learn data modeling and ETL basics',
                    'Build end-to-end analysis projects for portfolio',
                    'Practice with real datasets from Kaggle'
                ]
            }
        ]
    },
    'Data Scientist': {
        'icon': 'fas fa-brain',
        'color': '#FF6B9D',
        'steps': [
            {
                'phase': 'Phase 1: Math & Statistics',
                'duration': '2-3 Months',
                'tasks': [
                    'Linear algebra (matrices, vectors, eigenvalues)',
                    'Probability and statistics',
                    'Calculus (derivatives, gradients)',
                    'Learn Python programming fundamentals'
                ]
            },
            {
                'phase': 'Phase 2: Data Manipulation',
                'duration': '2-3 Months',
                'tasks': [
                    'Master Pandas, NumPy, and SQL',
                    'Data cleaning and preprocessing techniques',
                    'Feature engineering and selection',
                    'Exploratory Data Analysis (EDA)'
                ]
            },
            {
                'phase': 'Phase 3: Machine Learning',
                'duration': '3-4 Months',
                'tasks': [
                    'Supervised learning (regression, classification)',
                    'Unsupervised learning (clustering, dimensionality reduction)',
                    'Model evaluation and validation',
                    'Scikit-learn, XGBoost, LightGBM',
                    'Build 5+ ML projects'
                ]
            },
            {
                'phase': 'Phase 4: Deep Learning & Specialization',
                'duration': '2-3 Months',
                'tasks': [
                    'Neural networks with TensorFlow/PyTorch',
                    'NLP or Computer Vision specialization',
                    'Model deployment (Flask, Docker, Cloud)',
                    'Participate in Kaggle competitions',
                    'Build production-ready ML pipeline'
                ]
            }
        ]
    },
    'ML Engineer': {
        'icon': 'fas fa-robot',
        'color': '#00D4FF',
        'steps': [
            {
                'phase': 'Phase 1: Programming & Math',
                'duration': '2-3 Months',
                'tasks': [
                    'Advanced Python (OOP, design patterns)',
                    'Data structures and algorithms',
                    'Linear algebra and calculus',
                    'Version control with Git'
                ]
            },
            {
                'phase': 'Phase 2: ML Fundamentals',
                'duration': '3-4 Months',
                'tasks': [
                    'Classical ML algorithms',
                    'Deep learning frameworks (TensorFlow, PyTorch)',
                    'Feature engineering and model optimization',
                    'Experiment tracking (MLflow, Weights & Biases)'
                ]
            },
            {
                'phase': 'Phase 3: MLOps & Engineering',
                'duration': '2-3 Months',
                'tasks': [
                    'Docker and containerization',
                    'CI/CD for ML pipelines',
                    'Model serving (FastAPI, TensorFlow Serving)',
                    'Cloud platforms (AWS SageMaker, GCP AI Platform)'
                ]
            },
            {
                'phase': 'Phase 4: Production Systems',
                'duration': '2-3 Months',
                'tasks': [
                    'Distributed computing (Spark)',
                    'Model monitoring and retraining',
                    'A/B testing for ML models',
                    'Build end-to-end ML platform',
                    'System design for ML systems'
                ]
            }
        ]
    },
    'Frontend Developer': {
        'icon': 'fas fa-palette',
        'color': '#FFB347',
        'steps': [
            {
                'phase': 'Phase 1: Web Basics',
                'duration': '1-2 Months',
                'tasks': [
                    'HTML5 semantic elements and accessibility',
                    'CSS3 (Flexbox, Grid, animations, responsive design)',
                    'JavaScript fundamentals (ES6+)',
                    'Version control with Git'
                ]
            },
            {
                'phase': 'Phase 2: Modern Frameworks',
                'duration': '2-3 Months',
                'tasks': [
                    'React.js (hooks, state management, routing)',
                    'TypeScript for type safety',
                    'CSS frameworks (Tailwind CSS, Bootstrap)',
                    'Build 3-5 responsive web projects'
                ]
            },
            {
                'phase': 'Phase 3: Advanced Frontend',
                'duration': '2-3 Months',
                'tasks': [
                    'State management (Redux, Zustand)',
                    'Testing (Jest, React Testing Library)',
                    'Performance optimization',
                    'Next.js for SSR and SSG',
                    'API integration and authentication'
                ]
            },
            {
                'phase': 'Phase 4: Professional Level',
                'duration': '1-2 Months',
                'tasks': [
                    'Design systems and component libraries',
                    'Web accessibility (WCAG standards)',
                    'PWA development',
                    'Build portfolio website',
                    'Contribute to open source projects'
                ]
            }
        ]
    },
    'Backend Developer': {
        'icon': 'fas fa-server',
        'color': '#77DD77',
        'steps': [
            {
                'phase': 'Phase 1: Programming Basics',
                'duration': '2-3 Months',
                'tasks': [
                    'Python or Node.js fundamentals',
                    'Data structures and algorithms',
                    'SQL and database design',
                    'HTTP, REST APIs, and networking basics'
                ]
            },
            {
                'phase': 'Phase 2: Backend Frameworks',
                'duration': '2-3 Months',
                'tasks': [
                    'Flask/Django (Python) or Express.js (Node.js)',
                    'ORM (SQLAlchemy, Sequelize)',
                    'Authentication and authorization',
                    'API design and documentation (Swagger)'
                ]
            },
            {
                'phase': 'Phase 3: Databases & Caching',
                'duration': '2-3 Months',
                'tasks': [
                    'PostgreSQL advanced features',
                    'MongoDB for NoSQL',
                    'Redis for caching',
                    'Message queues (RabbitMQ, Kafka)',
                    'Database optimization'
                ]
            },
            {
                'phase': 'Phase 4: DevOps & Scale',
                'duration': '2-3 Months',
                'tasks': [
                    'Docker and containerization',
                    'CI/CD pipelines',
                    'Cloud deployment (AWS, GCP)',
                    'Microservices architecture',
                    'System design and scalability'
                ]
            }
        ]
    },
    'Full Stack Developer': {
        'icon': 'fas fa-layer-group',
        'color': '#C49BFF',
        'steps': [
            {
                'phase': 'Phase 1: Frontend Foundation',
                'duration': '2-3 Months',
                'tasks': [
                    'HTML5, CSS3, JavaScript (ES6+)',
                    'Responsive design and CSS frameworks',
                    'React.js fundamentals',
                    'Git version control'
                ]
            },
            {
                'phase': 'Phase 2: Backend Foundation',
                'duration': '2-3 Months',
                'tasks': [
                    'Node.js and Express.js',
                    'Python and Flask/Django',
                    'SQL and NoSQL databases',
                    'REST API development'
                ]
            },
            {
                'phase': 'Phase 3: Full Stack Integration',
                'duration': '2-3 Months',
                'tasks': [
                    'Build full-stack applications (MERN/PERN stack)',
                    'Authentication (JWT, OAuth)',
                    'File uploads and cloud storage',
                    'Real-time features (WebSockets)',
                    'Testing (frontend + backend)'
                ]
            },
            {
                'phase': 'Phase 4: Deployment & DevOps',
                'duration': '1-2 Months',
                'tasks': [
                    'Docker and containerization',
                    'CI/CD pipelines',
                    'Cloud deployment (Vercel, AWS, Heroku)',
                    'Performance optimization',
                    'Build 3+ production-ready projects'
                ]
            }
        ]
    },
    'Python Developer': {
        'icon': 'fab fa-python',
        'color': '#FFD43B',
        'steps': [
            {
                'phase': 'Phase 1: Python Mastery',
                'duration': '2-3 Months',
                'tasks': [
                    'Python fundamentals (data types, control flow, functions)',
                    'OOP in Python (classes, inheritance, polymorphism)',
                    'File handling and exception management',
                    'Python standard library essentials'
                ]
            },
            {
                'phase': 'Phase 2: Web Development',
                'duration': '2-3 Months',
                'tasks': [
                    'Flask or Django web framework',
                    'RESTful API development',
                    'Database integration (SQLAlchemy)',
                    'Template engines and frontend basics'
                ]
            },
            {
                'phase': 'Phase 3: Advanced Python',
                'duration': '2-3 Months',
                'tasks': [
                    'Async programming (asyncio)',
                    'Testing (pytest, unittest)',
                    'Package management and virtual environments',
                    'Design patterns in Python',
                    'FastAPI for high-performance APIs'
                ]
            },
            {
                'phase': 'Phase 4: Specialization',
                'duration': '2-3 Months',
                'tasks': [
                    'Choose: Data Science, DevOps, or Web Dev track',
                    'Docker and deployment',
                    'CI/CD and code quality tools',
                    'Open source contributions',
                    'Build production-grade applications'
                ]
            }
        ]
    },
    'Java Developer': {
        'icon': 'fab fa-java',
        'color': '#ED8B00',
        'steps': [
            {
                'phase': 'Phase 1: Java Core',
                'duration': '2-3 Months',
                'tasks': [
                    'Java fundamentals and OOP concepts',
                    'Collections framework',
                    'Exception handling and I/O',
                    'Multithreading basics'
                ]
            },
            {
                'phase': 'Phase 2: Enterprise Java',
                'duration': '3-4 Months',
                'tasks': [
                    'Spring Framework and Spring Boot',
                    'Hibernate and JPA',
                    'RESTful web services',
                    'Maven/Gradle build tools'
                ]
            },
            {
                'phase': 'Phase 3: Database & Testing',
                'duration': '2-3 Months',
                'tasks': [
                    'SQL and database design',
                    'JUnit and Mockito testing',
                    'Spring Security',
                    'Microservices with Spring Cloud'
                ]
            },
            {
                'phase': 'Phase 4: DevOps & Cloud',
                'duration': '2-3 Months',
                'tasks': [
                    'Docker and Kubernetes',
                    'CI/CD with Jenkins',
                    'AWS deployment',
                    'Performance tuning and monitoring',
                    'System design patterns'
                ]
            }
        ]
    }
}


def get_roadmap(role):
    """Get the career roadmap for a specific role."""
    return CAREER_ROADMAPS.get(role)


def get_all_roles():
    """Return all available career roles."""
    return list(CAREER_ROADMAPS.keys())


def get_role_summary():
    """Return summary info for all roles (for selection UI)."""
    summaries = []
    for role, data in CAREER_ROADMAPS.items():
        total_duration = sum(
            int(step['duration'].split('-')[0]) for step in data['steps']
        )
        total_tasks = sum(len(step['tasks']) for step in data['steps'])
        summaries.append({
            'role': role,
            'icon': data['icon'],
            'color': data['color'],
            'phases': len(data['steps']),
            'estimated_months': f'{total_duration}-{total_duration + 4}',
            'total_tasks': total_tasks
        })
    return summaries
