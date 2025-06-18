from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from podcast_generator import PodcastContentGenerator, load_config
import os

# Load configuration
config = load_config()

app = Flask(__name__)
CORS(app)

# Initialize the generator
generator = PodcastContentGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate/outline', methods=['POST'])
def generate_outline():
    try:
        data = request.get_json()
        topic = data.get('topic')
        duration = data.get('duration', 30)
        style = data.get('style', 'deep')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
            
        outline = generator.generate_outline(topic, duration, style)
        
        if outline:
            return jsonify({'outline': outline})
        else:
            return jsonify({'error': 'Failed to generate outline'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate/questions', methods=['POST'])
def generate_questions():
    try:
        data = request.get_json()
        topic = data.get('topic')
        guest_expertise = data.get('guest_expertise')
        style = data.get('style', 'deep')
        
        if not topic or not guest_expertise:
            return jsonify({'error': 'Topic and guest expertise are required'}), 400
            
        questions = generator.generate_questions(topic, guest_expertise, style)
        
        if questions:
            return jsonify({'questions': questions})
        else:
            return jsonify({'error': 'Failed to generate questions'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate/title', methods=['POST'])
def generate_title():
    try:
        data = request.get_json()
        topic = data.get('topic')
        style = data.get('style', 'deep')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
            
        titles = generator.generate_title(topic, style)
        
        if titles:
            return jsonify({'titles': titles})
        else:
            return jsonify({'error': 'Failed to generate titles'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_research', methods=['POST'])
def generate_research():
    try:
        topic = request.form.get('topic')
        keywords = request.form.get('keywords')
        analysis_type = request.form.get('analysisType')
        
        if not all([topic, keywords, analysis_type]):
            return '<div class="error-message">Please provide all required fields</div>', 400
            
        result = generator.generate_research(topic, keywords, analysis_type)
        if result is None:
            return '<div class="error-message">Failed to generate research analysis. Please try again.</div>', 500
            
        # Ensure we always return the result as a response
        return result if isinstance(result, tuple) else (result, 200)
        
    except Exception as e:
        print(f"Error in generate_research: {str(e)}")  # Log the error
        return '<div class="error-message">An error occurred while generating research analysis: ' + str(e) + '</div>', 500

@app.route('/generate_questions', methods=['POST'])
def generate_questions_form():
    try:
        topic = request.form.get('topic')
        guest_expertise = request.form.get('guest_expertise')
        style = request.form.get('style')
        
        if not all([topic, guest_expertise, style]):
            return '<div class="error-message">Please provide all required fields</div>', 400
            
        result = generator.generate_questions(topic, guest_expertise, style)
        if result is None:
            return '<div class="error-message">Failed to generate questions. Please try again.</div>', 500
            
        return result
        
    except Exception as e:
        print(f"Error in generate_questions: {str(e)}")  # Log the error
        return '<div class="error-message">An error occurred while generating questions: ' + str(e) + '</div>', 500

@app.route('/generate_title', methods=['POST'])
def generate_title_form():
    try:
        topic = request.form.get('topic')
        style = request.form.get('style')
        
        if not all([topic, style]):
            return '<div class="error-message">Please provide all required fields</div>', 400
            
        result = generator.generate_title(topic, style)
        if result is None:
            return '<div class="error-message">Failed to generate titles. Please try again.</div>', 500
            
        return result
        
    except Exception as e:
        print(f"Error in generate_title: {str(e)}")  # Log the error
        return '<div class="error-message">An error occurred while generating titles: ' + str(e) + '</div>', 500

if __name__ == '__main__':
    # Get host and port from config
    host = config['server']['host']
    port = config['server']['port']
    debug = config['server']['debug']
    
    print(f"Starting server on {host}:{port}")
    app.run(host=host, port=port, debug=debug) 