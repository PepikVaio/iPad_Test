import locale
import markdown
import os
import re
import shutil
import subprocess
import sys

from languages import INFO, TEXTS
from datetime import datetime
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from pypdf.xmp import XmpInformation
from weasyprint import HTML


def get_Language():
    if sys.platform == "darwin":
        result = subprocess.run(["defaults", "read", "-g", "AppleLanguages"], capture_output=True, text=True)
        match = re.search(r'"([a-z]{2})', result.stdout)

        if match:
            language = match.group(1)
        else:
            language = "en"

    else:
        language = locale.getlocale()[0]

        if language:
            language = language[:2]

        if language not in TEXTS:
            language = "en"

    return language


def select_Folder(title):
    if sys.platform == "darwin":
        script = f'''
            tell application "System Events"
                activate
                set selectedFolder to choose folder with prompt "{title}"
                return POSIX path of selectedFolder
            end tell
        '''

        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)

        if result.returncode != 0:
            sys.exit()

        return result.stdout.strip()

    if sys.platform == "win32":
        script = f'''
            Add-Type -AssemblyName System.Windows.Forms
            $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
            $dialog.Description = "{title}"
            $dialog.ShowNewFolderButton = $true

            if ($dialog.ShowDialog() -eq "OK") {{
                Write-Output $dialog.SelectedPath
            }}
        '''

        result = subprocess.run(["powershell", "-NoProfile", "-Command", script], capture_output=True, text=True)

        if result.returncode != 0 or not result.stdout.strip():
            sys.exit()

        return result.stdout.strip()

    raise RuntimeError(TEXTS[LANGUAGE]["error_Unsupported_Os"])


LANGUAGE = get_Language()


def get_Path_Book_Root():
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, "Book")

    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "Book")


def get_Path_Book(path):
    return os.path.join(DIR_BASE, path)


def sync_Book():
    book_root = get_Path_Book_Root()

    user_chapter_01 = os.path.join(DIR_BASE, "Pages", "chapter_01.md")
    has_user_chapter_01 = os.path.isfile(user_chapter_01)

    for root, directories, files in os.walk(book_root):
        relative_root = os.path.relpath(root, book_root)

        if relative_root == ".":
            user_root = DIR_BASE
        else:
            user_root = os.path.join(DIR_BASE, relative_root)

        os.makedirs(user_root, exist_ok=True)

        for file in files:
            if relative_root == "Pages":
                name = os.path.splitext(file)[0].lower()

                if has_user_chapter_01 and re.match(r"chapter_\d+$", name):
                    continue

            source = os.path.join(root, file)
            destination = os.path.join(user_root, file)

            if not os.path.exists(destination):
                shutil.copy2(source, destination)


def show_Message(message):
    if sys.platform == "darwin":
        icon_path = os.path.join(sys._MEIPASS if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__)), "Bindery.icns")

        script = f'''
            tell application "System Events"
                activate
                display dialog "{message}" with title "Bindery" buttons {{"OK"}} default button "OK" with icon POSIX file "{icon_path}"
            end tell
        '''

        subprocess.run(["osascript", "-e", script])

    elif sys.platform == "win32":
        base_path = sys._MEIPASS if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_path, "Bindery.ico")
        message = message.replace('"', '\\"')

        script = f'''
            Add-Type -AssemblyName System.Windows.Forms
            Add-Type -AssemblyName System.Drawing

            $form = New-Object System.Windows.Forms.Form
            $form.Text = "Bindery"
            $form.StartPosition = "CenterScreen"
            $form.FormBorderStyle = "FixedDialog"
            $form.MaximizeBox = $false
            $form.MinimizeBox = $false
            $form.AutoSize = $true
            $form.AutoSizeMode = "GrowAndShrink"
            $form.Padding = New-Object System.Windows.Forms.Padding(25)

            $form.Icon = New-Object System.Drawing.Icon("{icon_path}")

            $label = New-Object System.Windows.Forms.Label
            $label.Text = "{message}"
            $label.AutoSize = $true
            $label.MaximumSize = New-Object System.Drawing.Size(500, 0)
            $label.Font = New-Object System.Drawing.Font("Segoe UI", 10)
            $label.Margin = New-Object System.Windows.Forms.Padding(0, 0, 0, 20)

            $button = New-Object System.Windows.Forms.Button
            $button.Text = "OK"
            $button.Width = 80
            $button.DialogResult = [System.Windows.Forms.DialogResult]::OK

            $panel = New-Object System.Windows.Forms.FlowLayoutPanel
            $panel.FlowDirection = "TopDown"
            $panel.AutoSize = $true
            $panel.WrapContents = $false
            $panel.Dock = "Fill"

            $panel.Controls.Add($label)
            $panel.Controls.Add($button)

            $form.Controls.Add($panel)
            $form.AcceptButton = $button

            $form.ShowDialog() | Out-Null
            $form.Dispose()
        '''

        subprocess.run(["powershell", "-NoProfile", "-Command", script])

                
