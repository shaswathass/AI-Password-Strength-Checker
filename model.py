import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Larger dataset
data = {
    "password": [
        # Weak
        "1", "12", "123", "1234", "12345", "123456",
        "password", "qwerty", "111111", "000000",

        # Medium
        "hello123", "abc12345", "letmein2024",
        "user2023", "welcome1", "india123",

        # Strong
        "Xy@9!kLm2", "Str0ng#Pass!", "A1b2C3$%",
        "Secure@2024!", "My$tr0ngP@ss"
    ],
    "strength": [
        0,0,0,0,0,0,
        0,0,0,0,

        1,1,1,
        1,1,1,

        2,2,2,
        2,2
    ]
}

df = pd.DataFrame(data)

X = df["password"]
y = df["strength"]

vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1,2))
X_vectorized = vectorizer.fit_transform(X)

model = LogisticRegression(max_iter=1000)
model.fit(X_vectorized, y)

pickle.dump((vectorizer, model), open("password_model.pkl", "wb"))

print("Improved model trained and saved!")
