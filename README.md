# Rule Engine with Abstract Syntax Tree (AST)

## Overview

This project implements a simple rule engine that evaluates user eligibility based on various attributes such as age, department, salary, and experience. It utilizes an Abstract Syntax Tree (AST) to dynamically create, combine, and modify rules.

## Features

- **AST Representation**: Rules are represented as an Abstract Syntax Tree, allowing for efficient evaluation and modification.
- **Dynamic Rule Creation**: Create individual rules using a user-friendly string format.
- **Rule Combination**: Combine multiple rules into a single AST for collective evaluation.
- **Evaluation Logic**: Evaluate user data against the rules to determine eligibility.
- **Error Handling**: Robust error handling for invalid rule formats and user data.
- **Attribute Validation**: Ensure attributes conform to a predefined catalog.

## Data Structure

The rule engine defines a `Node` class to represent the AST:

```python
class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type  # "operator" or "operand"
        self.left = left            # Reference to left child
        self.right = right          # Reference to right child
        self.value = value          # Optional value (for operands)
