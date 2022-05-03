import markdown
import frontmatter
import os
import shutil
import sass
from bs4 import BeautifulSoup as Soup

styles_path = "./src/styles"
build_dir = "./build"
path = "./src/blog/md/"
post_out_path = "./build/blog/posts/"

def prepare_folders():
    if os.path.exists("build"):
        shutil.rmtree("build")

    os.makedirs("./build/blog/")
    shutil.copyfile("./src/blog/index.html", "./build/blog/index.html")

    shutil.copyfile("./src/index.html", "./build/index.html")
    shutil.copytree("./src/icons", "./build/icons/")

    if os.path.exists(post_out_path):
        shutil.rmtree(post_out_path)
    if not os.path.exists(post_out_path):
        os.makedirs(post_out_path)

def generate_css(folder_path):
    sass.compile(dirname=('src/styles/sass', 'build/styles/css'))

def generate_blog():
    with open('./src/blog/post_template.html', 'r') as f:
        soup = Soup(f.read(), 'html.parser')
        container = soup.find('div', attrs={'class':'container'})
        title_tag = soup.find('title')
        
        
        pages = []

        for i, fname in enumerate(os.listdir(path)[::-1]):
            with open(path + fname, 'r') as md:
                content = md.read()

                post = markdown.markdown(content, extensions=['meta'])
                metadata = frontmatter.loads(content)
                title = '<h1>{}</h1>'.format(metadata['title'])
                container.append(
                    Soup(title + post, 'html.parser')
                )
                title_tag.string = metadata['title']

                filename = metadata['title'].replace(' ', '_')
                post_path = post_out_path + filename + '.html'
                pages.append([post_path, f'#{i} ' + metadata['title']])

                with open(post_path, 'w') as p:
                    p.write(str(soup))

                container.string = ''

        blog_file = open('./src/blog/index.html', 'r+')
        content = blog_file.read()
        blog_file.close()

        index_soup = Soup(content, 'html.parser')
        main = index_soup.find(id="article")
        if main:
            for x, v in enumerate(pages):
                innerHTML = '<a href="{}"><h2>{}</h2></a>'.format("./posts/" + v[0].split("/")[-1], v[1])
                main.append(Soup(innerHTML, "html.parser"))

        with open('./build/blog/index.html', 'w') as blog_index:
                blog_index.write(str(index_soup))


try:
    prepare_folders()
    generate_css(styles_path)
    generate_blog()
except Exception as e:
    print(e)