"""
ResumeIQ - PDF Report Generator
Generates downloadable PDF analysis reports using ReportLab.
"""
import os
import tempfile
from datetime import datetime


def generate_pdf_report(resume, analysis_data):
    """Generate a PDF report for the resume analysis."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
    except ImportError:
        # Fallback: create a simple text file if reportlab not available
        return _generate_text_report(resume, analysis_data)

    # Create temp file for PDF
    pdf_path = os.path.join(tempfile.gettempdir(), f'resumeiq_report_{resume.id}.pdf')

    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)

    styles = getSampleStyleSheet()
    elements = []

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle', parent=styles['Title'],
        fontSize=24, textColor=HexColor('#6C63FF'),
        spaceAfter=20
    )
    heading_style = ParagraphStyle(
        'CustomHeading', parent=styles['Heading2'],
        fontSize=16, textColor=HexColor('#6C63FF'),
        spaceBefore=15, spaceAfter=10
    )
    body_style = ParagraphStyle(
        'CustomBody', parent=styles['Normal'],
        fontSize=11, leading=16
    )
    score_style = ParagraphStyle(
        'ScoreStyle', parent=styles['Normal'],
        fontSize=14, textColor=HexColor('#333333'),
        spaceAfter=5
    )

    # Title
    elements.append(Paragraph('ResumeIQ Analysis Report', title_style))
    elements.append(Paragraph(f'Generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}', body_style))
    elements.append(Spacer(1, 20))

    # File info
    elements.append(Paragraph('Resume Information', heading_style))
    elements.append(Paragraph(f'<b>File:</b> {resume.original_filename}', body_style))
    elements.append(Paragraph(f'<b>Uploaded:</b> {resume.upload_date.strftime("%B %d, %Y")}', body_style))
    elements.append(Spacer(1, 15))

    analysis = analysis_data.get('analysis', {})
    skills = analysis_data.get('skills', {})
    jobs = analysis_data.get('jobs', [])

    # Scores
    elements.append(Paragraph('Scores', heading_style))
    elements.append(Paragraph(f'<b>Resume Score:</b> {analysis.get("resume_score", 0)}/100', score_style))
    elements.append(Paragraph(f'<b>ATS Score:</b> {analysis.get("ats_score", 0)}/100', score_style))
    elements.append(Paragraph(f'<b>Word Count:</b> {analysis.get("word_count", 0)}', body_style))
    elements.append(Spacer(1, 15))

    # Strengths
    strengths = analysis.get('strengths', [])
    if strengths:
        elements.append(Paragraph('Strengths', heading_style))
        for s in strengths:
            elements.append(Paragraph(f'✓ {s}', body_style))
        elements.append(Spacer(1, 10))

    # Weaknesses
    weaknesses = analysis.get('weaknesses', [])
    if weaknesses:
        elements.append(Paragraph('Areas for Improvement', heading_style))
        for w in weaknesses:
            elements.append(Paragraph(f'✗ {w}', body_style))
        elements.append(Spacer(1, 10))

    # Missing Sections
    missing = analysis.get('missing_sections', [])
    if missing:
        elements.append(Paragraph('Missing Sections', heading_style))
        for m in missing:
            elements.append(Paragraph(f'• {m}', body_style))
        elements.append(Spacer(1, 10))

    # Skills
    found_skills = skills.get('found', [])
    if found_skills:
        elements.append(Paragraph('Detected Skills', heading_style))
        elements.append(Paragraph(', '.join(found_skills), body_style))
        elements.append(Spacer(1, 10))

    suggested = skills.get('suggested', [])
    if suggested:
        elements.append(Paragraph('Suggested Skills to Learn', heading_style))
        elements.append(Paragraph(', '.join(suggested), body_style))
        elements.append(Spacer(1, 10))

    # Job Recommendations
    if jobs:
        elements.append(Paragraph('Recommended Job Roles', heading_style))
        for job in jobs[:5]:
            elements.append(Paragraph(
                f'<b>{job["role"]}</b> - {job["match_score"]}% match | {job.get("demand", "")} demand',
                body_style
            ))
        elements.append(Spacer(1, 10))

    # Suggestions
    suggestions = analysis.get('suggestions', [])
    if suggestions:
        elements.append(Paragraph('Improvement Suggestions', heading_style))
        for s in suggestions:
            title = s.get('title', '') if isinstance(s, dict) else str(s)
            desc = s.get('description', '') if isinstance(s, dict) else ''
            elements.append(Paragraph(f'<b>{title}</b>', body_style))
            if desc:
                elements.append(Paragraph(f'  {desc}', body_style))
            elements.append(Spacer(1, 5))

    # Footer
    elements.append(Spacer(1, 30))
    elements.append(Paragraph('— Generated by ResumeIQ AI Resume Analyzer —',
                              ParagraphStyle('Footer', parent=styles['Normal'],
                                             fontSize=9, textColor=HexColor('#999999'),
                                             alignment=1)))

    doc.build(elements)
    return pdf_path


def _generate_text_report(resume, analysis_data):
    """Fallback: generate a simple text report."""
    import tempfile
    analysis = analysis_data.get('analysis', {})
    skills = analysis_data.get('skills', {})

    report_path = os.path.join(tempfile.gettempdir(), f'resumeiq_report_{resume.id}.txt')
    with open(report_path, 'w') as f:
        f.write('=' * 60 + '\n')
        f.write('ResumeIQ Analysis Report\n')
        f.write('=' * 60 + '\n\n')
        f.write(f'File: {resume.original_filename}\n')
        f.write(f'Date: {datetime.now().strftime("%B %d, %Y")}\n\n')
        f.write(f'Resume Score: {analysis.get("resume_score", 0)}/100\n')
        f.write(f'ATS Score: {analysis.get("ats_score", 0)}/100\n\n')

        f.write('Strengths:\n')
        for s in analysis.get('strengths', []):
            f.write(f'  + {s}\n')

        f.write('\nWeaknesses:\n')
        for w in analysis.get('weaknesses', []):
            f.write(f'  - {w}\n')

        f.write('\nDetected Skills:\n')
        f.write(', '.join(skills.get('found', [])) + '\n')

    return report_path
