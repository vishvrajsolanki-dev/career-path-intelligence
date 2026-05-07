# utils/recommender.py
# PURPOSE: Generate a learning roadmap for missing skills
#
# HOW IT WORKS:
# 1. Takes the list of missing skill keywords
# 2. Matches each keyword against a curated resource library
# 3. Returns prioritized learning steps with free resource links

# ─────────────────────────────────────────
# RESOURCE LIBRARY
# Maps skill keywords → learning resources
# Format: keyword → {title, platform, url, duration}
# ─────────────────────────────────────────

RESOURCE_LIBRARY = {
    # Python & Programming
    "python": {
        "title": "Python for Everybody",
        "platform": "Coursera (Free Audit)",
        "url": "https://www.coursera.org/specializations/python",
        "duration": "2–3 weeks"
    },
    "programming": {
        "title": "CS50: Introduction to Programming",
        "platform": "edX (Free)",
        "url": "https://cs50.harvard.edu/python",
        "duration": "3–4 weeks"
    },

    # Data & ML
    "machine": {
        "title": "Machine Learning Specialization",
        "platform": "Coursera (Free Audit)",
        "url": "https://www.coursera.org/specializations/machine-learning-introduction",
        "duration": "3–4 weeks"
    },
    "learning": {
        "title": "Machine Learning Specialization",
        "platform": "Coursera (Free Audit)",
        "url": "https://www.coursera.org/specializations/machine-learning-introduction",
        "duration": "3–4 weeks"
    },
    "deep": {
        "title": "Deep Learning Specialization",
        "platform": "Coursera (Free Audit)",
        "url": "https://www.coursera.org/specializations/deep-learning",
        "duration": "4–5 weeks"
    },
    "neural": {
        "title": "Deep Learning Specialization",
        "platform": "Coursera (Free Audit)",
        "url": "https://www.coursera.org/specializations/deep-learning",
        "duration": "4–5 weeks"
    },
    "pandas": {
        "title": "Pandas Documentation + Kaggle Course",
        "platform": "Kaggle (Free)",
        "url": "https://www.kaggle.com/learn/pandas",
        "duration": "3–5 days"
    },
    "numpy": {
        "title": "NumPy Fundamentals",
        "platform": "Kaggle (Free)",
        "url": "https://www.kaggle.com/learn/intro-to-machine-learning",
        "duration": "3–5 days"
    },
    "scikit": {
        "title": "Scikit-learn: Machine Learning in Python",
        "platform": "Official Docs + Kaggle",
        "url": "https://scikit-learn.org/stable/tutorial",
        "duration": "1 week"
    },
    "tensorflow": {
        "title": "TensorFlow Developer Certificate Prep",
        "platform": "Coursera (Free Audit)",
        "url": "https://www.coursera.org/professional-certificates/tensorflow-in-practice",
        "duration": "4 weeks"
    },
    "pytorch": {
        "title": "PyTorch Tutorials",
        "platform": "PyTorch Official (Free)",
        "url": "https://pytorch.org/tutorials",
        "duration": "1–2 weeks"
    },

    # Data Engineering
    "sql": {
        "title": "SQL for Data Science",
        "platform": "Coursera (Free Audit)",
        "url": "https://www.coursera.org/learn/sql-for-data-science",
        "duration": "1–2 weeks"
    },
    "database": {
        "title": "Databases and SQL for Data Science",
        "platform": "Coursera (Free Audit)",
        "url": "https://www.coursera.org/learn/sql-data-science",
        "duration": "1–2 weeks"
    },
    "spark": {
        "title": "Apache Spark with Python (PySpark)",
        "platform": "Udemy / YouTube",
        "url": "https://www.youtube.com/results?search_query=pyspark+tutorial",
        "duration": "1–2 weeks"
    },
    "hadoop": {
        "title": "Hadoop Platform and Application Framework",
        "platform": "Coursera (Free Audit)",
        "url": "https://www.coursera.org/learn/hadoop",
        "duration": "2 weeks"
    },
    "etl": {
        "title": "ETL and Data Pipelines with Shell, Airflow and Kafka",
        "platform": "Coursera (Free Audit)",
        "url": "https://www.coursera.org/learn/etl-and-data-pipelines-shell-airflow-kafka",
        "duration": "2 weeks"
    },
    "warehousing": {
        "title": "Data Warehousing for Business Intelligence",
        "platform": "Coursera (Free Audit)",
        "url": "https://www.coursera.org/specializations/data-warehousing",
        "duration": "2–3 weeks"
    },

    # Web Development
    "javascript": {
        "title": "JavaScript Algorithms and Data Structures",
        "platform": "freeCodeCamp (Free)",
        "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures",
        "duration": "2–3 weeks"
    },
    "react": {
        "title": "React - The Complete Guide",
        "platform": "freeCodeCamp (Free)",
        "url": "https://www.freecodecamp.org/learn/front-end-development-libraries",
        "duration": "2 weeks"
    },
    "html": {
        "title": "Responsive Web Design",
        "platform": "freeCodeCamp (Free)",
        "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design",
        "duration": "1–2 weeks"
    },
    "css": {
        "title": "Responsive Web Design",
        "platform": "freeCodeCamp (Free)",
        "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design",
        "duration": "1–2 weeks"
    },
    "node": {
        "title": "Node.js Tutorial for Beginners",
        "platform": "YouTube (Free)",
        "url": "https://www.youtube.com/results?search_query=node.js+tutorial+beginners",
        "duration": "1 week"
    },
    "api": {
        "title": "APIs and Microservices",
        "platform": "freeCodeCamp (Free)",
        "url": "https://www.freecodecamp.org/learn/back-end-development-and-apis",
        "duration": "1–2 weeks"
    },

    # DevOps & Cloud
    "docker": {
        "title": "Docker for Beginners",
        "platform": "Docker Official Docs (Free)",
        "url": "https://docs.docker.com/get-started",
        "duration": "3–5 days"
    },
    "kubernetes": {
        "title": "Kubernetes Basics",
        "platform": "Kubernetes Official (Free)",
        "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics",
        "duration": "1 week"
    },
    "cloud": {
        "title": "AWS Cloud Practitioner Essentials",
        "platform": "AWS Training (Free)",
        "url": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials",
        "duration": "1–2 weeks"
    },
    "aws": {
        "title": "AWS Cloud Practitioner Essentials",
        "platform": "AWS Training (Free)",
        "url": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials",
        "duration": "1–2 weeks"
    },
    "azure": {
        "title": "Microsoft Azure Fundamentals (AZ-900)",
        "platform": "Microsoft Learn (Free)",
        "url": "https://learn.microsoft.com/en-us/training/paths/azure-fundamentals",
        "duration": "1–2 weeks"
    },

    # Security
    "security": {
        "title": "Introduction to Cyber Security",
        "platform": "Coursera (Free Audit)",
        "url": "https://www.coursera.org/specializations/intro-cyber-security",
        "duration": "2–3 weeks"
    },
    "encryption": {
        "title": "Cryptography and Information Theory",
        "platform": "Coursera (Free Audit)",
        "url": "https://www.coursera.org/learn/crypto",
        "duration": "2 weeks"
    },

    # Marketing & Analytics
    "marketing": {
        "title": "Fundamentals of Digital Marketing",
        "platform": "Google Digital Garage (Free)",
        "url": "https://learndigital.withgoogle.com/digitalgarage/course/digital-marketing",
        "duration": "1–2 weeks"
    },
    "analytics": {
        "title": "Google Analytics Certification",
        "platform": "Google (Free)",
        "url": "https://skillshop.google.com/google-analytics",
        "duration": "1 week"
    },
    "seo": {
        "title": "SEO Fundamentals",
        "platform": "SEMrush Academy (Free)",
        "url": "https://www.semrush.com/academy/courses/seo-fundamentals-course-with-greg-gifford",
        "duration": "1 week"
    },

    # Design
    "design": {
        "title": "Graphic Design Fundamentals",
        "platform": "Canva Design School (Free)",
        "url": "https://www.canva.com/designschool",
        "duration": "1 week"
    },
    "figma": {
        "title": "Figma Tutorial for Beginners",
        "platform": "YouTube (Free)",
        "url": "https://www.youtube.com/results?search_query=figma+tutorial+beginners",
        "duration": "3–5 days"
    },

    # Data Visualization
    "visualization": {
        "title": "Data Visualization with Python",
        "platform": "Coursera (Free Audit)",
        "url": "https://www.coursera.org/learn/python-for-data-visualization",
        "duration": "1 week"
    },
    "tableau": {
        "title": "Tableau Public Training",
        "platform": "Tableau Official (Free)",
        "url": "https://www.tableau.com/learn/training",
        "duration": "1 week"
    },
    "power": {
        "title": "Power BI Desktop for Beginners",
        "platform": "YouTube / Microsoft Learn (Free)",
        "url": "https://learn.microsoft.com/en-us/power-bi/fundamentals/service-get-started",
        "duration": "1 week"
    },

    # Networking
    "network": {
        "title": "Computer Networking: A Top-Down Approach",
        "platform": "Coursera (Free Audit)",
        "url": "https://www.coursera.org/learn/computer-networking",
        "duration": "2–3 weeks"
    },
    "linux": {
        "title": "Linux Command Line Basics",
        "platform": "Udacity (Free)",
        "url": "https://www.udacity.com/course/linux-command-line-basics--ud595",
        "duration": "1 week"
    },
}

