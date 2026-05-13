"""
ResumeIQ - AI Career Chatbot Engine
Rule-based chatbot for resume tips, career advice, and interview preparation.
"""
import random
import re


# ─── Knowledge Base ──────────────────────────────────────────────────────────

GREETINGS = [
    "Hey there! 👋 I'm ResumeIQ's career assistant. Ask me about resume tips, interview prep, career paths, or ATS optimization!",
    "Hello! 🚀 I'm here to help with your career journey. What would you like to know about resumes, interviews, or career planning?",
    "Hi! ✨ Welcome to ResumeIQ chat. I can help with resume writing, skill building, interview prep, and more!"
]

FALLBACK_RESPONSES = [
    "That's a great question! While I specialize in resume & career advice, I'd suggest checking out our Career Roadmap section for detailed guidance. Try asking me about resume tips, ATS scores, interview prep, or career paths!",
    "Hmm, I'm not sure about that one. But I can definitely help with resume optimization, interview questions, career planning, and skill recommendations. What would you like to know?",
    "I'm best at helping with career-related topics! Try asking me about: \n• Resume formatting tips\n• ATS optimization\n• Interview preparation\n• Career path suggestions\n• Skill recommendations"
]

RESPONSES = {
    'resume_tips': {
        'patterns': [r'resume\s*tip', r'improve\s*resume', r'better\s*resume', r'resume\s*advice',
                     r'write\s*resume', r'make\s*resume', r'good\s*resume', r'strong\s*resume',
                     r'resume\s*help', r'fix\s*resume', r'update\s*resume'],
        'responses': [
            "📝 **Top Resume Tips:**\n\n1. **Start with a strong summary** — 2-3 sentences highlighting your value proposition\n2. **Use action verbs** — Led, Developed, Optimized, Delivered, Increased\n3. **Quantify achievements** — \"Increased revenue by 30%\" beats \"Helped increase revenue\"\n4. **Keep it to 1-2 pages** — Recruiters spend ~7 seconds on initial scan\n5. **Tailor for each job** — Mirror keywords from the job description\n6. **Use reverse chronological order** — Most recent experience first",
            "✅ **Resume Best Practices:**\n\n• Use a clean, professional format with consistent fonts\n• Include relevant keywords from the job description\n• Start bullet points with strong action verbs\n• Add quantifiable metrics (numbers, percentages, dollar amounts)\n• Include links to LinkedIn, GitHub, or portfolio\n• Proofread carefully — one typo can cost you an interview!"
        ]
    },
    'ats': {
        'patterns': [r'ats', r'applicant\s*tracking', r'ats\s*score', r'ats\s*friendly',
                     r'ats\s*compatible', r'ats\s*optim', r'pass\s*ats', r'beat\s*ats'],
        'responses': [
            "🤖 **ATS Optimization Tips:**\n\n1. **Use standard section headings** — \"Experience\", \"Education\", \"Skills\" (not creative alternatives)\n2. **Avoid tables, columns, headers/footers** — ATS can't parse them properly\n3. **Use standard fonts** — Arial, Calibri, Times New Roman\n4. **Include exact keywords** from the job description\n5. **Save as PDF** (unless the job asks for .docx)\n6. **Don't use images or icons** — ATS can't read them\n7. **Use standard date formats** — \"Jan 2023 - Present\"",
            "📊 **Boost Your ATS Score:**\n\n• Match 60-80% of keywords from the job posting\n• Use both spelled-out terms AND acronyms (e.g., \"Machine Learning (ML)\")\n• Keep formatting simple — no fancy graphics\n• Include a dedicated Skills section with relevant technologies\n• Use standard headings the ATS expects to find\n\n💡 Upload your resume on ResumeIQ to get your ATS compatibility score!"
        ]
    },
    'interview': {
        'patterns': [r'interview', r'prepare\s*interview', r'interview\s*tip', r'interview\s*question',
                     r'crack\s*interview', r'interview\s*prep', r'behavioral\s*question'],
        'responses': [
            "🎯 **Interview Preparation Guide:**\n\n1. **Research the company** — Know their mission, products, recent news\n2. **Use the STAR method** for behavioral questions (Situation, Task, Action, Result)\n3. **Prepare your elevator pitch** — 60-second introduction of yourself\n4. **Have questions ready** — Ask about team culture, growth opportunities\n5. **Practice common questions:**\n   - Tell me about yourself\n   - Why this company?\n   - Describe a challenge you overcame\n   - Where do you see yourself in 5 years?",
            "💼 **Interview Success Tips:**\n\n• **Technical rounds:** Practice on LeetCode, HackerRank for coding roles\n• **Behavioral rounds:** Prepare 5-6 STAR stories covering leadership, conflict, failure, teamwork\n• **System Design:** Study architecture patterns for senior roles\n• **Soft skills:** Communication, problem-solving, and teamwork matter!\n• **Follow up:** Send a thank-you email within 24 hours\n\n💡 Check our Analysis page — we generate interview questions based on your skills!"
        ]
    },
    'skills': {
        'patterns': [r'skill', r'learn\s*what', r'what\s*to\s*learn', r'trending\s*skill',
                     r'in\s*demand', r'top\s*skill', r'best\s*skill', r'must\s*know',
                     r'technology', r'tech\s*stack'],
        'responses': [
            "🔥 **In-Demand Tech Skills (2026):**\n\n**Data & AI:** Python, SQL, TensorFlow, PyTorch, LLMs, RAG\n**Web Dev:** React, Next.js, TypeScript, Node.js, Tailwind\n**Cloud:** AWS, Azure, Docker, Kubernetes, Terraform\n**Other Hot Skills:** System Design, CI/CD, GraphQL, Rust\n\n**Soft Skills Matter Too:**\n• Communication & presentation\n• Problem-solving & critical thinking\n• Leadership & teamwork\n• Adaptability & continuous learning",
            "📚 **Skills to Add to Your Resume:**\n\n1. **Always include:** Programming languages, frameworks, tools you actually use\n2. **Categorize them:** Languages | Frameworks | Databases | Tools | Soft Skills\n3. **Be honest:** Only list skills you can discuss in an interview\n4. **Add proficiency levels** if appropriate (Expert, Intermediate, Beginner)\n\n💡 Upload your resume and our AI will detect your skills and suggest missing ones!"
        ]
    },
    'career_path': {
        'patterns': [r'career\s*path', r'career\s*advice', r'career\s*change', r'career\s*plan',
                     r'switch\s*career', r'roadmap', r'become\s*a', r'how\s*to\s*become',
                     r'career\s*grow', r'career\s*guid'],
        'responses': [
            "🗺️ **Career Planning Tips:**\n\n1. **Identify your strengths** — What are you naturally good at?\n2. **Explore roles** that match your skills and interests\n3. **Build a learning roadmap** — Break it into 3-month phases\n4. **Network actively** — LinkedIn, meetups, tech communities\n5. **Build projects** — A portfolio speaks louder than certifications\n\n💡 Check out our **Career Roadmap** feature for detailed step-by-step paths for 8+ career roles!",
            "🚀 **Career Growth Strategies:**\n\n• **Short-term (0-6 months):** Learn one new skill deeply\n• **Mid-term (6-12 months):** Build 3-5 portfolio projects\n• **Long-term (1-2 years):** Specialize in a niche area\n\n**Popular Career Paths:**\n→ Data Analyst → Data Scientist → ML Engineer\n→ Frontend Dev → Full Stack Dev → Tech Lead\n→ Python Dev → Backend Dev → Cloud Architect\n\n📍 Visit our Career Roadmap section for structured learning paths!"
        ]
    },
    'salary': {
        'patterns': [r'salary', r'pay', r'compensation', r'how\s*much\s*earn',
                     r'average\s*salary', r'negotiate', r'offer'],
        'responses': [
            "💰 **Salary Negotiation Tips:**\n\n1. **Research market rates** on Glassdoor, Levels.fyi, LinkedIn Salary\n2. **Know your worth** — Factor in your skills, experience, and location\n3. **Never share your current salary first** — Let the employer make an offer\n4. **Negotiate total compensation** — Base + bonus + equity + benefits\n5. **Practice your pitch** — \"Based on my research and experience, I'm targeting...\"\n6. **Get it in writing** before accepting\n\n💡 Upload your resume — our job matching shows salary ranges for roles you're qualified for!"
        ]
    },
    'linkedin': {
        'patterns': [r'linkedin', r'profile', r'networking', r'network'],
        'responses': [
            "🔗 **LinkedIn Profile Tips:**\n\n1. **Professional headshot** — Profiles with photos get 21x more views\n2. **Compelling headline** — Not just your title, but your value proposition\n3. **Detailed About section** — Tell your career story in first person\n4. **Add all skills** — Get endorsements from colleagues\n5. **Request recommendations** — 2-3 from managers or peers\n6. **Post regularly** — Share insights, articles, and achievements\n7. **Engage with others** — Comment on posts in your industry\n\n💡 Don't forget to add your LinkedIn URL to your resume!"
        ]
    },
    'format': {
        'patterns': [r'format', r'template', r'layout', r'design\s*resume', r'font',
                     r'how\s*long', r'page', r'length'],
        'responses': [
            "📐 **Resume Formatting Guide:**\n\n**Length:** 1 page for <5 years exp, 2 pages for senior roles\n**Font:** 10-12pt, use Arial, Calibri, or Garamond\n**Margins:** 0.5-1 inch on all sides\n**Sections order:**\n1. Contact Info & LinkedIn\n2. Professional Summary\n3. Work Experience (reverse chronological)\n4. Projects\n5. Skills\n6. Education\n7. Certifications\n\n**Pro tip:** Use consistent formatting — same bullet style, date alignment, and heading sizes throughout!"
        ]
    },
    'cover_letter': {
        'patterns': [r'cover\s*letter', r'cover\s*note'],
        'responses': [
            "✉️ **Cover Letter Tips:**\n\n1. **Keep it to 3-4 paragraphs** — Under 300 words\n2. **Para 1:** Why you're interested in THIS specific role/company\n3. **Para 2:** Your most relevant achievements (with numbers)\n4. **Para 3:** How you'll add value to their team\n5. **Para 4:** Call to action — express enthusiasm for an interview\n\n**Don'ts:**\n• Don't repeat your resume verbatim\n• Don't use \"To Whom It May Concern\"\n• Don't be generic — customize for each application"
        ]
    },
    'fresher': {
        'patterns': [r'fresher', r'no\s*experience', r'fresh\s*grad', r'entry\s*level',
                     r'first\s*job', r'new\s*grad', r'beginner', r'student'],
        'responses': [
            "🎓 **Tips for Freshers / Entry-Level:**\n\n1. **Lead with Education** — GPA (if >3.5), relevant coursework, thesis\n2. **Highlight Projects** — Academic, personal, or open-source contributions\n3. **Include Internships** — Even short ones count!\n4. **Add Certifications** — Coursera, Udemy, freeCodeCamp, Google certs\n5. **Volunteer work & extracurriculars** show leadership and initiative\n6. **Skills section is crucial** — List all relevant technologies\n7. **Write a strong objective** — Show enthusiasm and willingness to learn\n\n💡 Don't apologize for lack of experience — focus on potential and eagerness to grow!"
        ]
    },
    'gap': {
        'patterns': [r'gap', r'employment\s*gap', r'career\s*gap', r'break\s*in\s*career',
                     r'took\s*time\s*off'],
        'responses': [
            "⏸️ **Handling Career Gaps:**\n\n1. **Be honest** — Don't try to hide gaps with fake dates\n2. **Frame positively** — What did you learn or do during the gap?\n3. **Show continuous learning** — Online courses, freelance work, volunteering\n4. **Use a functional/hybrid resume format** — Emphasize skills over chronology\n5. **Brief explanation in cover letter** — Keep it professional and forward-looking\n\n**Good reasons:** Further education, family care, health recovery, personal projects, travel, freelancing — all valid!"
        ]
    },
    'thanks': {
        'patterns': [r'thank', r'thanks', r'thx', r'appreciate', r'helpful'],
        'responses': [
            "You're welcome! 😊 Happy to help with your career journey. Feel free to ask me anything else about resumes, interviews, or career planning!",
            "Glad I could help! 🌟 Remember, a great resume is just the beginning — keep building skills and networking. Good luck!",
            "Anytime! 💪 Your career success matters to us. Upload your resume for a detailed AI analysis whenever you're ready!"
        ]
    },
    'hello': {
        'patterns': [r'^hi$', r'^hello$', r'^hey$', r'^hii+$', r'^heyy+$', r'^yo$',
                     r'good\s*(morning|afternoon|evening)', r'^sup$', r'^howdy$'],
        'responses': GREETINGS
    }
}

def get_chatbot_response(message):
    """
    Process a user message and return a relevant response.
    Uses keyword matching against the knowledge base.
    """
    if not message or not message.strip():
        return random.choice(GREETINGS)

    msg = message.strip().lower()

    best_match = None
    best_score = 0

    for category, data in RESPONSES.items():
        for pattern in data['patterns']:
            if re.search(pattern, msg, re.IGNORECASE):
                # Count number of pattern matches for this category
                score = sum(1 for p in data['patterns'] if re.search(p, msg, re.IGNORECASE))
                if score > best_score:
                    best_score = score
                    best_match = category

    if best_match:
        return random.choice(RESPONSES[best_match]['responses'])

    return random.choice(FALLBACK_RESPONSES)
