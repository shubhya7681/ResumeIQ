"""
ResumeIQ - Resume Analyzer Module
Performs comprehensive resume analysis including scoring, ATS compatibility,
strength/weakness detection, and improvement suggestions.
"""
import re
from utils.resume_parser import extract_sections


# Action verbs commonly used in strong resumes
ACTION_VERBS = [
    'achieved', 'administered', 'analyzed', 'architected', 'automated',
    'built', 'collaborated', 'conducted', 'created', 'decreased',
    'delivered', 'designed', 'developed', 'directed', 'enhanced',
    'established', 'executed', 'generated', 'implemented', 'improved',
    'increased', 'initiated', 'integrated', 'launched', 'led',
    'managed', 'mentored', 'migrated', 'monitored', 'negotiated',
    'optimized', 'orchestrated', 'organized', 'oversaw', 'performed',
    'pioneered', 'planned', 'produced', 'programmed', 'published',
    'reduced', 'refactored', 'resolved', 'revamped', 'scaled',
    'spearheaded', 'streamlined', 'supervised', 'tested', 'trained',
    'transformed', 'troubleshot', 'utilized'
]

# Important ATS keywords
ATS_KEYWORDS = [
    'experience', 'education', 'skills', 'projects', 'certifications',
    'objective', 'summary', 'professional', 'achievements', 'responsibilities',
    'bachelor', 'master', 'degree', 'university', 'college',
    'internship', 'full-time', 'part-time', 'remote', 'hybrid'
]


def analyze_resume(text, found_skills=None):
    """
    Perform comprehensive resume analysis.
    Returns a dictionary with scores, strengths, weaknesses, and suggestions.
    """
    if not text:
        return _empty_analysis()

    sections = extract_sections(text)
    text_lower = text.lower()
    word_count = len(text.split())

    # Calculate individual scores
    section_score = _score_sections(sections)
    length_score = _score_length(word_count)
    action_verb_score = _score_action_verbs(text_lower)
    formatting_score = _score_formatting(text)
    contact_score = _score_contact_info(text)
    quantification_score = _score_quantification(text)

    # Calculate overall resume score (weighted average)
    resume_score = round(
        section_score * 0.25 +
        length_score * 0.10 +
        action_verb_score * 0.15 +
        formatting_score * 0.10 +
        contact_score * 0.15 +
        quantification_score * 0.10 +
        (len(found_skills) * 2 if found_skills else 0) * 0.15
    )
    resume_score = min(resume_score, 100)

    # Calculate ATS score
    ats_score = _calculate_ats_score(text, sections)

    # Identify strengths and weaknesses
    strengths = _identify_strengths(text, sections, word_count)
    weaknesses = _identify_weaknesses(text, sections, word_count)

    # Detect missing sections
    missing_sections = _detect_missing_sections(sections)

    # Generate suggestions
    suggestions = _generate_suggestions(text, sections, word_count, found_skills)

    return {
        'resume_score': resume_score,
        'ats_score': ats_score,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'missing_sections': missing_sections,
        'suggestions': suggestions,
        'word_count': word_count,
        'section_scores': {
            'sections': section_score,
            'length': length_score,
            'action_verbs': action_verb_score,
            'formatting': formatting_score,
            'contact_info': contact_score,
            'quantification': quantification_score
        }
    }


def _empty_analysis():
    """Return empty analysis results."""
    return {
        'resume_score': 0,
        'ats_score': 0,
        'strengths': [],
        'weaknesses': ['No text could be extracted from the resume'],
        'missing_sections': ['All sections are missing'],
        'suggestions': ['Please upload a valid resume file'],
        'word_count': 0,
        'section_scores': {}
    }


def _score_sections(sections):
    """Score based on presence of key resume sections (0-100)."""
    important_sections = ['education', 'experience', 'skills', 'objective', 'projects']
    found = sum(1 for s in important_sections if sections.get(s, '').strip())
    return round((found / len(important_sections)) * 100)


def _score_length(word_count):
    """Score based on resume length (0-100). Ideal: 300-800 words."""
    if 300 <= word_count <= 800:
        return 100
    elif 200 <= word_count < 300 or 800 < word_count <= 1200:
        return 75
    elif 100 <= word_count < 200 or 1200 < word_count <= 1500:
        return 50
    elif word_count < 100:
        return 25
    else:
        return 40


def _score_action_verbs(text_lower):
    """Score based on usage of action verbs (0-100)."""
    found_verbs = [v for v in ACTION_VERBS if v in text_lower]
    count = len(found_verbs)
    if count >= 10:
        return 100
    elif count >= 7:
        return 85
    elif count >= 5:
        return 70
    elif count >= 3:
        return 50
    elif count >= 1:
        return 30
    return 10