# Default resource for skills not in the library
DEFAULT_RESOURCE = {
    "title": "Search on Coursera / YouTube",
    "platform": "Coursera or YouTube (Free)",
    "url": "https://www.coursera.org",
    "duration": "Varies"
}


# ─────────────────────────────────────────
# MAIN FUNCTION — GENERATE ROADMAP
# ─────────────────────────────────────────

def generate_roadmap(missing_keywords, role_name):
    """
    Takes a list of missing skill keywords and returns
    a prioritized learning roadmap.

    Parameters:
      missing_keywords → list of strings from gap_detector
      role_name        → string, job role title

    Returns:
      list of dicts, each with:
        'skill'    → the missing keyword
        'resource' → learning resource details
        'priority' → 'High' / 'Medium' / 'Low'
    """

    if not missing_keywords:
        return []

    roadmap = []

    # Deduplicate: some keywords map to the same resource
    # e.g. "machine" and "learning" both map to ML course
    seen_titles = set()

    for i, keyword in enumerate(missing_keywords):
        # Look up resource for this keyword
        resource = RESOURCE_LIBRARY.get(keyword, DEFAULT_RESOURCE)

        # Skip if we already added this exact course
        if resource['title'] in seen_titles:
            continue

        seen_titles.add(resource['title'])

        # Assign priority based on position in missing list
        # Earlier in list = appeared more in role skills = more important
        if i < 3:
            priority = "High"
        elif i < 7:
            priority = "Medium"
        else:
            priority = "Low"

        roadmap.append({
            'skill': keyword,
            'resource': resource,
            'priority': priority
        })

    return roadmap


# ─────────────────────────────────────────
# SELF-TEST
# ─────────────────────────────────────────

if __name__ == "__main__":
    # Simulate missing skills for a data scientist
    test_missing = [
        "spark", "hadoop", "docker", "tensorflow",
        "warehousing", "etl", "kubernetes", "cloud"
    ]

    print(f"Generating roadmap for missing skills:")
    print(f"Missing: {test_missing}\n")

    roadmap = generate_roadmap(test_missing, "data scientist")

    for i, step in enumerate(roadmap, 1):
        r = step['resource']
        print(f"Step {i} [{step['priority']} Priority]")
        print(f"  Skill    : {step['skill'].title()}")
        print(f"  Course   : {r['title']}")
        print(f"  Platform : {r['platform']}")
        print(f"  Duration : {r['duration']}")
        print(f"  Link     : {r['url']}")
        print()