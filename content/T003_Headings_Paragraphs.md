\# T003: Headings and Paragraphs



\*\*Grade Level:\*\* 7 | \*\*Duration:\*\* 15 minutes | \*\*Difficulty:\*\* 1 (Easy)



\---



\## Giving Your Webpage Structure

When you look at a newspaper or a school textbook, the text isn't just one giant block. It has a big title at the top, smaller titles for different sections, and paragraphs of text underneath. HTML uses special tags to create this exact same structure on a webpage. 



\## Headings: `<h1>` to `<h6>`

Headings are used for titles and subheadings. HTML gives us \*\*six levels of headings\*\*, from `<h1>` to `<h6>`.



\*   `<h1>` is the biggest and most important heading on the page. You should only use it once, usually for the main title.

\*   `<h2>` is for main sections.

\*   `<h3>` is for sub-sections, and so on, down to `<h6>`, which is the smallest.



Just like a school project, the headings help the reader know what the page is about. Every heading needs an opening tag and a closing tag. 



\*\*Example:\*\*

```html

<h1>My School</h1>

<h2>Subjects I Like</h2>

<h3>Computer Applications Technology</h3>

```



\## Paragraphs: `<p>`

While headings are for titles, the `<p>` tag is used for blocks of normal text. Whenever you want to write a paragraph, you put the text between `<p>` and `</p>`. 



When the browser sees a `<p>` tag, it automatically adds a little bit of space above and below the paragraph so it is easy to read. 



\*\*Example:\*\*

```html

<p>Welcome to my school website. I am learning HTML.</p>

```



\## Line Breaks and Horizontal Rules

Sometimes you want to start a new line without making a whole new paragraph. You can use the `<br>` tag (break) to push text to the next line. You can also use the `<hr>` tag (horizontal rule) to draw a line across the page, which is great for separating different topics.



\*\*Example:\*\*

```html

<p>This is the first line. <br> This is the second line.</p>

<hr>

```



> \*\*NB:\*\* Tags like `<br>` and `<hr>` are called \*\*empty tags\*\* because they don't wrap around any text, so they don't need a closing tag!



\## Why Does This Matter?

If you just typed text on a page without tags, it would all blend into one messy block. Headings and paragraphs make your webpage look neat, professional, and easy for your visitors to read.

