import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from math import sqrt


def delete_duplicate(row):
    return list(set(row))


def delete_space(row):
    for i in range(0, len(row)):
        row[i] = row[i].replace(" ", "")
    return row


def convert_to_dataframe(df):
    return pd.DataFrame(df)


def preprocessing(df):
    # delete duplicates
    df['purpose'] = df['purpose'].apply(delete_duplicate)
    df['interest'] = df['interest'].apply(delete_duplicate)
    df['can'] = df['can'].apply(delete_duplicate)
    df['want'] = df['want'].apply(delete_duplicate)

    # delete space
    df['purpose'] = df['purpose'].apply(delete_space)
    df['interest'] = df['interest'].apply(delete_space)
    df['can'] = df['can'].apply(delete_space)
    df['want'] = df['want'].apply(delete_space)

    # convert to literal
    df['purpose'] = df['purpose'].apply(lambda x : (' ').join(x))
    df['interest'] = df['interest'].apply(lambda x : (' ').join(x))
    df['can'] = df['can'].apply(lambda x : (' ').join(x))
    df['want'] = df['want'].apply(lambda x : (' ').join(x))

    return df


def get_results(df, id):
    df = convert_to_dataframe(df)


    df = preprocessing(df)

    print(df)

    # CountVectorizer
    count_vect = CountVectorizer(ngram_range=(1, 1))
    purpose_mat = count_vect.fit_transform(df['purpose'])
    interest_mat = count_vect.fit_transform(df['interest'])
    can_mat = count_vect.fit_transform(df['can'])
    want_mat = count_vect.fit_transform(df['want'])

    # calculate cosine similarity
    purpose_sim = cosine_similarity(purpose_mat, purpose_mat)
    interest_sim = cosine_similarity(interest_mat, interest_mat)
    lan_sim = cosine_similarity(can_mat, want_mat)

    # specific user profile
    profile = df[df['id'] == id]
    profile_idx = profile.index.values

    # add similarity column
    df["purpose_similarity"] = purpose_sim[profile_idx, :].reshape(-1, 1)
    df["interest_similarity"] = interest_sim[profile_idx, :].reshape(-1, 1)
    df["language_similarity"] = lan_sim[profile_idx, :].reshape(-1,1)

    my_purpose = df.iloc[profile_idx[0], 1]

    if '친목' in my_purpose:
        minmax_scaler = MinMaxScaler()
        df['similarity'] = 0.3*df['purpose_similarity'] + 0.2*df['interest_similarity'] + 0.5*df['language_similarity']
        df = df.sort_values(by="similarity", ascending=False)
        print(df)
        print(df['id'].to_list())
        return df['id'].to_list()
    elif '언어교류' in my_purpose:
        minmax_scaler = MinMaxScaler()
        df['similarity'] = 0.3*df['purpose_similarity'] + 0.2*df['interest_similarity'] + 0.5*df['language_similarity']
        df = df.sort_values(by="similarity", ascending=False)
        print(df)
        print(df['id'].to_list())
        return df['id'].to_list()
    elif '문화교류' in my_purpose:
        minmax_scaler = MinMaxScaler()
        df['similarity'] = 0.3*df['purpose_similarity'] + 0.2*df['interest_similarity'] + 0.5*df['language_similarity']
        df = df.sort_values(by="similarity", ascending=False)
        print(df)
        print(df['id'].to_list())
        return df['id'].to_list()