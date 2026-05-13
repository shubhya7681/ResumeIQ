"""
Generate sample PDF resumes for testing ResumeIQ.
Requires reportlab.
"""
import os
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
except ImportError:
    print("ReportLab is not installed. Please run: pip install reportlab")
    exit(1)

def create_data_scientist_resume():
    filepath = "sample_data_scientist.pdf"
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    header = ParagraphStyle('Header', parent=styles['Heading1'], fontSize=16, spaceAfter=12)
    subhead = ParagraphStyle('Subhead', parent=styles['Heading2'], fontSize=12, spaceAfter=6, spaceBefore=10)
    normal = styles['Normal']
    
    content = []
    
    # Contact Info
    content.append(Paragraph("Aarav Patel", header))
    content.append(Paragraph("aarav.patel@example.com | +91 9876543210 | linkedin.com/in/aaravp | github.com/aaravp", normal))
    content.append(Spacer(1, 12))
    
    # Summary
    content.append(Paragraph("Professional Summary", subhead))
    content.append(Paragraph("Results-driven Data Scientist with 3+ years of experience in developing machine learning models and analyzing complex datasets. Proven track record of increasing efficiency by 30% through predictive modeling. Strong background in Python, Machine Learning, and Data Analysis.", normal))
    
    # Skills
    content.append(Paragraph("Technical Skills", subhead))
    content.append(Paragraph("Python, SQL, R, Machine Learning, Deep Learning, TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy, Data Analysis, Power BI, Docker, AWS.", normal))
    
    # Experience
    content.append(Paragraph("Work Experience", subhead))
    content.append(Paragraph("<b>Data Scientist | TechCorp Inc. | 2021 - Present</b>", normal))
    content.append(Paragraph("• Developed a churn prediction model using Random Forest that reduced customer churn by 15%.", normal))
    content.append(Paragraph("• Analyzed user behavior data using Pandas and SQL to identify key trends, increasing user engagement by 20%.", normal))
    content.append(Paragraph("• Collaborated with cross-functional teams to deploy ML models via REST API using Flask and Docker.", normal))
    content.append(Spacer(1, 6))
    
    content.append(Paragraph("<b>Data Analyst Intern | DataSolutions | 2020 - 2021</b>", normal))
    content.append(Paragraph("• Automated daily reporting dashboards using Python and Power BI, saving 10 hours per week.", normal))
    content.append(Paragraph("• Performed data cleaning and preprocessing on datasets of 1M+ rows.", normal))
    
    # Projects
    content.append(Paragraph("Projects", subhead))
    content.append(Paragraph("<b>E-Commerce Recommendation System</b>: Built a collaborative filtering recommendation engine using Python and Scikit-learn, resulting in a 12% increase in sales.", normal))
    content.append(Paragraph("<b>Sentiment Analysis App</b>: Developed an NLP pipeline using NLTK and deployed a Flask web app to analyze Twitter sentiment in real-time.", normal))
    
    # Education
    content.append(Paragraph("Education", subhead))
    content.append(Paragraph("<b>Bachelor of Technology in Computer Science</b> | XYZ University | 2016 - 2020", normal))
    content.append(Paragraph("CGPA: 8.5/10", normal))
    
    # Certifications
    content.append(Paragraph("Certifications", subhead))
    content.append(Paragraph("AWS Certified Machine Learning – Specialty", normal))
    
    doc.build(content)
    print(f"Created {filepath}")

def create_frontend_dev_resume():
    filepath = "sample_frontend_dev.pdf"
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    
    header = ParagraphStyle('Header', parent=styles['Heading1'], fontSize=16, spaceAfter=12)
    subhead = ParagraphStyle('Subhead', parent=styles['Heading2'], fontSize=12, spaceAfter=6, spaceBefore=10)
    normal = styles['Normal']
    
    content = []
    
    content.append(Paragraph("Priya Sharma", header))
    content.append(Paragraph("priya.sharma@example.com | +91 9123456789 | linkedin.com/in/priyasharma | github.com/priyas", normal))
    content.append(Spacer(1, 12))
    
    content.append(Paragraph("Career Objective", subhead))
    content.append(Paragraph("Creative Frontend Developer with 2 years of experience building responsive, user-friendly web applications. Passionate about UI/UX and modern web technologies. Seeking to leverage my skills in React and JavaScript to create engaging user experiences.", normal))
    
    content.append(Paragraph("Technical Skills", subhead))
    content.append(Paragraph("HTML, CSS, JavaScript, React, Redux, Tailwind CSS, Bootstrap, Node.js, Git, Figma, REST API.", normal))
    
    content.append(Paragraph("Professional Experience", subhead))
    content.append(Paragraph("<b>Frontend Developer | WebWorks Studio | 2022 - Present</b>", normal))
    content.append(Paragraph("• Redesigned the main product dashboard using React and Tailwind CSS, improving load times by 40%.", normal))
    content.append(Paragraph("• Implemented responsive designs ensuring cross-browser compatibility and mobile-first approach.", normal))
    content.append(Paragraph("• Integrated REST APIs to fetch and display dynamic content efficiently.", normal))
    
    content.append(Paragraph("Education", subhead))
    content.append(Paragraph("<b>B.Sc. in Information Technology</b> | ABC College | 2019 - 2022", normal))
    
    doc.build(content)
    print(f"Created {filepath}")

def create_poor_resume():
    filepath = "sample_poor_resume.pdf"
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    
    content = []
    content.append(Paragraph("John Doe", styles['Heading1']))
    content.append(Paragraph("Phone: 1234567890", styles['Normal']))
    content.append(Spacer(1, 20))
    content.append(Paragraph("I am looking for a job in IT. I know computers.", styles['Normal']))
    content.append(Spacer(1, 20))
    content.append(Paragraph("Experience:", styles['Heading2']))
    content.append(Paragraph("Worked at a shop for a year.", styles['Normal']))
    content.append(Spacer(1, 20))
    content.append(Paragraph("Education:", styles['Heading2']))
    content.append(Paragraph("High School", styles['Normal']))
    
    doc.build(content)
    print(f"Created {filepath}")

if __name__ == "__main__":
    create_data_scientist_resume()
    create_frontend_dev_resume()
    create_poor_resume()
    print("Done generating sample resumes.")