def _score_formatting(text):
    """Score based on text formatting quality (0-100)."""
    score = 50  # Base score

    # Check for bullet points or structured lists
    if re.search(r'[•\-\*]\s', text):
        score += 15

    # Check for consistent spacing
    lines = text.split('\n')
    non_empty = [l for l in lines if l.strip()]
    if len(non_empty) > 5:
        score += 10

    # Check for section headers (capitalized lines)
    caps_lines = [l for l in lines if l.strip().isupper() and len(l.strip()) > 3]
    if len(caps_lines) >= 3:
        score += 15

    # Check for dates
    if re.search(r'\d{4}\s*[-–]\s*(\d{4}|present|current)', text, re.IGNORECASE):
        score += 10

    return min(score, 100)


def _score_contact_info(text):
    """Score based on presence of contact information (0-100)."""
    score = 0
    text_lower = text.lower()

    # Email
    if re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', text):
        score += 25

    # Phone number
    if re.search(r'[\+]?[\d\s\-\(\)]{10,}', text):
        score += 25

    # LinkedIn
    if 'linkedin' in text_lower:
        score += 25

    # GitHub
    if 'github' in text_lower:
        score += 15

    # Portfolio / Website
    if re.search(r'(?i)(portfolio|website|http|www\.)', text):
        score += 10

    return min(score, 100)


def _score_quantification(text):
    """Score based on quantifiable achievements (0-100)."""
    # Look for numbers, percentages, dollar amounts
    numbers = re.findall(r'\d+[%+]|\$[\d,]+|\d+\s*(?:users|clients|projects|team|members|employees)', text, re.IGNORECASE)
    percentages = re.findall(r'\d+\s*%', text)

    count = len(numbers) + len(percentages)
    if count >= 5:
        return 100
    elif count >= 3:
        return 75
    elif count >= 1:
        return 50
    return 20


def _calculate_ats_score(text, sections):
    """Calculate ATS (Applicant Tracking System) compatibility score."""
    score = 0
    text_lower = text.lower()

    # Check for ATS-friendly formatting (no tables, images references)
    score += 15  # Base score for being parseable text

    # Check for keyword presence
    keyword_count = sum(1 for kw in ATS_KEYWORDS if kw in text_lower)
    score += min(keyword_count * 4, 30)

    # Check for standard section headings
    standard_headings = ['education', 'experience', 'skills', 'summary', 'objective']
    heading_count = sum(1 for h in standard_headings if sections.get(h, '').strip())
    score += heading_count * 6

    # Check for contact information
    if re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', text):
        score += 10
    if re.search(r'[\+]?[\d\s\-\(\)]{10,}', text):
        score += 5

    # Check for date formats
    if re.search(r'\d{4}', text):
        score += 5

    # Check for proper length
    word_count = len(text.split())
    if 200 <= word_count <= 1000:
        score += 5

    return min(round(score), 100)


def _identify_strengths(text, sections, word_count):
    """Identify strong points of the resume."""
    strengths = []
    text_lower = text.lower()

    if sections.get('experience', '').strip():
        strengths.append('Work experience section is present')
    if sections.get('education', '').strip():
        strengths.append('Education section is well-defined')
    if sections.get('skills', '').strip():
        strengths.append('Skills section is included')
    if sections.get('projects', '').strip():
        strengths.append('Projects section demonstrates practical experience')
    if re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', text):
        strengths.append('Contact email is provided')
    if 'linkedin' in text_lower:
        strengths.append('LinkedIn profile is referenced')
    if 'github' in text_lower:
        strengths.append('GitHub profile showcases coding activity')

    # Check action verbs
    found_verbs = [v for v in ACTION_VERBS if v in text_lower]
    if len(found_verbs) >= 5:
        strengths.append(f'Strong use of action verbs ({len(found_verbs)} found)')

    # Check quantification
    numbers = re.findall(r'\d+[%+]|\$[\d,]+', text)
    if len(numbers) >= 2:
        strengths.append('Includes quantifiable achievements')

    if 300 <= word_count <= 800:
        strengths.append('Resume length is optimal')

    if not strengths:
        strengths.append('Resume has been successfully parsed')

    return strengths


