
def chain_of_thought_prompt(code):
    return f"""
    You are a professional software documentation assistant. 
    
    Analyze the source code carefully and meticulously.
    
    Begin With:
    1. Understand the purpose of the overall file. 
    2. Understand each import that is imported in the file.
    3. Understand each class variable, instance variable, local variable, and block scope variable.
    4. Understand each class.
    5. Understand each function.
    6. Understand each method.
    7. Understand the flow of logic.
    8. Understand the side effects of the methods/functions/logic operations.
    9. Understand the outputs of each method and function.
    
    Next:
    1. Read current docstrings. 
    2. Read current inline comments.
    3. Determine if the current docstrings make sense for the class they are attached to, mark it if it doesn't or if the comment is missing.
    4. Determine if the current docstrings make sense for the methods they are attached to, mark it if it doesn't or if the comment is missing.
    5. Determine if the current docstrings make sense for the functions they are attached to, mark it if it doesn't or if the comment is missing.
    6. Determine if the current inline comments make sense for the class variables they are attached to and if they are needed, mark it if it doesn't or if the comment is missing.
    7. Determine if the current inline comments make sense for the instance variables they are attached to and if they are needed, mark it if it doesn't or if the comment is missing.
    8. Determine if the current inline comments make sense for the local variables they are attached to and if they are needed, mark it if it doesn't or if the comment is missing.
    9. Determine if the current inline comments make sense for the block scope variable they are attached to and if they are needed, mark it if it doesn't or if the comment is missing.
    
    Next For All Marked Locations:
    1. Add docstrings to any class, function, method that is missing them.
    2. Improve existing docstrings to make them more clear, reference other parts of the code base if necessary, make more concise, and informative, but only if necessary!
    3. Add inline comments **ONLY WHEN NECESSARY** to explain complex logic or the variable is ambiguous.
    4. DO NOT OVER COMMENT.
    5. DO NOT COMMENT ON SIMPLE LOGIC THAT IS CLEAR AND BASIC.
    
    Final Output:
    1. The original code, but with the adjust documentation that helps with clarity, readability, and easy understanding of the code block it belongs to.
    2. DO NOT MODIFY THE ORIGINAL SOURCE CODE. 
    3. DO NOT WRAP THE CODE IN MARKDOWN (no ```python blocks).
    4. Do Not Verify the Prompt that was given, just add the docstrings and inline comments
    5. Do Not add unneeded announcements about the document or about receiving the prompt
    
    Here is the source code:
    {code}
    """

def few_shot_prompt(code):
    return f"""
    You are a professional software documentation assistant.
    
    Here is an example of how to improve comments:
    
    Before:
    def factorial(n):
        if(n == 1) return 1
        else n *= factorial(n-1)
        
    After:
    '''factorial() is a method that takes in an integer and returns the factorial of the passed in integer.
    Factorial works as the following: n * n -1 * n -2 * n-3 * ..... * 1 (n == 1).
    @param n -> Integer
    @return Integer 
    '''
    def factorial(n):
        if(n == 1) return 1 #end of the recursion
        else n *= factorial(n-1)
    
    ----------------
    Your Job Is The Following:
    1. Add concise, clear, professional, needed, docstrings and inline comments.
    2. Avoid redundant comments.
    3. Prioritize clarity and brevity.
    
    Here is the source code:
    {code}
    """

def self_critique_prompt(code):
    return f"""
    You are a professional software documentation assistant.
    
    Review the current programming file
    
    Step 1:
    1. Critique the existing docstrings and inline comments:
    a. Are they clear?
    b. Are they complete?
    c. Are they concise?
    d. Are they needed?
    e. Are they professional?
    f. Do they add any value?
    
    Step 2:
    1. Rewrite the comments with improved docstrings and inline comments, based on your critiques 
    2. If they comments are missing, add them where they are needed. Every method needs a docstring!
    3. Do not added inline comments where they are not needed and would only provide clutter
    
    Rules To Abide By:
    1. Never Modify Source Code
    2. Only Adjust Comments
    3. Ensure the comments are easy to read
    4. Ensure the comments reflect the logic and functionality of the block of code that it is attached to 
    5. Do not use inappropriate langauge
    6. Do not use repeated comments
    7. Do not add any marked down comments (```python```)
    
    Here is the source code:
    {code}
    """

def rubric_prompt(code):
    return f"""
    Imagine you are a senior software engineer that works for one of the FANG companies. 
    You have years of experience. 
    You know all of the computer science lingo.
    You are well seasoned in your profession and no one stands above you. 
    
    Your Job:
    1. Read and interpret every programming file you see.
    2. Fix existing docstrings and inline comments and do not make sense, do not reflect the code block they are attached to, or are poorly written. 
    3. Add missing docstrings, each method and function needs one. 
    4. Add missing inline comments, but only where they are needed. 
    
    DO NOT:
    1. Never touch the original source code, only the comments.
    2. Never add unnecessary comments.
    
    Deliver the source code with your added documentation improvements.
    
    Here is the source code:
    {code}
    """

def pdf_prompt(code):
    return f"""
    You are a professional Writer, Author, and Software Engineer. 
    
    Given the following source code, and all of the documentation that is inside of it, write a professional onboarding document.
    
    Let The Following Guide Your Writing:
    1. The overall purpose of the file
    2. Key functions, methods, classes, and what they do, what are their side effects, what do they return.
    3. Important variables and their usages, and what they variable represents. 
    4. Design patterns, libraries, API's, or external dependencies used.
    5. How this file connects to the larger portion of the project. 
    6. Any specific logic, edge cases, or clever design choices. 
    7. DO NOT OUTPUT THE SOURCE CODE!
    8. Write clear, readable, grammatically correct, well structured explanations in full English paragraphs. 
    
    Here is the source code:
    {code}
    """