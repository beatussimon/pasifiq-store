import re
from collections import deque

def validate_template_structure(template_content):
    """
    Validate Django template block structure using a stack-based approach.
    
    Returns:
        - valid: bool - whether structure is valid
        - errors: list - list of error messages
        - stack: list - final stack state
        - line_numbers: dict - mapping of tags to line numbers
    """
    # Stack for tracking open blocks
    stack = deque()
    
    # Track line numbers for each tag
    line_numbers = {}
    
    # Regular expressions for Django template tags
    block_start_re = re.compile(r'\{\%\s*(\w+)(.*?)\s*\%\}')
    block_end_re = re.compile(r'\{\%\s*end(\w+)\s*\%\}')
    
    # Split template into lines for better error reporting
    lines = template_content.split('\n')
    
    errors = []
    
    for i, line in enumerate(lines, 1):
        # Find all start tags in this line
        for match in block_start_re.finditer(line):
            tag = match.group(1)
            line_numbers[tag] = i
            stack.append((tag, i))
            
            # Special handling for certain tags
            if tag == 'for' and 'in' not in match.group(2):
                errors.append(f"Line {i}: 'for' tag missing 'in' keyword")
            elif tag == 'if' and '==' not in match.group(2) and '!=' not in match.group(2):
                # Check for common comparison operators
                pass
        
        # Find all end tags in this line
        for match in block_end_re.finditer(line):
            end_tag = match.group(1)
            line_numbers[f'end{end_tag}'] = i
            
            if stack:
                last_tag, last_line = stack.pop()
                if last_tag != end_tag:
                    errors.append(f"Line {i}: Mismatched block - expected 'end{last_tag}' but found 'end{end_tag}'")
                    # Try to recover by pushing back the mismatched tag
                    stack.append((last_tag, last_line))
            else:
                errors.append(f"Line {i}: Unexpected 'end{end_tag}' - no matching start tag")
    
    # Check for unclosed blocks
    if stack:
        for tag, line in stack:
            errors.append(f"Line {line}: Unclosed '{tag}' block")
    
    valid = len(errors) == 0
    
    return {
        'valid': valid,
        'errors': errors,
        'stack': list(stack),
        'line_numbers': line_numbers
    }

def find_misnested_blocks(template_content):
    """
    Find misnested blocks where endif appears before endfor.
    
    Returns:
        - issues: list of tuples (line_number, issue_description)
    """
    lines = template_content.split('\n')
    issues = []
    
    # Track block nesting state
    for i, line in enumerate(lines, 1):
        if '{% if' in line:
            # Check if there's an unclosed for loop
            if 'for' in line:
                continue
            # Look ahead for potential nesting issues
            for j in range(i+1, len(lines)+1):
                if '{% endfor' in lines[j-1]:
                    break
                if '{% endif' in lines[j-1] and '{% for' in lines[i-1]:
                    issues.append((i, "Potential misnesting: 'if' inside 'for' without proper closure"))
                    break
    
    return issues

def convert_multi_line_tags(template_content):
    """
    Convert multi-line Django tags to single-line expressions.
    
    Returns:
        - converted_content: str - modified template content
        - changes: list - list of changes made
    """
    lines = template_content.split('\n')
    converted_content = []
    changes = []
    
    for i, line in enumerate(lines, 1):
        # Convert multi-line if statements
        if '{% if' in line and '==' not in line and '!=' not in line:
            # Look for multi-line if statements
            if '==' in lines[i] or '!=' in lines[i]:
                converted_content.append(line)
                continue
            
            # Check if this is a multi-line if
            if any(char in line for char in ['\n', '\t', '    '] if '{% if' in line):
                # Try to convert to single line
                new_line = line.strip()
                if new_line != line:
                    converted_content.append(new_line)
                    changes.append(f"Line {i}: Converted multi-line if to single line")
                else:
                    converted_content.append(line)
            else:
                converted_content.append(line)
        else:
            converted_content.append(line)
    
    return '\n'.join(converted_content), changes

def validate_template_syntax(template_path):
    """
    Validate template syntax using Django's Template class.
    
    Returns:
        - valid: bool - whether syntax is valid
        - error: str - error message if invalid
    """
    try:
        import django
        from django.conf import settings
        from django.template import Template, Engine
        if not settings.configured:
            settings.configure(TEMPLATES=[{
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                    'builtins': ['core.templatetags.core_tags'],
                },
            }])
            django.setup()
        
        # Load from string
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        Engine.get_default().from_string(content)
        return True, "Template syntax is valid"
    except Exception as e:
        import traceback
        return False, traceback.format_exc()

if __name__ == "__main__":
    # Test with the current template
    with open('templates/products/detail.html', 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    print("=== Template Structure Analysis ===")
    result = validate_template_structure(template_content)
    
    if result['valid']:
        print("\n✅ Template structure is valid!")
    else:
        print(f"\nERROR: Template structure is invalid ({len(result['errors'])} errors):")
        for error in result['errors']:
            print(f"  - {error}")
    
    print(f"\nStack state: {result['stack']}")
    
    # Check for misnested blocks
    misnested = find_misnested_blocks(template_content)
    if misnested:
        print("\n⚠️  Potential misnested blocks detected:")
        for line, issue in misnested:
            print(f"  Line {line}: {issue}")
    else:
        print("\n✅ No obvious misnested blocks detected")
    
    # Convert multi-line tags
    converted_content, changes = convert_multi_line_tags(template_content)
    if changes:
        print(f"\n✨ Converted multi-line tags:")
        for change in changes:
            print(f"  - {change}")
    else:
        print("\n✅ No multi-line tags to convert")
    
    # Save converted version
    with open('templates/products/detail_converted.html', 'w', encoding='utf-8') as f:
        f.write(converted_content)
    
    print(f"\nℹ️  Converted template saved to: templates/products/detail_converted.html")
    
    # Validate syntax of converted template
    valid, message = validate_template_syntax('templates/products/detail_converted.html')
    print(f"\n✅ Syntax validation: {message}")
