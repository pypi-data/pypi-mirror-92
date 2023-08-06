import os

from .PSPExamplePage import PSPExamplePage


class View(PSPExamplePage):
    """View the source of a PSP page.

    For each PSP example, you will see a sidebar with various menu items,
    one of which is "View source of <em>example</em>". This link points to the
    View servlet and passes the filename of the current servlet. The View
    servlet then loads that PSP file's source code and displays it in the
    browser for your viewing pleasure.

    Note that if the View servlet isn't passed a PSP filename, it prints the
    View's docstring which you are reading right now.
    """

    def writeContent(self):
        req = self.request()
        if req.hasField('filename'):
            filename = req.field('filename')
            basename = os.path.basename(filename)
            filename = self.request().serverSidePath(basename)
            if not os.path.exists(filename):
                self.write('<p style="color:red">'
                           f'No such file {basename} exists</p>')
                return
            text = open(filename).read()
            text = self.htmlEncode(text)
            text = text.replace('\n', '<br>').replace('\t', ' '*4)
            self.write(f'<pre>{text}</pre>')
        else:
            doc = self.__class__.__doc__.split('\n', 1)
            doc[1] = '</p>\n<p>'.join(doc[1].split('\n\n'))
            self.writeln(f'<h2>{doc[0]}</h2>\n<p>{doc[1]}</p>')
