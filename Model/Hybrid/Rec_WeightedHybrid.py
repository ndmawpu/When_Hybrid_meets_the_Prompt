import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

np.random.seed(32)

def weighted_hybrid_recommend(course_name, predictions_knn, predictions_lasso, rating_info_subset , num_recommendations=5, cf_weight=0.05, cbf_weight=0.95):

    # Combine predictions using weighted hybrid approach
    combined_predictions = [(cf_weight * cf_pred) + (cbf_weight * cbf_pred) for cf_pred, cbf_pred in zip(predictions_knn, predictions_lasso)]
    
    # Sort predictions and get top recommendations
    top_indices = np.argsort(combined_predictions)[::-1][:num_recommendations]
    top_recommendations = rating_info_subset.iloc[top_indices][['item_id', 'item_name', 'item_category', 'rating']]
    top_recommendations = top_recommendations.rename(columns={'rating': 'item_avg_rating'})
    
    return top_recommendations

def cbf_recommend(course_name, rating_info_subset, lasso_model, num_recommendations=5):
    if isinstance(course_name, list):
        course_name = course_name[-1]
    content_features = ['item_category', 'item_subcategory', 'item_description']

    index = rating_info_subset[rating_info_subset['item_name'] == course_name].index[0]
    
    course_description_vector = lasso_model.named_steps['preprocessor'].transform(rating_info_subset.iloc[[index]][content_features]).toarray()
    
    similarities = cosine_similarity(course_description_vector, lasso_model.named_steps['preprocessor'].transform(rating_info_subset[content_features]).toarray())
    
    similar_courses_indices = similarities.argsort()[0][::-1][1:]
    unique_courses_indices = rating_info_subset.iloc[similar_courses_indices].drop_duplicates(subset='item_name').index[:num_recommendations+1]

    similar_courses = rating_info_subset.loc[unique_courses_indices][['item_id','item_name', 'item_category', 'rating']]
    similar_courses = similar_courses.rename(columns={'rating': 'item_avg_rating'}).iloc[1:,:]
    
    return similar_courses