import yaml

def yaml_to_mermaid_flowchart(yaml_content):
    """
    Convert a multi-agent YAML configuration to a Mermaid flowchart diagram.
    
    Args:
        yaml_content (str): The YAML content as a string
        
    Returns:
        str: Mermaid flowchart diagram code
    """
    try:
        # Parse the YAML content
        config = yaml.safe_load(yaml_content)
        
        # Start building the Mermaid flowchart
        mermaid = ["flowchart TD"]
        mermaid.append("    User --> Supervisor[\"" + config.get('name', 'Multi Agent') + " (Supervisor)\"]")
        mermaid.append("")
        
        # Create nodes for each agent
        for agent in config.get('agents', []):
            agent_name = agent.get('name', '')
            agent_var = agent_name.replace(' ', '')
            mermaid.append(f"    Supervisor --> {agent_var}[\"{agent_name}\"]")
        
        mermaid.append("")
        
        # Process sub-agents and their tools
        for sub_agent in config.get('sub_agents', []):
            agent_name = sub_agent.get('name', '')
            agent_var = agent_name.replace(' ', '')
            
            # Process tools for this agent
            tools = sub_agent.get('nodes', {}).get('tools', [])
            for i, tool in enumerate(tools, 1):
                tool_name = tool.get('name', f'Tool{i}')
                tool_var = f"{agent_var[0]}{i}"
                
                # Add tool connection to agent
                mermaid.append(f"    {agent_var} --> {tool_var}[\"{tool_name}  ({tool.get('type', '')})\"]")
                
                # Process input parameters for this tool
                params = tool.get('input_params', [])
                if params:
                    param_lines = []
                    for param in params:
                        param_name = param.get('name', '')
                        param_type = param.get('type', '')
                        param_lines.append(f"- {param_name}: {param_type}")
                    
                    params_text = "<br/>".join(param_lines)
                    mermaid.append(f"    {tool_var} --- {tool_var}_params[\"Inputs:<br/>{params_text}\"]")
            
            # Add a blank line between agents for readability
            mermaid.append("")
        
        return "\n".join(mermaid)
        
    except Exception as e:
        return f"Error generating Mermaid diagram: {str(e)}"

# Example usage
if __name__ == "__main__":
    with open('settings/multi_agent.yaml', 'r') as file:
        yaml_content = file.read()
    
    mermaid_diagram = yaml_to_mermaid_flowchart(yaml_content)
    print(mermaid_diagram)
