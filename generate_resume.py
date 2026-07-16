import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def build_pdf():
    pdf_path = "resume.pdf"
    
    # Page setup
    # A4 is 595.27 x 841.89 points. 
    # Margins: 36 pt (0.5 inch) all around.
    # Printable width: 595.27 - 72 = 523.27 pt.
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = colors.HexColor("#0f172a") # Dark Slate
    secondary_color = colors.HexColor("#4f46e5") # Indigo Accent
    text_color = colors.HexColor("#27272a") # Zinc 800
    light_text_color = colors.HexColor("#71717a") # Zinc 500
    border_color = colors.HexColor("#e4e4e7") # Zinc 200
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=light_text_color,
        spaceAfter=12
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=13,
        textColor=primary_color,
        spaceAfter=0
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=text_color
    )
    
    body_bold_style = ParagraphStyle(
        'BodyTextBoldCustom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=text_color
    )
    
    project_title_style = ParagraphStyle(
        'ProjectTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=primary_color,
        spaceAfter=3
    )
    
    project_desc_style = ParagraphStyle(
        'ProjectDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=text_color,
        spaceAfter=6
    )

    story = []
    
    # ---------------------------------------------------------
    # 1. HEADER (Image on left, Name & Contacts on right)
    # ---------------------------------------------------------
    # Image aspect ratio is 3:4. Let's make it 84 pt wide, 112 pt high.
    profile_img_path = "profile.png"
    if os.path.exists(profile_img_path):
        profile_img = Image(profile_img_path, width=84, height=112)
    else:
        # Fallback if image doesn't exist (should not happen in this environment)
        profile_img = Paragraph("<b>[Photo]</b>", body_style)
        
    # Header texts
    name_para = Paragraph("GUNTINAN PENMONGKON", title_style)
    role_para = Paragraph("IT Support | Network Engineer", subtitle_style)
    
    # Contact items formatting
    c_phone = "<b>Phone:</b> 084-256-8211"
    c_email = "<b>Email:</b> guntinan.penmongkon@gmail.com"
    c_web = "<b>Web:</b> guntinanpmk.vercel.app"
    c_github = "<b>GitHub:</b> github.com/GGun32993"
    
    contact_table_data = [
        [Paragraph(c_phone, contact_style), Paragraph(c_email, contact_style)],
        [Paragraph(c_web, contact_style), Paragraph(c_github, contact_style)]
    ]
    
    # Contact table inside the header
    contact_table = Table(contact_table_data, colWidths=[150, 250])
    contact_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    
    header_right_flowables = [
        name_para,
        role_para,
        Spacer(1, 4),
        contact_table
    ]
    
    header_table_data = [[profile_img, header_right_flowables]]
    header_table = Table(header_table_data, colWidths=[100, 423])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 10))
    
    # Helper to create a section header table with bottom line
    def create_section_header(title):
        header_table = Table([[Paragraph(title, section_title_style)]], colWidths=[523])
        header_table.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor("#0f172a")),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        return header_table

    # ---------------------------------------------------------
    # 2. ABOUT ME
    # ---------------------------------------------------------
    story.append(create_section_header("ABOUT ME"))
    story.append(Spacer(1, 5))
    about_text = (
        "<b>Computer Science</b> student at Suan Dusit University pursuing a career as a <b>Network Engineer</b>. "
        "Hands-on experience designing and managing network infrastructure, automation, and security through real "
        "Home Lab projects. Committed to continuous learning to deliver reliable, secure, and professional-grade systems."
    )
    story.append(Paragraph(about_text, body_style))
    story.append(Spacer(1, 5))
    
    # ---------------------------------------------------------
    # 3. EDUCATION
    # ---------------------------------------------------------
    story.append(create_section_header("EDUCATION"))
    story.append(Spacer(1, 5))
    
    edu_data = [
        [Paragraph("&bull; 2022 - Present", body_style), Paragraph("<b>Suan Dusit University</b>", body_bold_style), Paragraph("Major: Computer Science", body_style)],
        [Paragraph("&bull; 2016 - 2022", body_style), Paragraph("<b>High School</b>", body_bold_style), Paragraph("Mathematics - English Program (Suratpittaya School)", body_style)]
    ]
    edu_table = Table(edu_data, colWidths=[90, 130, 303])
    edu_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(edu_table)
    story.append(Spacer(1, 5))
    
    # ---------------------------------------------------------
    # 4. PROJECTS (Two columns)
    # ---------------------------------------------------------
    story.append(create_section_header("PROJECTS"))
    story.append(Spacer(1, 6))
    
    # Left column flowables
    p1_title = Paragraph("Secure Hybrid Infrastructure IaC", project_title_style)
    p1_desc = Paragraph(
        "Designed and deployed a highly secure, simulated network infrastructure featuring 3 internal servers, "
        "automated via Infrastructure as Code (IaC) principles. The system includes a comprehensive monitoring "
        "stack using Prometheus and Grafana for real-time infrastructure visibility and performance tracking.",
        project_desc_style
    )
    
    p2_title = Paragraph("HR Intelligent RAG Chatbot", project_title_style)
    p2_desc = Paragraph(
        "Developed an HR RAG Chatbot designed to query and answer questions from company policy documents "
        "using Python, Streamlit, ChromaDB, and the Gemini API. The system strictly constrains responses to the "
        "actual data within the employee handbook to mitigate hallucinations and ensure factual accuracy.",
        project_desc_style
    )
    
    col1_flowables = [p1_title, p1_desc, Spacer(1, 4), p2_title, p2_desc]
    
    # Right column flowables
    p3_title = Paragraph("Automated Backup System", project_title_style)
    p3_desc = Paragraph(
        "Designed and implemented a highly secure, automated Home Lab backup infrastructure using Ansible "
        "to orchestrate Restic and Rclone. The system encrypts and backs up critical data—including Docker "
        "volumes, configurations, and PostgreSQL/SQLite databases—directly to Google Drive, featuring real-time "
        "status alerts integrated via Discord Webhooks.",
        project_desc_style
    )
    
    p4_title = Paragraph("Freelance Matching Online", project_title_style)
    p4_desc = Paragraph(
        "Developed a freelance job-matching platform utilizing PHP for robust server-side processing and backend logic, "
        "integrated with Leaflet and Geoapify API to enable precise geolocation search and location-based filtering "
        "for users.",
        project_desc_style
    )
    
    col2_flowables = [p3_title, p3_desc, Spacer(1, 4), p4_title, p4_desc]
    
    # Wrap columns in a single table row
    projects_table_data = [[col1_flowables, col2_flowables]]
    projects_table = Table(projects_table_data, colWidths=[251, 252])
    projects_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (0,0), 0),
        ('RIGHTPADDING', (0,0), (0,0), 10), # Gap between columns
        ('LEFTPADDING', (1,0), (1,0), 10), # Gap between columns
        ('RIGHTPADDING', (1,0), (1,0), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(projects_table)
    story.append(Spacer(1, 2))
    
    # ---------------------------------------------------------
    # 5. SKILLS
    # ---------------------------------------------------------
    story.append(create_section_header("SKILLS"))
    story.append(Spacer(1, 5))
    
    skills_data = [
        [
            Paragraph("&bull; <b>Networking & Protocols:</b> Cisco Routers & Switches, Cisco IOS, IPv4/IPv6 Subnetting, TCP/IP &amp; NAT/Routing, WireGuard VPN, DNS/DHCP, Wireless Access", body_style)
        ],
        [
            Paragraph("&bull; <b>Systems & Security:</b> Linux Server Admin, Active Directory &amp; GPO, PC &amp; Laptop Hardware Support, Firewall (UFW &amp; iptables)", body_style)
        ],
        [
            Paragraph("&bull; <b>Tools & Automation:</b> Ansible (IaC), Vagrant, Docker, VirtualBox, Git, Python &amp; Bash Scripting", body_style)
        ]
    ]
    skills_table = Table(skills_data, colWidths=[523])
    skills_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 5))
    
    # ---------------------------------------------------------
    # 6. CERTIFICATIONS
    # ---------------------------------------------------------
    story.append(create_section_header("CERTIFICATIONS"))
    story.append(Spacer(1, 5))
    
    certs_data = [
        [Paragraph("&bull; Networking Basics ( Cisco Networking Academy )", body_style)],
        [Paragraph("&bull; Networking Devices and Initial Configuration ( Cisco Networking Academy )", body_style)],
        [Paragraph("&bull; Network Addressing and Basic Troubleshooting ( Cisco Networking Academy )", body_style)],
        [Paragraph("&bull; Network Support and Security ( Cisco Networking Academy )", body_style)]
    ]
    certs_table = Table(certs_data, colWidths=[523])
    certs_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(certs_table)
    
    # Build Document
    doc.build(story)
    print("PDF generated successfully as resume.pdf")

if __name__ == "__main__":
    build_pdf()