DIR_BASE = select_Folder(TEXTS[LANGUAGE]["select_Folder"])

first_run = not os.path.isfile(
    os.path.join(DIR_BASE, "Pages", "description.md")
)

if first_run:
    show_Message(INFO[LANGUAGE])

sync_Book()

DIR_OUTPUT = DIR_BASE
DIR_PAGES = os.path.join(DIR_BASE, "Pages")
DIR_HTML = os.path.join(DIR_OUTPUT, "HTML")
DIR_TEMPLATES = os.path.join(DIR_BASE, "Templates")
DIR_FONTS = os.path.join(DIR_BASE, "Fonts")
DIR_STYLES = os.path.join(DIR_BASE, "Styles")


def show_Notification(message):
    if sys.platform == "darwin":
        subprocess.run(["osascript", "-e", f'display notification "{message}" with title "Bindery" sound name ""'])

    elif sys.platform == "win32":
        message = message.replace('"', '\\"')

        script = f'''
            Add-Type -AssemblyName System.Windows.Forms
            Add-Type -AssemblyName System.Drawing

            $notify = New-Object System.Windows.Forms.NotifyIcon
            $notify.Icon = [System.Drawing.SystemIcons]::Information
            $notify.Visible = $true
            $notify.BalloonTipTitle = "Bindery"
            $notify.BalloonTipText = "{message}"
            $notify.ShowBalloonTip(5000)

            Start-Sleep -Seconds 5
            $notify.Dispose()
        '''

        subprocess.Popen(["powershell", "-NoProfile", "-Command", script])


def clean_Name_File(filename):
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = re.sub(r'\s+', ' ', filename).strip()
    filename = filename.rstrip(". ")

    if not filename:
        filename = "book"

    return filename


def create_Chapter(markdown_text):
    markdown_text = re.sub(r'"([^"\n]+)"', r'<span class="quote">"\1"</span>', markdown_text)
    markdown_text = re.sub(r'^>\s*(.+)$', r'<p class="subtitle">\1</p>', markdown_text, flags=re.MULTILINE)

    html_content = markdown.markdown(markdown_text, extensions=["extra", "tables", "fenced_code"])
    html_content = html_content.replace("\n", "\n    ")

    return html_content


def create_Document(document_name, content, file_name, replacements=None):
    template = load_Template(document_name)
    styles = load_Styles(document_name)

    document_html = template.replace("{{STYLES}}", styles).replace("{{CONTENT}}", content)

    if replacements:
        for key, value in replacements.items():
            document_html = document_html.replace(f"{{{{{key}}}}}", value)

    html_name = os.path.splitext(file_name)[0] + ".html"
    html_file = os.path.join(DIR_HTML, html_name)

    with open(html_file, "w", encoding="utf-8") as output:
        output.write(document_html)

    pdf_data = BytesIO()

    HTML(filename=html_file, base_url=DIR_HTML).write_pdf(pdf_data)

    pdf_data.seek(0)

    return PdfReader(pdf_data)


