import os
import google.generativeai as genai
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from datetime import datetime

def load_config():
    """Load configuration from YAML file."""
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

# Load configuration
config = load_config()

# Configure Gemini
try:
    genai.configure(api_key=config['api']['gemini_key'])
    # List available models to ensure we're using a valid one
    models = [m.name for m in genai.list_models()]
    print("Available models:", models)
    
    # Use Gemini 1.5 Flash
    MODEL_NAME = 'models/gemini-1.5-flash'
    print(f"Using model: {MODEL_NAME}")
except Exception as e:
    print(f"Error configuring Gemini: {str(e)}")
    raise

class PodcastContentGenerator:
    def __init__(self):
        self.console = Console()
        try:
            self.model = genai.GenerativeModel(MODEL_NAME)
            print(f"Successfully initialized model: {MODEL_NAME}")
        except Exception as e:
            print(f"Error initializing model: {str(e)}")
            raise
        self.config = config
        
    def format_duration(self, minutes):
        """Convert minutes to a formatted duration string."""
        hours = minutes // 60
        mins = minutes % 60
        if hours > 0:
            return f"{hours}h {mins}m"
        return f"{mins}m"
        
    def create_timestamp(self, current_time, duration):
        """Create a timestamp string from minutes."""
        total_minutes = current_time
        hours = total_minutes // 60
        minutes = total_minutes % 60
        timestamp = f"{hours:02d}:{minutes:02d}"
        duration_str = self.format_duration(duration)
        return f"{timestamp} ({duration_str})"

    def generate_outline(self, topic, duration, style):
        prompt = f"""You are a professional podcast content creator. Create a clear and engaging podcast outline for:
        
        Topic: {topic}
        Duration: {duration} minutes
        Style: {style}
        
        Follow this EXACT format:
        
        # [Write a catchy title here - max 60 chars]
        
        ## 📝 Episode Summary
        [Write 2-3 clear sentences about what this episode covers]
        
        ## ⏰ Episode Timeline
        
        ### 1. Introduction ({self.format_duration(5)})
        • Opening Hook: [Write a strong hook]
        • Topic Introduction
        • Episode Goals
        
        ### 2. Main Segments
        
        #### Segment 1: [Title] ({self.format_duration(10)})
        • Main Point 1
        • Main Point 2
        • Main Point 3
        • Key Takeaway
        
        #### Segment 2: [Title] ({self.format_duration(15)})
        • Main Point 1
        • Main Point 2
        • Main Point 3
        • Key Takeaway
        
        #### Segment 3: [Title] ({self.format_duration(15)})
        • Main Point 1
        • Main Point 2
        • Main Point 3
        • Key Takeaway
        
        ### 3. Conclusion ({self.format_duration(5)})
        • Recap Key Points
        • Call to Action
        • Next Episode Preview
        
        ## 🎵 Production Notes
        • Music Type:
        • Sound Effects:
        • Special Elements:
        
        Remember:
        1. Be specific and clear
        2. Use engaging language
        3. Keep points concise
        4. Maintain consistent formatting
        """
        
        try:
            generation_config = {
                "temperature": 0.7,  # Slightly lower for more focused content
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            outline = response.text
            
            # Format the response with clear styling
            formatted_response = f"""
            <div style="color: #000000; font-family: Arial, sans-serif; line-height: 1.6; padding: 20px;">
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
            <h2 style="color: #1a73e8;">Podcast Episode Outline</h2>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            <p>Duration: {self.format_duration(duration)}</p>
            <p>Topic: {topic}</p>
            <p>Style: {style.title()}</p>
            </div>
            
            <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            {outline}
            </div>
            </div>
            """
            
            return formatted_response
            
        except Exception as e:
            error_msg = f"Error generating outline: {str(e)}"
            print(error_msg)  # Print to console for debugging
            self.console.print(f"[red]{error_msg}[/red]")
            return None

    def generate_questions(self, topic, guest_expertise, style):
        prompt = f"""Create engaging interview questions for a podcast episode with the following details:
        Topic: {topic}
        Guest Expertise: {guest_expertise}
        Style: {style}
        
        Structure the response in this format using markdown:
        
        # Interview Questions for [Topic]
        
        ## 🤝 Opening Questions (5-7 minutes)
        [Questions to build rapport and set the tone]
        
        ## 🎯 Main Discussion (30-40 minutes)
        [Core questions about the topic]
        
        ## 🌟 Lightning Round (5 minutes)
        [Quick, fun questions to energize the conversation]
        
        ## 🎬 Closing Questions (5-10 minutes)
        [Questions to wrap up and leave a lasting impression]
        
        For each question, include:
        - The question itself
        - Purpose/goal of the question
        - Potential follow-ups
        
        Add timestamps and pacing suggestions where appropriate.
        """
        
        try:
            generation_config = {
                "temperature": 0.8,
                "top_p": 1,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            questions = response.text
            
            # Add header with metadata
            metadata = f"""
            # Interview Questions
            
            - Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            - Guest Expertise: {guest_expertise}
            - Topic: {topic}
            - Style: {style.title()}
            
            ---
            
            {questions}
            """
            
            return metadata
            
        except Exception as e:
            error_msg = f"Error generating questions: {str(e)}"
            print(error_msg)  # Print to console for debugging
            self.console.print(f"[red]{error_msg}[/red]")
            return None

    def generate_title(self, topic, style):
        prompt = f"""Create 5 engaging podcast episode titles for the following topic:
        Topic: {topic}
        Style: {style}
        
        Structure the response in this format using markdown:
        
        # Title Options for [Topic]
        
        For each title:
        - The title (under 60 characters)
        - Brief explanation of its appeal
        - Style elements used
        - Emotional hook
        
        Make titles:
        - Attention-grabbing
        - SEO-friendly
        - Easy to remember
        - Mix of question-based and statement titles
        """
        
        try:
            generation_config = {
                "temperature": 0.9,  # Higher temperature for more creative titles
                "top_p": 1,
                "top_k": 40,
                "max_output_tokens": 1024,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            titles = response.text
            
            # Add header with metadata
            metadata = f"""
            # Episode Title Options
            
            - Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            - Topic: {topic}
            - Style: {style.title()}
            
            ---
            
            {titles}
            """
            
            return metadata
            
        except Exception as e:
            error_msg = f"Error generating titles: {str(e)}"
            print(error_msg)  # Print to console for debugging
            self.console.print(f"[red]{error_msg}[/red]")
            return None

    def generate_research(self, topic, keywords, analysis_type):
        """Generate content research and analysis based on topic and type."""
        
        analysis_prompts = {
            'trends': f"""Create a clear, structured analysis of trends for the podcast topic:
            Topic: {topic}
            Keywords/Areas: {keywords}
            
            Format your response in these clear sections:

            # Executive Summary
            • Brief overview of the topic (2-3 sentences)
            • Key findings highlight (3-4 bullet points)
            
            # Current Trends Analysis
            ## Major Trend 1: [Name]
            • What it is
            • Why it matters
            • Key statistics
            • Impact on the industry
            
            ## Major Trend 2: [Name]
            • What it is
            • Why it matters
            • Key statistics
            • Impact on the industry
            
            ## Major Trend 3: [Name]
            • What it is
            • Why it matters
            • Key statistics
            • Impact on the industry
            
            # Emerging Patterns
            ## Pattern 1: [Name]
            • Description
            • Expected impact
            • Timeline
            
            ## Pattern 2: [Name]
            • Description
            • Expected impact
            • Timeline
            
            # Content Opportunities
            ## Opportunity 1: [Name]
            • Description
            • Target audience
            • Potential format
            • Expected impact
            
            ## Opportunity 2: [Name]
            • Description
            • Target audience
            • Potential format
            • Expected impact
            
            # Expert Insights
            • Quote 1: [Expert name] - [Key point]
            • Quote 2: [Expert name] - [Key point]
            • Quote 3: [Expert name] - [Key point]
            
            # Action Items
            ## Immediate Steps
            • Action 1
            • Action 2
            • Action 3
            
            ## Long-term Strategy
            • Strategy point 1
            • Strategy point 2
            • Strategy point 3""",
            
            'competitors': f"""Create a clear, structured analysis of competitor content:
            Topic: {topic}
            Keywords/Areas: {keywords}
            
            Format your response in these clear sections:

            # Executive Summary
            • Overview of competitive landscape
            • Key findings (3-4 bullet points)
            
            # Top Performing Content Analysis
            ## Category 1: [Content Type]
            • What works
            • Why it works
            • Key examples
            • Success metrics
            
            ## Category 2: [Content Type]
            • What works
            • Why it works
            • Key examples
            • Success metrics
            
            # Content Gap Analysis
            ## Gap 1: [Area]
            • Description
            • Market need
            • Opportunity size
            • Potential approach
            
            ## Gap 2: [Area]
            • Description
            • Market need
            • Opportunity size
            • Potential approach
            
            # Differentiation Opportunities
            ## Opportunity 1: [Name]
            • Unique angle
            • Target audience
            • Content format
            • Expected impact
            
            ## Opportunity 2: [Name]
            • Unique angle
            • Target audience
            • Content format
            • Expected impact
            
            # Strategic Recommendations
            ## Short-term Actions
            • Action 1
            • Action 2
            • Action 3
            
            ## Long-term Strategy
            • Strategy 1
            • Strategy 2
            • Strategy 3""",
            
            'audience': f"""Create a clear, structured analysis of audience interests:
            Topic: {topic}
            Keywords/Areas: {keywords}
            
            Format your response in these clear sections:

            # Executive Summary
            • Overview of audience analysis
            • Key insights (3-4 bullet points)
            
            # Audience Segments
            ## Segment 1: [Name]
            • Demographics
            • Key interests
            • Content preferences
            • Engagement patterns
            
            ## Segment 2: [Name]
            • Demographics
            • Key interests
            • Content preferences
            • Engagement patterns
            
            # Common Questions Analysis
            ## Category 1: [Topic Area]
            • Question 1
            • Question 2
            • Question 3
            • How to address
            
            ## Category 2: [Topic Area]
            • Question 1
            • Question 2
            • Question 3
            • How to address
            
            # Platform Analysis
            ## Platform 1: [Name]
            • Audience presence
            • Content performance
            • Engagement metrics
            • Best practices
            
            ## Platform 2: [Name]
            • Audience presence
            • Content performance
            • Engagement metrics
            • Best practices
            
            # Content Strategy
            ## Content Types
            • Type 1: [Description and approach]
            • Type 2: [Description and approach]
            • Type 3: [Description and approach]
            
            ## Engagement Strategy
            • Strategy 1
            • Strategy 2
            • Strategy 3""",
            
            'gaps': f"""Create a clear, structured analysis of content gaps:
            Topic: {topic}
            Keywords/Areas: {keywords}
            
            Format your response in these clear sections:

            # Executive Summary
            • Overview of content gap analysis
            • Key findings (3-4 bullet points)
            
            # Market Overview
            ## Current State
            • Key players
            • Content types
            • Market trends
            • Audience needs
            
            # Content Gaps
            ## Gap 1: [Area]
            • Description
            • Market need
            • Competition level
            • Opportunity size
            
            ## Gap 2: [Area]
            • Description
            • Market need
            • Competition level
            • Opportunity size
            
            # Opportunity Analysis
            ## Opportunity 1: [Name]
            • Description
            • Target audience
            • Content approach
            • Expected impact
            
            ## Opportunity 2: [Name]
            • Description
            • Target audience
            • Content approach
            • Expected impact
            
            # Implementation Strategy
            ## Quick Wins
            • Action 1
            • Action 2
            • Action 3
            
            ## Long-term Plan
            • Strategy 1
            • Strategy 2
            • Strategy 3
            
            # Success Metrics
            • Metric 1: [Description and target]
            • Metric 2: [Description and target]
            • Metric 3: [Description and target]"""
        }
        
        if analysis_type not in analysis_prompts:
            error_msg = f"Invalid analysis type: {analysis_type}"
            print(error_msg)
            return f'<div class="error-message">{error_msg}</div>'
        
        prompt = analysis_prompts[analysis_type]
        
        try:
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            if not response or not response.text:
                error_msg = "No content generated from the AI model"
                print(error_msg)
                return f'<div class="error-message">{error_msg}</div>'
            
            analysis = response.text
            
            # Format the response with clear styling and sections
            formatted_response = f"""
            <div style="color: #000000; font-family: Arial, sans-serif; line-height: 1.6; padding: 20px;">
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                    <h2 style="color: #1a73e8; margin-bottom: 15px;">Content Research & Analysis</h2>
                    <p style="margin: 5px 0;"><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                    <p style="margin: 5px 0;"><strong>Topic:</strong> {topic}</p>
                    <p style="margin: 5px 0;"><strong>Analysis Type:</strong> {analysis_type.title()}</p>
                </div>
                
                <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="max-width: 800px; margin: 0 auto;">
                        {analysis}
                    </div>
                </div>
            </div>
            """
            
            return formatted_response
            
        except Exception as e:
            error_msg = f"Error generating research analysis: {str(e)}"
            print(error_msg)
            return f'<div class="error-message">{error_msg}</div>' 