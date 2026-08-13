import os
from PIL import Image as PILImage, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_resume_icons():
    size = 128
    bg_color = (15, 23, 42) # #0f172a
    fg_color = (255, 255, 255)
    
    # 1. Phone Icon
    img_phone = PILImage.new('RGBA', (size, size), (0,0,0,0))
    d_p = ImageDraw.Draw(img_phone)
    d_p.ellipse((0, 0, size-1, size-1), fill=bg_color)
    d_p.polygon([
        (48, 40), (60, 40), (64, 52), (57, 59), 
        (69, 71), (76, 64), (88, 68), (88, 80), 
        (78, 86), (60, 86), (42, 68), (42, 52)
    ], fill=fg_color)
    img_phone.save('icon_phone.png')

    # 2. Email Icon
    img_email = PILImage.new('RGBA', (size, size), (0,0,0,0))
    d_e = ImageDraw.Draw(img_email)
    d_e.ellipse((0, 0, size-1, size-1), fill=bg_color)
    d_e.rounded_rectangle((32, 44, 96, 84), radius=6, outline=fg_color, width=7)
    d_e.line([(34, 46), (64, 68), (94, 46)], fill=fg_color, width=7)
    img_email.save('icon_email.png')

    # 3. Globe Icon (Web)
    img_web = PILImage.new('RGBA', (size, size), (0,0,0,0))
    d_w = ImageDraw.Draw(img_web)
    d_w.ellipse((0, 0, size-1, size-1), fill=bg_color)
    d_w.ellipse((34, 34, 94, 94), outline=fg_color, width=6)
    d_w.line([(34, 64), (94, 64)], fill=fg_color, width=6)
    d_w.ellipse((48, 34, 80, 94), outline=fg_color, width=6)
    img_web.save('icon_web.png')

    # 4. GitHub Icon
    img_gh = PILImage.new('RGBA', (size, size), (0,0,0,0))
    d_g = ImageDraw.Draw(img_gh)
    d_g.ellipse((0, 0, size-1, size-1), fill=bg_color)
    d_g.ellipse((36, 36, 92, 92), fill=fg_color)
    d_g.polygon([(36, 36), (48, 50), (40, 58)], fill=bg_color)
    d_g.polygon([(92, 36), (80, 50), (88, 58)], fill=bg_color)
    d_g.ellipse((48, 56, 80, 88), fill=bg_color)
    d_g.polygon([(56, 76), (64, 66), (72, 76), (64, 88)], fill=fg_color)
    img_gh.save('icon_github.png')

