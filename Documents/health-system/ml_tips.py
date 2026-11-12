import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import numpy as np

# 1. Create a synthetic training dataset
X_train = np.array([
    [2, 4, 0], [3, 5, 10], [5, 6, 20], [6, 7, 30], [8, 8, 45], [9, 9, 60]
])
y_train = np.array([0, 0, 1, 1, 2, 2])

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

def get_personalized_tip(water, sleep, exercise):
    try:
        water = int(water)
        sleep = float(sleep)
        exercise = int(exercise)
    except ValueError:
        return "Please log your habits to get a personalized tip!", []

    prediction = model.predict([[water, sleep, exercise]])[0]
    
    # Text Advice
    if prediction == 0:
        tip = "🚨 Wellness Alert: Your body needs immediate care! Your current habits are leading to fatigue."
    elif prediction == 1:
        tip = "⚠️ Needs Improvement: You are on the right track, but consistency is key to long-term health."
    else:
        tip = "🌟 Excellent! You are crushing your health goals! Keep maintaining this routine."

    # 2. AI Video Selection Logic (Using 100% Embeddable Educational IDs)
    recommended_videos = []

    if water < 8:
        # AsapSCIENCE: What Happens If You Don't Drink Water? (Always allows embed)
        recommended_videos.append({"title": "💧 The Importance of Hydration", "id": "UW5kZ9m4uXg"}) 
    
    if sleep < 8:
        # TED-Ed: Why do we sleep? (TED always allows embed)
        recommended_videos.append({"title": "😴 Science of Better Sleep", "id": "h2a5xO_yJkE"}) 
        
    if exercise < 30:
        # AsapSCIENCE: Benefits of Exercise
        recommended_videos.append({"title": "🏃 Quick Home Workouts", "id": "gC_L9qAHVJ8"}) 
        
    # If they meet ALL goals, suggest mental wellness
    if water >= 8 and sleep >= 8 and exercise >= 30:
        # Goodful: 5-Minute Meditation
        recommended_videos.append({"title": "🧘 Daily Mindfulness & Meditation", "id": "inpok4MKVLM"}) 
        
    # Fallback
    if not recommended_videos: 
        recommended_videos.append({"title": "🧘 Stress Management Tips", "id": "inpok4MKVLM"})

    return tip, recommended_videos

    prediction = model.predict([[water, sleep, exercise]])[0]
    
    # Text Advice
    if prediction == 0:
        tip = "🚨 Wellness Alert: Your body needs immediate care! Your current habits are leading to fatigue."
    elif prediction == 1:
        tip = "⚠️ Needs Improvement: You are on the right track, but consistency is key to long-term health."
    else:
        tip = "🌟 Excellent! You are crushing your health goals! Keep maintaining this routine."

    # 2. AI Video Selection Logic (Using Verified Direct IDs)
    recommended_videos = []

    # Goal is 8 glasses.
    if water < 8:
        # ID for "Why You Should Drink More Water" (Safe to embed)
        recommended_videos.append({"title": "💧 The Importance of Hydration", "id": "C31lS42916s"}) 
    
    # Goal is 8 hours.
    if sleep < 8:
        # ID for TED-Ed "Why do we sleep?"
        recommended_videos.append({"title": "😴 Science of Better Sleep", "id": "h2a5xO_yJkE"}) 
        
    # Goal is 30 mins.
    if exercise < 30:
        # ID for "Benefits of Exercise"
        recommended_videos.append({"title": "🏃 Quick Home Workouts", "id": "UBMk30rjy0o"}) 
        
    # If they meet ALL goals, suggest mental wellness
    if water >= 8 and sleep >= 8 and exercise >= 30:
        # ID for Headspace Meditation
        recommended_videos.append({"title": "🧘 Daily Mindfulness & Meditation", "id": "inpok4MKVLM"}) 
        
    # Fallback
    if not recommended_videos: 
        recommended_videos.append({"title": "🧘 Stress Management Tips", "id": "inpok4MKVLM"})

    return tip, recommended_videos