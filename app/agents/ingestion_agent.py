
from app.core.agent_base import Agent

class IngestionAgent(Agent):
    """
    First agent in pipeline.
    Job: Receive user input, validate it, search for similar.
    """
    
    def __init__(self, tools: dict):
        """
        Initialize with tools it can use
        """
        super().__init__(
            name="IngestionAgent",
            role="Receive and validate user input",
            tools=tools
        )
    
    def decide(self, input_data: dict) -> dict:
        """
        Agent thinks: Should I process this input?
        
        Simple logic:
        - If empty → REJECT
        - If too short → REJECT
        - If valid → SEARCH
        """
        
        user_text = input_data.get("text", "")
        
        print(f"\n🧠 {self.name} is thinking...")
        
        # Validation
        if not user_text:
            decision = "REJECT"
            reasoning = "Input is empty"
        elif len(user_text) < 5:
            decision = "REJECT"
            reasoning = "Input too short (less than 5 characters)"
        else:
            decision = "SEARCH"
            reasoning = "Input is valid, will search for similar notes"
        
        print(f"   Reasoning: {reasoning}")
        print(f"   Decision: {decision}")
        
        # Save to memory
        self.memory.append({
            "action": "decided",
            "decision": decision,
            "reasoning": reasoning,
            "input_length": len(user_text)
        })
        
        return {
            "decision": decision,
            "reasoning": reasoning,
            "input": user_text,
            "valid": (decision == "SEARCH")
        }
    
    def process_input(self, user_text: str, next_agent: Agent = None) -> dict:
        """
        Main method: Process user input
        
        Steps:
        1. Decide if input is valid
        2. If valid, execute search tool
        3. Hand off to next agent
        """
        
        print(f"\n{'='*70}")
        print(f"📥 {self.name} received input: '{user_text[:50]}...'")
        print(f"{'='*70}")
        
        # Step 1: Make decision
        decision_result = self.decide({"text": user_text})
        
        # Step 2: If rejected, return error
        if not decision_result["valid"]:
            print(f"\n❌ {self.name}: Input rejected")
            return {
                "success": False,
                "error": decision_result["reasoning"],
                "agent": self.name
            }
        
        # Step 3: Execute search tool
        print(f"\n🔍 {self.name}: Searching for similar notes...")
        search_result = self.execute_tool(
            "search",
            {"query": user_text, "top_k": 1}
        )
        print(f"✅ Found similar notes")
        
        # Step 4: Hand off to next agent (if provided)
        if next_agent:
            print(f"\n📨 {self.name} → {next_agent.name}")
            result = self.communicate(
                next_agent,
                {
                    "from": self.name,
                    "user_input": user_text,
                    "similar_notes": search_result,
                    "timestamp": "now"
                }
            )
            return result
        
        # If no next agent, return result
        return {
            "success": True,
            "agent": self.name,
            "decision": decision_result["decision"],
            "similar_notes": search_result,
            "user_input": user_text
        }
    
    def get_status(self):
        """
        Return agent's current status
        """
        return {
            "name": self.name,
            "role": self.role,
            "memory": self.memory,
            "total_actions": len(self.memory)
        }
    