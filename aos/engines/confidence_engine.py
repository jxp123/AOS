def confidence_from_evidence(evidence):
    score=30; joined=' '.join(evidence).lower()
    if 'inspection date' in joined or 'latest inspection date' in joined: score+=20
    if 'queen seen: yes' in joined: score+=15
    if 'eggs seen: yes' in joined: score+=15
    if 'brood frames:' in joined: score+=10
    if 'bee coverage frames:' in joined: score+=10
    if 'no inspection record' in joined: score-=25
    if 'unknown' in joined: score-=10
    score=max(0,min(100,score)); return {'score':score,'band':'High' if score>=80 else 'Medium' if score>=50 else 'Low'}
