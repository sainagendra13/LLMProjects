from utils import get_website_content,get_website_links
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv(override=True)

def llmAction(client: OpenAI,sys_prompt:str, user_prompt:str, response_format=None):
    messages=[
        {"role":"system","content":sys_prompt},
        {"role":"user","content":user_prompt}
    ]
    res=client.chat.completions.create(model="gpt-4o-mini",messages=messages, response_format=response_format)
    response=res.choices[0].message.content
    return response

def get_links_user_prompt(url, type_select):
    user_prompt = f"""
Here is the list of links on the website of {type_select} {url} -
Please decide which of these are relevant web links for a brochure about the company, 
respond with the full https URL in JSON format.
Do not include Terms of Service, Privacy, email links.

Links (some might be relative links):

"""
    content_links,img_links = get_website_links(url)
    user_prompt += "\n".join(content_links)
    return user_prompt,img_links

    
def llm1_controller(url,type_select):
    api_key=os.getenv('OPENAI_API_KEY')
    client=OpenAI()
    llm1_prompt=f'''
    You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the {type_select},
such as links to an About page, or a Company page, or Careers/Jobs pages if it is company or event details such as event venue, event information, date, contacts etc for invitation and marketing if available. Also add if any new events in the website are coming up.
You should respond in JSON as in this example:

{{
    "links": [
        {{"type": "about page", "url": "https://full.url/goes/here/about"}},
        {{"type": "careers page", "url": "https://another.full.url/careers"}}
    ]
}}
    
    '''
    content_prompt,img_links=get_links_user_prompt(url,type_select)
    response_format={"type": "json_object"}
    response=llmAction(client,llm1_prompt,content_prompt, response_format )
    links=json.loads(response)
    return links, img_links


    
def llm2_controller(text,tone, name,type_select):
    api_key=os.getenv('OPENAI_API_KEY')
    client=OpenAI()
    # llm2_prompt=f'''
    # You are an assistant that analyzes the contents of several relevant pages from a company or an event website given by user
    # and creates a short brochure about the prospective customers, investors and recruits if it is a company or event details such event information, date etc if it data seems like an event
    # Respond in markdown without code blocks with tome set as {tone}. If it business/professional, then it should be professional format. If it is jovial or humorous or snarky, make sure it won't hurt others.
    # Include details of company culture, customers and careers/jobs if you have the information.
    # '''
    # user_prompt = f"""
    # You are looking at a {type_select} called: {name}
    # Here are the contents of its landing page and other relevant pages;
    # use this information to build a short brochure of the {type_select} in markdown without code blocks. Maximum word limit is 5000\n\n
    # """
    
    llm2_prompt = f'''
You are a master layout editor. Analyze the website content and output a professional, corporate brochure split into a two-panel bi-fold design.
You MUST respond strictly in valid JSON format matching the example below.
Do not use Markdown formatting inside the strings; use clean HTML blocks like <h2>, <p>, <ul>, <li> for structural presentation.

Tone setting: {tone}.

Expected Output JSON structure:
{{
    "left_fold_html": "<h2>About the {type_select}</h2><p>Content...</p><h2>Key Highlights</h2><ul><li>Point 1</li></ul>",
    "right_fold_html": "<h2>Logistics & Schedule</h2><p>Date/Location...</p><h2>About the Organizer</h2><p>Details...</p>"
}}
'''
    user_prompt = f"""
Build a short, clear business brochure layout for a {type_select} named: {name}.
Here are the contents of its landing page and other relevant pages:
"""

    if "links" in text:
        for link in text["links"]:
            page_url = link.get("url")
            page_type = link.get("type", "page")
            if page_url:
                try:
                    scraped_text = get_website_content(page_url)
                    user_prompt += f"Section ({page_type}):\n{scraped_text}\n\n"
                except Exception:
                    pass
    
    response_format = {"type": "json_object"}
    textdata = llmAction(client, llm2_prompt, user_prompt, response_format)
    
    try:
        # Return the parsed multi-column layout structure
        return json.loads(textdata)
    except Exception:
        # Fallback dictionary if formatting fails
        return {
            "left_fold_html": f"<h2>{name}</h2><p>Review website data for processing blocks.</p>",
            "right_fold_html": "<h2>Details</h2><p>Data parsing error fallback.</p>"
        }
    