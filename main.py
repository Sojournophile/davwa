from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Mock internal health check endpoint
@app.route('/internal-api/health')
def healthcheck():
    if request.remote_addr not in ['127.0.0.1', '::1']:
        return "Unauthorized", 403
    return "INTERNAL API STATUS: OK\nVersion: 2.4.1\nActive: true", 200

# Website status checker feature
@app.route('/check-status')
def status_checker():
    url = request.args.get('url')
    if not url:
        return "Missing URL parameter", 400
    
    try:
        response = requests.get(
            url,
            timeout=5,
            headers={'User-Agent': 'DaveCorp-StatusChecker/1.2'},
            allow_redirects=True
        )
        
        status_message = "Site is up! ✅" if response.status_code == 200 else "Site may be down ⚠️"
        
        return render_template_string('''
            <h3>Dave's Vulnerable Web App</h3>
            <h4>Status Check Results for: {{ url }}</h4>
            <div style="border: 1px solid #ddd; padding: 15px; margin: 20px;">
                <b>Status:</b> {{ status_message }}<br>
                <b>HTTP Code:</b> {{ status_code }}<br>
                <b>Response Time:</b> {{ response_time|round(2) }}s
            </div>
            <a href="/">Check another URL</a>
        ''', url=url, status_message=status_message, 
           status_code=response.status_code, response_time=response.elapsed.total_seconds())
    
    except Exception as e:
        return f'''
            <h3>Dave's Vulnerable Web App</h3>
            <div style="color: red; padding: 15px;">
                Error checking URL: {str(e)}
            </div>
            <a href="/">Try again</a>
        ''', 500

# Homepage with form
@app.route('/')
def index():
    return '''
        <h1>Dave's Vulnerable Web App</h1>
        <h3>Website Status Checker</h3>
        <form action="/check-status">
            Enter URL to check: <br>
            <input type="text" name="url" size="50" placeholder="http://example.com"><br>
            <input type="submit" value="Check Status">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=5000)
