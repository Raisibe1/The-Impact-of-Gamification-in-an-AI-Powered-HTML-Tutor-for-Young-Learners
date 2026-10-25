\# T008: Semantic HTML and Accessibility



\*\*Grade Level:\*\* 9 | \*\*Duration:\*\* 15 minutes | \*\*Difficulty:\*\* 3 (Hard)



\---



\## What is Semantic HTML?

The word "semantic" means "relating to meaning." Semantic HTML simply means using tags that clearly describe what the content inside them is for. 



Instead of using a generic `<div>` for everything, we use tags that act like labels. Think of it like a house: instead of putting a sign on every door that just says "Room," you put signs that say "Kitchen," "Bedroom," and "Bathroom." 



The main semantic tags we use to structure a webpage are:

\*   `<header>`: The top section of the page (usually contains the logo and title).

\*   `<nav>`: A section for navigation links (menus).

\*   `<main>`: The main content of the page.

\*   `<footer>`: The bottom section of the page (usually contains copyright info).



\*\*Example:\*\*

```html

<header>

&#x20; <h1>My Awesome Website</h1>

</header>



<main>

&#x20; <p>Welcome to my page!</p>

</main>



<footer>

&#x20; <p>Created by a Grade 9 Learner</p>

</footer>

```



\## Why is Semantic HTML Important for Accessibility?

"Accessibility" means making sure everyone can use your website, including people with disabilities. 



Visually impaired people often use a \*\*screen reader\*\* (a software program that reads the webpage out loud to them). 

If your page is full of generic tags, the screen reader gets confused. But if you use semantic tags, the screen reader can say, \*"You are now entering the main content"\* or \*"You are now in the navigation menu."\* This makes navigating the page much easier!



\## The `<img>` Tag and Alt Text

Another crucial part of accessibility is the \*\*`alt` attribute\*\*. When you add an image to a webpage using the `<img>` tag, you must include an `alt` (alternative) description.



If a blind learner uses a screen reader, they can't see the image. The screen reader will read the `alt` text out loud so they know what the image shows. If the image fails to load, the alt text will also display on the screen for everyone to see.



\*\*Example:\*\*

```html

<img src="puppy.jpg" alt="A small brown puppy playing with a red ball">

```



\## Why Does This Matter?

Building a website that is accessible means you are including everyone. Using semantic tags and alt text shows that you care about all your visitors, regardless of how they access the internet. Plus, search engines like Google love semantic HTML because it helps them understand your page better!

