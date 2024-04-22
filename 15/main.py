import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

X = np.nan
R = np.array([
    [5, 4, X, 1, 2, 1], #  
    [4, X, 3, 1, 1, 2], #
    [X, 5, 5, X, 3, 3], # item
    [2, X, 1, 4, 5, 4], # 
    [1, 2, 1, X, 5, 4]  #
   #       user 
])

class CF(object):
    def __init__(self, R):
        self.ori_data = R.copy()
        self.data = R.copy()
        self.n, self.m = self.data.shape
        self.kneighbors = 2
    
    def __normalize(self):
        self.col_means = np.nanmean(self.data, axis=0)
        nan_indices = np.isnan(self.data)
        self.data -= self.col_means
        self.data[nan_indices] = 0

    def __similarity(self):
        self.S = cosine_similarity(self.data.T)

    def fit(self):
        self.__normalize()
        self.__similarity()
    
    def predict(self, u, i):
        similiar_users = np.argsort(self.S[u])[::-1][1:self.kneighbors+1]
        users_with_rating = [v for v in similiar_users if not np.isnan(self.ori_data[i, v])]

        if len(users_with_rating) == 0:
            return -1
        
        weighted_sum = np.sum([self.S[u, v] * self.data[i, v] for v in users_with_rating])
        sum_of_weights = np.sum([np.abs(self.S[u, v]) for v in users_with_rating])

        if sum_of_weights == 0:
            return -1
        
        return weighted_sum / sum_of_weights

    def recommend(self, u):
        recommended_items = []
        for i in range(self.n):
            if np.isnan(self.ori_data[i, u]):
                rating = self.predict(u, i)
                if rating > 0:
                    recommended_items.append(i)
        return recommended_items

cf = CF(R)
cf.fit()

print(cf.recommend(1))