def create_Pdf():
    if os.path.exists(DIR_HTML):
        shutil.rmtree(DIR_HTML)

    os.makedirs(DIR_HTML)

    book = load_Data_Book()
    pages = load_Markdown()
    writer = PdfWriter()
    chapters = []

    for file, content in pages:
        name = os.path.splitext(file)[0].lower()

        if name.startswith("chapter_"):
            chapter_title = re.search(r'<h1>(.*?)</h1>', content)

            if chapter_title:
                chapters.append({"title": chapter_title.group(1), "file": file})

    cover_reader = create_Document("cover", "", "cover.html", {"TITLE": book["title"], "SUBTITLE": book["subtitle"], "AUTHOR": book["author"]})

    for page in cover_reader.pages:
        writer.add_page(page)

    for file, content in pages:
        reader = create_Document("chapter", content, file)

        for page in reader.pages:
            writer.add_page(page)

        name = os.path.splitext(file)[0].lower()

        if name.startswith("chapter_"):
            chapter = next(
                (
                    item
                    for item in chapters
                    if item["file"] == file
                ),
                None
            )

            if chapter:
                chapter["page"] = (
                    len(writer.pages)
                    - len(reader.pages)
                )

    for chapter in chapters:
        writer.add_outline_item(chapter["title"], chapter["page"])

    safe_title = clean_Name_File(book["title"])

    OUTPUT_FILE = os.path.join(DIR_OUTPUT, f"{safe_title}.pdf")

    writer.add_metadata({
        "/Title": book["title"],
        "/Author": book["author"],
        "/CreationDate": datetime.now().astimezone().strftime("D:%Y%m%d%H%M%S%z")
    })

    xmp = XmpInformation.create()

    if book["title"]:
        xmp.dc_title = {"x-default": book["title"]}

    if book["author"]:
        xmp.dc_creator = [book["author"]]

    if book["tags"]:
        xmp.dc_subject = book["tags"]

    if book["identifier"] and book["identifier"].lower() != "none":
        identifier = book["identifier"]

        if identifier.lower().startswith("isbn:"):
            isbn = identifier[5:].strip()
            namespace = "http://prismstandard.org/namespaces/basic/2.0/"
            prefix = "prism"
            description = xmp._get_or_create_description()
            description.setAttributeNS("http://www.w3.org/2000/xmlns/", f"xmlns:{prefix}", namespace)
            document = xmp.rdf_root.ownerDocument
            element = document.createElementNS(namespace, f"{prefix}:isbn")
            element.appendChild(document.createTextNode(isbn))
            description.appendChild(element)
            xmp._update_stream()
        else:
            xmp.dc_identifier = identifier

    if book["published"] and book["published"].lower() != "none":
        published = datetime.strptime(book["published"], "%d/%m/%Y")
        xmp.dc_date = [published.strftime("%Y-%m-%dT00:00:00+00:00")]

    if book["date"] and book["date"].lower() != "none":
        set_Xmp(xmp, "Date", book["date"])

    if book["publisher"] and book["publisher"].lower() != "none":
        xmp.dc_publisher = [book["publisher"]]

    if book["language"] and book["language"].lower() != "none":
        xmp.dc_language = [book["language"]]

    if book["description"]:
        xmp.dc_description = {"x-default": book["description"]}

    if book["subtitle"]:
        set_Xmp(xmp, "Subtitle", book["subtitle"])

    set_Calibre_Series(xmp, book["series"], book["number"])
    set_Calibre_Rating(xmp, book["rating"])

    xmp.dc_format = "application/pdf"

    writer.xmp_metadata = xmp

    with open(OUTPUT_FILE, "wb") as output:
        writer.write(output)


def load_Data_Book():
    description_file = os.path.join(DIR_PAGES, "description.md")

    if not os.path.exists(description_file):
        return {
            "title": "",
            "subtitle": "",
            "author": "",
            "series": "",
            "number": "",
            "rating": "",
            "tags": [],
            "identifier": "",
            "date": "",
            "published": "",
            "publisher": "",
            "language": "",
            "description": ""
        }

    markdown_text = open(description_file, "r", encoding="utf-8").read()

    sections = {}
    current_section = None
    current_lines = []

    for line in markdown_text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)

        if match:
            if current_section is not None:
                sections[current_section] = "\n".join(current_lines).strip()

            current_section = match.group(1).strip().lower()
            current_lines = []

            continue

        if current_section is not None:
            current_lines.append(line)

    if current_section is not None:
        sections[current_section] = "\n".join(current_lines).strip()

    tags = [
        tag.strip()
        for tag in sections.get("tags", "").split(",")
        if tag.strip()
    ]

    description_markdown = sections.get("description", "")
    description = markdown.markdown(description_markdown, extensions=["extra", "tables", "fenced_code"])

    return {
        "title": sections.get("title", ""),
        "subtitle": sections.get("subtitle", ""),
        "author": sections.get("author", ""),
        "series": sections.get("series", ""),
        "number": sections.get("number", ""),
        "rating": sections.get("hodnocení", ""),
        "tags": tags,
        "identifier": sections.get("identifier", ""),
        "date": sections.get("date", ""),
        "published": sections.get("published", ""),
        "publisher": sections.get("publisher", ""),
        "language": sections.get("language", ""),
        "description": description
    }


