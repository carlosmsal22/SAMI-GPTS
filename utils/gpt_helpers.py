def analyze_sentiment(company_name, texts, sources):
    """Enhanced sentiment analysis with source weighting"""
    from collections import defaultdict
    
    # Simple scoring (replace with actual GPT call in production)
    scores = []
    source_scores = defaultdict(list)
    
    for text, source in zip(texts, sources):
        # Simple mock analysis - replace with:
        # result = run_gpt_prompt(f"Analyze sentiment (1-10) for: {text}")
        score = random.randint(3, 9)  # Mock score
        scores.append(score)
        source_scores[source].append(score)
    
    # Generate mock report
    return {
        'summary': f"""
        {company_name} Digital Sentiment Report:
        - Average Score: {sum(scores)/len(scores):.1f}/10
        - Strongest Source: {max(source_scores, key=lambda k: sum(source_scores[k])/len(source_scores[k]))}
        - Weakest Source: {min(source_scores, key=lambda k: sum(source_scores[k])/len(source_scores[k]))}
        """,
        'sentiment_by_source': [
            {'source': k, 'score': sum(v)/len(v)} 
            for k, v in source_scores.items()
        ]
    }
