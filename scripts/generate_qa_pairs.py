import pandas as pd

def create_qa_pairs():
    """Create 60 corrected multiple-choice HTML question-answer pairs"""
    
    qa_data = {
        'question_id': [f"Q{i:03d}" for i in range(1, 61)],
        'topic_id': [
            'T001', 'T001', 'T001', 'T001', 'T001', 'T001', 'T001',
            'T002', 'T002', 'T002', 'T002', 'T002', 'T002', 'T002',
            'T003', 'T003', 'T003', 'T003', 'T003', 'T003',
            'T004', 'T004', 'T004', 'T004', 'T004', 'T004', 'T004',
            'T005', 'T005', 'T005', 'T005', 'T005', 'T005', 'T005',
            'T006', 'T006', 'T006', 'T006', 'T006', 'T006', 'T006',
            'T007', 'T007', 'T007', 'T007', 'T007', 'T007', 'T007',
            'T008', 'T008', 'T008', 'T008', 'T008', 'T008',
            'T009', 'T009', 'T009', 'T009', 'T009', 'T009'
        ],
        'question_text': [
            # T001
            "What does HTML stand for?",
            "What is the main job of HTML on a webpage?",
            "What declaration should appear at the beginning of a modern HTML document?",
            "When you open an HTML file in a web browser, what does the browser normally do?",
            "What is an HTML tag?",
            "Which HTML element contains the main content displayed within a webpage?",
            "Which two main sections sit inside the <html> element in a basic HTML document?",
            # T002
            "Which HTML element marks a paragraph?",
            "How many levels of HTML headings are defined, from <h1> to <h6>?",
            "Which heading element has the highest heading rank and is usually largest in default browser styling?",
            "Which heading element has the lowest heading rank and is usually smallest in default browser styling?",
            "Which kind of information belongs in the <head> element of an HTML document?",
            "Which HTML element inserts a line break without starting a new paragraph?",
            "What is technically special about the <br> element in HTML?",
            # T003
            "Which heading element is commonly used for the main heading in the page content?",
            "What does the <p> element represent on a webpage?",
            "If an author forgets a closing </p> tag, what will usually happen in a browser?",
            "Which heading element is one level below <h1>?",
            "How does <h1> differ from <h2> in heading hierarchy?",
            "Can a heading element be nested inside a paragraph element?",
            # T004
            "Which attribute specifies the destination of a hyperlink on an <a> element?",
            "Which HTML element normally creates a hyperlink when it has an href attribute?",
            "What does the href attribute specify on a hyperlink?",
            "Which attribute value requests that a link open in a new browsing context, often a new tab or window?",
            "Which example correctly links the text Google to the Google website?",
            "What normally happens when someone activates a working hyperlink?",
            "How can an image be made into a clickable hyperlink?",
            # T005
            "Which HTML element embeds an image in a webpage?",
            "Which attribute identifies the image resource to load in an <img> element?",
            "What does the alt attribute provide for an image?",
            "Why should an informative image have meaningful alt text?",
            "Which statement about image formats on modern webpages is correct?",
            "What is a common sign that an image source is broken or unavailable?",
            "Which pair of HTML attributes can specify an image's width and height?",
            # T006
            "Which element creates an unordered list, commonly shown with bullets by default?",
            "Which element creates an ordered list, commonly shown with numbers by default?",
            "What is the default distinction between <ul> and <ol>?",
            "Which element represents an individual item inside an HTML list?",
            "Which HTML table element represents a row?",
            "Which HTML table element creates a header cell?",
            "Which HTML table element creates a standard data cell?",
            # T007
            "Which HTML element can create a single-line text input control?",
            "Which attribute supplies the field name included when form data is submitted?",
            "What does the type attribute do on an <input> element?",
            "What is the main purpose of an HTML form?",
            "Which control below is explicitly configured to submit a form when activated?",
            'What is the usual difference between type="text" and type="password" inputs?',
            "How do you specify a checkbox using an input element?",
            # T008
            "Why use semantic HTML elements such as <nav>, <main> and <footer>?",
            "Which semantic element commonly contains introductory content for a page or section?",
            "Which semantic element represents a section containing major navigation links?",
            "Which semantic element represents the dominant main content of a page?",
            "Which semantic element commonly contains footer information for a page or section?",
            "How can semantic HTML help people using screen readers?",
            # T009
            "What is a sensible first step when beginning to plan a website?",
            "What information is commonly placed in a webpage footer?",
            "Why should you test a webpage after building it?",
            "Who is a visitor to a website?",
            "What does responsive web design mean?",
            "Why is it helpful to plan a webpage before coding?"
        ],
        'option_a': [
            # T001
            "HighText Markdown Language", "To control all colours and visual styling by itself", "<!DOCTYPE html>", "It automatically edits the source code", "A markup token written in angle brackets, such as <p> or </p>", "<body>", "A <header> section and a <footer> section",
            # T002
            "<h1>", "7 levels", "<h3>", "<h4>", "Document metadata, including the page title and links to resources", "<p>", "It is not a valid HTML element",
            # T003
            "<h2>", "A heading", "The browser always refuses to load the whole page", "<h3>", "They always represent exactly the same heading level", "Yes, as long as the heading is <h1>",
            # T004
            "src", "<link>", "The image file shown inside the link", 'target="_blank"', '<a src="https://www.google.com">Google</a>', "The browser navigates to the linked resource", "Place an <a> element inside the <img> element",
            # T005
            "<image>", "alt", "A text alternative that assistive technology can present and that may appear if the image cannot load", "It makes the image file load faster", "Only JPEG images can appear on webpages", "The browser may show a broken-image indicator and/or the alt text", "width and height",
            # T006
            "<list>", "<ul>", "<ul> represents an unordered list and <ol> represents an ordered list", "<point>", "<table>", "<th>", "<data>",
            # T007
            '<input type="text">', "placeholder", "It adds a visible label automatically", "To change the webpage's colours by itself", '<input type="submit">', "Both types always encrypt the entered value in the browser", 'Set type="checkbox"',
            # T008
            "They automatically make a page colourful", "<section>", "<nav>", "<content>", "<footer>", "It guarantees that the page looks modern",
            # T009
            "Decide the page's purpose, audience and content", "Only social media links are allowed", "To guarantee that the page will never contain an error", "A person who views or uses the website", "The layout adapts to different screen sizes and devices", "It helps organise content and clarify what needs to be built"
        ],
        'option_b': [
            # T001
            "HyperText Markup Language", "To run database queries and server-side code", "<body>", "It parses the HTML and renders the webpage", "A complete programming application", "<head>", "A <head> section and a <body> section",
            # T002
            "<div>", "5 levels", "<h1>", "<h5>", "The list items displayed as part of the page content", "<hr>", "It is a void element and does not have a separate closing tag",
            # T003
            "<h1>", "A paragraph of text", "The browser often still displays the text, but the document structure may not be as intended", "<h2>", "<h1> has a lower heading rank than <h2>", "Yes, if the paragraph has a class attribute",
            # T004
            "link", "<hyperlink>", "The text colour of the link", "new_window", '<a href="https://www.google.com">Google</a>', "The browser checks all spelling in the page", 'Place the <img> element inside an <a href="..."> element',
            # T005
            "<img>", "href", "A command that makes the image larger", "It changes the image colour", "Common formats such as JPEG, PNG, GIF and WebP can be used, subject to browser support", "The browser automatically repairs the missing image file", "size and image-size",
            # T006
            "<ul>", "<ol>", "Both elements always create bulleted lists", "<list>", "<row>", "<thead>", "<td>",
            # T007
            "<form>", "id", "It determines the font size of the input", "To collect user input and submit it for processing", "<submit>", "Text displays typed characters; password visually masks them", 'Set type="check"',
            # T008
            "They automatically make every page load faster", "<footer>", "<navigation>", "<section>", "<bottom>", "It automatically makes all text larger",
            # T009
            "Choose random images before planning the content", "Copyright information, contact details or related links", "To find problems with links, layout, content or functionality", "A person who maintains the website's server as their job", "The layout stays fixed even when it no longer fits the screen", "Planning guarantees that testing will never find errors"
        ],
        'option_c': [
            # T001
            "Hyperlink and Text Markup Language", "To define the structure and meaning of webpage content", "<html>", "It automatically saves the file to your computer", "A type of web browser", "<meta>", "A <title> section and a <nav> section",
            # T002
            "<p>", "6 levels", "<h2>", "<h6>", "The main paragraphs and images displayed in the page body", "<br>", "It always requires a separate </br> closing tag",
            # T003
            "<h6>", "A line break only", "The browser always repairs every possible markup problem perfectly", "<p>", "<h1> has a higher heading rank than <h2>", "No. A paragraph element cannot contain a heading element",
            # T004
            "href", "<a>", "The destination URL or resource for the link", "open_new", "<a>Google</a>", "The browser automatically inserts an image", "Images can never be placed inside hyperlinks",
            # T005
            "<picture>", "src", "A visible caption automatically displayed underneath the image", "It helps people using screen readers access the image's information", "Only GIF images can appear on webpages", "The browser closes the entire webpage", "length and breadth",
            # T006
            "<ol>", "<item>", "<ul> is ordered and <ol> is unordered", "<li>", "<tr>", "<tr>", "<tc>",
            # T007
            "<textarea>", "name", "It specifies the kind of input control, such as text, password or checkbox", "To create animations by itself", '<button type="button">Submit</button>', "Text fields always mask characters; password fields show them openly", 'Set type="tickbox"',
            # T008
            "They communicate the role and structure of different page regions", "<header>", "<footer>", "<main>", "<lower>", "It exposes meaningful structure and landmarks that assistive technology can identify",
            # T009
            "Start typing HTML before deciding what the page is for", "Only the page title and nothing else", "To make the webpage colourful without changing its code", "A person who necessarily wrote the website's HTML", "The website only works on desktop computers", "Planning is unnecessary for every small webpage"
        ],
        'correct_answer': [
            # T001
            'B', 'C', 'A', 'B', 'A', 'A', 'B',
            # T002
            'C', 'C', 'B', 'C', 'A', 'C', 'B',
            # T003
            'B', 'B', 'B', 'B', 'C', 'C',
            # T004
            'C', 'C', 'C', 'A', 'B', 'A', 'B',
            # T005
            'B', 'C', 'A', 'C', 'B', 'A', 'A',
            # T006
            'B', 'B', 'A', 'C', 'C', 'A', 'B',
            # T007
            'A', 'C', 'C', 'B', 'A', 'B', 'A',
            # T008
            'C', 'C', 'A', 'C', 'A', 'C',
            # T009
            'A', 'B', 'B', 'A', 'A', 'A'
        ],
        'hint_text': [
            # T001
            "Think about the four letters H, T, M and L.",
            "Think about the page structure rather than its colours or animations.",
            "Look for the declaration that identifies the document type.",
            "Think about how the browser turns markup into a displayed page.",
            "Look at the angle brackets around markup names.",
            "Think of the element for page content, rather than document metadata.",
            "Think about document information versus displayed page content.",
            # T002
            "The element name begins with the letter p.",
            "Count the heading elements from h1 through h6.",
            "The heading ranks run from h1 down to h6.",
            "The highest heading rank is h1; follow the sequence down to its end.",
            "Think about document information and resources, not the main visible content.",
            "Its name is short for a line break.",
            "Check whether this element has content that needs an end tag.",
            # T003
            "Choose the highest-level heading for the page's main heading.",
            "The p in the element name stands for paragraph.",
            "Browsers often recover from some markup mistakes, but that does not make the code correct.",
            "Move one step down from h1 in the heading sequence.",
            "The heading number indicates the rank in the hierarchy.",
            "Think about which kinds of content are allowed inside a paragraph.",
            # T004
            "This attribute name begins with h and points to the linked resource.",
            "It is a one-letter element name.",
            "Think about where the browser should go when the link is activated.",
            "Look for the target attribute and its special underscore-prefixed value.",
            "A hyperlink uses href to specify its destination.",
            "Think about what a link is designed to navigate to.",
            "The link element can wrap the content that should be clickable.",
            # T005
            "The element name is a short form of image.",
            "This attribute is short for source.",
            "Think about text that can communicate the image's purpose when the image cannot be seen.",
            "Think about accessibility for people who cannot see the image.",
            "Modern browsers support several common image formats.",
            "Think about what the browser can display when it cannot retrieve an image.",
            "Use the attribute names that correspond directly to the dimensions.",
            # T006
            "UL stands for unordered list.",
            "OL stands for ordered list.",
            "Look at what UL and OL stand for.",
            "Its name stands for list item.",
            "TR stands for table row.",
            "TH stands for table header cell.",
            "TD stands for table data cell.",
            # T007
            "Input controls use the input element; textarea is for multi-line text.",
            "The submitted form-data key is supplied by this attribute.",
            "Different type values create different input controls.",
            "Forms are used to collect information from users.",
            'A submit control has a specific type; a button with type="button" does not submit by default.',
            "Password inputs mask characters on screen; visual masking is not the same as encryption.",
            "The type value is the standard HTML name for the control.",
            # T008
            "Semantic elements add meaning to the structure of the page.",
            "It commonly contains introductory content or navigation for a page or section.",
            "The element name is a short form of navigation.",
            "Choose the element specifically named for the page's main content.",
            "Its name describes the end or footer area of a page or section.",
            "Think about how assistive technology identifies sections and their roles.",
            # T009
            "Plan what the site should do and who it is for before coding.",
            "Footers often contain supporting information about the site or page.",
            "Testing helps find issues that need fixing.",
            "A visitor is someone who uses or views a website.",
            "Think about making content usable on phones, tablets and computers.",
            "A plan helps organise ideas and identify requirements before implementation."
        ],
        'difficulty': [
            # T001
            1, 1, 1, 1, 1, 1, 1,
            # T002
            1, 1, 1, 1, 1, 1, 1,
            # T003
            1, 1, 1, 1, 1, 1,
            # T004
            1, 1, 1, 1, 1, 1, 2,
            # T005
            1, 1, 1, 2, 1, 1, 2,
            # T006
            1, 1, 1, 1, 1, 1, 1,
            # T007
            1, 1, 1, 1, 1, 1, 2,
            # T008
            2, 1, 1, 1, 1, 2,
            # T009
            1, 1, 2, 1, 2, 1
        ]
    }
    
    df = pd.DataFrame(qa_data)
    df = df[['question_id', 'topic_id', 'question_text', 'option_a', 'option_b', 'option_c', 'correct_answer', 'hint_text', 'difficulty']]
    return df

if __name__ == "__main__":
    df = create_qa_pairs()
    output_path = 'data/reference/qa_pairs.csv'
    df.to_csv(output_path, index=False)
    print(f" Created {len(df)} CORRECTED multiple-choice QA pairs")
    print(f" Saved to: {output_path}")
    print(f"\n Answer Distribution:")
    print(df['correct_answer'].value_counts())