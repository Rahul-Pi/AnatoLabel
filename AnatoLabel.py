from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
from anatomial_config import COLOR_MAP, region_groups

app = Flask(__name__)

# Global data storage
annotations = {}

# Create region to group mapping
region_to_group = {r: g for g, regs in region_groups.items() for r in regs}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config')
def get_config():
    """Get the anatomical configuration data"""
    return jsonify({
        'region_groups': region_groups,
        'region_to_group': region_to_group,
        'color_map': COLOR_MAP
    })

@app.route('/api/annotations', methods=['GET'])
def get_annotations():
    """Get all annotations"""
    return jsonify(annotations)

@app.route('/api/annotations/<case_id>', methods=['GET'])
def get_case_annotations(case_id):
    """Get annotations for a specific case"""
    return jsonify(annotations.get(case_id, {}))

@app.route('/api/annotations/<case_id>', methods=['POST'])
def save_case_annotations(case_id):
    """Save annotations for a specific case"""
    data = request.json
    annotations[case_id] = data
    
    # Save to file
    try:
        with open('annotations.json', 'w') as f:
            json.dump(annotations, f, indent=2)
        return jsonify({'success': True, 'message': f'Annotations saved for case {case_id}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/annotations/<case_id>/<label>', methods=['DELETE'])
def remove_annotation(case_id, label):
    """Remove a specific annotation"""
    if case_id in annotations and label in annotations[case_id]:
        del annotations[case_id][label]
        # Save to file
        try:
            with open('annotations.json', 'w') as f:
                json.dump(annotations, f, indent=2)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    return jsonify({'success': False, 'error': 'Annotation not found'}), 404

@app.route('/api/import', methods=['POST'])
def import_dataset():
    """Import annotations from JSON file"""
    try:
        data = request.json
        annotations.update(data)
        with open('annotations.json', 'w') as f:
            json.dump(annotations, f, indent=2)
        return jsonify({'success': True, 'message': f'Imported {len(data)} cases'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/report')
def get_report_data():
    """Get data for the injury report with AIS levels"""
    case_map = {}
    for case, parts in annotations.items():
        for part, ais_level in parts.items():
            if part not in case_map:
                case_map[part] = []
            case_map[part].append({'case': case, 'ais': ais_level})
    
    max_count = max(len(v) for v in case_map.values()) if case_map else 1
    
    return jsonify({
        'case_map': case_map,
        'max_count': max_count
    })

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/api/svg')
def get_svg():
    """Get the SVG file content with enhanced clickability"""
    try:
        with open('Tool_example.svg', 'r') as f:
            svg_content = f.read()
        
        # Add invisible stroke to all paths with IDs to improve click detection
        # This makes the clickable area larger and closes gaps between paths
        import re
        
        def add_stroke_to_path(match):
            path_tag = match.group(0)
            # Check if path has an id attribute and it's not empty
            id_match = re.search(r'id="([^"]*)"', path_tag)
            if id_match and id_match.group(1).strip():
                # Add stroke attributes if not already present
                if 'stroke=' not in path_tag:
                    path_tag = path_tag.replace('<path', '<path stroke="transparent" stroke-width="4"')
                # Ensure pointer-events are enabled
                if 'pointer-events=' not in path_tag:
                    path_tag = path_tag.replace('<path', '<path pointer-events="all"')
            return path_tag
        
        # Apply to all path elements
        svg_content = re.sub(r'<path[^>]*>', add_stroke_to_path, svg_content)
        
        return svg_content, 200, {'Content-Type': 'image/svg+xml'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load existing annotations if file exists
    if os.path.exists('annotations.json'):
        try:
            with open('annotations.json', 'r') as f:
                annotations = json.load(f)
        except:
            annotations = {}
    
    app.run(host='localhost', port=5000)
