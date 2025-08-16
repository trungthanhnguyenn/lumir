#!/usr/bin/env python3
"""
Lumir AI Numerology Demo Web App
A beautiful web interface for testing the numerology API
"""

from flask import Flask, render_template, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

# API Configuration
API_BASE_URL = "http://localhost:8686"
API_ENDPOINT = f"{API_BASE_URL}/api/v1/numerology/calculate"

@app.route('/')
def index():
    """Main page with numerology lookup form"""
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate_numerology():
    """API endpoint to calculate numerology"""
    try:
        data = request.get_json()
        full_name = data.get('full_name', '').strip()
        date_of_birth = data.get('date_of_birth', '').strip()
        
        if not full_name or not date_of_birth:
            return jsonify({
                'success': False,
                'error': 'Vui lòng nhập đầy đủ họ tên và ngày sinh'
            }), 400
        
        # Prepare payload for API
        payload = {
            "full_name": full_name,
            "date_of_birth": date_of_birth,
            "current_date": datetime.now().strftime("%d/%m/%Y")
        }
        
        # Call the numerology API
        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                return jsonify({
                    'success': True,
                    'data': result['data']['pwi_indices'],
                    'input': result['data']['input']
                })
            else:
                return jsonify({
                    'success': False,
                    'error': result.get('message', 'Lỗi tính toán')
                }), 400
        else:
            return jsonify({
                'success': False,
                'error': f'API Error: {response.status_code}'
            }), 500
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False,
            'error': 'Không thể kết nối đến API server. Vui lòng kiểm tra server.'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Lỗi: {str(e)}'
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'numerology-demo-webapp'})

if __name__ == '__main__':
    print("🔮 Starting Lumir AI Numerology Demo Web App...")
    print(f"📡 API URL: {API_ENDPOINT}")
    print("🌐 Web App: http://localhost:5000")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
