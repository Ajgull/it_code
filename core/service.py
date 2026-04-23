def calculate_comment_depth(parent_comment):
    if parent_comment:
        if parent_comment.depth_level > 2:
            return 2
        else:
            return parent_comment.depth_level + 1
    return 0
