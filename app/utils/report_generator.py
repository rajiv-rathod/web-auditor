from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import json
from typing import Dict, Any, List

class ReportGenerator:
    """Generate security audit reports in PDF format"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.darkblue
        )
        
    def generate_pdf_report(self, scan_data: Dict[str, Any], output_path: str) -> str:
        """Generate a PDF security audit report"""
        
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        story = []
        
        # Title
        title = Paragraph("Web Security Audit Report", self.title_style)
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Report metadata
        meta_data = [
            ['Target:', scan_data.get('target', 'N/A')],
            ['Scan Type:', scan_data.get('scan_type', 'N/A')],
            ['Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Status:', scan_data.get('status', 'N/A')]
        ]
        
        meta_table = Table(meta_data, colWidths=[1.5*inch, 4*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(meta_table)
        story.append(Spacer(1, 20))
        
        # Executive Summary
        summary_title = Paragraph("Executive Summary", self.styles['Heading2'])
        story.append(summary_title)
        
        summary_text = self._generate_summary(scan_data)
        summary_para = Paragraph(summary_text, self.styles['Normal'])
        story.append(summary_para)
        story.append(Spacer(1, 20))
        
        # Findings
        if 'vulnerabilities' in scan_data:
            findings_title = Paragraph("Security Findings", self.styles['Heading2'])
            story.append(findings_title)
            
            for vuln in scan_data['vulnerabilities']:
                story.extend(self._format_vulnerability(vuln))
        
        # Recommendations
        recommendations_title = Paragraph("Recommendations", self.styles['Heading2'])
        story.append(recommendations_title)
        
        recommendations = scan_data.get('recommendations', [])
        for rec in recommendations:
            bullet = Paragraph(f"• {rec}", self.styles['Normal'])
            story.append(bullet)
        
        story.append(Spacer(1, 20))
        
        # Technical Details
        tech_title = Paragraph("Technical Details", self.styles['Heading2'])
        story.append(tech_title)
        
        results = scan_data.get('results', {})
        if isinstance(results, str):
            try:
                results = json.loads(results)
            except:
                results = {"raw_results": results}
        
        for key, value in results.items():
            detail = Paragraph(f"<b>{key}:</b> {value}", self.styles['Normal'])
            story.append(detail)
        
        # Build PDF
        doc.build(story)
        return output_path
    
    def _generate_summary(self, scan_data: Dict[str, Any]) -> str:
        """Generate executive summary"""
        target = scan_data.get('target', 'Unknown')
        scan_type = scan_data.get('scan_type', 'Unknown')
        
        vuln_count = len(scan_data.get('vulnerabilities', []))
        
        if vuln_count == 0:
            risk_level = "Low"
            summary = f"The security assessment of {target} using {scan_type} scanning revealed no immediate security vulnerabilities."
        elif vuln_count <= 2:
            risk_level = "Medium"
            summary = f"The security assessment of {target} identified {vuln_count} security issue(s) that should be addressed."
        else:
            risk_level = "High"
            summary = f"The security assessment of {target} identified {vuln_count} security vulnerabilities requiring immediate attention."
        
        return f"{summary} Overall risk level: {risk_level}."
    
    def _format_vulnerability(self, vuln: Dict[str, Any]) -> List:
        """Format vulnerability for report"""
        elements = []
        
        # Vulnerability title
        title = Paragraph(f"<b>{vuln.get('type', 'Unknown Vulnerability')}</b>", 
                         self.styles['Heading3'])
        elements.append(title)
        
        # Vulnerability details
        details = [
            ['Severity:', vuln.get('severity', 'Unknown')],
            ['URL:', vuln.get('url', 'N/A')],
            ['Parameter:', vuln.get('parameter', 'N/A')],
            ['CVSS Score:', vuln.get('cvss_score', 'N/A')]
        ]
        
        detail_table = Table(details, colWidths=[1.5*inch, 4*inch])
        detail_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(detail_table)
        
        # Description
        if 'description' in vuln:
            desc = Paragraph(f"<b>Description:</b> {vuln['description']}", 
                           self.styles['Normal'])
            elements.append(desc)
        
        # Payload
        if 'payload' in vuln:
            payload = Paragraph(f"<b>Proof of Concept:</b> <font name='Courier'>{vuln['payload']}</font>", 
                              self.styles['Normal'])
            elements.append(payload)
        
        elements.append(Spacer(1, 12))
        
        return elements

class HTMLReportGenerator:
    """Generate security audit reports in HTML format"""
    
    def generate_html_report(self, scan_data: Dict[str, Any], output_path: str) -> str:
        """Generate HTML security audit report"""
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Web Security Audit Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { background-color: #f4f4f4; padding: 20px; border-radius: 5px; }
                .vulnerability { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
                .high { border-left: 5px solid #ff4444; }
                .medium { border-left: 5px solid #ffaa00; }
                .low { border-left: 5px solid #44ff44; }
                .code { background-color: #f8f8f8; padding: 10px; font-family: monospace; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Web Security Audit Report</h1>
                <p><strong>Target:</strong> {target}</p>
                <p><strong>Scan Type:</strong> {scan_type}</p>
                <p><strong>Date:</strong> {date}</p>
            </div>
            
            <h2>Executive Summary</h2>
            <p>{summary}</p>
            
            <h2>Security Findings</h2>
            {vulnerabilities_html}
            
            <h2>Recommendations</h2>
            <ul>
                {recommendations_html}
            </ul>
            
            <h2>Technical Details</h2>
            <div class="code">
                <pre>{technical_details}</pre>
            </div>
        </body>
        </html>
        """
        
        # Generate vulnerabilities HTML
        vulnerabilities_html = ""
        for vuln in scan_data.get('vulnerabilities', []):
            severity_class = vuln.get('severity', 'low').lower()
            vuln_html = f"""
            <div class="vulnerability {severity_class}">
                <h3>{vuln.get('type', 'Unknown Vulnerability')}</h3>
                <p><strong>Severity:</strong> {vuln.get('severity', 'Unknown')}</p>
                <p><strong>URL:</strong> {vuln.get('url', 'N/A')}</p>
                <p><strong>Description:</strong> {vuln.get('description', 'N/A')}</p>
                {f'<div class="code">{vuln["payload"]}</div>' if 'payload' in vuln else ''}
            </div>
            """
            vulnerabilities_html += vuln_html
        
        # Generate recommendations HTML
        recommendations_html = ""
        for rec in scan_data.get('recommendations', []):
            recommendations_html += f"<li>{rec}</li>"
        
        # Fill template
        html_content = html_template.format(
            target=scan_data.get('target', 'Unknown'),
            scan_type=scan_data.get('scan_type', 'Unknown'),
            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            summary=self._generate_summary(scan_data),
            vulnerabilities_html=vulnerabilities_html,
            recommendations_html=recommendations_html,
            technical_details=json.dumps(scan_data.get('results', {}), indent=2)
        )
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        return output_path
    
    def _generate_summary(self, scan_data: Dict[str, Any]) -> str:
        """Generate executive summary"""
        target = scan_data.get('target', 'Unknown')
        vuln_count = len(scan_data.get('vulnerabilities', []))
        
        if vuln_count == 0:
            return f"No security vulnerabilities were identified during the assessment of {target}."
        else:
            return f"The security assessment identified {vuln_count} vulnerability(ies) that require attention."