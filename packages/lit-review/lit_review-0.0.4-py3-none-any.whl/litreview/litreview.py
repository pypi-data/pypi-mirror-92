#!/usr/bin/python3
from litreview.src.argparser import get_args
from litreview.src.extractor import Arxiv
from litreview.src.get_post import get_post
from litreview.src.shell_utils import download_pdf, copy_file, run
from litreview.src.utils import makedirs


def doit():
    args = get_args()
    data = Arxiv(args.paperurl)

    print(args.postdirname)

    print(data.pdflink())
    print(data.bibtex())
    print(data.abstract())
    print(data.authors())
    print(data.title())
    print(data.date())
    print(args.categories)

    filepath = download_pdf(data.pdflink(), data.filename())

    pdfpath = f"./{args.pdfdirname}/{data.filename()}"
    with makedirs(pdfpath):
        copy_file(filepath, f"{pdfpath}/{data.filename()}.pdf")
        copy_file(filepath, f"{pdfpath}/{data.filename()}_annotated.pdf")

    # with makedirs(args.postdirname):

    agggg = get_post(data.title(), data.authors(), data.abstract(), data.pdflink(), data.bibtex(), data.date(),
                     args.categories, args.layout)
    print(agggg)
    i = 0

def mkconf():
    configdir = run("echo $HOME", shell=True)+"/.config"

    #with makedirs(configdir):


def main():
    mkconf()
    doit()


if __name__ == "__main__":
    main()