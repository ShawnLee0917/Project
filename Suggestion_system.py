def _calculate_unified_match_score(
    candidate_project,
    reference_data=None,
    user_interests=None,
    user_skills=None,
    mode='ai'
):
    """
    Unified matching algorithm for both AI suggestions and similar projects.
    
    Args:
        candidate_project: Project object to score
        reference_data: Dict with keys: 'languages', 'description' (for similar projects mode)
        user_interests: List of user interests (for AI suggestions mode)
        user_skills: List of user skills (for AI suggestions mode)
        mode: 'ai' for AI suggestions or 'similar' for similar projects
    
    Returns:
        Score from 0-100 representing project relevance
    """
    
    STOPWORDS = {
        'the', 'a', 'an', 'and', 'or', 'in', 'on', 'is', 'to', 'for', 'of',
        'with', 'that', 'this', 'it', 'as', 'are', 'was', 'be', 'from', 'at',
        'by', 'we', 'our', 'your', 'not', 'has', 'have', 'will', 'can', 'i',
        'its', 'an', 'using', 'used', 'use', 'based', 'built', 'build',
        'project', 'help', 'need', 'team', 'member', 'members'
    }
    
    PROGRAMMING_LANGUAGES = {
        'python': ['python', 'py'],
        'javascript': ['javascript', 'js'],
        'typescript': ['typescript', 'ts'],
        'java': ['java'],
        'c++': ['c++', 'cpp'],
        'c#': ['c#', 'csharp', '.net', 'dotnet'],
        'php': ['php'],
        'ruby': ['ruby', 'rails'],
        'go': ['go', 'golang'],
        'rust': ['rust'],
        'kotlin': ['kotlin'],
        'swift': ['swift'],
        'sql': ['sql', 'plsql', 'mysql', 'postgres', 'postgresql'],
        'html': ['html', 'html5'],
        'css': ['css', 'scss', 'sass', 'less'],
        'react': ['react', 'reactjs', 'react.js'],
        'vue': ['vue', 'vuejs', 'vue.js'],
        'angular': ['angular', 'angularjs'],
        'nodejs': ['nodejs', 'node.js', 'node'],
        'django': ['django'],
        'flask': ['flask'],
        'spring': ['spring', 'springboot', 'spring boot'],
        'docker': ['docker'],
        'kubernetes': ['kubernetes', 'k8s'],
        'terraform': ['terraform'],
    }
    
    interest_keywords = {
        'web development': ['web', 'frontend', 'backend', 'react', 'vue', 'django', 'flask', 'nodejs', 'node.js', 'express', 'html', 'css', 'javascript', 'typescript', 'responsive', 'api', 'rest', 'graphql'],
        'mobile development': ['mobile', 'ios', 'android', 'flutter', 'react native', 'swift', 'kotlin', 'app', 'native', 'cross-platform'],
        'ai/ml': ['ai', 'ml', 'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'nlp', 'cv', 'neural', 'model', 'algorithm', 'prediction'],
        'data science': ['data', 'science', 'analytics', 'pandas', 'numpy', 'visualization', 'dashboard', 'bi', 'warehouse', 'etl', 'spark'],
        'devops': ['devops', 'docker', 'kubernetes', 'ci/cd', 'jenkins', 'automation', 'infrastructure', 'deployment', 'pipeline'],
        'cloud': ['cloud', 'aws', 'azure', 'gcp', 'google cloud', 'serverless', 'lambda', 'ec2', 'rds'],
        'blockchain': ['blockchain', 'crypto', 'cryptocurrency', 'web3', 'ethereum', 'smart contract', 'solidity'],
        'iot': ['iot', 'embedded', 'arduino', 'raspberry', 'sensor', 'microcontroller', 'hardware'],
        'python': ['python', 'django', 'flask', 'pandas', 'numpy', 'scikit', 'jupyter', 'fastapi'],
        'java': ['java', 'spring', 'springboot', 'android', 'maven', 'gradle', 'microservices'],
        'c++': ['c++', 'cpp', 'gaming', 'graphics', 'performance', 'embedded', 'real-time'],
        'c#': ['c#', 'csharp', '.net', 'dotnet', 'unity', 'windows', 'blazor', 'aspnet'],
        'javascript': ['javascript', 'js', 'nodejs', 'node.js', 'react', 'vue', 'angular', 'typescript'],
        'database': ['database', 'sql', 'mongodb', 'postgres', 'postgresql', 'mysql', 'redis', 'cassandra', 'elastic'],
        'design': ['design', 'ui', 'ux', 'figma', 'adobe', 'photoshop', 'wireframe', 'prototype'],
        'security': ['security', 'encryption', 'cryptography', 'penetration', 'authentication', 'authorization', 'oauth', 'jwt'],
    }
    
    score = 0
    candidate_langs = (candidate_project.languages or '').lower()
    candidate_desc = (candidate_project.description or '').lower()
    candidate_roles = (candidate_project.roles_needed or '').lower()
    
    candidate_langs_set = set(l.strip().lower() for l in candidate_langs.split(',') if l.strip())
    candidate_desc_words = set(w for w in candidate_desc.split() if w not in STOPWORDS and len(w) > 2)
    
    if mode == 'similar':
        # SIMILAR PROJECTS MODE: Compare with reference project
        ref_langs = (reference_data.get('languages', '') or '').lower()
        ref_desc = (reference_data.get('description', '') or '').lower()
        
        ref_langs_set = set(l.strip().lower() for l in ref_langs.split(',') if l.strip())
        ref_desc_words = set(w for w in ref_desc.split() if w not in STOPWORDS and len(w) > 2)
        
        # Language overlap (30 pts max)
        lang_overlap = len(candidate_langs_set & ref_langs_set)
        lang_score = min(lang_overlap * 15, 30)
        score += lang_score
        
        # Description keyword overlap (25 pts max)
        if ref_desc_words and candidate_desc_words:
            desc_overlap = len(candidate_desc_words & ref_desc_words)
            desc_score = min(desc_overlap * 3, 25)
            score += desc_score
        
        # User interests bonus (20 pts max) - if user logged in
        if user_interests:
            user_interests_lower = [i.lower() for i in user_interests]
            combined_text = candidate_langs + ' ' + candidate_desc
            interest_hits = 0
            for interest in user_interests_lower:
                keywords = interest_keywords.get(interest, [])
                for keyword in keywords:
                    if keyword in combined_text:
                        interest_hits += 1
            
            interest_score = min(interest_hits * 5, 20)
            score += interest_score
        
        # Baseline score of 15 to ensure visibility
        score = min(100, 15 + score)
        
    else:  # mode == 'ai'
        # AI SUGGESTIONS MODE: Compare with user interests/skills
        if not user_interests:
            return 0
        
        user_interests_lower = [i.lower() for i in user_interests]
        
        # Factor 1: Direct Programming Language Matching (35 pts max)
        language_match_bonus = 0
        for interest in user_interests_lower:
            if interest in PROGRAMMING_LANGUAGES:
                lang_variants = PROGRAMMING_LANGUAGES[interest]
                for variant in lang_variants:
                    if variant in candidate_langs:
                        language_match_bonus += 12
            
            if interest in candidate_langs:
                language_match_bonus += 15
        
        for lang_name, lang_variants in PROGRAMMING_LANGUAGES.items():
            for variant in lang_variants:
                if variant in candidate_langs:
                    if lang_name in user_interests_lower or lang_name.lower() in ' '.join(user_interests_lower):
                        language_match_bonus += 6
        
        language_match_bonus = min(language_match_bonus, 35)
        score += language_match_bonus
        
        # Factor 2: Direct Interest Keyword Matching (30 pts max)
        interest_keyword_hits = set()
        for interest in user_interests_lower:
            keywords = interest_keywords.get(interest, [])
            for keyword in keywords:
                if keyword in candidate_desc or keyword in candidate_langs:
                    interest_keyword_hits.add(keyword)
        
        interest_match_score = min(len(interest_keyword_hits) * 2, 30)
        score += interest_match_score
        
        # Factor 3: Language Overlap with Interest Keywords (20 pts max)
        language_keyword_score = 0
        for interest in user_interests_lower:
            keywords = interest_keywords.get(interest, [])
            for keyword in keywords:
                for proj_lang in candidate_langs_set:
                    if keyword in proj_lang or proj_lang in keyword:
                        language_keyword_score += 6
        
        language_keyword_score = min(language_keyword_score, 20)
        score += language_keyword_score
        
        # Factor 4: Description Quality & Keyword Density (10 pts max)
        if candidate_desc:
            desc_keyword_matches = 0
            for interest in user_interests_lower:
                keywords = interest_keywords.get(interest, [])
                for keyword in keywords:
                    keyword_words = set(keyword.split())
                    if keyword_words & candidate_desc_words:
                        desc_keyword_matches += 1
            
            desc_match_score = min(desc_keyword_matches * 2, 10)
            score += desc_match_score
        
        # Factor 5: Skills-to-Roles Alignment Bonus (5 pts max)
        if user_skills and candidate_roles:
            user_skills_lower = [s.lower() for s in user_skills]
            skills_in_roles = 0
            for skill in user_skills_lower:
                if skill in candidate_roles:
                    skills_in_roles += 1
            
            skills_bonus = min(skills_in_roles * 2, 5)
            score += skills_bonus
        
        # Precision filters
        if score > 70:
            pass  # High quality, keep as is
        elif score < 30:
            score = max(score, 10)  # Minimum 10% for showing
        
        score = min(100, max(0, score))
    
    return int(score)


class Project:
    def __init__(self, name, languages, description, roles_needed=''):
        self.name = name
        self.languages = languages
        self.description = description
        self.roles_needed = roles_needed


def main():
    projects = [
        Project(
            'Study Planner',
            'Python, Django, JavaScript',
            'A web app that helps students plan study sessions and track progress.',
            'Python developer, frontend developer',
        ),
        Project(
            'Plant Disease Detector',
            'Python, TensorFlow',
            'An AI and machine learning tool that identifies plant diseases from images.',
            'Machine learning, data science',
        ),
        Project(
            'Community Events App',
            'JavaScript, React, Node.js',
            'A mobile-friendly web app for discovering local events and meeting people.',
            'Frontend developer, backend developer',
        ),
    ]

    print('Project suggestion system')
    interests = input('Enter your interests (comma-separated): ').strip()
    if not interests:
        print('Please enter at least one interest to get suggestions.')
        return

    skills = input('Enter your skills (comma-separated, optional): ').strip()
    user_interests = [interest.strip() for interest in interests.split(',') if interest.strip()]
    user_skills = [skill.strip() for skill in skills.split(',') if skill.strip()]

    suggestions = [
        (
            _calculate_unified_match_score(
                project,
                user_interests=user_interests,
                user_skills=user_skills,
            ),
            project,
        )
        for project in projects
    ]
    suggestions.sort(key=lambda item: item[0], reverse=True)

    print('\nSuggested projects:')
    for score, project in suggestions:
        print(f'  {project.name} - {score}% match')
        print(f'    Languages: {project.languages}')
        print(f'    {project.description}')


if __name__ == '__main__':
    main()





