"""
Training Scenarios for Waiter Training Agent
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class TrainingScenario:
    """Represents a training scenario for waiters"""
    category: str
    difficulty_levels: List[str]
    
    def generate_prompt(self, difficulty_level: str) -> str:
        """Generate a training prompt based on category and difficulty"""
        if difficulty_level not in self.difficulty_levels:
            difficulty_level = "beginner"
        
        scenarios = self._get_scenarios()
        if self.category in scenarios:
            return scenarios[self.category][difficulty_level]
        
        return f"Please provide a response to a {self.category} scenario at {difficulty_level} level."
    
    def _get_scenarios(self) -> Dict[str, Dict[str, str]]:
        """Get all available training scenarios"""
        return {
            "customer_greeting": {
                "beginner": """Scenario: Customer Greeting (Beginner)
                
                A customer enters the restaurant during a busy dinner service. You notice they look around uncertainly and seem to be waiting for someone to acknowledge them.
                
                What would you do to greet this customer and make them feel welcome? Please describe your approach step by step.
                
                Consider:
                - How to approach the customer
                - What to say
                - How to handle the situation professionally
                - What to do next""",
                
                "intermediate": """Scenario: Customer Greeting (Intermediate)
                
                A group of 6 customers enters the restaurant, including two children and an elderly person who appears to have difficulty walking. The restaurant is moderately busy, and you're the first staff member they encounter.
                
                How would you handle this greeting situation? Please provide a comprehensive response covering:
                
                - Initial greeting approach
                - Special considerations for the elderly customer
                - How to manage the group efficiently
                - Seating arrangements
                - Any additional assistance needed""",
                
                "advanced": """Scenario: Customer Greeting (Advanced)
                
                A well-dressed couple enters the restaurant, and you immediately recognize them as returning customers who previously complained about slow service. They seem tense and are speaking in hushed tones. The restaurant is at 90% capacity.
                
                How would you handle this challenging greeting situation? Consider:
                
                - Acknowledging their previous experience
                - Building trust and confidence
                - Managing expectations
                - Coordinating with kitchen staff
                - Creating a positive experience despite past issues"""
            },
            
            "menu_knowledge": {
                "beginner": """Scenario: Menu Knowledge (Beginner)
                
                A customer asks you about the ingredients in the "Chef's Special Pasta" dish. You're not entirely sure about all the ingredients, but you want to be helpful.
                
                How would you handle this situation? Please explain:
                
                - What you would say to the customer
                - How to get accurate information
                - What to do if you're unsure
                - How to maintain professionalism""",
                
                "intermediate": """Scenario: Menu Knowledge (Intermediate)
                
                A customer with a severe nut allergy asks detailed questions about multiple dishes, including preparation methods, cross-contamination risks, and ingredient sourcing. They seem very concerned about their safety.
                
                How would you handle this situation? Please provide a comprehensive response covering:
                
                - How to address their concerns professionally
                - What information you need to gather
                - How to communicate with kitchen staff
                - Safety protocols to follow
                - Alternative menu suggestions""",
                
                "advanced": """Scenario: Menu Knowledge (Advanced)
                
                A food critic and their companion are dining at the restaurant. The critic asks extremely detailed questions about every dish, including cooking techniques, ingredient origins, wine pairings, and chef's inspiration. They're taking notes and seem to be evaluating everything critically.
                
                How would you handle this high-pressure situation? Consider:
                
                - Maintaining composure under scrutiny
                - Providing detailed, accurate information
                - Coordinating with kitchen and sommelier
                - Handling follow-up questions professionally
                - Managing the overall dining experience"""
            },
            
            "order_taking": {
                "beginner": """Scenario: Order Taking (Beginner)
                
                You're taking an order from a table of 4 customers. One person is still deciding, another keeps changing their mind, and the other two are ready but getting impatient.
                
                How would you handle this situation? Please explain:
                
                - How to manage the indecisive customer
                - How to keep the ready customers happy
                - How to maintain order and efficiency
                - What to do if tensions rise""",
                
                "intermediate": """Scenario: Order Taking (Intermediate)
                
                A table of 8 customers has multiple dietary restrictions: 2 vegetarians, 1 gluten-free, 1 dairy-free, and 1 with severe shellfish allergy. They're all ordering different dishes and want to ensure their dietary needs are met.
                
                How would you handle this complex order? Please provide a comprehensive response covering:
                
                - How to track multiple dietary requirements
                - Communication with kitchen staff
                - Double-checking orders for accuracy
                - Handling special requests
                - Ensuring customer satisfaction""",
                
                "advanced": """Scenario: Order Taking (Advanced)
                
                A VIP customer (celebrity) is dining with their entourage of 6 people. They're making last-minute changes to a pre-arranged menu, requesting off-menu items, and need everything to be perfect for a business meeting. The kitchen is already busy with regular orders.
                
                How would you handle this high-stakes situation? Consider:
                
                - Managing VIP expectations professionally
                - Coordinating with kitchen and management
                - Handling off-menu requests
                - Maintaining service quality for other tables
                - Crisis management if things go wrong"""
            },
            
            "upselling": {
                "beginner": """Scenario: Upselling (Beginner)
                
                A customer orders a main course and seems satisfied with their choice. You notice they didn't order any appetizers, drinks, or desserts.
                
                How would you approach upselling without being pushy? Please explain:
                
                - What you would suggest and why
                - How to present options naturally
                - How to read customer interest
                - When to stop if they're not interested""",
                
                "intermediate": """Scenario: Upselling (Intermediate)
                
                A couple is celebrating their anniversary and has ordered a mid-range bottle of wine. They seem to be enjoying their meal and are in a celebratory mood.
                
                How would you approach upselling to enhance their experience? Please provide a comprehensive response covering:
                
                - Wine upgrade opportunities
                - Dessert and after-dinner drink suggestions
                - Anniversary-specific recommendations
                - How to make suggestions feel special, not salesy
                - Timing of upselling attempts""",
                
                "advanced": """Scenario: Upselling (Advanced)
                
                A business group of 8 executives is dining for a corporate dinner. They've ordered premium wine and appetizers, but you notice they're discussing an important deal and seem focused on business rather than food.
                
                How would you approach upselling in this sophisticated context? Consider:
                
                - Reading the business atmosphere
                - Suggesting premium options without interrupting
                - Timing recommendations appropriately
                - Handling multiple decision-makers
                - Creating opportunities for celebration if the deal closes"""
            },
            
            "problem_resolution": {
                "beginner": """Scenario: Problem Resolution (Beginner)
                
                A customer receives their order and immediately says the food is too cold. They seem disappointed but not angry.
                
                How would you handle this situation? Please explain:
                
                - What you would say to the customer
                - How to apologize appropriately
                - What actions you would take
                - How to prevent this in the future""",
                
                "intermediate": """Scenario: Problem Resolution (Intermediate)
                
                A customer becomes very upset because their reservation was lost, and they've been waiting 30 minutes. They have a special occasion planned and are threatening to leave a bad review online.
                
                How would you handle this escalated situation? Please provide a comprehensive response covering:
                
                - How to de-escalate the customer's anger
                - Immediate solutions to offer
                - How to make amends for the inconvenience
                - Follow-up actions to prevent future issues
                - Managing online reputation concerns""",
                
                "advanced": """Scenario: Problem Resolution (Advanced)
                
                A customer has a severe allergic reaction to a dish that was supposed to be allergen-free. They're experiencing symptoms and are very frightened. Other customers are noticing the commotion, and the situation is becoming chaotic.
                
                How would you handle this emergency situation? Consider:
                
                - Immediate emergency response
                - Coordinating with medical professionals
                - Managing other customers' concerns
                - Communication with management and kitchen
                - Legal and liability considerations
                - Post-incident follow-up"""
            },
            
            "service_recovery": {
                "beginner": """Scenario: Service Recovery (Beginner)
                
                A customer's order took longer than expected to arrive, and they mention they're in a hurry to get back to work.
                
                How would you handle this situation? Please explain:
                
                - How to acknowledge the delay
                - What you can do to speed things up
                - How to make amends
                - How to ensure they leave satisfied""",
                
                "intermediate": """Scenario: Service Recovery (Intermediate)
                
                A customer's anniversary dinner was ruined by multiple service issues: wrong wine served, overcooked steak, and a 45-minute wait between courses. They're very disappointed and have already paid, but are clearly unhappy.
                
                How would you attempt to recover this situation? Please provide a comprehensive response covering:
                
                - How to acknowledge the failures
                - What compensation to offer
                - How to restore their trust
                - Follow-up actions
                - Learning from the experience""",
                
                "advanced": """Scenario: Service Recovery (Advanced)
                
                A high-profile customer's private dining experience was completely ruined by a kitchen fire that forced evacuation. The event was for a major business deal, and the customer is furious about the lost opportunity and embarrassment in front of their clients.
                
                How would you attempt to recover from this catastrophic service failure? Consider:
                
                - Immediate crisis management
                - Alternative venue arrangements
                - Financial compensation strategies
                - Reputation management
                - Legal considerations
                - Long-term relationship rebuilding
                - Preventing future incidents"""
            }
        }
    
    def get_scenario_summary(self) -> Dict[str, str]:
        """Get a summary of what this scenario category covers"""
        summaries = {
            "customer_greeting": "First impressions and welcoming customers to the restaurant",
            "menu_knowledge": "Understanding dishes, ingredients, and dietary requirements",
            "order_taking": "Efficiently processing orders and managing customer preferences",
            "upselling": "Suggesting additional items to enhance the dining experience",
            "problem_resolution": "Handling complaints and service issues professionally",
            "service_recovery": "Turning negative experiences into positive outcomes"
        }
        
        return {
            "category": self.category,
            "description": summaries.get(self.category, "Training scenario for restaurant service"),
            "difficulty_levels": self.difficulty_levels
        } 