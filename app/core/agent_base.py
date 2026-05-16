
class Agent:
    """
    Base class for all agents.
    Simple version that can be extended with more complex logic, tools, and communication.
    """
    
    def __init__(self, name: str, role: str, tools: dict = None):
        """
        Initialize agent
        
        name: "IngestionAgent"
        role: "Process user input"
        tools: {"search": search_function, "format": format_function}
        """
        self.name = name
        self.role = role
        self.tools = tools or {}
        self.memory = []  # List of what agent did
        self.state = "idle"  # Current status
    
    def decide(self, input_data: dict) -> dict:
        """
        Agent thinks and decides what to do.
        Override this in each specific agent.
        """
        return {
            "action": "UNKNOWN",
            "reasoning": "No decision logic"
        }
    
    def execute_tool(self, tool_name: str, params: dict):
        """
        Agent uses a tool
        """
        if tool_name not in self.tools:
            return {"error": f"Tool {tool_name} not found"}
        
        tool = self.tools[tool_name]
        result = tool(**params)
        
        # Save to memory
        self.memory.append({
            "action": f"used tool: {tool_name}",
            "result": result
        })
        
        return result
    
    def communicate(self, agent: 'Agent', message: dict):
        """
        Send message to another agent
        """
        print(f"📨 {self.name} → {agent.name}")
        return agent.receive_message(message)
    
    def receive_message(self, message: dict):
        """
        Receive message from another agent
        """
        self.memory.append({
            "action": "received message",
            "from": message.get("from"),
            "message": message
        })
        
        return self.decide(message)
    
    def get_memory(self):
        """
        Return what agent remembers
        """
        return self.memory
    
    def get_status(self):
        """
        Return agent's status
        """
        return {
            "name": self.name,
            "state": self.state,
            "memory_size": len(self.memory),
            "recent_actions": self.memory[-3:] if self.memory else []
        }