def _identify_weaknesses(text, sections, word_count):
    """Identify weak points of the resume."""
    weaknesses = []
    text_lower = text.lower()

    if not sections.get('objective', '').strip() and not sections.get('summary', '').strip():
        weaknesses.append('Missing career objective or professional summary')
    if not sections.get('experience', '').strip():
        weaknesses.append('No work experience section detected')
    if not sections.get('skills', '').strip():
        weaknesses.append('Skills section is missing or not clearly defined')
    if not sections.get('projects', '').strip():
        weaknesses.append('No projects section found')
    if not sections.get('certifications', '').strip():
        weaknesses.append('No certifications mentioned')

    if 'linkedin' not in text_lower:
        weaknesses.append('LinkedIn profile not included')
    if 'github' not in text_lower:
        weaknesses.append('GitHub profile not included')

    found_verbs = [v for v in ACTION_VERBS if v in text_lower]
    if len(found_verbs) < 3:
        weaknesses.append('Insufficient use of action verbs')

    if word_count < 200:
        weaknesses.append('Resume is too short - add more detail')
    elif word_count > 1000:
        weaknesses.append('Resume may be too long - consider condensing')

    numbers = re.findall(r'\d+[%+]|\$[\d,]+', text)
    if len(numbers) < 2:
        weaknesses.append('Lacks quantifiable achievements and metrics')

    return weaknesses


def _detect_missing_sections(sections):
    """Detect which important sections are missing."""
    missing = []
    required_sections = {
        'objective': 'Career Objective / Summary',
        'education': 'Education',
        'experience': 'Work Experience',
        'skills': 'Technical Skills',
        'projects': 'Projects',
        'certifications': 'Certifications'
    }

    for key, label in required_sections.items():
        if not sections.get(key, '').strip():
            missing.append(label)

    return missing


def _generate_suggestions(text, sections, word_count, found_skills=None):
    """Generate actionable improvement suggestions."""
    suggestions = []
    text_lower = text.lower()

    if not sections.get('objective', '').strip() and not sections.get('summary', '').strip():
        suggestions.append({
            'title': 'Add a Professional Summary',
            'description': 'Start with a 2-3 sentence summary highlighting your key qualifications and career goals.',
            'priority': 'high'
        })

    if not sections.get('projects', '').strip():
        suggestions.append({
            'title': 'Add a Projects Section',
            'description': 'Include 2-4 relevant projects with descriptions of technologies used and outcomes achieved.',
            'priority': 'high'
        })

    numbers = re.findall(r'\d+[%+]|\$[\d,]+', text)
    if len(numbers) < 2:
        suggestions.append({
            'title': 'Add Measurable Achievements',
            'description': 'Quantify your accomplishments. E.g., "Increased efficiency by 30%" or "Managed a team of 5".',
            'priority': 'high'
        })

    found_verbs = [v for v in ACTION_VERBS if v in text_lower]
    if len(found_verbs) < 5:
        suggestions.append({
            'title': 'Use More Action Verbs',
            'description': 'Start bullet points with strong action verbs like "Developed", "Implemented", "Optimized", "Led".',
            'priority': 'medium'
        })

    if 'linkedin' not in text_lower:
        suggestions.append({
            'title': 'Add LinkedIn Profile',
            'description': 'Include your LinkedIn URL to enhance professional visibility and networking.',
            'priority': 'medium'
        })

    if 'github' not in text_lower:
        suggestions.append({
            'title': 'Add GitHub Profile',
            'description': 'Showcase your coding projects by including your GitHub profile link.',
            'priority': 'medium'
        })

    if not sections.get('certifications', '').strip():
        suggestions.append({
            'title': 'Add Certifications',
            'description': 'Include relevant certifications to validate your skills (e.g., AWS, Google, Microsoft).',
            'priority': 'medium'
        })

    if word_count < 200:
        suggestions.append({
            'title': 'Expand Your Resume',
            'description': 'Your resume is too brief. Aim for 300-700 words with detailed descriptions.',
            'priority': 'high'
        })
    elif word_count > 1000:
        suggestions.append({
            'title': 'Condense Your Resume',
            'description': 'Keep your resume concise. Focus on the most relevant and recent experience.',
            'priority': 'medium'
        })

    if not re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', text):
        suggestions.append({
            'title': 'Add Email Address',
            'description': 'Ensure your professional email is clearly visible at the top of the resume.',
            'priority': 'high'
        })

    suggestions.append({
        'title': 'Tailor for Each Application',
        'description': 'Customize your resume for each job by matching keywords from the job description.',
        'priority': 'low'
    })

    suggestions.append({
        'title': 'Use Clean Formatting',
        'description': 'Use consistent fonts, proper spacing, and clear section headings for ATS compatibility.',
        'priority': 'low'
    })

    return suggestions