def load_Markdown():
    files = [
        file
        for file in os.listdir(DIR_PAGES)
        if file.lower().endswith(".md")
        and os.path.splitext(file)[0].lower() != "description"
    ]

    def sort_key(file):
        name = os.path.splitext(file)[0].lower()
        match = re.match(r"chapter_(\d+)$", name)

        if match:
            return (0, int(match.group(1)))

        return (1, name)

    files.sort(key=sort_key)

    pages = []

    for file in files:
        markdown_text = open(os.path.join(DIR_PAGES, file), "r", encoding="utf-8").read()
        content = create_Chapter(markdown_text)

        pages.append((file, content))

    return pages


def load_Styles(document_name):
    files = []

    for file in os.listdir(DIR_STYLES):
        if not file.lower().endswith(".css"):
            continue

        style_name = os.path.splitext(file)[0].lower()

        if not style_name.startswith("style_"):
            continue

        style_name = style_name[6:]

        if style_name in ["cover", "chapter"] and style_name != document_name:
            continue

        files.append(file)

    styles = []

    for file in sorted(files):
        path = os.path.join(DIR_STYLES, file)
        styles.append(f'<link rel="stylesheet" href="file://{path}">')

    return "\n    ".join(styles)



def load_Template(document_name):
    template_file = f"template_{document_name}.html"
    path = get_Path_Book(os.path.join("Templates", template_file))

    return open(path, "r", encoding="utf-8").read()


def set_Calibre_Rating(xmp, value):
    if not value or value.lower() == "none":
        return

    stars = value.count("*")

    if stars == 0:
        return

    rating = min(stars * 2, 10)

    namespace = "http://calibre-ebook.com/xmp-namespace"
    prefix = "calibre"
    description = xmp._get_or_create_description()
    description.setAttributeNS("http://www.w3.org/2000/xmlns/", f"xmlns:{prefix}", namespace)
    document = xmp.rdf_root.ownerDocument
    element = document.createElementNS(namespace, f"{prefix}:rating")

    element.appendChild(document.createTextNode(str(rating)))
    description.appendChild(element)
    xmp._update_stream()


def set_Calibre_Series(xmp, series, number):

    if not series or series.lower() == "none":
        return

    namespace = "http://calibre-ebook.com/xmp-namespace"
    series_index_namespace = ("http://calibre-ebook.com/xmp-namespace-series-index")
    description = xmp._get_or_create_description()

    description.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:calibre", namespace)
    description.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:calibreSI", series_index_namespace)

    document = xmp.rdf_root.ownerDocument

    series_element = document.createElementNS(namespace, "calibre:series")
    series_element.setAttributeNS("http://www.w3.org/1999/02/22-rdf-syntax-ns#", "rdf:parseType", "Resource")
    value_element = document.createElementNS("http://www.w3.org/1999/02/22-rdf-syntax-ns#", "rdf:value")

    value_element.appendChild(document.createTextNode(series))
    series_element.appendChild(value_element)

    if number and number.lower() != "none":
        number_element = document.createElementNS(series_index_namespace, "calibreSI:series_index")
        number_element.appendChild(document.createTextNode(number))
        series_element.appendChild(number_element)

    description.appendChild(series_element)
    xmp._update_stream()


def set_Xmp(xmp, name, value):
    if not value or value.lower() == "none":
        return

    namespace = "http://wajsar.cz/xmp/book/1.0/"
    prefix = "book"

    description = xmp._get_or_create_description()

    description.setAttributeNS("http://www.w3.org/2000/xmlns/", f"xmlns:{prefix}", namespace)

    document = xmp.rdf_root.ownerDocument
    element = document.createElementNS(namespace, f"{prefix}:{name}")

    element.appendChild(document.createTextNode(value))
    description.appendChild(element)

    xmp._update_stream()


show_Notification(TEXTS[LANGUAGE]["info_Generating"])


try:
    create_Pdf()
    show_Notification(TEXTS[LANGUAGE]["info_Done"])
except Exception as error:
    with open(FILE_ERROR, "w", encoding="utf-8") as output:
        output.write(repr(error))
