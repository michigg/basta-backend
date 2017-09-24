from shutil import copytree

# PI
OUTPUTFILE = "/media/data_1/www/pub-html/ofu-food.html"
CSSFILE_SRC = "../css/bootstrap-4.0.0-beta-dist"
CSSFILE_DEST = "/media/data_1/www/css/bootstrap-4.0.0-beta-dist"

copytree(CSSFILE_SRC, CSSFILE_DEST)
