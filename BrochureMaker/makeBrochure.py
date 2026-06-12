import base64

def generate_brochure_html(brochure_data, image_source, title):
    """
    Transforms the structured dictionary panels into a pixel-perfect,
    professional bifold brochure with a faded background image wrapper.
    """
    img_url = ""
    if hasattr(image_source, "read"):
        bytes_data = image_source.getvalue()
        base64_img = base64.b64encode(bytes_data).decode("utf-8")
        img_url = f"data:image/png;base64,{base64_img}"
    elif isinstance(image_source, str):
        img_url = image_source

    # Safely extract left and right track sections
    left_content = brochure_data.get("left_fold_html", "")
    right_content = brochure_data.get("right_fold_html", "")

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @page {{
                size: A4 landscape;
                margin: 0;
            }}
            body {{
                font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
                margin: 0; padding: 0;
                background-color: #f8f9fa;
                color: #2b2b2b;
            }}
            .brochure-container {{
                width: 297mm; height: 210mm;
                position: relative; box-sizing: border-box;
                padding: 25mm 20mm; display: flex; gap: 24mm;
                background: white; overflow: hidden;
            }}
            /* Soft, faded brand background graphic */
            .brochure-container::before {{
                content: ' ';
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                opacity: 0.06;
                background-image: url('{img_url}');
                background-size: cover; background-position: center;
                z-index: 1;
            }}
            .fold-column {{
                flex: 1; width: 50%;
                z-index: 2; position: relative;
                display: flex; flex-direction: column;
            }}
            .header-block {{
                border-bottom: 3px solid #003366; /* Elegant Navy Blue Theme */
                padding-bottom: 12px;
                margin-bottom: 18px;
            }}
            h1 {{
                font-size: 26px; color: #003366; margin: 0;
                text-transform: uppercase; letter-spacing: 0.5px;
            }}
            h2 {{
                font-size: 16px; color: #4682B4; margin-top: 22px; margin-bottom: 10px;
                text-transform: uppercase; letter-spacing: 0.5px; border-left: 4px solid #003366; padding-left: 8px;
            }}
            p {{
                font-size: 12.5px; line-height: 1.6; color: #333333; margin-bottom: 12px; text-align: justify;
            }}
            ul {{ padding-left: 18px; margin-top: 5px; margin-bottom: 12px; }}
            li {{ font-size: 12.5px; color: #333333; margin-bottom: 6px; line-height: 1.5; }}
            .right-panel {{
                border-left: 1px dashed #d1d5db; padding-left: 12mm;
            }}
        </style>
    </head>
    <body>
        <div class="brochure-container">
            <!-- Left Fold -->
            <div class="fold-column">
                <div class="header-block">
                    <h1>{title}</h1>
                </div>
                {left_content}
            </div>
            
            <!-- Right Fold -->
            <div class="fold-column right-panel">
                {right_content}
            </div>
        </div>
    </body>
    </html>
    """
    return html_template