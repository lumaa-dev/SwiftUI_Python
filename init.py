import yaml
import os
import util
import http.server
import webbrowser
import glob
 
PORT = 8080
server_address = ("", PORT)
has_web = False

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

if not os.path.exists(util.removeSlash(config["docsPath"])):
    os.mkdir("docs")
    print('Created "docs" directory')

if not os.path.exists(util.removeSlash(config["webPath"])) or os.path.exists(
    util.removeSlash(config["webPath"]) + "\index.html"
):
    print(
        f"No web visualizer found, if this is a mistake make sure your 'index.html' file exists in a '{config['webPath']}' directory"
    )
else:
    has_web = True

def all_docs():
    files = glob.glob(os.path.join(util.removeSlash(config["docsPath"]), '*.txt'))
    return files
    
def doc_to_html(doc: str):
    '''Converts a doc to HTML code'''
    f = open(doc, "r")
    strs = f.read().split(";;", 1)

    title = strs[0]
    desc = strs[1][:25]
    return f"""<div class="d">
            <p class="t">{title.strip()}</p>
            <p class="q">{desc.strip()}</p>
        </div>"""

if has_web:
    with open(util.removeSlash(config["webPath"]) + "/template.html", "r") as file:
        original_content = file.read()

    docs = all_docs()
    htmls = []
    for doc in docs:
        if doc.find("template") == -1:
            htmls.append(doc_to_html(doc))

    modified_content = original_content.replace("%docs", " ".join(htmls))

    with open(util.removeSlash(config["webPath"]) + "/index.html", "w") as file:
        if not file.writable():
            print("Not writable")
        file.write(modified_content)

    server = http.server.HTTPServer
    handler = http.server.CGIHTTPRequestHandler
    handler.extensions_map.update({
        '.html': 'text/html',
    })
    # handler.cgi_directories = [config["webPath"] + "\\index.html"]
    print("Server is on port: ", PORT)

    httpd = server(server_address, handler)
    
    httpd.serve_forever()
    webbrowser.open(f"http://localhost:{PORT}/web/")
else:
    exit()