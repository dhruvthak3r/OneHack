def generate_email_template(user_name: str, hackathon_name: str, start_date: str, reg_end_date: str, url: str):
    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f7f7f7;
                padding: 20px;
            }}
            .container {{
                background-color: #ffffff;
                border-radius: 8px;
                padding: 30px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                max-width: 600px;
                margin: auto;
            }}
            h2 {{
                color: #333;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
            }}
            .footer {{
                font-size: 12px;
                color: #999;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Hello {user_name},</h2>
            <p>We have some exciting news for you! 🚀</p>
            <p>You showed interest in <strong>{hackathon_name}</strong>, and it's right around the corner.</p>
            <p><strong>Start Date:</strong> {start_date}</p>
            <p><strong>Registrations Ends On:</strong> {reg_end_date}</p>
            <p>Make sure to register and prepare ahead of time.</p>
            <a href="{url}" class="button">Register Now</a>
            <div class="footer">
                You received this email because you bookmarked this hackathon. If this was a mistake, you can ignore this message.
            </div>
        </div>
    </body>
    </html>
    """
