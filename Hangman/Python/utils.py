def levenshtein(current_word, next_word):
    if len(current_word) < len(next_word):
        return levenshtein(next_word, current_word)
    if not current_word:
        return len(next_word)
 
    previous_row = xrange(len(next_word) + 1)
    
    for i, c1 in enumerate(current_word):
        current_row = [i + 1]
        for j, c2 in enumerate(next_word):
            insertions = previous_row[j + 1] + 1 
            deletions = current_row[j] + 1       
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]

def average(nums):
    return (sum(nums) + 0.0) / len(nums)
