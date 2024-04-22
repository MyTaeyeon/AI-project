import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

X = np.nan
R = np.array([
    [5, 5, 2, 0, 1, X, X], #  
    [4, X, X, 0, X, 2, X], #
    [X, 4, 1, X, X, 1, 1], # item
    [2, 2, 3, 4, 4, X, 4], # 
    [2, 0, 4, X, X, X, 5]  #
   #       user 
])

class CF(object):
    def __init__(self, R):
        self.ori_data = R.copy()
        self.data = R.copy()
        self.n, self.m = self.data.shape
        self.kneighbors = 2 # set kneighbor here
    
    def __normalize(self):
        self.row_means = np.nanmean(self.data, axis=1)
        nan_indices = np.isnan(self.data)
        self.data -= self.row_means[:, np.newaxis]
        self.data[nan_indices] = 0

    def __similarity(self):
        self.S = cosine_similarity(self.data)

    def fit(self):
        self.__normalize()
        self.__similarity()
    
    def predict(self, u, i):
        similiar_items = np.argsort(self.S[i])[::-1][1:self.kneighbors+1]
        rated_items = [v for v in similiar_items if not np.isnan(self.ori_data[v, u])]

        if len(rated_items) == 0:
            return -1
        
        weighted_sum = np.sum([self.S[i, v] * self.data[v, u] for v in rated_items])
        sum_of_weights = np.sum([np.abs(self.S[i, v]) for v in rated_items]) + 1e-8
        
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
print(cf.predict(0, 2))