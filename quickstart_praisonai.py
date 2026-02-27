import os
from praisonaiagents import Agent

def main():
    # Ensure there's an API key (Using OpenAI as an example, though others work)
    if "OPENAI_API_KEY" not in os.environ and "ANTHROPIC_API_KEY" not in os.environ:
        print("WARNING: No OPENAI_API_KEY or ANTHROPIC_API_KEY found in environment variables.")
        print("PraisonAI requires an API key to run models.")
        # Proceeding anyway as the user might have local LLMs configured or it might pick it up automatically.
    
    # Define a simple agent
    solar_expert = Agent(
        name="SolarExpert",
        role="Renewable Energy Analyst",
        goal="Provide expert advice on solar energy systems.",
        backstory="You have 20 years of experience designing and analyzing photovoltaic systems.",
        instructions="Be precise, use technical terminology, and provide actionable recommendations."
    )

    print("Starting the agent task...")
    
    # Start the agent with a specific task
    result = solar_expert.start("Genera un reporte ejecutivo breve sobre la viabilidad de un sistema fotovoltaico de 10kW en Colombia.")
    
    print("\n--- Agent Result ---")
    print(result)

if __name__ == "__main__":
    main()
