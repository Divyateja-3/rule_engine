import re
import mysql.connector

# Define the Node class for the AST
class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type
        self.value = value
        self.left = left
        self.right = right

# MySQL database connection
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='mysql123',  # Replace with your MySQL password
        database='rule_engine'
    )

# Function to create a rule and save it to the database
def create_rule(rule_string):
    tokens = re.split(r'(\s+AND\s+|\s+OR\s+|\s*\(\s*|\s*\)\s*)', rule_string)
    stack = []
    operators = []

    for token in tokens:
        token = token.strip()
        if not token:
            continue
        if token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                right = stack.pop()
                operator = operators.pop()
                left = stack.pop()
                stack.append(Node('operator', value=operator, left=left, right=right))
            operators.pop()  # Remove '('
        elif token in ['AND', 'OR']:
            while (operators and operators[-1] in ['AND', 'OR']):
                right = stack.pop()
                operator = operators.pop()
                left = stack.pop()
                stack.append(Node('operator', value=operator, left=left, right=right))
            operators.append(token)
        else:
            parts = re.split(r'(\s*>\s*|\s*<\s*|\s*=\s*)', token)
            if len(parts) == 3:
                left_operand = parts[0].strip()
                operator = parts[1].strip()
                right_value = parts[2].strip()
                left_node = Node('operand', value=left_operand)
                right_node = Node('operand', value=right_value)
                comparison_node = Node('comparison', left=left_node, right=right_node)
                comparison_node.value = operator  # Set the operator as value
                stack.append(comparison_node)
            else:
                raise ValueError(f"Invalid condition format: {token}")

    while operators:
        right = stack.pop()
        operator = operators.pop()
        left = stack.pop()
        stack.append(Node('operator', value=operator, left=left, right=right))

    return stack.pop()
# Function to save the rule to the database
def save_rule_to_db(rule_string):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO rules (rule_string) VALUES (%s)", (rule_string,))
    connection.commit()
    cursor.close()
    connection.close()

# Function to evaluate the AST against provided data
def evaluate_rule(ast, data):
    if ast.type == 'operator':
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)
        return left_result and right_result if ast.value == 'AND' else left_result or right_result
    elif ast.type == 'comparison':
        field = ast.left.value
        operator = ast.value
        value = ast.right.value

        if operator == '>':
            return data[field] > float(value)
        elif operator == '<':
            return data[field] < float(value)
        elif operator == '=':
            return data[field] == value

    return False

# Example usage
if __name__ == "__main__":
    # Define your rule string
    rule_string = input("Enter the rule string: ")

    # Create the AST for the rule
    ast = create_rule(rule_string)

    # Gather user data dynamically
    user_data = {}
    user_data["age"] = int(input("Enter age: "))
    user_data["department"] = input("Enter department: ")
    user_data["salary"] = float(input("Enter salary: "))
    user_data["experience"] = int(input("Enter years of experience: "))

    # Evaluate the rule against the user data
    result = evaluate_rule(ast, user_data)
    print("User eligibility:", result)