def build_pdf():
    pdf_path = "resume.pdf"
    
    # Ensure icons exist
    if not (os.path.exists("icon_phone.png") and os.path.exists("icon_email.png") and os.path.exists("icon_web.png") and os.path.exists("icon_github.png")):
        create_resume_icons()
        
    # Page setup
    # A4 is 595.27 x 841.89 points.
    # Margins: 36 pt (0.5 inch) all around.
    # Printable width: 595.27 - 72 = 523.27 pt.
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=32,
        bottomMargin=32
    )
    
    styles = getSampleStyleSheet()
    
    # Colors
    primary_color = colors.HexColor("#0f172a") # Dark Slate
    text_color = colors.HexColor("#1e293b") # Slate 800
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=26,
        textColor=primary_color,
        spaceAfter=10
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
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
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
        leading=11.5,
        textColor=text_color
    )

    story = []
    
    # ---------------------------------------------------------
    # 1. HEADER (Image on left, Name & Contacts on right)
    # ---------------------------------------------------------
    profile_img_path = "profile.png"
    if os.path.exists(profile_img_path):
        profile_img = Image(profile_img_path, width=84, height=112)
    else:
        profile_img = Paragraph("<b>[Photo]</b>", body_style)
        
    name_para = Paragraph("GUNTINAN PENMONGKON", title_style)
    
    # Contact items with icons
    icon_w, icon_h = 13, 13
    
    def make_contact_cell(icon_path, text_str):
        img_icon = Image(icon_path, width=icon_w, height=icon_h)
        text_p = Paragraph(text_str, contact_style)
        t = Table([[img_icon, text_p]], colWidths=[18, None])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        return t

    c_phone_cell = make_contact_cell("icon_phone.png", "084-256-8211")
    c_email_cell = make_contact_cell("icon_email.png", "guntinan.penmongkon@gmail.com")
    c_web_cell = make_contact_cell("icon_web.png", "https://guntinanpmk.vercel.app")
    c_github_cell = make_contact_cell("icon_github.png", "https://github.com/GGun32993")
    
    contact_table_data = [
        [c_phone_cell, c_email_cell],
        [c_web_cell, c_github_cell]
    ]
    
    contact_table = Table(contact_table_data, colWidths=[175, 230])
    contact_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    
    header_right_flowables = [
        name_para,
        contact_table
    ]
    
    header_table_data = [[profile_img, header_right_flowables]]
    header_table = Table(header_table_data, colWidths=[100, 423])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 8))
    
    # Helper to create a section header table with bottom line
    def create_section_header(title):
        header_table = Table([[Paragraph(title, section_title_style)]], colWidths=[523])
        header_table.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor("#0f172a")),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        return header_table

    # ---------------------------------------------------------
    # 2. ABOUT ME
    # ---------------------------------------------------------
    story.append(create_section_header("ABOUT ME"))
    story.append(Spacer(1, 4))
    about_text = (
        "<b>Computer Science</b> student at SuanDusit University pursuing a career as a <b>Network Engineer</b>. "
        "Hands-on experience designing and managing network infrastructure, automation, and security through real "
        "Home Lab projects. Committed to continuous learning to deliver reliable, secure, and professional-grade systems."
    )
    story.append(Paragraph(about_text, body_style))
    story.append(Spacer(1, 4))
    
    # ---------------------------------------------------------
    # 3. EDUCATION
    # ---------------------------------------------------------
    story.append(create_section_header("EDUCATION"))
    story.append(Spacer(1, 4))
    
    edu_p1 = Paragraph("&bull; 2022 - Present SuanDusit University Major : Computer Science", body_style)
    edu_p2 = Paragraph("&bull; 2016 - 2022 High School : Mathematics - English Program", body_style)
    
    edu_table_data = [[edu_p1], [edu_p2]]
    edu_table = Table(edu_table_data, colWidths=[523])
    edu_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(edu_table)
    story.append(Spacer(1, 4))
    
    # ---------------------------------------------------------
    # 4. PROJECTS (Two columns)
    # ---------------------------------------------------------
    story.append(create_section_header("PROJECTS"))
    story.append(Spacer(1, 5))
    
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
    
    col1_flowables = [p1_title, p1_desc, Spacer(1, 6), p2_title, p2_desc]
    
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
    
    col2_flowables = [p3_title, p3_desc, Spacer(1, 6), p4_title, p4_desc]
    
    # Wrap columns in a single table row
    projects_table_data = [[col1_flowables, col2_flowables]]
    projects_table = Table(projects_table_data, colWidths=[251, 252])
    projects_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (0,0), 0),
        ('RIGHTPADDING', (0,0), (0,0), 10),
        ('LEFTPADDING', (1,0), (1,0), 10),
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
    story.append(Spacer(1, 4))
    
    skills_data = [
        [
            Paragraph("&bull; <b>Networking &amp; Protocols :</b> Cisco Routers &amp; Switches, Cisco IOS, IPv4/IPv6 Subnetting, TCP/IP &amp; NAT/Routing, WireGuard VPN, DNS/DHCP, Wireless Access", body_style)
        ],
        [
            Paragraph("&bull; <b>Systems &amp; Security :</b> Linux Server Admin, Active Directory &amp; GPO, Firewall (UFW &amp; iptables)", body_style)
        ],
        [
            Paragraph("&bull; <b>Tools &amp; Automation :</b> Ansible (IaC), Vagrant, Docker, VirtualBox, Git, Python &amp; Bash Scripting", body_style)
        ]
    ]
    skills_table = Table(skills_data, colWidths=[523])
    skills_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 4))
    
    # ---------------------------------------------------------
    # 6. CERTIFICATIONS
    # ---------------------------------------------------------
    story.append(create_section_header("CERTIFICATIONS"))
    story.append(Spacer(1, 4))
    
    certs_data = [
        [Paragraph("&bull; <b>Networking Basics ( Cisco Networking Academy )</b>", body_style)],
        [Paragraph("&bull; <b>Networking Devices and Initial Configuration ( Cisco Networking Academy )</b>", body_style)],
        [Paragraph("&bull; <b>Network Addressing and Basic Troubleshooting ( Cisco Networking Academy )</b>", body_style)],
        [Paragraph("&bull; <b>Network Support and Security ( Cisco Networking Academy )</b>", body_style)]
    ]
    certs_table = Table(certs_data, colWidths=[523])
    certs_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(certs_table)
    
    # Build Document
    doc.build(story)
    print("PDF generated successfully as resume.pdf")

if __name__ == "__main__":
    build_pdf()
