import pandas as pd

class ContextGeneration:
    
    posts_file='Dataset/reddit_posts.csv'
    comments_file = 'Dataset/reddit_post_comments.csv'

    def find_related_posts_and_comments(posts_file, comments_file, search_string):
        # Convert the search string to lowercase for case-insensitive comparison
        search_string_lower = search_string.lower()

        # Process posts and comments in chunks to save memory
        results = {}
        
        # Process the posts in chunks
        posts_chunk_iterator = pd.read_csv(posts_file, chunksize=1000)  # Adjust chunksize based on memory availability
        for posts_chunk in posts_chunk_iterator:
            # Fill NaN values with empty strings for this chunk
            posts_chunk['post_title'] = posts_chunk['post_title'].fillna('')
            posts_chunk['selftext'] = posts_chunk['selftext'].fillna('')

            # Search for matching posts in the chunk
            matching_posts = posts_chunk[
                (posts_chunk['post_title'].str.contains(search_string_lower, case=False, na=False)) |
                (posts_chunk['selftext'].str.contains(search_string_lower, case=False, na=False))
            ]

            # Store matching posts in the results
            for _, post_row in matching_posts.iterrows():
                post_id = post_row['post_id']
                if post_id not in results:
                    results[post_id] = {
                        'post title': post_row['post_title'],
                        'texts': post_row['selftext'],
                        'comments': []
                    }

        # Process the comments in chunks
        comments_chunk_iterator = pd.read_csv(comments_file, chunksize=1000)  # Adjust chunksize based on memory availability
        for comments_chunk in comments_chunk_iterator:
            # Fill NaN values with empty strings for this chunk
            comments_chunk['comment'] = comments_chunk['comment'].fillna('')

            # Search for matching comments in the chunk
            matching_comments = comments_chunk[
                comments_chunk['comment'].str.contains(search_string_lower, case=False, na=False)
            ]

            # Store matching comments in the results
            for _, comment_row in matching_comments.iterrows():
                post_id = comment_row['post_id']
                if post_id in results:
                    results[post_id]['comments'].append(comment_row['comment'])

        return results
    
    def generateContext(message):
        
        find_relative_result=ContextGeneration.find_related_posts_and_comments(ContextGeneration.posts_file,ContextGeneration.comments_file, message)
        
        posts_title=[]
        posts_text=[]
        post_comments=[]
        
        for post_id, content in find_relative_result.items():
            # print(f"Post ID: {post_id}")
            # print(f"Title: {content['post title']}")
            posts_title.append(content['post title'][:5])
            # print(f"Text: {content['texts']}")
            posts_text.append(content['texts'][:5])
            # print(f"Comments: {content['comments']}")
            post_comments.append(content['comments'][:5])
        
        return posts_title,posts_text,post_comments