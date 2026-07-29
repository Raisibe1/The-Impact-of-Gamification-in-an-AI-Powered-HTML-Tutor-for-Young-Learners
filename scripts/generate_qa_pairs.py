import pandas as pd

def create_qa_pairs():
    """Create 60 multiple-choice HTML question-answer pairs for Grades 7-9 (5.5/10 difficulty)"""
    
    qa_data = {
        'question_id': [
            # T001 - Introduction to HTML (7 questions)
            'Q001', 'Q002', 'Q003', 'Q004', 'Q005', 'Q006', 'Q007',
            # T002 - HTML Tags & Structure (7 questions)
            'Q008', 'Q009', 'Q010', 'Q011', 'Q012', 'Q013', 'Q014',
            # T003 - Headings & Paragraphs (6 questions)
            'Q015', 'Q016', 'Q017', 'Q018', 'Q019', 'Q020',
            # T004 - Hyperlinks (7 questions)
            'Q021', 'Q022', 'Q023', 'Q024', 'Q025', 'Q026', 'Q027',
            # T005 - Images & Multimedia (7 questions)
            'Q028', 'Q029', 'Q030', 'Q031', 'Q032', 'Q033', 'Q034',
            # T006 - Lists & Tables (7 questions)
            'Q035', 'Q036', 'Q037', 'Q038', 'Q039', 'Q040', 'Q041',
            # T007 - Forms (7 questions)
            'Q042', 'Q043', 'Q044', 'Q045', 'Q046', 'Q047', 'Q048',
            # T008 - Semantic HTML (6 questions)
            'Q049', 'Q050', 'Q051', 'Q052', 'Q053', 'Q054',
            # T009 - Mini Website Project (6 questions)
            'Q055', 'Q056', 'Q057', 'Q058', 'Q059', 'Q060'
        ],
        'topic_id': [
            # T001
            'T001', 'T001', 'T001', 'T001', 'T001', 'T001', 'T001',
            # T002
            'T002', 'T002', 'T002', 'T002', 'T002', 'T002', 'T002',
            # T003
            'T003', 'T003', 'T003', 'T003', 'T003', 'T003',
            # T004
            'T004', 'T004', 'T004', 'T004', 'T004', 'T004', 'T004',
            # T005
            'T005', 'T005', 'T005', 'T005', 'T005', 'T005', 'T005',
            # T006
            'T006', 'T006', 'T006', 'T006', 'T006', 'T006', 'T006',
            # T007
            'T007', 'T007', 'T007', 'T007', 'T007', 'T007', 'T007',
            # T008
            'T008', 'T008', 'T008', 'T008', 'T008', 'T008',
            # T009
            'T009', 'T009', 'T009', 'T009', 'T009', 'T009'
        ],
        'question_text': [
            # T001 - Introduction to HTML (SIMPLIFIED)
            'What does HTML stand for?',
            'What is the main job of HTML?',
            'What is the very first tag you type in a new HTML file?',
            'What happens when you open an HTML file in a web browser?',
            'What is an HTML tag?',
            'Which tag holds everything you can SEE on a webpage?',
            'What two main parts does every HTML page have?',
            
            # T002 - HTML Tags & Structure (SIMPLIFIED)
            'Which tag makes a new paragraph?',
            'How many heading sizes can you use in HTML?',
            'Which heading is the BIGGEST on a webpage?',
            'Which heading is the SMALLEST on a webpage?',
            'What kind of information goes inside the <head> tag?',
            'Which tag creates a new line without starting a new paragraph?',
            'What is special about the <br> tag?',
            
            # T003 - Headings & Paragraphs (SIMPLIFIED)
            'Which heading tag is used for the MAIN title of a page?',
            'What does the <p> tag create on your webpage?',
            'If you forget to close a <p> tag, what usually happens?',
            'Which tag would you use for a section title that is smaller than <h1>?',
            'How is <h1> different from <h2>?',
            'Can you put a heading tag inside a paragraph tag?',
            
            # T004 - Hyperlinks (SIMPLIFIED)
            'What attribute do you use to add a web address to a link?',
            'Which HTML tag creates a clickable link?',
            'What does "href" mean in a link?',
            'How do you make a link open in a new browser tab?',
            'Which is the correct way to write a link to Google?',
            'What happens when someone clicks on a link?',
            'Can you make an image clickable like a link?',
            
            # T005 - Images & Multimedia (SIMPLIFIED)
            'Which tag adds a picture to your webpage?',
            'What attribute tells the browser where the image is?',
            'What does the "alt" attribute do for an image?',
            'Why should you always add alt text to images?',
            'What types of image files work on webpages?',
            'What appears if your image file is missing or broken?',
            'How can you change the size of an image on your page?',
            
            # T006 - Lists & Tables (SIMPLIFIED)
            'Which tag creates a bulleted (unordered) list?',
            'Which tag creates a numbered (ordered) list?',
            'What is the main difference between <ul> and <ol>?',
            'Which tag is used for each item in a list?',
            'Which tag starts a new row in a table?',
            'Which tag creates the heading cells in a table?',
            'Which tag creates the data cells in a table?',
            
            # T007 - Forms (SIMPLIFIED)
            'Which tag creates a box where users can type information?',
            'What attribute gives the input field a name?',
            'What does the "type" attribute do for an input field?',
            'What is the main purpose of a form on a website?',
            'Which tag creates a button that submits the form?',
            'What is the difference between type="text" and type="password"?',
            'How do you create a checkbox in a form?',
            
            # T008 - Semantic HTML (SIMPLIFIED)
            'Why do we use semantic HTML tags?',
            'Which tag is used for the top part of a webpage or section?',
            'Which tag contains the navigation menu links?',
            'Which tag holds the main content of your webpage?',
            'Which tag is used for the bottom part of a webpage?',
            'Why are semantic tags helpful for people using screen readers?',
            
            # T009 - Mini Website Project (SIMPLIFIED)
            'What should you do FIRST when building a website?',
            'What information usually goes in the footer of a webpage?',
            'Why is it important to test your webpage?',
            'Who is a "visitor" to your website?',
            'What does "responsive design" mean for a website?',
            'Why is it helpful to plan your webpage before coding?'
        ],
        'option_a': [
            # T001 - SIMPLIFIED options
            'HyperText Markup Language', 'To add colours to webpages', '<html>',
            'The browser shows you the webpage', 'A special word in angle brackets like <p>',
            '<body>', 'A head and a body',
            
            # T002
            '<p>', '6', '<h1>', '<h6>', 'Information about the page (like the title)',
            '<br>', 'It does not need a closing tag',
            
            # T003
            '<h1>', 'A block of text', 'The browser still shows the text normally',
            '<h2>', '<h1> is bigger', 'No, headings must be on their own line',
            
            # T004
            'href', '<a>', 'Hypertext Reference', 'target="_blank"',
            '<a href="google.com">Google</a>', 'It takes them to another webpage',
            'Yes, by putting <img> inside <a>',
            
            # T005
            '<img>', 'src', 'Describes the image for people who cannot see it',
            'It helps people who use screen readers', 'Many types work (jpg, png, gif)',
            'A broken image icon', 'Use width and height attributes',
            
            # T006
            '<ul>', '<ol>', '<ul> has bullets, <ol> has numbers',
            '<li>', '<tr>', '<th>', '<td>',
            
            # T007
            '<input>', 'name', 'It decides what kind of input box it is',
            'To get information from users', '<input type="submit">',
            'text shows letters, password hides them with dots',
            'Use type="checkbox"',
            
            # T008
            'To give more meaning to the content', '<header>', '<nav>',
            '<main>', '<footer>', 'It helps them understand the page better',
            
            # T009
            'Plan what you want on your webpage', 'Copyright info and links',
            'To find and fix problems', 'Someone who looks at your webpage',
            'It works well on computers, tablets, and phones', 'To stay organized and not forget things'
        ],
        'option_b': [
            # T001
            'HyperText Markup Language', 'To build the structure of a webpage', '<!DOCTYPE html>',
            'It edits the code for you', 'A programming language', '<head>',
            'A header and a footer',
            
            # T002
            '<h1>', '6', '<h2>', '<h5>', 'The text you see on the page',
            '<p>', 'It is empty and has no content',
            
            # T003
            '<h6>', 'A heading', 'The page will show an error',
            '<h3>', '<h1> is smaller', 'Yes, you can put them anywhere',
            
            # T004
            'src', '<link>', 'Hypertext Help', 'new_window',
            '<a src="google.com">Google</a>', 'It checks for spelling mistakes',
            'No, only text can be links',
            
            # T005
            '<image>', 'alt', 'It makes the image bigger', 'It makes the page load faster',
            'Only jpg files', 'The page will not load', 'Use the size attribute',
            
            # T006
            '<ol>', '<ul>', 'Both use bullet points', '<list>', '<row>', '<tr>', '<data>',
            
            # T007
            '<form>', 'id', 'It makes the input bigger', 'To change the page colour',
            '<submit>', 'text is for passwords, password is for text',
            'Use type="check"',
            
            # T008
            'To make pages load faster', '<section>', '<menu>',
            '<content>', '<bottom>', 'It makes the text bigger',
            
            # T009
            'Start typing code right away', 'Only social media links',
            'To make the page look pretty', 'Someone who builds websites',
            'It only works on desktop computers', 'To make coding more complicated'
        ],
        'option_c': [
            # T001
            'HyperText Markup Language', 'To create animations', '<body>',
            'It saves the file automatically', 'A type of software', '<footer>',
            'A title and a footer',
            
            # T002
            '<div>', '4', '<h3>', '<h4>', 'The page title and settings',
            '<hr>', 'It has no opening tag',
            
            # T003
            '<h2>', 'A new line', 'The browser will not show anything',
            '<p>', 'They are exactly the same', 'Only in special cases',
            
            # T004
            'link', '<hyperlink>', 'Hypertext Link', 'open_new',
            '<a href="google.com">Google</a>', 'It adds a picture to the page',
            'Yes, by putting <a> inside <img>',
            
            # T005
            '<picture>', 'href', 'It creates a caption under the image',
            'It changes the image colour', 'Only gif files',
            'A broken image icon', 'Use the image-size attribute',
            
            # T006
            '<list>', '<item>', '<ul> has numbers, <ol> has bullets',
            '<point>', '<table>', '<thead>', '<tc>',
            
            # T007
            '<text>', 'placeholder', 'It adds a label to the input',
            'To create animations', '<button type="submit">',
            'text is for passwords, password is for text',
            'Use type="box"',
            
            # T008
            'To make pages more colourful', '<header>', '<navigation>',
            '<section>', '<lower>', 'It makes pages look more modern',
            
            # T009
            'Find pictures for the page', 'The page title',
            'To make it more interesting', 'Someone who clicks on links',
            'It only works on mobile phones', 'To make sure you have enough time'
        ],
        'correct_answer': [
            # T001 - All A is correct
            'A', 'B', 'B', 'A', 'A', 'A', 'A',
            # T002
            'A', 'A', 'A', 'A', 'A', 'A', 'A',
            # T003
            'A', 'A', 'A', 'A', 'A', 'A',
            # T004
            'A', 'A', 'A', 'A', 'A', 'A', 'A',
            # T005
            'A', 'A', 'A', 'B', 'A', 'A', 'A',
            # T006
            'A', 'B', 'A', 'A', 'A', 'A', 'A',
            # T007
            'A', 'A', 'A', 'A', 'A', 'A', 'A',
            # T008
            'A', 'A', 'A', 'A', 'A', 'A',
            # T009
            'A', 'A', 'A', 'A', 'A', 'A'
        ],
        'hint_text': [
            # T001 - Clearer hints
            'Think about the three words that make up HTML',
            'What does HTML do for a webpage?',
            'This goes at the very top of the file',
            'What does the browser do with the code?',
            'Look at the symbols used - what goes inside them?',
            'What part of the page can you actually see?',
            'Think about the two sections every HTML page has',
            
            # T002 - Simpler hints
            'This tag is one letter and starts with p',
            'Count from h1 to h6',
            'Which number gives the biggest heading?',
            'Which number gives the smallest heading?',
            'This is stuff the user doesn\'t see',
            'This tag starts with br and is short for "break"',
            'Does it have a closing tag?',
            
            # T003
            'Which heading is the most important?',
            'What does the p stand for?',
            'Browsers are forgiving with small mistakes',
            'Which heading is one level below h1?',
            'Think about the size difference',
            'Headings are block elements - they take their own line',
            
            # T004
            'This attribute starts with h',
            'This tag is a single letter',
            'The "ref" part means "reference"',
            'Look for the attribute that starts with "target"',
            'You need the href attribute in the opening tag',
            'What happens to the user when they click?',
            'You can wrap an image with a link tag',
            
            # T005
            'This tag is short for "image"',
            'This stands for "source"',
            'The "alt" is like a description',
            'Think about people who can\'t see the image',
            'Most common image formats work',
            'What does the browser show as a placeholder?',
            'You can use attributes for width and height',
            
            # T006
            'UL stands for "unordered list"',
            'OL stands for "ordered list"',
            'Think about bullets vs numbers',
            'LI stands for "list item"',
            'TR stands for "table row"',
            'TH stands for "table header"',
            'TD stands for "table data"',
            
            # T007
            'This tag collects user information',
            'This is how you identify the field',
            'Different types show different input boxes',
            'Forms send information somewhere',
            'This tag creates the clickable button',
            'Think about what each one shows on screen',
            'This is a common input type for choices',
            
            # T008
            'It\'s about meaning, not just appearance',
            'This goes at the top of a section',
            'This has navigation links',
            'This has the main content',
            'This goes at the bottom',
            'Screen readers read pages aloud',
            
            # T009
            'Think about what you need before starting',
            'This goes at the very bottom',
            'Testing helps catch errors',
            'This is the person using your site',
            'Think about different devices people use',
            'A plan helps you work better'
        ],
        'difficulty': [
            # T001 - ALL LEVEL 1 (easier)
            1, 1, 1, 1, 1, 1, 1,
            # T002 - ALL LEVEL 1
            1, 1, 1, 1, 1, 1, 1,
            # T003 - ALL LEVEL 1
            1, 1, 1, 1, 1, 1,
            # T004 - MOSTLY LEVEL 1, one Level 2
            1, 1, 1, 1, 1, 1, 2,
            # T005 - MOSTLY LEVEL 1
            1, 1, 1, 2, 1, 1, 2,
            # T006 - ALL LEVEL 1
            1, 1, 1, 1, 1, 1, 1,
            # T007 - MOSTLY LEVEL 1
            1, 1, 1, 1, 1, 1, 2,
            # T008 - MIX OF 1 and 2
            2, 1, 1, 1, 1, 2,
            # T009 - MOSTLY LEVEL 1
            1, 1, 2, 1, 2, 1
        ]
    }
    
    df = pd.DataFrame(qa_data)
    
    # Reorder columns for better readability
    df = df[['question_id', 'topic_id', 'question_text', 'option_a', 'option_b', 'option_c', 'correct_answer', 'hint_text', 'difficulty']]
    
    return df

if __name__ == "__main__":
    df = create_qa_pairs()
    output_path = 'data/reference/qa_pairs.csv'
    df.to_csv(output_path, index=False)
    print(f"✅ Created {len(df)} multiple-choice QA pairs")
    print(f"📁 Saved to: {output_path}")
    print(f"\n📊 Topics covered:")
    print(df['topic_id'].value_counts().sort_index())
    print(f"\n📊 Difficulty breakdown:")
    print(df['difficulty'].value_counts().sort_index())
    print(f"\n🔍 First 5 questions:")
    print(df[['question_id', 'topic_id', 'question_text', 'correct_answer']].head())