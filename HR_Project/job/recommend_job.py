import re

import pandas as pd
from ftfy import fix_text
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# list of unnecessary words
stopw = set(stopwords.words("english"))


def get_jobs_recommendations(df, skills, nb=5):
    skills = skills["skills"]
    skills_list = skills.split(" ")
    skills = []
    skills.append(" ".join(word for word in skills_list))
    print(skills)

    # job requirements cleaning up
    df["test"] = df["requirements"].apply(
        lambda x: " ".join(
            [word for word in str(x).split() if len(word) > 2 and word not in (stopw)]
        )
    )
    df["job_requirements"] = df["test"]

    print(df)

    # skills to clean up
    org_name_clean = skills

    def ngrams(string, n=3):
        # Fix text using the 'ftfy' library
        string = fix_text(string)

        # Remove non-ASCII characters
        string = string.encode("ascii", errors="ignore").decode()

        string = string.lower()
        # Remove specified characters
        chars_to_remove = [")", "(", ".", "|", "[", "]", "{", "}", "'"]
        rx = "[" + re.escape("".join(chars_to_remove)) + "]"
        # print("RX ", rx)
        string = re.sub(rx, "", string)
        # Replace "&" with "and"
        string = string.replace("&", "and")
        # Replace "," with space
        string = string.replace(",", " ")
        # Replace "-" with space
        string = string.replace("-", " ")
        # Normalize case - capitalize the start of each word
        string = string.title()
        # Get rid of multiple spaces and replace with a single space
        string = re.sub(" +", " ", string).strip()
        # Pad names for n-grams
        string = " " + string + " "
        # Remove certain characters and create n-grams
        string = re.sub(r"[,-./]|\sBD", r"", string)
        ngrams = zip(*[string[i:] for i in range(n)])
        # Join the n-grams to form a list of strings
        return ["".join(ngram) for ngram in ngrams]

    # creation of vector to vectorize the cleaned skills (org_name_clean)
    vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams, lowercase=False)
    # transform skills to vector
    tfidf = vectorizer.fit_transform(org_name_clean)
    print("BOOOOO Vectorization completed...")

    # get the distance between the vectors
    def getNearestN(query):
        queryTFIDF_ = vectorizer.transform(query)
        distances, indices = nbrs.kneighbors(queryTFIDF_)
        return distances, indices

    # model KNN for prediction
    nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1).fit(tfidf)
    # get cleaned up job descriptions
    unique_org = df["test"].values
    #
    distances, indices = getNearestN(unique_org)
    unique_org = list(unique_org)
    matches = []
    for i, j in enumerate(indices):
        # dist = round(distances[i][0], 2)
        dist = round(1 / (1 + distances[i][0]) * 100, 2)
        temp = [dist]
        matches.append(temp)

    val = matches
    matches = pd.DataFrame(matches, columns=["Match confidence"])
    print(matches)
    df["match"] = matches["Match confidence"]
    df1 = df.sort_values("match", ascending=False)
    df2 = (
        df1[["id", "title", "salary", "job_type", "job_requirements", "match"]]
        .head(nb)
        .reset_index()
    )
    print(df2)
    val = round(matches.at[0, "Match confidence"], 2)
    return (df2, val)
