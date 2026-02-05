
import sys
import os

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.rag import get_rag_service

def seed_expanded_data():
    print("🚀 Starting expanded knowledge base seeding...")
    rag = get_rag_service()
    
    knowledge_items = [
        # --- HEART RATE (AHA/Medical sources) ---
        {
            "content": "According to the American Heart Association (AHA), a normal resting heart rate for adults (ages 18+) ranges from 60 to 100 beats per minute (bpm). For children ages 6 to 15, the normal range is 70 to 100 bpm. Athletes may have lower resting heart rates, sometimes below 60 bpm, which can significantly indicate good cardiovascular fitness.",
            "category": "heart_rate",
            "tier": 1,
            "source": "American Heart Association",
            "title": "Normal Resting Heart Rate by Age (AHA)",
            "source_url": "https://www.heart.org/en/health-topics/high-blood-pressure/the-facts-about-high-blood-pressure/all-about-heart-rate-pulse"
        },
        {
            "content": "Factors influencing resting heart rate include: air temperature (increases hr), body position (standing > lying), emotions (stress/anxiety increases hr), body size (obesity may increase hr), and medication use (beta blockers decrease hr).",
            "category": "heart_rate",
            "tier": 2,
            "source": "American Heart Association",
            "title": "Factors Affecting Heart Rate",
            "source_url": "https://www.heart.org/en/health-topics/high-blood-pressure/the-facts-about-high-blood-pressure/all-about-heart-rate-pulse"
        },
        {
            "content": "Tachycardia is defined as a heart rate greater than 100 beats per minute while at rest. Bradycardia is defined as a heart rate slower than 60 beats per minute. Consult a doctor if you frequently experience these outside of exercise or sleep, especially if accompanied by fainting, dizziness, or shortness of breath.",
            "category": "heart_rate",
            "tier": 2,
            "source": "Mayo Clinic",
            "title": "Tachycardia and Bradycardia Definitions",
            "source_url": "https://www.mayoclinic.org/diseases-conditions/heart-arrhythmia/symptoms-causes/syc-20350668"
        },
         {
            "content": "Newborns (0-1 month) have a resting heart rate of 70-190 bpm. Infants (1-11 months) range from 80-160 bpm. Children 1-2 years: 80-130 bpm. Children 3-4 years: 80-120 bpm. Children 5-6 years: 75-115 bpm. Children 7-9 years: 70-110 bpm. Children 10+ years: 60-100 bpm.",
            "category": "heart_rate",
            "tier": 2,
            "source": "Cleveland Clinic / Lancet",
            "title": "Pediatric Heart Rate Ranges",
            "source_url": "https://my.clevelandclinic.org/health/diagnostics/17402-pulse--heart-rate"
        },

        # --- SLEEP (National Sleep Foundation) ---
        {
            "content": "The National Sleep Foundation recommends the following sleep durations: Newborns (0-3 months): 14-17 hours. Infants (4-11 months): 12-15 hours. Toddlers (1-2 years): 11-14 hours. Preschoolers (3-5 years): 10-13 hours. School-aged (6-13 years): 9-11 hours.",
            "category": "sleep",
            "tier": 1,
            "source": "National Sleep Foundation",
            "title": "Sleep Duration Recommendations (Children)",
            "source_url": "https://www.sleepfoundation.org/how-sleep-works/how-much-sleep-do-we-really-need"
        },
        {
            "content": "The National Sleep Foundation recommends the following sleep durations for adults: Teenagers (14-17 years): 8-10 hours. Young Adults (18-25 years): 7-9 hours. Adults (26-64 years): 7-9 hours. Older Adults (65+): 7-8 hours. Sleep needs are individual, but consistently sleeping out of range may indicate health issues.",
            "category": "sleep",
            "tier": 1,
            "source": "National Sleep Foundation",
            "title": "Sleep Duration Recommendations (Adults)",
            "source_url": "https://www.sleepfoundation.org/how-sleep-works/how-much-sleep-do-we-really-need"
        },
        {
            "content": "Sleep stages cycle every 90-120 minutes. A typical night includes 3-5 cycles. Stage 1 (N1): Light sleep, 1-7 mins. Stage 2 (N2): Light sleep, body temp drops, ~50% of total sleep. Stage 3 (N3): Deep sleep/Slow Wave Sleep, tissue repair and growth, immune boosting. REM (Rapid Eye Movement): Dreaming, memory consolidation, brain activity peaks.",
            "category": "sleep",
            "tier": 2,
            "source": "National Institutes of Health (NIH)",
            "title": "Sleep Stages and Architecture",
            "source_url": "https://www.ninds.nih.gov/health-information/public-education/brain-basics/brain-basics-understanding-sleep"
        },
        {
            "content": "Deep sleep (Stage N3) is crucial for physical restoration. It typically makes up 13-23% of total sleep for young adults. Deep sleep decreases with age. Lack of deep sleep is linked to reduced immunity and physical recovery.",
            "category": "sleep",
            "tier": 3,
            "source": "Sleep Medicine Reviews",
            "title": "Deep Sleep Importance",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/15892914/"
        },
        {
            "content": "REM sleep typically comprises 20-25% of total sleep in healthy adults. It is essential for cognitive functions like memory consolidation, learning, and emotional processing. Alcohol consumption can significantly suppress REM sleep.",
            "category": "sleep",
            "tier": 3,
            "source": "National Sleep Foundation",
            "title": "REM Sleep Functions",
            "source_url": "https://www.sleepfoundation.org/stages-of-sleep/rem-sleep"
        },

        # --- EXERCISE (ACSM Guidelines) ---
        {
            "content": "ACSM defines Moderate-intensity aerobic activity as 40% to 59% of Heart Rate Reserve (HRR) or VO2 Reserve. Vigorous-intensity activity is 60% to 89% of HRR. For most adults, ACSM recommends at least 150 minutes of moderate-intensity exercise per week.",
            "category": "exercise",
            "tier": 1,
            "source": "American College of Sports Medicine (ACSM)",
            "title": "ACSM Exercise Intensity Definitions",
            "source_url": "https://www.acsm.org/docs/default-source/files-for-resource-library/exercise-intensity-infographic.pdf"
        },
        {
            "content": "Heart Rate Reserve (HRR) Calculation (Karvonen Formula): Target HR = ((Max HR − Resting HR) × %Intensity) + Resting HR. This method is more accurate than straight percentage of Max HR because it accounts for individual resting heart rate differences.",
            "category": "exercise",
            "tier": 2,
            "source": "ACSM Guidelines for Exercise Testing and Prescription",
            "title": "Calculating Heart Rate Reserve (Karvonen Method)",
            "source_url": "https://www.acsm.org/education-resources/trending-topics-resources/physical-activity-guidelines"
        },
         {
            "content": "Zone 2 Training often refers to exercising at 60-70% of Maximum Heart Rate (or high-end of moderate intensity). It improves mitochondrial efficiency, fat oxidation, and lactate clearance capacity. It is considered the foundation of endurance performance.",
            "category": "exercise",
            "tier": 2,
            "source": "Sports Medicine",
            "title": "Zone 2 Training Benefits",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/15315486/"
        },
        {
            "content": "Maximum Heart Rate (MHR) is commonly estimated as 220 minus age. However, this formula can verify significantly (±10-12 bpm). More accurate formulas exist, such as Tanaka (208 - 0.7 × age), but a maximal stress test is the gold standard.",
            "category": "exercise",
            "tier": 2,
            "source": "Journal of American College of Cardiology",
            "title": "Maximum Heart Rate Estimation",
            "source_url": "https://www.acc.org/latest-in-cardiology/articles/2014/07/18/16/08/target-heart-rate-charts"
        },

        # --- HRV (Heart Rate Variability) ---
        {
            "content": "Heart Rate Variability (HRV) decreases naturally with age. There is no single 'normal' number that applies to everyone. Instead, HRV should be compared to your own baseline. A consistently trending down baseline may indicate chronic stress, overtraining, or illness.",
            "category": "hrv",
            "tier": 2,
            "source": "Cleveland Clinic",
            "title": "Age-Related HRV Changes",
            "source_url": "https://my.clevelandclinic.org/health/symptoms/21773-heart-rate-variability-hrv"
        },
        {
            "content": "High HRV is generally associated with a resilient autonomic nervous system and good cardiovascular fitness. Low HRV can indicate dominance of the sympathetic nervous system (fight or flight), stress, fatigue, or inflammation.",
            "category": "hrv",
            "tier": 2,
            "source": "Frontiers in Public Health",
            "title": "Interpreting HRV Highs and Lows",
            "source_url": "https://www.frontiersin.org/articles/10.3389/fpubh.2017.00258/full"
        },
        {
            "content": "RMSSD (Root Mean Square of Successive Differences) is the most common time-domain metric for tracking daily recovery via HRV. It primarily reflects parasympathetic (rest-and-digest) activity.",
            "category": "hrv",
            "tier": 3,
            "source": "Circulation (AHA Journal)",
            "title": "HRV Metrics: RMSSD",
            "source_url": "https://www.ahajournals.org/doi/10.1161/01.CIR.93.5.1043"
        },

        # --- STRESS ---
        {
            "content": "Chronic stress keeps the body in a state of sympathetic dominance, leading to elevated resting heart rate, suppressed HRV, and disrupted sleep architecture (less deep sleep). Long-term risks include hypertension and cardiovascular disease.",
            "category": "stress",
            "tier": 2,
            "source": "American Psychological Association",
            "title": "Physiological Impact of Chronic Stress",
            "source_url": "https://www.apa.org/topics/stress/body"
        },
        {
            "content": "Breathing exercises (like Box Breathing or 4-7-8 breathing) can acutely activate the vagus nerve, increasing HRV and lowering heart rate by shifting the autonomic nervous system towards a parasympathetic state.",
            "category": "stress",
            "tier": 2,
            "source": "PubMed Central / Nature",
            "title": "Breathing Techniques for Stress Reduction",
            "source_url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6137615/"
        }
    ]

    print(f"📦 Prepared {len(knowledge_items)} items for ingestion.")
    
    # Process items
    docs = [item["content"] for item in knowledge_items]
    metadatas = [
        {
            "category": item["category"],
            "source": item["source"],
            "tier": item["tier"],
            "title": item["title"],
            "source_url": item["source_url"]
        } 
        for item in knowledge_items
    ]
    ids = [f"seed_exp_{i}" for i in range(len(knowledge_items))]

    print("💾 Ingesting into ChromaDB...")
    rag.collection.add(
        documents=docs,
        metadatas=metadatas,
        ids=ids
    )
    print("✅ Successfully expanded knowledge base!")

if __name__ == "__main__":
    seed_expanded_data()
