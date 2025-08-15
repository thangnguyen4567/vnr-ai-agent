from ui.flowchart import yaml_to_mermaid_flowchart

# Example usage
if __name__ == "__main__":
    with open('settings/prod_multi_agent.yaml', 'r') as file:
        yaml_content = file.read()
    
    mermaid_diagram = yaml_to_mermaid_flowchart(yaml_content)
    print(mermaid_diagram)
