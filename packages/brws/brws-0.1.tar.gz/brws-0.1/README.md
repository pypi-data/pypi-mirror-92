# brws: Browse documents based on content and not filename

For large collections of documents, we it can be very hard to get a sense to find the ones that are similar or very different.
If the documents have useful names, you may be able to get some information from the filename, but there are a number of situations, where documents naturally don't have useful filenames.
For example, you might have downloaded a bunch of papers from arXiv&mdash;and now all of them have numbers as name, that are entirely unrelated to their content.
Or you might have received 200 job applications and it is almost impossible to tell if the best candidate hides behind "application_ochi_effezi.pdf" or "justin_bieber_cv.pdf" or maybe "application_document.pdf"

`brws` helps you get an overview of large numbers of files.
Instead of showing you filenames, it uses AI to "read" every document and then visualizes the documents as dots in a two dimensional plane.
Importantly, documents with similar content are shown in similar locations.
Simply click on one of the dots to open the associated document.


## Installation

I recommend installing `brws` into a virtual environment to keep it separate from your system python.
Inside the virtual environment, you can simply run
```
pip install brws
```
If you want `brws` to be available from anywhere on the command line, try out [triforce](https://github.com/esc/triforce), which manages a global virtual environment for cases like this.


## Basic Usage

Navigate to the folder in which your documents are and just run
```
brws
```
Alternatively, you can point `brws` to a folder by using the `--folder` argument.
