import re, urllib.parse

try:
    from .newsitems import *
except:
    from newsitems import *

LINK_REGEX = re.compile(r'(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?')

def link_htmlize(match):
    link = match.group()
    return '<a href="z">z</a>'.replace("z", link)

class DestinationBase:
    def __init__(self, filename):
        self.filename = filename
    def receive_items(self, items):
        pass

class PlainDestination(DestinationBase):
    """
    A news destination that formats all its news items as plain text.
    """
    def __init__(self):
        pass
    def receive_items(self, items):
        for item in items:
            print(item.title)
            if " " in item.body:
                print('-' * len(item.title))
                print(item.body)
                print("From:", item.source)

class TextFileDestination(DestinationBase):
    """
    A news Destination that formats items into a .txt file.
    """
    def receive_items(self, items):
        f = open(self.filename, "w", encoding="utf-8")
        for i in items:
            f.write("From: "+i.source+"\n")
            f.write(i.title+"\n")
            if not " " in i.body:
                f.write("\n")
                continue
            f.write(i.body+"\n\n")
        f.close()

class HTMLDestination(DestinationBase):
    """
    A news destination that formats all its news items as HTML.
    """
    def receive_items(self, items):

        out = open(self.filename, 'w', encoding="utf-8")
        print("""
<html>
<head>
<meta charset="utf-8" />
<title>Today's News</title>
</head>
<body>
<center>
<h1>Today's News</h1>
        """, file=out)

        print('<ol>', file=out)
        id = 0
        for item in items:
            id += 1
            print('  <li><a href="#{}">{}</a></li>'
                    .format(id, item.title), file=out)
        print('</ol>', file=out)

        id = 0
        for item in items:
            id += 1
            print('<h2><a name="{}">{}</a></h2>'
                    .format(id, item.title), file=out)
            print("<h6>From: {}</h6>".format(item.source), file=out)
            if " " in item.body:
                if item.body.startswith("Link: "):
                    print('<pre>{}</pre>'
                          .format(LINK_REGEX.sub(link_htmlize, item.body)), file=out)
                else:
                    print('<pre>{}</pre>'.format(LINK_REGEX.sub(link_htmlize, item.body)), file=out)
            print("<br />", file=out)

        print("""
</center>
</body>
</html>
        """, file=out)
        out.close()

class XMLDestination(DestinationBase):
    """
    Output in XML Format.
    """
    def receive_items(self, items):
        f = open(self.filename, "w", encoding="utf-8")
        f.write("<?xml version='1.0' encoding='utf-8'?>\n")
        f.write("<content>\n")
        for i in items:
            f.write("<title>"+i.title+"</title>\n")
        f.write("</content>\n")
        f.write("<news>\n")
        for i in items:
            f.write("<title>"+i.title+"</title>\n")
            f.write("<body>"+i.body+"</body>\n")
        f.write("</news>")
        f.close()

class JSONDestination(DestinationBase):
    """
    
    Output in JSON Format.
    """
    def receive_items(self, items):
        f = open(self.filename, "w", encoding="utf-8")
        tab = " "*4
        f.write("[{}\n".format(tab))
        i = 0
        for item in items:
            i += 1
            f.write(tab+"{\n")
            f.write(tab*2+'"id":{},\n'.format(i))
            f.write(tab*2+'"title":{},'.format(repr(item.title))+"\n")
            f.write(tab*2+'"body":{},'.format(repr(item.body))+"\n")
            f.write(tab*2+'"origin":{}'.format(repr(item.source))+"\n")
            if i == len(items):
                f.write(tab+"}\n")
                break
            f.write(tab+"},\n")
        f.write("]")
        f.close()

